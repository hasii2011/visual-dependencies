
from typing import List
from typing import NewType

from dataclasses import dataclass
from dataclasses import field


@dataclass
class Dependency:
    packageName: str = ''
    version:     str = ''


Dependencies = NewType('Dependencies', List[Dependency])


@dataclass
class Information(Dependency):
    updated:          str = ''


def informationFactory() -> Information:
    return Information()


def dependenciesFactory() -> Dependencies:
    return Dependencies([])


@dataclass
class Package:
    """
    """
    information:  Information  = field(default_factory=informationFactory)
    dependencies: Dependencies = field(default_factory=dependenciesFactory)


Packages = NewType('Packages', List[Package])
