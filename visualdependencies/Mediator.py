
from typing import cast

from logging import Logger
from logging import getLogger

from wx import TreeItemIcon_Expanded
from wx import TreeItemIcon_Normal

from wx.lib.gizmos import TreeListCtrl
from wx.dataview import TreeListItem

from dataclass_wizard import Container

from visualdependencies.CLIAdapter import CLIAdapter
from visualdependencies.CLIAdapter import PackageNames
from visualdependencies.EnhancedImageList import EnhancedImageList
from visualdependencies.model.Types import Dependency
from visualdependencies.model.Types import Package


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

        cliAdapter: CLIAdapter = CLIAdapter()
        cliAdapter.execute(packageNames=PackageNames([]))

        self._container: Container = Package.from_json(cliAdapter.json)

    def populateTree(self):

        tree: TreeListCtrl = self.treeListCtrl
        root: TreeListItem = self._treeRoot

        enhancedImageList: EnhancedImageList = self._enhancedImageList

        for pkg in self._container:
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
                tree.SetItemImage(depItem, enhancedImageList.folderOpenIndex, which=TreeItemIcon_Expanded)

            # if len(package.dependencies) == 0:
            #     tree.SetItemImage(pkgItem, enhancedImageList.fileIndex, which=TreeItemIcon_Normal)

            # tree.Expand(pkgItem)

        # tree.Expand(root)
