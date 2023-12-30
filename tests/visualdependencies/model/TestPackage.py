
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from dataclass_wizard import Container
from dataclass_wizard import JSONListWizard
from dataclasses import dataclass

from codeallybasic.UnitTestBase import UnitTestBase
from visualdependencies.model.Types import Package


GOOD_PACKAGE_JSON: str = '''[
    {
        "package": {
            "key": "wxpython",
            "package_name": "wxPython",
            "installed_version": "4.2.1"
        },
        "dependencies": [
            {
                "key": "numpy",
                "package_name": "numpy",
                "installed_version": "1.26.2",
                "required_version": "None"
            },
            {
                "key": "pillow",
                "package_name": "Pillow",
                "installed_version": "10.1.0",
                "required_version": "None"
            },
            {
                "key": "six",
                "package_name": "six",
                "installed_version": "1.16.0",
                "required_version": "None"
            }
        ]
    }
]
'''


# clear; pipdeptree --json -p wxPython

@dataclass
class Outer(JSONListWizard):
    inner: list['Inner']


@dataclass
class Inner:
    other_str: str


class TestPackage(UnitTestBase):

    RESOURCES_DATA_PACKAGE_NAME:  str = 'tests.resources.testdata'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSpecifications(self):
        jsonList: list = [
            {
                "package": {
                    "key": "rich",
                    "package_name": "rich",
                    "installed_version": "13.7.0"
                },
                "dependencies": [
                    {
                        "key": "markdown-it-py",
                        "package_name": "markdown-it-py",
                        "installed_version": "3.0.0",
                        "required_version": ">=2.2.0"
                    },
                    {
                        "key": "pygments",
                        "package_name": "pygments",
                        "installed_version": "2.17.2",
                        "required_version": ">=2.13.0,<3.0.0"
                    }
                ]
            }
        ]

        container: Container = Package.from_list(jsonList)

        pkg: Package = container[0]

        self.assertEqual(2, len(pkg.dependencies), 'Incorrect length')

    def testBasicInline(self):

        simplePackages: list = [
            {
                "package": {
                    "key": "rich",
                    "package_name": 'rich',
                    "installed_version": "13.7.0",
                },

                "dependencies": []
            },
            {
                "package": {
                    "key": "zipp",
                    "package_name": 'zipp',
                    "installed_version": "3.7.0",
                },
                "dependencies": []
            },
        ]
        container: Container = Package.from_list(simplePackages)

        for pkg in container:
            package: Package = cast(Package, pkg)
            self.logger.info(f'{package=}')

        self.assertEqual(2, len(container), 'Incorrect length')

        specificPkg: Package = container[0]
        self.assertEqual('rich', specificPkg.package.key, 'What happened')

    def testFileInput(self):

        fqFile: str = UnitTestBase.getFullyQualifiedResourceFileName(package=TestPackage.RESOURCES_DATA_PACKAGE_NAME, fileName='Basic.json')
        container: Container = Package.from_json_file(fqFile)

        self.assertEqual(4, len(container), 'Missing packages')

    def testString(self):
        container: Container = Package.from_json(GOOD_PACKAGE_JSON)

        self.assertTrue(len(container) == 1, '')

    def testExample(self):
        my_list = [
            {"inner": [{"otherStr": "testing 123"}]},
            {"inner": [{"otherStr": "world"}]},
        ]

        # De-serialize the JSON string into a list of `MyClass` objects
        c = Outer.from_list(my_list)

        self.assertTrue(isinstance(c, list))
        self.assertEqual(type(c), Container, '')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPackage))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
