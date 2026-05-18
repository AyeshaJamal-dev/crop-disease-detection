# Crop Disease Detection System

An AI-powered web application that detects crop diseases from leaf images using Convolutional Neural Networks (CNN). Built with Flask, TensorFlow/Keras, and MySQL.

## 🌟 Features

- **User Registration & Login**: Farmer and admin accounts
- **Leaf Image Upload**: Drag-and-drop or browse to upload leaf images
- **Real-time Disease Detection**: CNN model predicts disease with confidence score
- **Treatment Recommendations**: Disease knowledge base with symptoms, causes, treatment, prevention
- **Detection History**: View and manage past predictions
- **Feedback**: Rate prediction accuracy
- **Admin Dashboard**: User management, disease CRUD, model metrics, analytics

---

## 📋 Prerequisites

- **Python 3.10+**
- **MySQL 8+** (local or remote)
- **Internet connection** (for first-time setup to download datasets & models)
- **~3-4GB disk space** (for datasets + models after setup)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YourUsername/crop-disease-detection.git
cd crop-disease-detection
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This automatically installs:

- Flask (Web framework)
- TensorFlow/Keras (AI Model)
- MySQL Connector (Database)
- OpenCV (Image processing)
- And all other dependencies

### Step 4: Setup MySQL Database

```bash
# Create database and tables
mysql -u root -p < database/schema.sql

# Load disease data
mysql -u root -p crop_disease_db < database/seed_data.sql
```

### Step 5: Create Environment Configuration

Create a `.env` file in the project root:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=crop_disease_db
MYSQL_PORT=3306
SECRET_KEY=change-this-to-a-random-secret-key
FLASK_ENV=development
DEBUG=True
```

**⚠️ Security Note**: Change `SECRET_KEY` to a strong random value in production.

### Step 6: Download Pre-trained Model & Dataset

Run the download script (one-time setup, ~2-3 GB, takes 10-30 minutes):

```bash
python preprocessing/download_dataset.py
```

This automatically:

- ✅ Downloads PlantVillage dataset (~2GB)
- ✅ Downloads pre-trained CNN model
- ✅ Sets up datasets/raw, datasets/train, datasets/test folders

### Step 7: Create Admin User

```bash
python -c "from database.db_connection import create_user; create_user('Admin', 'admin@cropdisease.com', 'admin123', 'admin')"
```

Or via the Flask shell:

```bash
python
>>> from database.db_connection import create_user
>>> create_user('Admin', 'admin@cropdisease.com', 'admin123', 'admin')
```

### Step 8: Run the Application

```bash
python app.py
```

Open your browser: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
crop-disease-detection/
├── app.py                          # Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create yourself)
├── .gitignore                      # Git ignore rules
│
├── database/
│   ├── __init__.py
│   ├── db_connection.py           # MySQL connection & queries
│   ├── schema.sql                 # Database schema
│   └── seed_data.sql              # Initial disease data
│
├── models/
│   ├── __init__.py
│   ├── model_architecture.py      # CNN model definition
│   ├── predict.py                 # Inference module
│   └── saved_model/               # Pre-trained model (downloaded at setup)
│       ├── crop_disease_model.keras
│       └── class_labels.json
│
├── preprocessing/
│   ├── __init__.py
│   ├── download_dataset.py        # Download datasets & models
│   ├── image_preprocessing.py     # Image processing utilities
│   └── data_augmentation.py       # Data augmentation techniques
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── images/                    # Static images
│   └── uploads/                   # User uploads (created at runtime)
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── results.html
│   ├── history.html
│   └── admin/                     # Admin dashboard templates
│
├── datasets/                      # Populated by download_dataset.py
│   ├── raw/
│   ├── train/
│   └── test/
│
├── docs/
│   ├── API.md
│   └── USER_MANUAL.md
│
├── training/
│   ├── __init__.py
│   └── train_model.py            # Model training script
│
└── README.md                      # This file
```

---

## 🌾 What's Included vs Downloaded

### ✅ In This GitHub Repository (~100-150 MB)

- Complete source code
- Flask application & routes
- Database schema & seed data
- HTML templates & CSS/JS
- Model architecture
- Pre-processing & utility scripts
- Documentation

### 📥 Downloaded During First Setup (~2-3 GB)

- PlantVillage dataset (~2GB)
- Pre-trained CNN model (~50-150 MB)
- Training splits (train/test/val)

Run `python preprocessing/download_dataset.py` to download automatically.

---

## 🧠 Model Information

- **Architecture**: Convolutional Neural Network (CNN)
  - 3 Conv blocks (32, 64, 128 filters)
  - Max pooling layers
  - Dense layer (256 units)
  - Dropout (0.5)
  - Output: Softmax over disease classes

- **Input**: 224×224 RGB images
- **Output**: Disease class + confidence score
- **Expected Accuracy**: 90-95% on test set
- **Training Data**: PlantVillage dataset (~25,000 images, 38 classes)

---

## 📊 Supported Crops & Diseases

The model is trained on:

- **Tomato** (10 classes): Bacterial spot, Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Tomato mosaic virus, Yellow leaf curl virus, Healthy
- **Potato** (3 classes): Early blight, Late blight, Healthy
- **Corn** (4 classes): Cercospora leaf spot, Common rust, Northern leaf blight, Healthy
- **Apple** (4 classes): Apple scab, Black rot, Cedar apple rust, Healthy
- **Grape** (4 classes): Black rot, Esca, Leaf blight, Healthy

Plus background images and other crops.

---

## 🔌 API Endpoints

| Route             | Method    | Description                |
| ----------------- | --------- | -------------------------- |
| `/`               | GET       | Home page                  |
| `/register`       | GET, POST | User registration          |
| `/login`          | GET, POST | User login                 |
| `/logout`         | GET       | User logout                |
| `/dashboard`      | GET       | User dashboard             |
| `/upload`         | GET, POST | Upload image for detection |
| `/results/<id>`   | GET       | View prediction details    |
| `/history`        | GET       | Detection history          |
| `/admin`          | GET       | Admin dashboard            |
| `/admin/diseases` | GET, POST | Manage diseases            |
| `/admin/users`    | GET       | User management            |
| `/admin/metrics`  | GET       | Model metrics              |

---

## 🛠️ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'mysql'`

**Solution**: Run `pip install -r requirements.txt` again

### Issue: MySQL connection failed

**Solution**:

- Ensure MySQL is running
- Check credentials in `.env`
- Verify database created: `mysql -u root -p -e "SHOW DATABASES;"`

### Issue: Dataset download fails

**Solution**:

- Check internet connection
- Ensure ~3GB free disk space
- Manually download from [PlantVillage](https://plantvillage.psu.edu/)

### Issue: Model not found at startup

**Solution**:

- Run `python preprocessing/download_dataset.py` first
- Check `models/saved_model/` folder exists with `.keras` file

---

## 📚 Documentation

- **API Details**: See [docs/API.md](docs/API.md)
- **User Manual**: See [docs/USER_MANUAL.md](docs/USER_MANUAL.md)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/YourFeature`
3. **Commit** changes: `git commit -m "Add YourFeature"`
4. **Push** to branch: `git push origin feature/YourFeature`
5. **Open** a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YourUsername/crop-disease-detection/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YourUsername/crop-disease-detection/discussions)

---

**Last Updated**: May 2026 | **Version**: 1.0
