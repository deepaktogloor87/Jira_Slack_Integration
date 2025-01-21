import configparser
import os

class ConfigReader:
    def __init__(self, config_file='./configurations/conf.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

    def read_config_values(self):
        # Check if the config file exists
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        # Read the config file
        self.config.read(self.config_file)

        return self.config

    def read_locators(self):
        # Check if the config file exists
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

        # Read the config file
        self.config.read(self.config_file)

        return self.config
