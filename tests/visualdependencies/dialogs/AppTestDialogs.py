
from logging import Logger
from logging import getLogger
from typing import cast

from codeallybasic.UnitTestBase import UnitTestBase

from wx import App

from tests.visualdependencies.dialogs.AppTestDialogFrame import AppTestDialogFrame


class AppTestDialogs(App):

    def __init__(self):

        UnitTestBase.setUpLogging()

        self.logger: Logger = getLogger(__name__)

        self._frame: AppTestDialogFrame = cast(AppTestDialogFrame, None)

        super().__init__(redirect=False)

    def OnInit(self):

        self._frame = AppTestDialogFrame()

        self._frame.SetAutoLayout(True)
        self._frame.Show(True)

        self.SetTopWindow(self._frame)

        return True


testApp: AppTestDialogs = AppTestDialogs()

testApp.MainLoop()
