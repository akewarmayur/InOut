import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pathlib
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import shutil
import warnings
from pathlib import Path
warnings.filterwarnings("ignore")


class GoogleAPI:

    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        """Shows basic usage of the Drive v3 API.
          Prints the names and ids of the first 10 files the user has access to.
          """
        self.creds = None

    def intiate_gdAPI(self):
        pa = os.getcwd() + "/helpers/token.pickle"
        try:
            if os.path.exists(pa):
                with open(pa, 'rb') as token:
                    self.creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        '/content/gdrive/My Drive/credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(pa, 'wb') as token:
                    pickle.dump(self.creds, token)

            service = build('drive', 'v3', credentials=self.creds)
            #build
            return service
        except Exception as e:
            print('Google Drive API connection Exception=>', e)
            return None

    def delete_file(self, service, file_id):
        try:
            service.files().delete(fileId=file_id).execute()
        except Exception as e:
            print(e)

    def upload_file(self, service, filename, filepath, folder_id, mime_type):
        # print(filepath)
        try:
            file_metadata = {'name': filename,
                             'parents': [folder_id]}
            media = MediaFileUpload(filepath, mimetype=mime_type)
            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
            # print('File ID: %s upload' % file.get('id'))
            # print('File upload success')
        except Exception as e:
            print('file upload exception=>', e)

    def search_file(self, service, file_name, mime_type, folder_id, search_in_folder=False):
        try:
            page_token = None
            c = False
            while True:
                if search_in_folder == False:
                    if mime_type == 'text/plain':
                        response = service.files().list(q="mimeType='text/plain'",
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()
                    elif mime_type == 'text/csv':
                        response = service.files().list(q="mimeType='text/csv'",
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()
                    elif mime_type == 'application/json':
                        response = service.files().list(q="mimeType='application/json'",
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()
                    elif mime_type == 'image/png' or mime_type == 'image/jpg':
                        response = service.files().list(q="mimeType='text/plain'",
                                                        spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()
                    else:
                        response = service.files().list(spaces='drive',
                                                        fields='nextPageToken, files(id, name)',
                                                        pageToken=page_token).execute()
                else:
                    response = service.files().list(q="parents in '{}'".format(folder_id),
                                                    spaces='drive',
                                                    fields='nextPageToken, files(id, name)',
                                                    pageToken=page_token).execute()
                for file in response.get('files', []):
                    # Process change

                    ff = file.get('name')
                    if ff == file_name:
                        c = True
                        # print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                        break
                if c == True:
                    break
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    return 0
            return file.get('id')
        except Exception as e:
            print(e)
            return 0

    def download_files(self, service, file_path, file_id, check=True):
        file = pathlib.Path(file_path)
        if file.exists() and check == True:
            print(' ')
            # print("File exist")
        else:
            # print("File not exist")
            # file_id = '1RZlYb9ufdqA5NjC5oJ8BgAPGW02riZTB'
            # file_name = 'yolov3.cfg'
            request = service.files().get_media(fileId=file_id)
            # request = service.files().export_media(fileId=file_id, mimeType='application/pdf')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            fh.seek(0)
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(fh, f)

    def createFolder(self, service, folder_name, folder_id):
        try:
            file_metadata = {
                'name': folder_name,
                'parents': [folder_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = service.files().create(body=file_metadata, fields='id').execute()
            f_id = file.get('id')
            return f_id
        except Exception as e:
            msg = f"Exception in creating folder on google drive: {e}"
            return 0



