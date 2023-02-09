from PreferencesHandler import preferences_read, preferences_write

preferences = preferences_read('/home/zavx0z/projects/bib/user_data_dir/Default/Preferences')
preferences_write(preferences, 'chrome_configs/Preferences.json', indent=True)
