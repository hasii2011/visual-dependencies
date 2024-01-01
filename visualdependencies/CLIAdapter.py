
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from subprocess import run as subProcessRun
from subprocess import CompletedProcess

from re import search as regExSearch
from re import sub as regExSub
from re import Match

PackageName  = NewType('PackageName',  str)
PackageNames = NewType('PackageNames', List[PackageName])


class CLIException(Exception):
    pass


class CLIAdapter:
    """
    The interface to the pipdeptree python script
    """
    BASIC_COMMAND:   str = 'pipdeptree --json '
    PACKNAME_OPTION: str = '--packages '
    PYTHON_OPTION:   str = '--python  '

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._json:   str = ''
        self._stderr: str = ''

    def execute(self, packageNames: PackageNames, interpreter: str = ''):
        """
        If this executes successfully, query the json property to retrieve the
        output
        Args:
            interpreter:    Fully qualified name of the interpreter
            packageNames:   Specify an empty list if you want all

        Returns:  The status of the command
        """

        status: int = self._runCommand(packageNames=packageNames, interpreter=interpreter)
        if status != 0:
            raise CLIException(f'Command failed {status}')

    @property
    def json(self) -> str:
        return self._json

    @property
    def stderr(self) -> str:
        return self._stderr

    def _runCommand(self, packageNames: PackageNames, interpreter: str) -> int:
        """
        If this completes w/o an error it stashes the CLI output in self._json
        If there is an error this method populates self._stderr
        Args:
            packageNames:  List of package names to query
            interpreter:   Fully qualified name of the interpreter


        Returns:  The status code of the executed command
        """

        optionStr: str = self._buildPackageNameOption(packageNames=packageNames, interpreter=interpreter)
        command:   str = f'{CLIAdapter.BASIC_COMMAND} {optionStr}'

        completedProcess: CompletedProcess = subProcessRun([command], shell=True, capture_output=True, text=True, check=False)

        if completedProcess.returncode == 0:
            self._json = CLIAdapter.fixJson(potentialBadJson=completedProcess.stdout)
        else:
            self._stderr = completedProcess.stderr

        return completedProcess.returncode

    def _buildPackageNameOption(self, packageNames: PackageNames, interpreter: str) -> str:
        """
        Build up a string of package names
        Args:
            packageNames:

        Returns:

        """

        optionString: str = ''

        for packageName in packageNames:
            optionString += f'{packageName},'

        if optionString == '':
            pass
        else:
            optionString = f'{CLIAdapter.PACKNAME_OPTION} {optionString}'
        optionString = optionString.strip(',')

        if interpreter != '':
            optionString = f'{optionString} {CLIAdapter.PYTHON_OPTION} {interpreter}'

        return optionString.strip(',')

    @classmethod
    def fixJson(cls, potentialBadJson: str) -> str:
        """
        This method necessary because of this issue with pipdeptree
            https://github.com/tox-dev/pipdeptree/issues/309

        Args:
            potentialBadJson:  The string we read in from the command output

        Returns: A 'fixed' string

        """
        """
        """
        badRequiredVersion:  str = '"required_version": null'
        goodRequiredVersion: str = '"required_version": "None"'

        match: Match | None = regExSearch(pattern=badRequiredVersion, string=potentialBadJson)
        if match is None:
            goodJson: str = potentialBadJson
        else:
            goodJson = regExSub(pattern=badRequiredVersion, repl=goodRequiredVersion, string=potentialBadJson)

        return goodJson
