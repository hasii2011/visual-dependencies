
from typing import Optional
from typing import cast

from logging import Logger
from logging import getLogger

from os import getenv as osGetEnv

from wx import DEFAULT_FRAME_STYLE
from wx import FRAME_EX_METAL
from wx import FRAME_FLOAT_ON_PARENT
from wx import FRAME_TOOL_WINDOW
from wx import ID_ANY

from wx import TreeItemIcon_Expanded
from wx import TreeItemIcon_Normal
from wx import Colour
from wx import ImageList

from wx.dataview import TreeListItem

from wx.lib.gizmos import TR_COLUMN_LINES
from wx.lib.gizmos import TR_DEFAULT_STYLE
from wx.lib.gizmos import TR_FULL_ROW_HIGHLIGHT
from wx.lib.gizmos import TreeListCtrl

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from visualdependencies.EnhancedImageList import EnhancedImageList
from visualdependencies.Mediator import Mediator


class ApplicationFrame (SizedFrame):
    APP_MODE:         str = 'APP_MODE'

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        appModeStr: Optional[str] = osGetEnv(ApplicationFrame.APP_MODE)
        if appModeStr is None:
            appMode: bool = False
        else:
            appMode = ApplicationFrame.secureBoolean(appModeStr)
        # wxPython 4.2.0 update:  using FRAME_TOOL_WINDOW causes the title to be above the toolbar
        # in production mode use FRAME_TOOL_WINDOW
        #
        frameStyle: int = DEFAULT_FRAME_STYLE | FRAME_EX_METAL | FRAME_FLOAT_ON_PARENT
        if appMode is True:
            frameStyle = frameStyle | FRAME_TOOL_WINDOW

        super().__init__(parent=None, id=ID_ANY, title="Visual Dependencies", size=(600, 400), style=frameStyle)

        self.SetBackgroundColour(Colour(204, 229, 255))
        self._treeRoot:          TreeListItem      = cast(TreeListItem, None)
        self._enhancedImageList: EnhancedImageList = cast(EnhancedImageList, None)

        self._treeListCtrl: TreeListCtrl   = self._makeTree()

        self._mediator: Mediator = Mediator(treeListCtrl=self._treeListCtrl, treeRoot=self._treeRoot, enhancedImageList=self._enhancedImageList)

        self._mediator.populateTree()

    def _makeTree(self) -> TreeListCtrl:

        # create the tree control
        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(expand=True, proportion=1)

        tree: TreeListCtrl = TreeListCtrl(parent=sizedPanel, size=(600, 400), agwStyle=TR_FULL_ROW_HIGHLIGHT | TR_DEFAULT_STYLE | TR_COLUMN_LINES)

        enhancedImageList: EnhancedImageList = EnhancedImageList()
        imageList:         ImageList         = enhancedImageList.imageList

        tree.SetImageList(imageList)

        tree.AddColumn("Package")
        tree.AddColumn("Installed")
        tree.AddColumn("Required")
        tree.SetMainColumn(0)  # the one with the tree in it...
        tree.SetColumnWidth(column=0, width=175)

        root: TreeListItem = tree.AddRoot("Visual Dependencies")
        tree.SetItemImage(root, enhancedImageList.folderIndex,     which=TreeItemIcon_Normal)
        tree.SetItemImage(root, enhancedImageList.folderOpenIndex, which=TreeItemIcon_Expanded)

        tree.Expand(root)
        self._treeRoot = root
        self._enhancedImageList = enhancedImageList

        return tree

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
