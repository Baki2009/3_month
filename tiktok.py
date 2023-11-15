import requests, os

input_url = input("URL video: ")
print(input_url)
#https://www.tiktok.com/@geeks_osh/video/7293896300020403474
#https://www.tiktok.com/@geeks_osh/video/7293896300020403474?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029
split_url = input_url.split("/")
print(split_url)
current_id = split_url[5].split("?")[0]
print(current_id)
video_api = requests.get(f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}").json()
# print(video_api)
video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
print(video_url)
if video_url:
    print("Скачиваем видео", video_api.get('aweme_list')[0].get('desc'))
    title = video_api.get('aweme_list')[0].get('desc')
    try:
        os.mkdir('video')
    except:
        pass
    try:
        with open(f'video/{title}.mp4', 'wb') as video_file:
            video_file.write(requests.get(video_url).content)
        print(f"Видео {title}.mp4 успешно скачан в папку video")
    except Exception as error:
        print(f"Error {error}")

        

  