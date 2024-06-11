from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GoogleDriveAdapter:
    def __init__(self, service_account_file):
        self.service_account_file = service_account_file
        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=['https://www.googleapis.com/auth/drive'])
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def create_folder(self, folder_name, parent_folder_id=None):
        """Create a folder in Google Drive and return its ID."""
        folder_metadata = {
            'name': folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            'parents': [parent_folder_id] if parent_folder_id else []
        }

        created_folder = self.drive_service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()

        print(f'Created Folder ID: {created_folder["id"]}')
        return created_folder["id"]

    def delete_files(self, file_or_folder_id):
        """Delete a file or folder in Google Drive by ID."""
        try:
            self.drive_service.files().delete(fileId=file_or_folder_id).execute()
            print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
        except Exception as e:
            print(f"Error deleting file/folder with ID: {file_or_folder_id}")
            print(f"Error details: {str(e)}")

    def upload_file(self, file_path, folder_id):
        """Upload a file to Google Drive."""
        file_metadata = {'name': file_path.split('/')[-1], 'parents': [folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Uploaded File ID: {uploaded_file["id"]}')
        return uploaded_file["id"]
