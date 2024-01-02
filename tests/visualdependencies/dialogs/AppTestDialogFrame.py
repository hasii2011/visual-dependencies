from typing import Any
from typing import Optional

from logging import Logger
from logging import getLogger

from enum import Enum

from os import getenv as osGetEnv

from wx import CB_READONLY
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_COMBOBOX
from wx import FRAME_EX_METAL
from wx import FRAME_FLOAT_ON_PARENT
from wx import FRAME_TOOL_WINDOW
from wx import ID_ANY

from wx import ComboBox
from wx import CommandEvent
from wx import ID_OK

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedStaticBox

from visualdependencies.dialogs.PreferencesDialog import PreferencesDialog


class DialogNamesEnum(Enum):

    DLG_PREFERENCES     = 'DlgPreferences'
    DLG_ABOUT           = 'DlgAbout'


class AppTestDialogFrame(SizedFrame):

    APP_MODE:         str = 'APP_MODE'

    NOTHING_SELECTED: int = -1

    def __init__(self):

        appModeStr: Optional[str] = osGetEnv(AppTestDialogFrame.APP_MODE)
        if appModeStr is None:
            appMode: bool = False
        else:
            appMode = AppTestDialogFrame.secureBoolean(appModeStr)
        # wxPython 4.2.0 update:  using FRAME_TOOL_WINDOW causes the title to be above the toolbar
        # in production mode use FRAME_TOOL_WINDOW
        #

        frameStyle: int = DEFAULT_FRAME_STYLE | FRAME_EX_METAL | FRAME_FLOAT_ON_PARENT
        if appMode is True:
            frameStyle = frameStyle | FRAME_TOOL_WINDOW

        super().__init__(parent=None, id=ID_ANY, title="Test A Dialog", size=(500, 300), style=frameStyle)

        self.logger: Logger = getLogger(__name__)

        self._dlgSelectionId: wxNewIdRef      = wxNewIdRef()

        self._createSelectionControls()

        self.CreateStatusBar()

    def _createSelectionControls(self):

        sizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('horizontal')

        comboPanel: SizedStaticBox = SizedStaticBox(sizedPanel, label='Select Dialog')
        comboPanel.SetSizerProps(expand=True, valign='top')
        dialogChoices = []
        for dlgName in DialogNamesEnum:
            dialogChoices.append(dlgName.value)

        self._cmbDlgName: ComboBox = ComboBox(comboPanel, self._dlgSelectionId, choices=dialogChoices, style=CB_READONLY, size=(160, -1))

        self._cmbDlgName.SetSelection(AppTestDialogFrame.NOTHING_SELECTED)

        self.Bind(EVT_COMBOBOX, self.onDlgNameSelectionChanged, self._dlgSelectionId)

    @classmethod
    def secureBoolean(cls, unsafeValue: str):
        """
        TODO: use code ally basic version when it is available
        Args:
            unsafeValue:

        Returns:  A rational value

        """
        try:
            if unsafeValue is not None:
                if unsafeValue in [True, "True", "true", 1, "1"]:
                    return True
        except (ValueError, Exception) as e:
            print(f'secureBoolean error: {e}')
        return False

    def onDlgNameSelectionChanged(self, event: CommandEvent):

        dialogName: str = event.GetString()

        dlgName: DialogNamesEnum = DialogNamesEnum(dialogName)
        self.logger.warning(f'Selected dialog: {dlgName}')

        dlgAnswer: str = 'No dialog invoked'

        match dlgName:
            case DialogNamesEnum.DLG_PREFERENCES:
                dlgAnswer = self._testDialogPreferences()
            case DialogNamesEnum.DLG_ABOUT:
                dlgAnswer = self.testDialogAbout()
            case _:
                self.logger.error(f'Unknown dialog')

        self.logger.warning(f'{dlgAnswer=}')

    def _testDialogPreferences(self) -> Any:

        with PreferencesDialog(self) as dlg:

            if dlg.ShowModal() == ID_OK:
                return 'Ok'
            else:
                return 'Canceled'

    def testDialogAbout(self) -> Any:

        return 'Under Construction'
