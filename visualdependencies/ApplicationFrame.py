
from typing import Optional
from typing import cast

from logging import Logger
from logging import getLogger

from os import getenv as osGetEnv

from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import EVT_TREE_ITEM_RIGHT_CLICK
from wx import FRAME_EX_METAL
from wx import FRAME_FLOAT_ON_PARENT
from wx import FRAME_TOOL_WINDOW
from wx import ID_ABOUT
from wx import ID_ANY
from wx import ID_EXIT
from wx import ID_OK
from wx import ID_PREFERENCES
from wx import Menu
from wx import MenuBar
from wx import TreeEvent

from wx import TreeItemIcon_Expanded
from wx import TreeItemIcon_Normal
from wx import Colour
from wx import ImageList

from wx import NewIdRef as wxNewIdRef

from wx.dataview import TreeListItem

from wx.lib.gizmos import TR_DEFAULT_STYLE
from wx.lib.gizmos import TR_ELLIPSIZE_LONG_ITEMS
from wx.lib.gizmos import TreeListCtrl

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from visualdependencies.EnhancedImageList import EnhancedImageList
from visualdependencies.Mediator import Mediator
from visualdependencies.Preferences import Preferences
from visualdependencies.dialogs.AboutDialog import AboutDialog
from visualdependencies.dialogs.PreferencesDialog import PreferencesDialog


class ApplicationFrame (SizedFrame):

    APP_MODE:                     str = 'APP_MODE'
    VIEW_NEW_VIRTUAL_ENVIRONMENT: int = wxNewIdRef()

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

        self._createApplicationMenuBar()

        self._tree:              TreeListCtrl      = cast(TreeListCtrl, None)
        self._treeRoot:          TreeListItem      = cast(TreeListItem, None)
        self._enhancedImageList: EnhancedImageList = cast(EnhancedImageList, None)

        self._treeListCtrl: TreeListCtrl   = self._makeTree()

        self._mediator: Mediator = Mediator(treeListCtrl=self._treeListCtrl, treeRoot=self._treeRoot, enhancedImageList=self._enhancedImageList)

        if Preferences().initialQuery is True:
            self._mediator.selectVirtualEnvironment()

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    def _makeTree(self) -> TreeListCtrl:

        # create the tree control
        sizedPanel: SizedPanel = self.GetContentsPane()
        sizedPanel.SetSizerType('vertical')
        sizedPanel.SetSizerProps(expand=True, proportion=1)

        agwStyle: int = TR_ELLIPSIZE_LONG_ITEMS | TR_DEFAULT_STYLE
        tree: TreeListCtrl = TreeListCtrl(parent=sizedPanel, size=(600, 400), agwStyle=agwStyle)

        tree.SetSizerProps(expand=True, proportion=1)
        enhancedImageList: EnhancedImageList = EnhancedImageList()
        imageList:         ImageList         = enhancedImageList.imageList

        tree.SetImageList(imageList)

        tree.AddColumn("Package")
        tree.AddColumn("Version")
        tree.AddColumn("Updated")
        tree.SetMainColumn(0)  # the one with the tree in it...
        tree.SetColumnWidth(column=0, width=175)

        root: TreeListItem = tree.AddRoot("Visual Dependencies")
        tree.SetItemImage(root, enhancedImageList.folderIndex,     which=TreeItemIcon_Normal)
        tree.SetItemImage(root, enhancedImageList.folderOpenIndex, which=TreeItemIcon_Expanded)

        tree.Expand(root)
        self._tree     = tree
        self._treeRoot = root
        self._enhancedImageList = enhancedImageList

        self.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self._onTreeRightClick, tree)
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

    def _createApplicationMenuBar(self):

        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu = Menu()
        helpMenu: Menu = Menu()

        fileMenu.Append(ID_PREFERENCES, 'Preferences', 'Make Preferences')

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")

        helpMenu.AppendSeparator()
        helpMenu.Append(ID_ABOUT, '&About', 'Tell you about me')

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(helpMenu, 'Help')

        self.SetMenuBar(menuBar)
        self.Bind(EVT_MENU, self._onAbout,       id=ID_ABOUT)
        self.Bind(EVT_MENU, self._onPreferences, id=ID_PREFERENCES)

        self.Bind(EVT_MENU, self.Close,        id=ID_EXIT)

    # noinspection PyUnusedLocal
    def _onAbout(self, event: CommandEvent):

        with AboutDialog(self) as dlg:
            dlg.ShowModal()

    # noinspection PyUnusedLocal
    def _onPreferences(self, event: CommandEvent):

        with PreferencesDialog(self) as dlg:

            if dlg.ShowModal() == ID_OK:
                self.logger.debug(f'Waiting for answer')
            else:
                self.logger.debug(f'Cancelled')

    # noinspection PyUnusedLocal
    def _onTreeRightClick(self, event: TreeEvent):

        menu:       Menu      = Menu()

        menu.Append(ApplicationFrame.VIEW_NEW_VIRTUAL_ENVIRONMENT, "View New Environment", "See requirements in new virtual environment")

        menu.Bind(EVT_MENU, self._OnMenuClick, id=ApplicationFrame.VIEW_NEW_VIRTUAL_ENVIRONMENT)

        self.PopupMenu(menu)

    # noinspection PyUnusedLocal
    def _OnMenuClick(self, event: CommandEvent):

        self._tree.DeleteChildren(self._treeRoot)
        self._mediator.selectVirtualEnvironment()
