import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = '-n auto'

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


version_contents = {}
with open("fast_arrow_auth/version.py", "r", encoding='utf-8') as f:
    exec(f.read(), version_contents)


with open("README.md", "r") as f:
    long_description = f.read()


deps = [
    'datetime',
    'deprecation',
    'pathlib2',
    'requests>=2.20.0',
    'yarl',
    'urllib3>=1.24.2'
]


test_deps = [
    'pipenv',
    'pytest',
    'pytest-cov',
    'detox',
    'flake8',
    'vcrpy'
]


setup(name='fast_arrow_auth',
    version=version_contents['VERSION'],
    description="A library to handle authentication with Robinhood's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Weston Platter',
    author_email='westonplatter@gmail.com',
    url='https://github.com/westonplatter/fast_arrow_auth/',
    license='MIT License',
    python_requires=">=3.5",
    packages=[
        'fast_arrow_auth',
        'fast_arrow_auth.resources',
    ],
    package_data={'fast_arrow_auth': ['ssl_certs/certs.pem']},
    install_requires=deps,
    tests_require=test_deps,
    cmdclass={'test': PyTest},
    project_urls={
        'Issue Tracker': 'https://github.com/westonplatter/fast_arrow_auth/issues',
        'Source Code': 'https://github.com/westonplatter/fast_arrow_auth',
    }
)
