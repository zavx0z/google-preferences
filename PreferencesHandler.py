import json
import os
from pathlib import Path
import yaml


def preferences_read(file_path):
    """ Read preferences from a file.

    Args:
        file_path (str or pathlib.Path): The file path of the preferences file.

    Returns:
        dict: A dictionary containing the preferences, or an empty dictionary if the file was not found.
    """
    file_path = Path(file_path)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def preferences_write(preferences, file_path, indent=False):
    """Write preferences to file

    Args:
        preferences (dict): The dictionary of preferences to write.
        file_path (str or Path): The path to the file to write.
        indent (bool, optional): Space formatted. Defaults to False..
    """
    kwargs = {}
    if indent:
        kwargs['indent'] = 2
    Path(file_path).write_text(json.dumps(preferences, ensure_ascii=False, **kwargs))


def update_nested_dict(source_dict, update_dict):
    """
    Updates the nested dictionary `source_dict` with the values from `update_dict`.

    Args:
        source_dict (dict): The dictionary to be updated.
        update_dict (dict): The dictionary whose values will be used to update `source_dict`.

    Returns:
        dict: The updated nested dictionary.
    """
    for key, value in update_dict.items():
        if isinstance(value, dict):
            source_dict[key] = update_nested_dict(source_dict.get(key, {}), value)
        else:
            source_dict[key] = value
    return source_dict


def serialize_config(confs, level=0):
    """
    Serializes values of a configuration for Google Chrome.

    Args:
        confs (dict): The dictionary to be serialized.
    Returns:
        dict: The serialized dictionary.
    """
    serialized_preferences = {}
    for key, value in confs.items():
        if key == 'devtools':
            if type(value) == dict:
                level += 1
                serialized_preferences[key] = serialize_config(value, level=level)
        elif level == 1 and type(value) == dict:
            serialized_preferences[key] = serialize_config(value, level=level + 1)
        elif level == 2:
            serialized_preferences[key] = json.dumps(value)
        else:
            if type(value) == dict:
                serialized_preferences[key] = serialize_config(value)
            else:
                serialized_preferences[key] = value
    return serialized_preferences


def load_config(file_path):
    """
    Load the config from a YAML file.

    Args:
        file_path (str or Path): The file path to load the preferences from.

    Returns:
        dict: The preferences loaded from the file.
    """
    file_path = Path(file_path)
    with open(file_path, 'r') as file:
        preferences = yaml.safe_load(file)
    return serialize_config(preferences)


def update_preferences(user_data_dir, config_file):
    """
    Updates preferences file with the default preferences.

    Args:
        user_data_dir (str or Path): The path to the google-chrome --user-data-dir.
        config_file (str or Path): The path to the default preferences file.
    """
    preferences_dir = Path(user_data_dir).resolve() / 'Default'
    preferences_dir.mkdir(parents=True, exist_ok=True)
    preferences_file = preferences_dir / "Preferences"

    conf_file = Path(config_file).resolve()

    preferences = preferences_read(preferences_file)
    default_preferences = load_config(conf_file)
    preferences = update_nested_dict(preferences, default_preferences)
    preferences_write(preferences, preferences_file)


if __name__ == '__main__':
    import argparse

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Process some preferences.')
    # Add arguments for the config file and user data directory
    parser.add_argument(
        '-c', '--config',
        type=str, required=False, help='Configuration in config.yml',
        default=Path(__file__).parent / 'config.yml'
    )
    parser.add_argument(
        '-u', '--user-data-dir',
        type=str, required=False,
        help='path google-chrome --user-data-dir',
        default=Path(os.environ.get('HOME')).resolve() / '.config/google-chrome'
    )
    # Parse the arguments
    args = parser.parse_args()
    # Call the update_preferences function
    update_preferences(args.user_data_dir, args.config)
