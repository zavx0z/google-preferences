from pathlib import Path

from PreferencesHandler import update_preferences


def test_update_preferences():
    update_preferences(Path("tests/Preferences.json"), Path('config.yml'))
    assert True
