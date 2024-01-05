
from typing import cast

from logging import Logger
from logging import getLogger

from os import getcwd

from pathlib import Path

from dataclasses import dataclass

from dataclass_wizard import Container

from wx import FD_CHANGE_DIR
from wx import FD_FILE_MUST_EXIST
from wx import FD_NO_FOLLOW
from wx import FD_OPEN
from wx import ICON_ERROR
from wx import TreeItemIcon_Expanded
from wx import TreeItemIcon_Normal
from wx import OK

from wx import FileSelector
from wx import MessageDialog

from wx.lib.gizmos import TreeListCtrl
from wx.dataview import TreeListItem

from visualdependencies.CLIAdapter import CLIAdapter
from visualdependencies.CLIAdapter import CLIException
from visualdependencies.CLIAdapter import PackageNames

from visualdependencies.EnhancedImageList import EnhancedImageList
from visualdependencies.Preferences import Preferences
from visualdependencies.model.Types import Dependency
from visualdependencies.model.Types import Package


@dataclass
class InterpreterRequestResponse:
    cancelled:       bool = False
    interpreterName: str  = ''


PYTHON_INTERPRETER: str = 'python*'


class Mediator:
    """
    This is a singleton
    """
    _instance = None

    def __init__(self, treeListCtrl: TreeListCtrl, treeRoot: TreeListItem, enhancedImageList: EnhancedImageList):

        self.logger: Logger = getLogger(__name__)

        self.treeListCtrl:       treeListCtrl      = treeListCtrl
        self._treeRoot:          TreeListItem      = treeRoot
        self._enhancedImageList: EnhancedImageList = enhancedImageList

        self._cliAdapter:  CLIAdapter  = CLIAdapter()
        self._preferences: Preferences = Preferences()

    def selectVirtualEnvironment(self):

        startDirectory: str = self._preferences.projectsBaseDirectory

        response: InterpreterRequestResponse = self._askForPythonInterpreter(startDirectory=startDirectory)
        if response.cancelled is True:
            pass        # Now what
        else:
            interpreter: str = response.interpreterName
            try:
                self._cliAdapter.execute(packageNames=PackageNames([]), interpreter=interpreter)
            except CLIException as ce:
                self.logger.error(f'{ce}  {self._cliAdapter.stderr}')
                booBoo: MessageDialog = MessageDialog(parent=None,
                                                      message=self._cliAdapter.stderr,
                                                      caption='Oops', style=OK | ICON_ERROR)
                booBoo.ShowModal()

            container: Container = Package.from_json(self._cliAdapter.json)
            self._displayDependencies(container=container)

    def _displayDependencies(self, container: Container):

        tree: TreeListCtrl = self.treeListCtrl
        root: TreeListItem = self._treeRoot

        enhancedImageList: EnhancedImageList = self._enhancedImageList

        for pkg in container:
            package: Package      = cast(Package, pkg)
            pkgItem: TreeListItem = tree.AppendItem(root, package.package.packageName)

            tree.SetItemText(pkgItem, package.package.installedVersion, 1)

            tree.SetItemImage(pkgItem, enhancedImageList.folderIndex,     which=TreeItemIcon_Normal)
            tree.SetItemImage(pkgItem, enhancedImageList.folderOpenIndex, which=TreeItemIcon_Expanded)

            for dep in package.dependencies:
                dependency: Dependency   = cast(Dependency, dep)
                depItem:    TreeListItem = tree.AppendItem(pkgItem, dependency.packageName)

                tree.SetItemText(depItem, dependency.installedVersion, 1)
                if dependency.requiredVersion == '':
                    dependency.requiredVersion = 'None'
                tree.SetItemText(depItem, dependency.requiredVersion, 2)

                # tree.SetItemImage(depItem, enhancedImageList.fileIndex,       which=TreeItemIcon_Normal)
                # tree.SetItemImage(depItem, enhancedImageList.folderOpenIndex, which=TreeItemIcon_Expanded)

            # if len(package.dependencies) == 0:
            #     tree.SetItemImage(pkgItem, enhancedImageList.fileIndex, which=TreeItemIcon_Normal)
            if self._preferences.expandDependencies is True:
                tree.Expand(pkgItem)

        if self._preferences.openProject is True:
            tree.Expand(root)

    def _askForPythonInterpreter(self, startDirectory: str) -> InterpreterRequestResponse:
        """
        Called by plugin to ask for a file to import

        Args:
            startDirectory: The directory to display

        Returns:  The request response
        """
        defaultDir: str = startDirectory

        if defaultDir is None:
            defaultDir = getcwd()
        while True:
            file = FileSelector(
                message="Choose a virtual environment",
                default_path=defaultDir,
                flags=FD_OPEN | FD_FILE_MUST_EXIST | FD_CHANGE_DIR | FD_NO_FOLLOW
            )

            response: InterpreterRequestResponse = InterpreterRequestResponse()
            if file == '':
                response.cancelled = True
                response.interpreterName  = ''
                break
            else:
                if self._isItAnInterpreter(file) is True:
                    response.cancelled = False
                    response.interpreterName = file
                    break
                else:
                    self._admonishDeveloper()

        return response

    def _isItAnInterpreter(self, fqFileName: str) -> bool:
        import fnmatch

        ans:      bool = False
        path:     Path = Path(fqFileName)
        fileName: str = path.name

        if fnmatch.fnmatch(name=fileName, pat=PYTHON_INTERPRETER) is True:
            ans = True

        return ans

    def _admonishDeveloper(self):
        """
        I wish I could ask the file selector to let me specify a file like
        PYTHON_INTERPRETER
        """
        booBoo: MessageDialog = MessageDialog(parent=None, message='You must select an interpreter',
                                              caption='Try Again!',
                                              style=OK | ICON_ERROR)
        booBoo.ShowModal()
