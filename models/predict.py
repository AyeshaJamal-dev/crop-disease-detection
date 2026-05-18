"""
Prediction module - load model and run inference on uploaded images.
"""
import json
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from preprocessing.image_preprocessing import preprocess_image

SAVED_MODEL_DIR = PROJECT_ROOT / 'models' / 'saved_model'
MODEL_PATH = SAVED_MODEL_DIR / 'crop_disease_model.keras'
CLASS_LABELS_PATH = SAVED_MODEL_DIR / 'class_labels.json'

_model = None
_class_labels = None


def _load_model():
    global _model, _class_labels
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found. Train first: {MODEL_PATH}")
        _model = tf.keras.models.load_model(str(MODEL_PATH))
        with open(CLASS_LABELS_PATH) as f:
            _class_labels = json.load(f)
    return _model, _class_labels


def predict(image_input):
    """
    Run disease prediction on an image.

    Args:
        image_input: file path (str) or numpy array or PIL Image

    Returns:
        dict: {
            'disease': str (e.g. 'Tomato___Early_blight'),
            'crop_type': str (e.g. 'Tomato'),
            'confidence': float (0-1),
            'status': 'detected' or 'healthy',
        }
    """
    model, labels = _load_model()
    img = preprocess_image(image_input)
    probs = model.predict(img, verbose=0)[0]
    pred_idx = int(np.argmax(probs))
    confidence = float(probs[pred_idx])

    idx_to_class = labels['idx_to_class']
    # idx_to_class keys may be int or str
    pred_class = idx_to_class.get(str(pred_idx), idx_to_class.get(pred_idx, 'Unknown'))

    # Extract crop type (e.g. "Tomato___Early_blight" -> "Tomato")
    crop_type = pred_class.split('___')[0] if '___' in pred_class else pred_class

    # Determine status
    status = 'healthy' if 'healthy' in pred_class.lower() else 'detected'

    return {
        'disease': pred_class,
        'crop_type': crop_type,
        'confidence': round(confidence * 100, 2),
        'status': status,
    }


def get_all_class_names():
    """Return list of all disease/class names for lookup."""
    _, labels = _load_model()
    idx_to_class = labels['idx_to_class']
    return [idx_to_class[str(i)] for i in range(labels['num_classes'])]
