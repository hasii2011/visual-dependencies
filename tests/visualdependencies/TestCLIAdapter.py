
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from visualdependencies.CLIAdapter import CLIAdapter
from visualdependencies.CLIAdapter import CLIException
from visualdependencies.CLIAdapter import PackageName
from visualdependencies.CLIAdapter import PackageNames

NAME_1: PackageName = PackageName('wxPython')
NAME_2: PackageName = PackageName('codeallybasic')
NAME_3: PackageName = PackageName('buildlackey')

# noinspection PyUnresolvedReferences
BAD_PACKAGE_JSON: str = '''[
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
                "required_version": null
            },
            {
                "key": "pillow",
                "package_name": "Pillow",
                "installed_version": "10.1.0",
                "required_version": null
            },
            {
                "key": "six",
                "package_name": "six",
                "installed_version": "1.16.0",
                "required_version": null
            }
        ]
    }
]
'''
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


class TestCLIAdapter(UnitTestBase):

    @classmethod
    def setUpClass(cls):
        """"""
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self._packageNames: PackageNames = PackageNames([NAME_1, NAME_2, NAME_3])

    def tearDown(self):
        super().tearDown()

    def testExecute(self):
        self._runExecuteTest(packageNames=self._packageNames, failMessage='Failed with package names specified')

    def testExecuteNoSpecifiedPackageNames(self):
        self._runExecuteTest(packageNames=PackageNames([]), failMessage='Failed with no package names specified')

    def testBuildPackageNameOption(self):

        adapter: CLIAdapter = CLIAdapter()

        actualOption:   str = adapter._buildPackageNameOption(packageNames=self._packageNames, interpreter='')
        expectedOption: str = f'{CLIAdapter.PACKNAME_OPTION} {NAME_1},{NAME_2},{NAME_3}'
        self.assertEqual(expectedOption, actualOption, 'Option not correctly built')

    def testFixJson(self):
        actualGoodPackageJson: str = CLIAdapter.fixJson(potentialBadJson=BAD_PACKAGE_JSON)

        self.assertEqual(GOOD_PACKAGE_JSON, actualGoodPackageJson, 'The Bad JSON was not fixed')

    def _runExecuteTest(self, packageNames: PackageNames, failMessage: str):

        adapter: CLIAdapter = CLIAdapter()
        try:
            adapter.execute(packageNames=packageNames)

            self.assertTrue(len(adapter.json) != 0, failMessage)
        except CLIException as e:
            self.logger.error(f'{e} - {adapter.stderr}')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestCLIAdapter))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
