import requests
from bs4 import BeautifulSoup as bs
import re


# Genius Song parts to strip from lyrics
song_parts_toremove = [ "\[Verse [0-9]\]\n",
                        "\[Chorus\]\n",
                        "\[Introduction (Intro)\]\n",
                        "\[Verse\]\n",
                        "\[Refrain\]\n",
                        "\[Pre-Chorus (Climb)\]\n",
                        "\[Chorus\]\n",
                        "\[Post-Chorus\]\n",
                        "\[Hooks\]\n",
                        "\[Riffs/Basslines\]\n",
                        "\[Turntablism\]\n",
                        "\[Bridge\]\n",
                        "\[Interlude\]\n",
                        "\[Skit\]\n",
                        "\[Collision\]\n",
                        "\[Instrumental or Solo\]\n",
                        "\[Ad lib\]\n",
                        "\[Segue\]\n",
                        "\[Outro\]\n"]

## Client access token for the API
token = [x.strip().split()[1] for x in open("ids.txt", 'r').readlines() if x.startswith('token')][0]

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer ' + token}

search_url = base_url + "/search"
song_title = "The Big Come Down"
data = {'q': song_title}

response = requests.get(search_url, data=data, headers=headers)
json = response.json()

artistpath = None
song_info = None
for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == "Nine Inch Nails":
        artistpath = hit["result"]["primary_artist"]["api_path"]
        song_info = hit
        break

songurl = base_url + artistpath + "/songs"
data = {"per_page": 20, "page": 1}
print data
response = requests.get(songurl, params=data, headers=headers)
json = response.json()
while json["response"]["next_page"]:
    songlist = json["response"]["songs"]
    data["page"] = json["response"]["next_page"]
    print data
    for song in songlist:
        print song["title"]
    response = requests.get(songurl, params=data, headers=headers) 
    json = response.json()


#if song_info:
#    songurl = song_info["result"]["url"]
#    lyricspage = requests.get(songurl)


#html = bs(lyricspage.text, "html.parser")
#[h.extract() for h in html('script')]
#lyrics = html.find("div", class_="lyrics").get_text()

#for part in song_parts_toremove:
#    lyrics = re.sub(part, "", lyrics)

#print lyrics


