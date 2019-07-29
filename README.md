# fast_arrow_auth
A simple yet robust API client for Robinhood

[![Build Status](https://travis-ci.com/westonplatter/fast_arrow_auth.svg?branch=master)](https://travis-ci.com/westonplatter/fast_arrow_auth)
&nbsp;
[![Coverage
Status](https://coveralls.io/repos/github/westonplatter/fast_arrow_auth/badge.svg?branch=master)](https://coveralls.io/github/westonplatter/fast_arrow_auth?branch=master)
&nbsp;
[![Version](https://img.shields.io/pypi/v/fast_arrow_auth.svg)](https://pypi.org/project/fast-arrow-auth/)


## example

```py
# @TODO
```

## install

Install the package from pypi,
```
pip install fast_arrow_auth
```

## design principles

## features

## development
Install [pipenv](https://github.com/pypa/pipenv), and then run,
```
pipenv install --dev
```

Run the test suite via,
```
make test
```

Run all the examples (make sure you add username/password to config.debug.ini),
```
sh run_all_examples.sh
```

Run the test suite against a specific python version,
```
pipenv run tox -e py36
```

### releases

Adding so I don't forget the next time I release a version,
```
python setup.py sdist bdist_wheel
twine upload dist/*
```

## projects using `fast_arrow_auth`
Add your projects here.
