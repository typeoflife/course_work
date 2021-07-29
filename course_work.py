import requests
from pprint import pprint
import json
from datetime import date
import time

vktoken = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
yatoken = ""
href_dict = dict()
json_list = []

class VkSaver:

    def photos_get_vk(self, user_id):
        url = "https://api.vk.com/method/photos.get"
        params = {
            "user_id": {user_id},
            "access_token": vktoken,
            "v": "5.77",
            "album_id" : "wall",
            "extended": "1"
        }
        current_date = date.today()
        response = requests.get(url=url, params=params)
        if "response" in response.json():
            photograph = response.json()["response"]["items"]
            for photo in photograph:
                if photo["likes"]["count"] in href_dict.values():
                    photo["likes"]["count"] = f'{photo["likes"]["count"]}({current_date})'
                href_dict[photo["sizes"][-1]["url"]] = photo["likes"]["count"]
                files_dict = dict()
                files_dict["file_name"] = f'{photo["likes"]["count"]}.jpg'
                files_dict["size"] = photo["sizes"][-1]["type"]
                json_list.append(files_dict)
        else:
            print("Profile closed or deleted")


    def get_ya_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(yatoken)
        }

    def upload_by_url(self, file_path, url):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_ya_headers()
        params = {"path": file_path, "url": url, "overwride": "true"}
        response = requests.post(upload_url, headers=headers, params=params)
        if response.status_code == 202:
            print("Response from server - OK")
        return response.json()

    def download_json(self,json_length):
        out_file = open('json_out', 'w+')
        json.dump(json_list[0:json_length], out_file)


    def upload_by_dict(self,user_id, quantity_photo=5):
        self.photos_get_vk(user_id=user_id)
        if len(href_dict) >= quantity_photo:
            print("Begin uploading...")
            dict_by_number = list(enumerate(href_dict.items()))
            for tuple_list in dict_by_number[0:quantity_photo]:
                time.sleep(1)
                self.upload_by_url(f"netology/{tuple_list[1][1]}.jpg", {tuple_list[1][0]})
                print(f"File {tuple_list[1][1]}.jpg upload")
            self.download_json(json_length=quantity_photo)
            print(f"Done, {quantity_photo} file(s) uploaded")
        elif len(href_dict) == 0:
            print("No photo for copy")
        else:
            print(f"Not enough photo in profile, only {len(href_dict)} photo(s) is available")


vkcopy = VkSaver()
vkcopy.upload_by_dict("21215", 11)



