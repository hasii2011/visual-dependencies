
from typing import Dict

from logging import Logger
from logging import getLogger

from configparser import ConfigParser

from pathlib import Path

from visualdependencies.futures.ConfigurationLocator import ConfigurationLocator
from visualdependencies.futures.SingletonV2 import singleton

from visualdependencies import __applicationName__


PREFERENCES_FILE_NAME: str = 'preferences.ini'

PREFERENCES_NAME_VALUES = Dict[str, str]

PREFERENCES_SECTION: str = __applicationName__

DEBUG_PROJECTS_DIRECTORY: str = '/Users/humberto.a.sanchez.ii/PycharmProjects/'

PROJECTS_BASE_DIRECTORY: str = 'projects_base_directory'
OPEN_PROJECT:            str = 'open_project'
EXPAND_DEPENDENCIES:     str = 'expand_dependencies'

PREFERENCES: PREFERENCES_NAME_VALUES = {
    PROJECTS_BASE_DIRECTORY: DEBUG_PROJECTS_DIRECTORY,
    OPEN_PROJECT:            'True',
    EXPAND_DEPENDENCIES:     'False',
}


@singleton
class Preferences:

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        cl: ConfigurationLocator = ConfigurationLocator()

        self._preferencesFileName: Path        = cl.applicationPath(f'{__applicationName__.lower()}') / PREFERENCES_FILE_NAME
        self._config:              ConfigParser = ConfigParser()
        self._loadPreferences()

    @property
    def projectsBaseDirectory(self) -> str:

        fullPath: str = self._config.get(PREFERENCES_SECTION, PROJECTS_BASE_DIRECTORY)
        return fullPath

    @projectsBaseDirectory.setter
    def projectsBaseDirectory(self, newValue: str):
        self._config.set(PREFERENCES_SECTION, PROJECTS_BASE_DIRECTORY, newValue)
        self._savePreferences()

    @property
    def openProject(self) -> bool:
        return self._config.getboolean(section=PREFERENCES_SECTION, option=OPEN_PROJECT)

    @openProject.setter
    def openProject(self, newValue: bool):
        self._config.set(section=PREFERENCES_SECTION, option=OPEN_PROJECT, value=str(newValue))
        self._savePreferences()

    @property
    def expandDependencies(self) -> bool:
        return self._config.getboolean(section=PREFERENCES_SECTION, option=EXPAND_DEPENDENCIES)

    @expandDependencies.setter
    def expandDependencies(self, newValue: bool):
        self._config.set(section=PREFERENCES_SECTION, option=EXPAND_DEPENDENCIES, value=str(newValue))
        self._savePreferences()

    def _loadPreferences(self):

        self._ensurePreferenceFileExists()

        # Read data
        self._config.read(self._preferencesFileName)
        self._addMissingPreferences()
        self._savePreferences()

    def _ensurePreferenceFileExists(self):

        try:
            # noinspection PyUnusedLocal
            with open(self._preferencesFileName, "r") as f:
                pass
        except (ValueError, Exception):
            try:
                with open(self._preferencesFileName, "w") as fw:
                    fw.write("")
                    self.logger.warning(f'Preferences file re-created')
            except (ValueError, Exception) as e:
                self.logger.error(f"Error: {e}")
                return

    def _addMissingPreferences(self):

        try:
            if self._config.has_section(PREFERENCES_SECTION) is False:
                self._config.add_section(PREFERENCES_SECTION)

            for preferenceName in PREFERENCES:
                if self._config.has_option(PREFERENCES_SECTION, preferenceName) is False:

                    self._config.set(section=PREFERENCES_SECTION, option=preferenceName, value=PREFERENCES[preferenceName])
                    self._savePreferences()

        except (ValueError, Exception) as e:
            self.logger.error(f"Error: {e}")

    def _savePreferences(self):
        """
        Save data to the preferences file
        """
        with open(self._preferencesFileName, "w") as fd:
            self._config.write(fd)
