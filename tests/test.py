from pathlib import Path

from PreferencesHandler import update_preferences, preferences_read, preferences_write


def test_update_preferences():
    update_preferences("google-chrome", "config.yml")
    assert True


def test_indent_json_preferences():
    preferences = preferences_read('google-chrome/Default/Preferences')
    preferences_write(preferences, 'tests/Preferences.json', indent=True)
