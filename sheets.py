import httplib2
import os

from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'AcademiaDasApostas'
file_id = '1_NmlDRUS0ITWVpQ7E_ImzT01HRgX4ZHyQJ1omVA7yv4'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'academiadasapostas.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	drive_service = discovery.build('drive', 'v3', http=http)

	file_metadata = {
		'name' : 'AcademiaDasApostas',
		'mimeType' : 'application/vnd.google-apps.spreadsheet'
	}
	media = MediaFileUpload('bets.txt', mimetype='text/csv', resumable=True)
	file = drive_service.files().update(fileId=file_id, body=file_metadata, media_body=media, fields='id').execute()
	print(file)


if __name__ == '__main__':
    main()