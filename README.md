# fast_arrow_auth
A brief python library to handler API authentication with Robinhood.

[![Build Status](https://travis-ci.com/westonplatter/fast_arrow_auth.svg?branch=master)](https://travis-ci.com/westonplatter/fast_arrow_auth)
&nbsp;
[![Coverage
Status](https://coveralls.io/repos/github/westonplatter/fast_arrow_auth/badge.svg?branch=master)](https://coveralls.io/github/westonplatter/fast_arrow_auth?branch=master)
&nbsp;
[![Version](https://img.shields.io/pypi/v/fast_arrow_auth.svg)](https://pypi.org/project/fast-arrow-auth/)


## example

```py
# input username and password. Or, alternatively, pull from a config file,
# see https://github.com/westonplatter/fast_arrow_auth/blob/master/examples/auth_generated_device_token.py
username = "my_username"
password = "my_device"

client = Client(username=username, password=password)
result = client.authenticate()

user = User.fetch(client)
print("Username = {}".format(user["username"]))
```

## install

Install the package from pypi,
```
pip install fast_arrow_auth
```

## design principles
`fast_arrow_auth` is focused **only** on authenticating with Robinhood's API.

It's focused on these discrete operations,
- authenticate via username/password or username/password/mfa
- write auth_token, etc to file for API clients to use

## development
Install [pipenv](https://github.com/pypa/pipenv), and then run,
```
pipenv install --dev
```

Run the test suite via,
```
make test
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
Add projects here.
