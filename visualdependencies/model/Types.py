
from typing import Annotated
from typing import List

from dataclasses import dataclass

from dataclass_wizard import JSONFileWizard
from dataclass_wizard import JSONListWizard
from dataclass_wizard import JSONSerializable
from dataclass_wizard import json_key


@dataclass
class PackageInformation:

    key:              str
    packageName:      Annotated[str, json_key('package_name',      'packageName', all=True)]
    installedVersion: Annotated[str, json_key('installed_version', 'installedVersion', all=True)]


@dataclass
class Dependency(PackageInformation):
    requiredVersion: Annotated[str, json_key('required_version', 'requiredVersion', all=True)]


Dependencies = List[Dependency]     # Cannot use NewType or the list contents becomes a dictionary


@dataclass
class Package(JSONFileWizard, JSONListWizard):
    """
    It is just a Container
    """
    package:      PackageInformation
    dependencies: Dependencies

    class Meta(JSONSerializable.Meta):
        """
        True to enable Debug mode for additional (more verbose) log output.

        For example, a message is logged whenever an unknown JSON key is
        encountered when `from_dict` or `from_json` is called.

        This also results in more helpful messages during error handling, which
        can be useful when debugging the cause when values are an invalid type
        (i.e. they don't match the annotation for the field) when unmarshalling
        a JSON object to a dataclass instance.

        Note there is a minor performance impact when DEBUG mode is enabled.
        """
        debug_enabled = False

