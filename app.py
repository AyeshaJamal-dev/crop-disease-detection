"""
Crop Disease Detection System - Flask Application
"""
import os
from functools import wraps
from pathlib import Path

from flask import (Flask, flash, redirect, render_template, request, send_from_directory,
                   url_for)
from flask_login import (LoginManager, current_user, login_required, login_user,
                         logout_user)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from config import (ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, UPLOAD_FOLDER)
from database import db_connection as db

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'


class User:
    """Simple user class for Flask-Login."""
    def __init__(self, user_id, email, user_type):
        self.id = user_id
        self.email = email
        self.user_type = user_type
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

    @property
    def is_admin(self):
        return self.user_type == 'admin'


@login_manager.user_loader
def load_user(user_id):
    row = db.get_user_by_id(int(user_id))
    if row:
        return User(row['user_id'], row['email'], row['user_type'])
    return None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


# ---------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        phone = request.form.get('phone', '').strip()
        location = request.form.get('location', '').strip()
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('register.html')
        user_id = db.create_user(full_name, email, password, 'farmer', phone, location)
        if user_id:
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        flash('Email already registered.', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        user_row = db.get_user_by_email(email)
        if user_row and check_password_hash(user_row['password'], password):
            user = User(user_row['user_id'], user_row['email'], user_row['user_type'])
            login_user(user)
            next_url = request.args.get('next') or url_for('dashboard')
            return redirect(next_url)
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    predictions = db.get_user_predictions(current_user.id, limit=10)
    total = len(db.get_user_predictions(current_user.id, limit=10000))
    return render_template('dashboard.html', predictions=predictions, total_predictions=total)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('upload'))
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('upload'))
        if not allowed_file(file.filename):
            flash('Invalid file type. Use JPG or PNG.', 'danger')
            return redirect(url_for('upload'))

        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        filename = secure_filename(file.filename)
        base, ext = os.path.splitext(filename)
        unique_name = f"{base}_{current_user.id}_{os.urandom(4).hex()}{ext}"
        filepath = UPLOAD_FOLDER / unique_name
        file.save(str(filepath))

        try:
            from models.predict import predict
            result = predict(str(filepath))
        except FileNotFoundError:
            flash('Model not trained yet. Please run training first.', 'warning')
            return redirect(url_for('upload'))
        except Exception as e:
            flash(f'Prediction error: {str(e)}', 'danger')
            return redirect(url_for('upload'))

        rel_path = f"uploads/{unique_name}"
        pred_id = db.insert_prediction(
            current_user.id,
            rel_path,
            result['disease'],
            result['confidence'],
            result['crop_type'],
            result['status'],
        )
        return redirect(url_for('results', prediction_id=pred_id))
    return render_template('upload.html')


@app.route('/results/<int:prediction_id>')
@login_required
def results(prediction_id):
    pred = db.get_prediction_by_id(prediction_id)
    if not pred or pred['user_id'] != current_user.id:
        flash('Prediction not found.', 'danger')
        return redirect(url_for('dashboard'))
    disease_info = db.get_disease_info(pred['predicted_disease'])
    return render_template('results.html', prediction=pred, disease_info=disease_info)


@app.route('/history')
@login_required
def history():
    predictions = db.get_user_predictions(current_user.id)
    return render_template('history.html', predictions=predictions)


@app.route('/feedback/<int:prediction_id>', methods=['POST'])
@login_required
def feedback(prediction_id):
    pred = db.get_prediction_by_id(prediction_id)
    if not pred or pred['user_id'] != current_user.id:
        flash('Prediction not found.', 'danger')
        return redirect(url_for('dashboard'))
    feedback_text = request.form.get('feedback', '').strip()
    rating = request.form.get('accuracy_rating', type=int)
    if rating and 1 <= rating <= 5:
        db.insert_feedback(current_user.id, prediction_id, feedback_text, rating)
        flash('Thank you for your feedback!', 'success')
    return redirect(url_for('results', prediction_id=prediction_id))


# Admin routes
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    user_count = db.get_user_count()
    pred_count = db.get_prediction_count()
    metrics = db.get_latest_model_metrics()
    return render_template('admin/dashboard.html',
                           user_count=user_count,
                           pred_count=pred_count,
                           metrics=metrics)


@app.route('/admin/metrics')
@login_required
@admin_required
def admin_metrics():
    metrics_list = db.get_all_model_metrics()
    return render_template('admin/metrics.html', metrics=metrics_list)


@app.route('/admin/predictions')
@login_required
@admin_required
def admin_predictions():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    predictions = db.get_all_predictions(limit=per_page, offset=offset)
    total = db.get_prediction_count()
    pages = (total + per_page - 1) // per_page
    return render_template('admin/predictions.html',
                           predictions=predictions,
                           page=page,
                           pages=pages,
                           total=total)


@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = db.get_all_users()
    return render_template('admin/users.html', users=users)


@app.route('/admin/diseases')
@login_required
@admin_required
def admin_diseases():
    diseases = db.get_all_diseases()
    return render_template('admin/diseases.html', diseases=diseases)


@app.route('/admin/diseases/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_disease_add():
    if request.method == 'POST':
        db.create_disease(
            request.form.get('disease_name'),
            request.form.get('crop_type'),
            request.form.get('description'),
            request.form.get('symptoms'),
            request.form.get('causes'),
            request.form.get('treatment'),
            request.form.get('prevention'),
            request.form.get('severity_level', 'medium'),
        )
        flash('Disease added.', 'success')
        return redirect(url_for('admin_diseases'))
    return render_template('admin/disease_form.html', disease=None)


@app.route('/admin/diseases/edit/<int:disease_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_disease_edit(disease_id):
    disease = db.get_disease_by_id(disease_id)
    if not disease:
        flash('Disease not found.', 'danger')
        return redirect(url_for('admin_diseases'))
    if request.method == 'POST':
        db.update_disease(
            disease_id,
            disease_name=request.form.get('disease_name'),
            crop_type=request.form.get('crop_type'),
            description=request.form.get('description'),
            symptoms=request.form.get('symptoms'),
            causes=request.form.get('causes'),
            treatment=request.form.get('treatment'),
            prevention=request.form.get('prevention'),
            severity_level=request.form.get('severity_level'),
        )
        flash('Disease updated.', 'success')
        return redirect(url_for('admin_diseases'))
    return render_template('admin/disease_form.html', disease=disease)


@app.route('/admin/diseases/delete/<int:disease_id>', methods=['POST'])
@login_required
@admin_required
def admin_disease_delete(disease_id):
    if db.delete_disease(disease_id):
        flash('Disease deleted.', 'success')
    else:
        flash('Failed to delete.', 'danger')
    return redirect(url_for('admin_diseases'))


# Static files for uploads
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(str(UPLOAD_FOLDER), filename)


if __name__ == '__main__':
    # Ensure upload folder exists
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    app.run(debug=True, port=5000)
