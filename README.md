# GoogleChrome PreferencesHandler

A Python library for modifying Google Chrome browser Preferences file.
This library is a tool for customizing the settings in a Google Chrome browser.
It allows users to load and update their preferences stored in a JSON file,
and to save the updated information back to the file.
If the user's preferences file is not found, the default values will be set.

## Features

* Load and write preferences from/to a file in JSON format
* Update a nested dictionary with another dictionary
* Serialize a nested dictionary of preferences into a flat dictionary
* Load preferences from a YAML file

## Requirements

* Python >= 3.6
* PyYAML >= 5.3.1

```shell
pip install -r requirements.txt
```

## Usage

To use the library, simply run it commandline program with the following arguments:

`--user-data-dir` - the path to the user data directory of Google Chrome, where the Preferences file is located.

`--config`- the path to the YAML file with the configuration. The default file is config.yml.

```shell
python PreferencesHandler.py --config=config.yml --user-data-dir=/home/$USER/.config/google-chrome/Default/Preferences
```

## License

This library is licensed under the MIT License

## Author
The library was created by zavx0z and is maintained by chat GPT, a language model created by OpenAI.
The library is available on [Github](https://github.com/zavx0z/google-preferences.git)