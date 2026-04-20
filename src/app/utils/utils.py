# -*- coding: utf-8 -*-

import logging
import os

from flask import g
from flask_appbuilder.filemanager import ImageManager
from PIL import Image
from werkzeug.utils import secure_filename

_logger = logging.getLogger(__name__)


def get_user():
    return g.user


def process_and_save_image(image_file, upload_folder):
    """Process and save an uploaded image, returning the saved filename."""
    image_manager = ImageManager()

    if not image_file:
        return None

    img = Image.open(image_file)

    # Ensure correct color mode
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    if img.mode in ("RGBA", "LA"):
        img = img.convert("RGB")

    img.thumbnail((530, 310))

    filename = secure_filename(image_file.filename)
    file_path = os.path.join(upload_folder, filename)
    image_manager.save_image(img, file_path)
    return filename
