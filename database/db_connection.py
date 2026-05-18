"""
Database connection and helper functions for Crop Disease Detection.
"""
import sys
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import (MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT,
                    MYSQL_USER)


def get_connection():
    """Create and return a MySQL connection."""
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT,
            autocommit=True,
        )
    except Error as e:
        raise RuntimeError(f"Database connection failed: {e}")


def create_user(full_name, email, password, user_type='farmer', phone=None, location=None):
    """Create a new user. Returns user_id or None on duplicate email."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        hashed = generate_password_hash(password)
        cursor.execute(
            """INSERT INTO users (full_name, email, password, user_type, phone, location)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (full_name, email, hashed, user_type, phone, location)
        )
        return cursor.lastrowid
    except Error as e:
        if e.errno == 1062:  # Duplicate entry
            return None
        raise
    finally:
        conn.close()


def get_user_by_email(email):
    """Get user dict by email or None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, full_name, email, password, user_type, phone, location, created_at FROM users WHERE email = %s",
            (email,)
        )
        return cursor.fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id):
    """Get user dict by user_id or None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, full_name, email, user_type, phone, location, created_at FROM users WHERE user_id = %s",
            (user_id,)
        )
        return cursor.fetchone()
    finally:
        conn.close()


def insert_prediction(user_id, image_path, predicted_disease, confidence_score, crop_type, status):
    """Insert a prediction record. Returns prediction_id."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO predictions (user_id, image_path, predicted_disease, confidence_score, crop_type, status)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, image_path, predicted_disease, confidence_score, crop_type, status)
        )
        return cursor.lastrowid
    finally:
        conn.close()


def get_prediction_by_id(prediction_id):
    """Get prediction dict by id or None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT p.*, u.full_name FROM predictions p
               JOIN users u ON p.user_id = u.user_id
               WHERE p.prediction_id = %s""",
            (prediction_id,)
        )
        return cursor.fetchone()
    finally:
        conn.close()


def get_user_predictions(user_id, limit=50):
    """Get predictions for a user, most recent first."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM predictions WHERE user_id = %s ORDER BY prediction_date DESC LIMIT %s""",
            (user_id, limit)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_disease_info(disease_name):
    """Get disease details by name (exact or fuzzy match). Returns dict or None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM diseases WHERE disease_name = %s",
            (disease_name,)
        )
        row = cursor.fetchone()
        if row:
            return row
        # Try LIKE match (disease_name may have variations)
        cursor.execute(
            "SELECT * FROM diseases WHERE disease_name LIKE %s LIMIT 1",
            (f"%{disease_name.split('___')[-1] if '___' in disease_name else disease_name}%",)
        )
        return cursor.fetchone()
    finally:
        conn.close()


def insert_feedback(user_id, prediction_id, feedback=None, accuracy_rating=None):
    """Insert detection history / feedback."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO detection_history (user_id, prediction_id, feedback, accuracy_rating)
               VALUES (%s, %s, %s, %s)""",
            (user_id, prediction_id, feedback, accuracy_rating)
        )
        return cursor.lastrowid
    finally:
        conn.close()


def insert_model_metrics(accuracy, precision_score, recall_score, f1_score, model_version='1.0'):
    """Insert model metrics after training."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO model_metrics (model_version, accuracy, precision_score, recall_score, f1_score)
               VALUES (%s, %s, %s, %s, %s)""",
            (model_version, accuracy, precision_score, recall_score, f1_score)
        )
        return cursor.lastrowid
    finally:
        conn.close()


def get_latest_model_metrics():
    """Get the most recent model metrics."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM model_metrics ORDER BY training_date DESC LIMIT 1"
        )
        return cursor.fetchone()
    finally:
        conn.close()


def get_all_model_metrics(limit=10):
    """Get recent model metrics for admin."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM model_metrics ORDER BY training_date DESC LIMIT %s",
            (limit,)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_user_count():
    """Get total user count."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def get_prediction_count():
    """Get total prediction count."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions")
        return cursor.fetchone()[0]
    finally:
        conn.close()


def get_all_predictions(limit=100, offset=0):
    """Get all predictions (admin)."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT p.*, u.full_name, u.email FROM predictions p
               JOIN users u ON p.user_id = u.user_id
               ORDER BY p.prediction_date DESC LIMIT %s OFFSET %s""",
            (limit, offset)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_all_users():
    """Get all users (admin)."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, full_name, email, user_type, phone, location, created_at FROM users"
        )
        return cursor.fetchall()
    finally:
        conn.close()


def get_disease_by_id(disease_id):
    """Get disease by id or None."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diseases WHERE disease_id = %s", (disease_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def get_all_diseases():
    """Get all diseases from knowledge base."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM diseases ORDER BY crop_type, disease_name")
        return cursor.fetchall()
    finally:
        conn.close()


def create_disease(disease_name, crop_type, description=None, symptoms=None, causes=None, treatment=None, prevention=None, severity_level='medium'):
    """Create a new disease entry."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO diseases (disease_name, crop_type, description, symptoms, causes, treatment, prevention, severity_level)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (disease_name, crop_type, description, symptoms, causes, treatment, prevention, severity_level)
        )
        return cursor.lastrowid
    finally:
        conn.close()


def update_disease(disease_id, **kwargs):
    """Update disease by id."""
    allowed = {'disease_name', 'crop_type', 'description', 'symptoms', 'causes', 'treatment', 'prevention', 'severity_level'}
    updates = [(k, v) for k, v in kwargs.items() if k in allowed and v is not None]
    if not updates:
        return False
    conn = get_connection()
    try:
        cursor = conn.cursor()
        set_clause = ', '.join(f"{k} = %s" for k, _ in updates)
        values = [v for _, v in updates] + [disease_id]
        cursor.execute(f"UPDATE diseases SET {set_clause} WHERE disease_id = %s", values)
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_disease(disease_id):
    """Delete disease by id."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diseases WHERE disease_id = %s", (disease_id,))
        return cursor.rowcount > 0
    finally:
        conn.close()
