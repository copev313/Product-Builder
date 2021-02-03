# drive.py

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def google_drive(upload_file_loc='', title=''):
    """
    Uses pydrive to create a document and uploads an Excel worksheet to
    Google Drive.

    Parameters
    ----------
    upload_file_loc : str, optional
        The file location of the file to be uploaded to Google Drive,
        by default ''.
    title : str, optional
        Name of the new document in Google Drive, by default ''.

    Returns
    -------
    url: str
        The url to the created Google Sheet document.
    """
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()      # Create local server to handle OAuth.

    except Exception as e:
        print(f'Google Auth ERR: {e}')

    try:
        # Create GoogleDrive instance with authenticated GoogleAuth instance.
        drive = GoogleDrive(gauth)

        # String parts...
        mime_str1 = "application/vnd.openxmlformats-officedocument."
        mime_str2 = "spreadsheetml.sheet"
        # Create GoogleDriveFile instance and specifiy the title.
        doc = drive.CreateFile({'title': title,
                                'mimeType': f"{mime_str1}{mime_str2}",
                                })

        # Set the content of the file to be the Excel worksheet.
        doc.SetContentFile(upload_file_loc)
        # Upload the file & convert to Google Sheet
        doc.Upload({'convert': True})
        # Link to newly created / uploaded document:
        link_me = doc['alternateLink']

        # debugging
        print(f"File uploaded successfully! The title is: {doc['title']}")
        print(f"Your Created Document Can Be Found Here ==> \n{link_me}")
        # Save to common variable
        url = link_me

    except Exception as e:
        print(f'PYDRIVE ERR: {e}')
        url = "https://www.youneedtoshutup.com/"

    return url
