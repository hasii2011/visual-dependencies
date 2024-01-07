
from typing import cast

from logging import Logger
from logging import getLogger

from os import getcwd

from pathlib import Path

from dataclasses import dataclass

from wx import DD_DEFAULT_STYLE
from wx import DD_DIR_MUST_EXIST
from wx import ICON_ERROR
from wx import TreeItemIcon_Expanded
from wx import TreeItemIcon_Normal
from wx import OK

from wx import DirSelector
from wx import MessageDialog

from wx.lib.gizmos import TreeListCtrl

from wx.dataview import TreeListItem

from visualdependencies.EnhancedImageList import EnhancedImageList
from visualdependencies.PipTreeAdapter import PackageNames
from visualdependencies.PipTreeAdapter import PipTreeAdapter
from visualdependencies.Preferences import Preferences
from visualdependencies.model.TypesV2 import Dependency
from visualdependencies.model.TypesV2 import Package

from visualdependencies.model.TypesV2 import Packages


@dataclass
class InterpreterRequestResponse:
    cancelled:       bool = False
    interpreterName: str  = ''


SITE_PACKAGES_DIRECTORY_NAME: str = 'site-packages'


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

        self._pipTreeAdapter: PipTreeAdapter = PipTreeAdapter()
        self._preferences:    Preferences    = Preferences()

    def selectVirtualEnvironment(self):

        startDirectory: str = self._preferences.projectsBaseDirectory

        response: InterpreterRequestResponse = self._askForPythonInterpreter(startDirectory=startDirectory)
        if response.cancelled is True:
            pass        # Now what
        else:
            interpreter: str      = response.interpreterName
            packages:    Packages = self._pipTreeAdapter.execute(packageNames=PackageNames([]), sitePackagePath=interpreter)

            self._displayDependencies(packages=packages)

    def _displayDependencies(self, packages: Packages):

        tree: TreeListCtrl = self.treeListCtrl
        root: TreeListItem = self._treeRoot

        enhancedImageList: EnhancedImageList = self._enhancedImageList

        for pkg in packages:
            package: Package      = cast(Package, pkg)
            pkgItem: TreeListItem = tree.AppendItem(root, package.information.packageName)

            tree.SetItemText(pkgItem, package.information.version, 1)
            tree.SetItemText(pkgItem, package.information.updated, 2)
            # tree.SetItemText(pkgItem, package.information.updated, 3)

            tree.SetItemImage(pkgItem, enhancedImageList.folderIndex,     which=TreeItemIcon_Normal)
            tree.SetItemImage(pkgItem, enhancedImageList.folderOpenIndex, which=TreeItemIcon_Expanded)

            for dep in package.dependencies:
                dependency: Dependency   = cast(Dependency, dep)
                depItem:    TreeListItem = tree.AppendItem(pkgItem, dependency.packageName)

                tree.SetItemText(depItem, dependency.version, 1)
                # if dependency.version == '':
                #     dependency.version = 'None'
                # tree.SetItemText(depItem, dependency.version, 2)

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
            selectedDirectory = DirSelector(
                message="Choose a virtual environment's site packages",
                default_path=defaultDir,
                style=DD_DIR_MUST_EXIST | DD_DEFAULT_STYLE
            )

            response: InterpreterRequestResponse = InterpreterRequestResponse()
            if selectedDirectory == '':
                response.cancelled = True
                response.interpreterName  = ''
                break
            else:
                if self._isItTheSitePackagesDirectory(selectedDirectory) is True:
                    response.cancelled = False
                    response.interpreterName = selectedDirectory
                    break
                else:
                    self._admonishDeveloper()

        return response

    def _isItTheSitePackagesDirectory(self, fqFileName: str) -> bool:
        import fnmatch

        ans:      bool = False
        path:     Path = Path(fqFileName)
        fileName: str = path.name

        if fnmatch.fnmatch(name=fileName, pat=SITE_PACKAGES_DIRECTORY_NAME) is True:
            ans = True

        return ans

    def _admonishDeveloper(self):
        """
        I wish I could ask the file selector to let me specify a file like
        SITE_PACKAGES_DIRECTORY_NAME
        """
        booBoo: MessageDialog = MessageDialog(parent=None, message='You must select an site-packages directory',
                                              caption='Try Again!',
                                              style=OK | ICON_ERROR)
        booBoo.ShowModal()
