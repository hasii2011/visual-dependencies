
from logging import Logger
from logging import getLogger

from sys import version as pythonVersion

from wx import CAPTION
from wx import DEFAULT_DIALOG_STYLE
from wx import FONTFAMILY_DEFAULT
from wx import FONTFAMILY_TELETYPE
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD
from wx import ID_ANY
from wx import OK
from wx import StaticBitmap
from wx import StaticText

from wx import __version__ as wxVersion
from wx import Font

from wx.lib.sized_controls import SizedDialog
from wx.lib.sized_controls import SizedPanel

from pip_tree._version import __version__ as pipTreeVersion

from visualdependencies import __version__
from visualdependencies.resources.icons import AboutDialogImage


class AboutDialog(SizedDialog):
    def __init__(self, parent):

        style:   int  = DEFAULT_DIALOG_STYLE
        # dlgSize: Size = Size(460, 240)

        # super().__init__(parent, ID_ANY, "About ...", size=dlgSize, style=style)
        super().__init__(parent, ID_ANY, "About ...", style=style)
        self.logger: Logger = getLogger(__name__)

        sizedPanel: SizedPanel = self.GetContentsPane()

        sizedPanel.SetSizerType('horizontal')
        sizedPanel.SetSizerProps(expand=True)

        self._layoutControls(sizedPanel=sizedPanel)
        self._setControlValues()

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(OK))

        # a little trick to make sure that you can't resize the dialog to
        # less screen space than the controls need
        self.Fit()
        self.SetMinSize(self.GetSize())

    def _layoutControls(self, sizedPanel: SizedPanel):

        leftPanel: SizedPanel = SizedPanel(parent=sizedPanel)
        leftPanel.SetSizerType('vertical')
        leftPanel.SetSizerProps(expand=True)

        StaticBitmap(leftPanel, ID_ANY, AboutDialogImage.embeddedImage.GetBitmap())

        versionText: str = f'Visual Dependencies {__version__}'
        summaryText: str = "2024 Humberto Sanchez II\nGNU AFFERO GENERAL PUBLIC LICENSE"

        font:          Font       = Font(14, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        myVersionText: StaticText = StaticText(leftPanel, ID_ANY, versionText,   style=CAPTION)
        myVersionText.SetFont(font)

        StaticText(leftPanel, ID_ANY, summaryText, style=CAPTION)

        rightPanel: SizedPanel = SizedPanel(parent=sizedPanel)
        rightPanel.SetSizerType('vertical')
        rightPanel.SetSizerProps(expand=False)

        depVersionText: str = (
            f'Python:           {pythonVersion.split(" ")[0]}\n'
            f'wxPython:         {wxVersion}\n'
            f'Py2App:           0.28.6\n'
            f'pip_tree:         {pipTreeVersion}'
        )

        versionFont: Font = Font(12, FONTFAMILY_TELETYPE, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        depVersion: StaticText = StaticText(rightPanel, ID_ANY, depVersionText, style=CAPTION)
        depVersion.SetFont(versionFont)

    def _setControlValues(self):
        pass
