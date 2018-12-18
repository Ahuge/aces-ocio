import distutils
import os
from setuptools import setup
import subprocess
import sys

ACES_OCIO_CTL_DIRECTORY_ENVIRON = 'ACES_OCIO_CTL_DIRECTORY'
ACES_OCIO_CONFIGURATION_DIRECTORY_ENVIRON = 'ACES_OCIO_CONFIGURATION_DIRECTORY'


class GenerateCommand(distutils.cmd.Command):
    description = "Build and Bake all LUTS"
    user_options = [
        (
            "acesCTLDir=",
            None,
            "CTL directory."
        ),
        (
            "configDir=",
            None,
            "Aces Configuration directory."
        ),
        (
            "lutResolution1d=",
            None,
            "1D Lut resolution."
        ),
        (
            "lutResolution3d=",
            None,
            "3D Lut resolution."
        ),
        (
            "dontBakeSecondaryLUTs=",
            None,
            "Don't bake secondary LUT files."
        ),
        (
            "keepTempImages=",
            None,
            "Keep temp images."
        ),
        (
            "createMultipleDisplays=",
            None,
            "Create multiple displays."
        ),
        (
            "copyCustomLUTs=",
            None,
            "Copy Custom LUTs."
        ),
        (
            "shaper=",
            None,
            "Log2 or DolbyPQ."
        ),
    ]

    def initialize_options(self):
        self.acesCTLDir = ""
        self.configDir = ""
        self.lutResolution1d = ""
        self.lutResolution3d = ""
        self.dontBakeSecondaryLUTs = ""
        self.keepTempImages = ""
        self.createMultipleDisplays = ""
        self.copyCustomLUTs = ""
        self.shaper = ""

    def finalize_options(self):
        self.acesCTLDir = self.acesCTLDir or os.environ.get(ACES_OCIO_CTL_DIRECTORY_ENVIRON, None)
        self.configDir = self.configDir or os.environ.get(ACES_OCIO_CONFIGURATION_DIRECTORY_ENVIRON, None)
        self.lutResolution1d = self.lutResolution1d or "4096"
        self.lutResolution3d = self.lutResolution3d or "64"
        self.dontBakeSecondaryLUTs = self.dontBakeSecondaryLUTs or "False"
        self.keepTempImages = self.keepTempImages or "False"
        self.createMultipleDisplays = self.createMultipleDisplays or "False"
        self.copyCustomLUTs = self.copyCustomLUTs or "False"
        self.shaper = self.shaper or "Log2"

        if self.shaper:
            assert self.shaper in ["Log2", "DolbyPQ"], "Must be either \"Log2\" or \"DolbyPQ\""

        if self.configDir:
            assert os.path.exists(self.configDir), "Build directory does not exist!"
        else:
            default_dir = os.path.join(os.path.dirname(__file__), "build")
            if not os.path.exists(default_dir):
                os.makedirs(default_dir)
            self.configDir = default_dir

    def run(self):
        command = [
            "src/bin/create_aces_config",
            "--acesCTLDir", self.acesCTLDir,
            "--configDir", self.configDir,
            "--lutResolution1d", self.lutResolution1d,
            "--lutResolution3d", self.lutResolution3d,
            "--dontBakeSecondaryLUTs", self.dontBakeSecondaryLUTs,
            "--keepTempImages", self.keepTempImages,
            "--createMultipleDisplays", self.createMultipleDisplays,
            "--copyCustomLUTs", self.copyCustomLUTs,
            "--shaper", self.shaper,
        ]
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        env = os.environ.copy()
        env["PYTHONPATH"] += os.pathsep + os.path.join(os.path.dirname(__file__), "src/python")

        subprocess.check_call(command, env=env)


setup(
    name='aces_ocio',
    version='1.0.1',
    description='AMPAS OCIO configuration library',
    url='http://github.com/digitaldomain/aces_ocio',
    author='AMPAS',
    package_dir={
        "aces_ocio": "src/python/aces_ocio",
        "aces_ocio.tests": "src/python/aces_ocio/tests",
    },
    packages=['aces_ocio', 'aces_ocio.tests'],
    scripts=["src/bin/create_aces_config", "src/bin/generate_lut", "src/bin/tests_aces_config"],
    test_suite="tests.tests_aces_config.TestACESConfig.test_ACES_config",
    install_requires=[
          'PyOpenColorIO',
      ],
    cmdclass={
        "bake": GenerateCommand,
    }
)

