import configparser
from fast_arrow_auth import Client
from fast_arrow_auth.resources.user import User

print("----- running {}".format(__file__))

#
# get the authentication configs
#
config_file = "config.dev.ini"
config = configparser.ConfigParser()
config.read(config_file)
username = config['account']['username']
password = config['account']['password']

client = Client(username=username, password=password)
result = client.authenticate()

print("Authenticated successfully = {}".format(result))

print("Account Url = {}".format(client.account_url))
print("Account Id = {}".format(client.account_id))

user = User.fetch(client)
print("Username = {}".format(user["username"]))

result = client.relogin_oauth2()
print("Re-Authenticated with refresh_token successfully = {}".format(result))

result = client.logout_oauth2()
print("Logged out successfully = {}".format(result))
