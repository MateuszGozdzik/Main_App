from django.shortcuts import render
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import random
from django.conf import settings


def get_photos(special_photos_user: bool):

    creds = Credentials.from_service_account_info({
        "type": "service_account",
        "project_id": settings.DRIVE_PROJECT_ID,
        "private_key_id": settings.DRIVE_PRIVATE_KEY_ID,
        "private_key": settings.DRIVE_PRIVATE_KEY,
        "client_email": settings.DRIVE_CLIENT_EMAIL,
        "client_id": settings.DRIVE_CLIENT_ID,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": settings.DRIVE_CLIENT_X509_CERT_URL
    })
    service = build('drive', 'v3', credentials=creds)
    folder_id = '15Y7olgVeeHq81NiTjGFEjvh4RW0bEEtR'
    special_folder_id = '1eJ3tUbQHl5Ghl83phldn8NqaEXxI_Rvj'

    # Fetch the list of image files from the folder
    results = service.files().list(
        q=f"mimeType contains 'image/' and trashed=false and '{folder_id}' in parents", fields="nextPageToken, files(id, name, webViewLink)").execute()
    items = results.get('files', [])
    if special_photos_user:
        results2 = service.files().list(
            q=f"mimeType contains 'image/' and trashed=false and '{special_folder_id}' in parents", fields="nextPageToken, files(id, name, webViewLink)").execute()
        items = results.get('files', []) + results2.get('files', [])

    random_photo_link = random.choice(items)["webViewLink"]
    return random_photo_link


def index(request):
    special_photos_user = request.user.groups.filter(
        name="special photos").exists()
    photo = get_photos(special_photos_user)
    img_id = photo.split("/")[-2]
    img_id = img_id.replace("d_", "")
    return render(request, "szymon/index.html", {
        "img_id": img_id,
    })
