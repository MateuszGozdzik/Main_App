from django.shortcuts import render
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import random
from django.conf import settings
import requests
import os


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
    img_id = random_photo_link.split("/")[-2]
    img_id = img_id.replace("d_", "")
    return f"https://drive.google.com/uc?id={img_id}"

def get_photo_cat_api():
    api_key = os.getenv("CAT_API_KEY")
    url = f"https://api.thecatapi.com/v1/images/search?api_key={api_key}"
    response = requests.get(url)
    cat = response.json()[0]
    return cat["url"]


def index(request):
    special_photos_user = request.user.groups.filter(
        name="special photos").exists()
    simon_photos_user = request.user.groups.filter(
        name="simon photos").exists()
    if special_photos_user:
        mode = "special"
        photo = get_photos(special_photos_user)
    elif simon_photos_user:
        mode = "simon"
        photo = get_photos(special_photos_user)
    else:
        mode = "cat"
        photo = get_photo_cat_api()
    return render(request, "szymon/index.html", {
        "photo_id": photo,
        "mode": mode,
    })
