
from typing import Dict
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger
from typing import Union
from typing import cast

from re import split as reSplit

import pip_tree

from visualdependencies.model.TypesV2 import Dependencies
from visualdependencies.model.TypesV2 import Dependency
from visualdependencies.model.TypesV2 import Package
from visualdependencies.model.TypesV2 import Packages

PackageName  = NewType('PackageName',  str)
PackageNames = NewType('PackageNames', List[PackageName])

RawPackageValue  = Union[str, List[str]]
RawPackageDetails = NewType('RawPackageDetails', Dict[str, RawPackageValue])

StringList = NewType('StringList', List[str])

NAME_KEY:     str = 'name'
VERSION_KEY:  str = 'version'
UPDATED_KEY:  str = 'updated'
REQUIRES_KEY: str = 'requires'

REQUIREMENT_PATTERN: str = "(>=)|(<=)|(==)|(!=)|(==)|(>)|(<)|(~=)|;"


class PipTreeAdapter:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def execute(self, packageNames: PackageNames, sitePackagePath: str = '') -> Packages:
        """

        Args:
            sitePackagePath:  Path to the virtual environment site package directory
            packageNames:     Specify an empty list if you want all

        Returns:  A List of Packages
        """
        doFilter: bool = True
        if len(packageNames) == 0:
            doFilter = False

        packages: Packages = Packages([])

        rawPackages = pip_tree.get_pip_package_list(sitePackagePath)
        for rawPackage in rawPackages:

            rawPackageDetails: RawPackageDetails = cast(RawPackageDetails, pip_tree.get_package_details(rawPackage))
            packageName:       RawPackageValue   = rawPackageDetails[NAME_KEY]
            if doFilter is True:
                if packageName in packageNames:
                    package: Package = self._extractPackage(rawPackageDetails=rawPackageDetails)
                else:
                    continue
            else:
                package = self._extractPackage(rawPackageDetails=rawPackageDetails)
                package.dependencies = self._extractDependencies(requirements=rawPackageDetails[REQUIRES_KEY])

            packages.append(package)

        return packages

    def _extractPackage(self, rawPackageDetails: RawPackageDetails) -> Package:

        package: Package = Package()

        package.information.packageName = cast(str, rawPackageDetails[NAME_KEY])
        package.information.version     = cast(str, rawPackageDetails[VERSION_KEY])
        package.information.updated     = cast(str, rawPackageDetails[UPDATED_KEY])

        return package

    def _extractDependencies(self, requirements: RawPackageValue) -> Dependencies:

        dependencies: Dependencies = Dependencies([])
        for require in requirements:
            dependency: Dependency = self._extractDependency(require=require)

            dependencies.append(dependency)

        return dependencies

    def _extractDependency(self, require: str) -> Dependency:

        dependency: Dependency = Dependency()
        splitList:  List[str]  = reSplit(REQUIREMENT_PATTERN, require)

        requirement:      str       = ''
        onlyRequirements: List[str] = splitList[1:]

        for piece in onlyRequirements:
            if piece is not None:
                requirement = f'{requirement} {piece}'

        self.logger.info(f'{splitList[0]} {requirement}')
        dependency.packageName = splitList[0].lstrip(' ').rstrip(' ')
        dependency.version     = requirement.lstrip(' ').rstrip(' ')

        return dependency
