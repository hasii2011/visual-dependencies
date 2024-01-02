
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CANCEL
from wx import CommandEvent
from wx import DEFAULT_DIALOG_STYLE
from wx import EVT_CHECKBOX
from wx import EVT_DIRPICKER_CHANGED
from wx import FileDirPickerEvent
from wx import ID_ANY
from wx import OK

from wx import CheckBox
from wx import DirPickerCtrl
from wx import Size

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from visualdependencies.Preferences import Preferences


class PreferencesDialog(SizedDialog):

    def __init__(self, parent):

        style:   int  = DEFAULT_DIALOG_STYLE
        dlgSize: Size = Size(340, 240)

        super().__init__(parent, ID_ANY, "Preferences", size=dlgSize, style=style)

        self.logger:        Logger     = getLogger(__name__)
        self._preferences: Preferences = Preferences()

        sizedPanel: SizedPanel = self.GetContentsPane()

        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(expand=True)

        self._directoryPicker:    DirPickerCtrl = cast(DirPickerCtrl, None)
        self._expandProject:      CheckBox      = cast(CheckBox, None)
        self._expandDependencies: CheckBox      = cast(CheckBox, None)

        self._directoryPickerId:    wxNewIdRef = wxNewIdRef()
        self._expandProjectId:      wxNewIdRef = wxNewIdRef()
        self._expandDependenciesId: wxNewIdRef = wxNewIdRef()

        self._layoutControls(sizedPanel=sizedPanel)
        self._setControlValues()

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(OK | CANCEL))

        self.Bind(EVT_DIRPICKER_CHANGED, self._projectsBaseDirectoryChanged, id=self._directoryPickerId)
        self.Bind(EVT_CHECKBOX,          self._onExpandProjectChanged,       id=self._expandProjectId)
        self.Bind(EVT_CHECKBOX,          self._onExpandDependenciesChange,   id=self._expandDependenciesId)

    def _layoutControls(self, sizedPanel: SizedPanel):
        """
        Initialize the controls

        Args:
            sizedPanel:  In case we use something other than the dialog panel
        """
        directoryPanel: SizedStaticBox = SizedStaticBox(sizedPanel, label='Projects Base Directory')

        directoryPanel.SetSizerType('vertical')
        directoryPanel.SetSizerProps(expand=True, proportion=1)

        directoryPicker: DirPickerCtrl = DirPickerCtrl(parent=directoryPanel, id=self._directoryPickerId, message='Projects Base Directory')
        directoryPicker.SetSizerProps(expand=True, proportion=1, valign='top')

        self._directoryPicker    = directoryPicker
        self._expandProject      = CheckBox(sizedPanel, self._expandProjectId,      "Expand Project Requirements")
        self._expandDependencies = CheckBox(sizedPanel, self._expandDependenciesId, "Expand Package Dependencies")

    def _setControlValues(self):

        self._directoryPicker.SetPath(self._preferences.projectsBaseDirectory)
        self._directoryPicker.SetInitialDirectory(self._preferences.projectsBaseDirectory)
        self._expandProject.SetValue(self._preferences.openProject)
        self._expandDependencies.SetValue(self._preferences.expandDependencies)

    def _projectsBaseDirectoryChanged(self, event: FileDirPickerEvent):

        newValue: str = event.GetPath()
        self._preferences.projectsBaseDirectory = newValue

    def _onExpandProjectChanged(self, event: CommandEvent):

        newValue: bool = event.IsChecked()

        self._preferences.openProject = newValue

    def _onExpandDependenciesChange(self, event: CommandEvent):

        newValue: bool = event.IsChecked()

        self._preferences.expandDependencies = newValue
