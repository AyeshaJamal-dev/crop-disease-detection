"""
Image preprocessing for crop disease detection.
Resize to 224x224, normalize to [0, 1], ensure RGB.
"""
import numpy as np
from PIL import Image

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

# Default dimensions (matches CNN input)
IMG_WIDTH = 224
IMG_HEIGHT = 224


def preprocess_image(image_input, target_size=(IMG_WIDTH, IMG_HEIGHT)):
    """
    Preprocess image for model inference.

    Args:
        image_input: numpy array (H,W,3) or file path or PIL Image
        target_size: (width, height) tuple

    Returns:
        numpy array of shape (1, H, W, 3) normalized to [0, 1]
    """
    if isinstance(image_input, str):
        img = np.array(Image.open(image_input).convert('RGB'))
    elif isinstance(image_input, Image.Image):
        img = np.array(image_input.convert('RGB'))
    else:
        img = np.asarray(image_input)
        if len(img.shape) == 2:
            img = np.stack([img] * 3, axis=-1)
        elif img.shape[-1] == 4:
            img = img[:, :, :3]

    # Resize
    if HAS_CV2:
        img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
    else:
        pil_img = Image.fromarray(img)
        pil_img = pil_img.resize(target_size, Image.BILINEAR)
        img = np.array(pil_img)

    # Normalize to [0, 1]
    img = img.astype(np.float32) / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    return img


def load_and_preprocess(file_path, target_size=(IMG_WIDTH, IMG_HEIGHT)):
    """Load image from path and preprocess. Returns (1, H, W, 3) array."""
    return preprocess_image(file_path, target_size)
