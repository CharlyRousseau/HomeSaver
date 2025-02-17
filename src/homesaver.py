import zipfile
import os
from pathlib import Path
import progressbar
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_home_directory():
    return Path.home()

def create_backup(backup_name="backup"):
    home_dir = get_home_directory()
    backup_path = home_dir / backup_name
    backup_file = str(backup_path) + ".zip"

    try:
        total_files = sum([len(files) for _, _, files in os.walk(home_dir)])

        bar = progressbar.ProgressBar(widgets=[
            ' [', progressbar.Percentage(), '] ',
            progressbar.Bar(), ' ',
            progressbar.ETA()
        ], max_value=total_files)

        bar.start()

        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
            file_count = 0
            for root, dirs, files in os.walk(home_dir):
                for file in files:
                    if file.endswith('.zip'):
                        continue
                    try:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), home_dir))
                    except Exception as e:
                        logger.error(f"An error occurred while adding {file} to the backup: {e}")

                    file_count += 1
                    bar.update(file_count)
        bar.finish()
        logger.info(f"Backup created successfully: {backup_file}")

    except Exception as e:
        logger.error(f"An error occurred during the backup process: {e}")

    finally:
        logger.info("Backup process completed.")
        return backup_file


if __name__ == "__main__":
    logger.info("Creating Backup...")
    backup_file = create_backup()
    logger.info(f"Backup created successfully: {backup_file}")
