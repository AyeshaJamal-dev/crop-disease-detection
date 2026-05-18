"""
Configuration settings for Crop Disease Detection System.
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# MySQL configuration
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'crop_disease_db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

# Upload configuration
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jpe'}

# ML Model configuration
MODEL_PATH = BASE_DIR / 'models' / 'saved_model' / 'crop_disease_model.keras'
CLASS_LABELS_PATH = BASE_DIR / 'models' / 'saved_model' / 'class_labels.json'
IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224

# Dataset paths
DATASETS_DIR = BASE_DIR / 'datasets'
TRAIN_DIR = DATASETS_DIR / 'train'
TEST_DIR = DATASETS_DIR / 'test'

# Static paths for admin
CONFUSION_MATRIX_PATH = BASE_DIR / 'static' / 'images' / 'confusion_matrix.png'
TRAINING_CURVES_PATH = BASE_DIR / 'static' / 'images' / 'training_curves.png'
