from django.shortcuts import render
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import random
from django.conf import settings


def get_photos():

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

    # Define the folder ID of the public folder containing the photos
    folder_id = '15Y7olgVeeHq81NiTjGFEjvh4RW0bEEtR'

    # Fetch the list of image files from the folder
    results = service.files().list(
        q="mimeType contains 'image/' and trashed=false and '{}' in parents".format(
            folder_id),
        fields="nextPageToken, files(id, name, webViewLink)").execute()
    items = results.get('files', [])

    # Get the public links for the photos
    photo_links = {}
    if items:
        for item in items:
            photo_links[item['name']] = item['webViewLink']
    return photo_links


def index(request):
    photos = get_photos()
    random_key = random.choice(list(photos.keys()))
    random_value = photos[random_key]
    img_id = random_value.split("/")[-2]
    img_id = img_id.replace("d_", "")
    return render(request, "szymon/index.html", {
        "img_id": img_id,
    })
