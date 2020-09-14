import vk_api
from vk_api.audio import VkAudio
import re
import requests

vk_session = vk_api.VkApi('+79162863084', 'L-02')
vk_session.auth()
vkaudio = VkAudio(vk_session, convert_m3u8_links=True)
albums = vkaudio.get_post_audio(-80472434,92776)
for album in list(albums):
        print(album['title'], album['url'].split("?")[0])

url = 'https://cs1-67v4.vkuseraudio.net/p17/d712cbd62f9408.mp3'  
r = requests.get(url)
with open('/Users/Илья/Music/Приёмка/'+название+'.mp3', 'wb') as f:  
    f.write(r.content)
