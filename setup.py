
from setuptools import setup

import pathlib

from visualdependencies import __version__
from visualdependencies import __applicationName__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

APP = ['visualdependencies/VisualDependencies.py']
DATA_FILES = [('visualdependencies/resources', ['visualdependencies/resources/loggingConfiguration.json']),
              ('visualdependencies/resources/images', ['visualdependencies/resources/images/DependencySplash.jpg']),
              ]
OPTIONS = {}
SRC_DIR = 'src'

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name=__applicationName__,
    version=__version__,
    app=APP,
    data_files=DATA_FILES,
    packages=['visualdependencies',
              'visualdependencies.dialogs',
              'visualdependencies.futures',
              'visualdependencies.model',
              'visualdependencies.resources.images',
              ],
    include_package_data=True,
    zip_safe=False,

    url='https://github.com/hasii2011/pyut',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Visual Python Dependencies',
    long_description='A graphical front end for pip dependencies.',
    options=dict(py2app=dict(
        plist=dict(
            NSRequiresAquaSystemAppearance='True',
            CFBundleGetInfoString='Displays pip dependencies',
            CFBundleIdentifier='pyut',
            CFBundleShortVersionString=__version__,
            CFBundleDocumentTypes=[
                {'CFBundleTypeName': 'visualdependencies'},
                {'CFBundleTypeRole': 'Display'},
                {'CFBundleTypeExtensions':  ['json']}
            ],
            LSMinimumSystemVersion='12',
            LSEnvironment=dict(
                APP_MODE='True',
                PYTHONOPTIMIZE='1',
            ),
            LSMultipleInstancesProhibited='True',
        )
    ),
    ),
    setup_requires=['py2app'],
    install_requires=['codeallybasic~=0.5.2',
                      'wxPython==4.2.1',
                      'chardet==5.2.0',
                      'pipdeptree==2.13.1',
                      'dataclass-wizard==0.22.2',
                      ]
)
