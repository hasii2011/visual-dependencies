
from typing import cast

from logging import Logger
from logging import getLogger
from logging import config as loggingConfig

from os import sep as osSep

from json import load as jsonLoad

from wx import App
from wx import BITMAP_TYPE_JPEG
from wx import BLACK
from wx import Bitmap
from wx import BoxSizer
from wx import Colour

from wx.lib.agw.advancedsplash import AS_CENTER_ON_PARENT
from wx.lib.agw.advancedsplash import AS_SHADOW_BITMAP
from wx.lib.agw.advancedsplash import AS_TIMEOUT

from wx.lib.agw.advancedsplash import AdvancedSplash

from codeallybasic.ResourceManager import ResourceManager

from visualdependencies.ApplicationFrame import ApplicationFrame


class VisualDependencies(App):

    MINI_GAP:         int = 3
    NOTHING_SELECTED: int = -1

    # noinspection SpellCheckingInspection
    RESOURCE_ENV_VAR:             str = 'RESOURCEPATH'
    # noinspection SpellCheckingInspection
    RESOURCES_PACKAGE_NAME:       str = 'visualdependencies.resources'
    RESOURCES_IMAGE_PACKAGE_NAME: str = f'{RESOURCES_PACKAGE_NAME}.images'

    # noinspection SpellCheckingInspection
    RESOURCES_PATH:       str = f'visualdependencies{osSep}resources'
    RESOURCES_IMAGE_PATH: str = f'{RESOURCES_PATH}{osSep}images'

    JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"

    def __init__(self, redirect: bool = False):

        self._frame: ApplicationFrame  = cast(ApplicationFrame, None)

        VisualDependencies.setupSystemLogging()

        self.logger: Logger = getLogger(__name__)

        super().__init__(redirect)

    def OnInit(self):

        self._frame = ApplicationFrame()

        self._frame.Show(False)

        self.SetTopWindow(self._frame)

        mainSizer: BoxSizer = self._frame.GetContainingSizer()

        self._frame.SetAutoLayout(True)
        self._frame.SetSizer(mainSizer)
        self._frame.Show(True)

        self._showSplash()
        return True

    def OnExit(self):
        """
        """
        try:
            return App.OnExit(self)
        except (ValueError, Exception) as e:
            self.logger.error(f'OnExit: {e}')

    @classmethod
    def setupSystemLogging(cls):

        import logging

        configFilePath: str = ResourceManager.retrieveResourcePath(bareFileName=VisualDependencies.JSON_LOGGING_CONFIG_FILENAME,
                                                                   resourcePath=VisualDependencies.RESOURCES_PATH,
                                                                   packageName=VisualDependencies.RESOURCES_PACKAGE_NAME)
        with open(configFilePath, 'r') as loggingConfigurationFile:
            configurationDictionary = jsonLoad(loggingConfigurationFile)

        loggingConfig.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads   = False

    def _showSplash(self):

        fqFileName: str = ResourceManager.retrieveResourcePath(bareFileName='DependencySplash.jpg',
                                                               resourcePath=VisualDependencies.RESOURCES_IMAGE_PATH,
                                                               packageName=VisualDependencies.RESOURCES_IMAGE_PACKAGE_NAME)
        splashBitmap: Bitmap = Bitmap(name=fqFileName, type=BITMAP_TYPE_JPEG)
        shadow:       Colour = BLACK
        agwStyle:     int    = AS_TIMEOUT | AS_CENTER_ON_PARENT | AS_SHADOW_BITMAP

        AdvancedSplash(parent=self._frame, bitmap=splashBitmap, timeout=5000, shadowcolour=shadow, agwStyle=agwStyle)

    def _createSelectionControls(self) -> BoxSizer:
        pass


if __name__ == "__main__":

    print(f'Starting Visual Dependencies')

    visualDependencies: VisualDependencies = VisualDependencies()

    visualDependencies.MainLoop()
