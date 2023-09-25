import requests
import os
import shutil
from urllib.request import urlretrieve
from model.surah import Surah
from model.ayah import Ayah


def main():
    surah_list = fetch_surah()['data']
    for surah in surah_list:
        store_surah(surah)
        print(f"Surah {surah['latin']} inserted")
        ayah_list = fetch_ayah(surah)['data']
        print(f"Inserting {len(ayah_list)} ayahs")
        for ayah in ayah_list:
            store_ayah(ayah)
            download_audio_ayah(ayah)


def fetch_surah():
    url = "https://web-api.qurankemenag.net/quran-surah"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def store_surah(surah):
    surah_item = Surah()
    surah_item.insert(
        id=surah['id'],
        arabic=surah['arabic'],
        latin=surah['latin'],
        transliteration=surah['transliteration'],
        translation=surah['translation'],
        num_ayah=surah['num_ayah'],
        page=surah['page'],
        location=surah['location'],
    ).on_conflict(
        conflict_target=[Surah.id],
        preserve=[Surah.id],
    ).execute()
    

def fetch_ayah(surah):
    url = f"https://web-api.qurankemenag.net/quran-ayah"
    response = requests.get(url, params={
        'surah': surah['id'],
        'start': 0,
        'limit': surah['num_ayah'],
    })
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

def store_ayah(ayah):
    ayah_item = Ayah()
    ayah_item.insert(
        id=ayah['id'],
        surah_id=ayah['surah_id'],
        ayah=ayah['ayah'],
        page=ayah['page'],
        quarter_hizb=ayah['quarter_hizb'],
        juz=ayah['juz'],
        manzil=ayah['manzil'],
        arabic=ayah['arabic'],
        kitabah=ayah['kitabah'],
        latin=ayah['latin'],
        translation=ayah['translation'],
        footnotes=ayah['footnotes'],
    ).on_conflict(
        conflict_target=[Ayah.id],
        preserve=[Ayah.id],
    ).execute()


def download_audio_ayah(ayah):
    path = f"audio/Abu_Bakr_Ash-Shaatree_aac64"
    url = f"https://media.qurankemenag.net/{path}/{ayah['surah_id'] :03d}{ayah['ayah'] :03d}.m4a"
    if not os.path.exists(f"{path}/{ayah['surah_id'] :03d}"):
        os.makedirs(f"{path}/{ayah['surah_id'] :03d}", exist_ok=True)
    urlretrieve(url, f"{path}/{ayah['surah_id'] :03d}/{ayah['ayah'] :03d}.m4a")
    

if __name__ == "__main__":
    main()
