import os
import shutil
import logging

logger = logging.getLogger(__name__)

def clean_temp_files(file_path: str):
    try:
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                shutil.rmtree(file_path)
    except Exception as e:
        logger.error(f"An error occurred while cleaning temporary files: {str(e)}")
        raise e

def validate_pdf(file):
    # Check file signature for PDF validation
    header = file.file.read(4)
    file.file.seek(0)
    if header != b'%PDF':
        raise ValueError("Invalid PDF file format")
    return True