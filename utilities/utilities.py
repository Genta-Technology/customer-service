"""
Utility file and code for environment loading
"""

import os
from dotenv import load_dotenv, find_dotenv

class EnvironmentVariables:
    """
    This class is used to load environment variables from a .env file.
    """

    def __init__(self):
        """
        Initialize the class.
        """

        # Load environment variables from .env file
        self.env_file = find_dotenv()
        if self.env_file:
            load_dotenv(self.env_file)

    def get(self, key: str) -> str:
        """
        Get an environment variable.

        Args:
            key (str): Environment variable key.

        Returns:
            str: Environment variable value.
        """

        return os.environ.get(key)

    def __call__(self, key: str) -> str:
        """
        Get an environment variable.

        Args:
            key (str): Environment variable key.

        Returns:
            str: Environment variable value.
        """

        return self.get(key)

    def __getitem__(self, key: str) -> str:
        """
        Get an environment variable.

        Args:
            key (str): Environment variable key.

        Returns:
            str: Environment variable value.
        """

        return self.get(key)
