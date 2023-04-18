import os
import random

import requests
from django.conf import settings
from django.shortcuts import render
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from core.decorators import group_required


def get_drive_photos(mode):
    creds = Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": settings.DRIVE_PROJECT_ID,
            "private_key_id": settings.DRIVE_PRIVATE_KEY_ID,
            "private_key": settings.DRIVE_PRIVATE_KEY,
            "client_email": settings.DRIVE_CLIENT_EMAIL,
            "client_id": settings.DRIVE_CLIENT_ID,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": settings.DRIVE_CLIENT_X509_CERT_URL,
        }
    )
    service = build("drive", "v3", credentials=creds)

    if mode == "simon":
        folder_id = os.getenv("DRIVE_SIMON_FOLDER")
    elif mode == "special":
        folder_id = os.getenv("DRIVE_SPECIAL_FOLDER")

    results = (
        service.files()
        .list(
            q=f"mimeType contains 'image/' and trashed=false and '{folder_id}' in parents",
            fields="nextPageToken, files(id, name, webViewLink)",
        )
        .execute()
    )
    items = results.get("files", [])

    random_photo_link = random.choice(items)["webViewLink"]
    img_id = random_photo_link.split("/")[-2]
    img_id = img_id.replace("d_", "")
    return f"https://drive.google.com/uc?id={img_id}"


def get_cat_photos():
    api_key = os.getenv("CAT_API_KEY")
    url = f"https://api.thecatapi.com/v1/images/search?api_key={api_key}"
    response = requests.get(url)
    cat = response.json()[0]
    return cat["url"]


def get_dog_photos():
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    dog_url = response.json()["message"]
    return dog_url


def render_photo(request, photo=None):
    return render(
        request,
        "szymon/index.html",
        {
            "photo_id": photo,
        },
    )


def index(request):
    return render_photo(request)


def cat_photos(request):
    photo = get_cat_photos()
    return render_photo(request, photo)


def dog_photos(request):
    photo = get_dog_photos()
    return render_photo(request, photo)


@group_required("special photos")
def special_photos(request):
    photo = get_drive_photos("special")
    return render_photo(request, photo)


@group_required("simon photos")
def simon_photos(request):
    photo = get_drive_photos("simon")
    return render_photo(request, photo)
