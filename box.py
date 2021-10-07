from boxsdk import OAuth2, Client
from settings import CLIENT_ID, CLIENT_SECRET, DEVELOPER_TOKEN

auth = OAuth2(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=DEVELOPER_TOKEN,
)
client = Client(auth)

user = client.user().get()
print('The current user ID is {0}'.format(user.id))
