from unittest.mock import patch
from homesaver import get_home_directory, create_backup
from pathlib import Path

@patch("pathlib.Path.home", return_value=Path("/mock/home"))
def test_get_home_directory(mock_home):
    home_dir = get_home_directory()
    assert home_dir == Path("/mock/home"), "Le répertoire personnel doit être mocké."

@patch("homesaver.get_home_directory")
def test_create_backup(mock_get_home_directory, tmp_path):
    mock_get_home_directory.return_value = tmp_path
    backup_file = create_backup("test_backup")
    assert Path(backup_file).exists(), "L'archive de sauvegarde doit être créée."
    assert backup_file.endswith(".zip"), "L'archive doit être au format ZIP."
