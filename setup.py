from setuptools import setup

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
)

