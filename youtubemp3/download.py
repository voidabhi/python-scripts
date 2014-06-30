
import os
import urllib
import re
import cPickle
import HTMLParser
import requests
import time

show_url = "http://www.tunefind.com/show/%s"
season_url = "http://www.tunefind.com/show/%s/season-%d"
episode_url = "http://www.tunefind.com/show/%s/season-%d/%s"


def get_youtube_mp3_url(url):
    for i in xrange(2):
        statusurl = None
        r = requests.post("http://www.listentoyoutube.com/cc/conversioncloud.php", data={"mediaurl": url, "client_urlmap": "none"})
        try:
            statusurl = eval(r.text)['statusurl'].replace('\\/', '/') + "&json"
            break
        except:
            print eval(r.text)['error']
            time.sleep(1)
    while True:
        if not statusurl:
            raise Exception("")
        try:
            resp = eval(requests.get(statusurl).text)
            if 'downloadurl' in resp:
                downloadurl = resp['downloadurl'].replace('\\/', '/')
                break
            time.sleep(1)
        except Exception:
            pass
    return downloadurl


def urlopen(url, tries=10):
    exc = "Couldn't open url %s" % url
    for i in xrange(tries):
        try:
            stream = urllib.urlopen(url)
            return str(stream.read())
        except Exception as e:
            exc = e
    raise Exception(exc)


def download_song(song, location):
    print song
    song_name = song[1] + " - " + song[0] + ".mp3"
    if not os.path.exists(location):
        os.makedirs(location)
    if not os.path.exists(os.path.join(location, song_name)):
        try:
            r = requests.get("https://youtube.com", params={"search_query": "%s %s" % (song[1], song[0])}).text
            top_vid_id = re.findall(r'data-context-item-id="(.*?)"', r)[0]
            mp3_url = get_youtube_mp3_url("YouTube" + top_vid_id)
            cmd = 'idman /d %s /p "%s" /f "%s" /a' % (mp3_url, os.path.join(os.getcwd(), location), song_name)
            os.system(cmd)
        except Exception:
            raise


def get_episode_music(show, season, episode):
    episode_num, episode_name = episode
    episode_dir = os.path.join(show, str(season), episode_name.replace(':', ''))
    episode_data_path = os.path.join(show, str(season), episode_name.replace(':', ''), "data")
    if not os.path.exists(episode_dir):
        os.mkdir(episode_dir)
    if os.path.exists(episode_data_path):
        with open(episode_data_path) as episode_data_file:
            episode_data = cPickle.load(episode_data_file)
    else:
        episode_data = {}
        pg = urlopen(episode_url % (show, season, episode_num))
        h = HTMLParser.HTMLParser()
        try:
            episode_data['songs'] = list((h.unescape(b), h.unescape(c), a) for (a, b, c, d) in re.findall(r'<a .*?name="song-\d+" href="(/song/\d+/\d+.*?)".*?><i.*?></i>(.*?)</a>\W*by (.*?)\W*<div.*?>\W*<div.*?>(.*?)</div>\W*</div>', pg))
        except:
            episode_data['songs'] = list((b, c, a) for (a, b, c, d) in re.findall(r'<a .*?name="song-\d+" href="(/song/\d+/\d+.*?)".*?><i.*?></i>(.*?)</a>\W*by (.*?)\W*<div.*?>\W*<div.*?>(.*?)</div>\W*</div>', pg))
        with open(episode_data_path, 'wb') as episode_data_file:
            cPickle.dump(episode_data, episode_data_file)

    for song in episode_data['songs']:
        download_song(song, episode_dir)


def get_season_music(show, season):
    season_dir = os.path.join(show, str(season))
    season_data_path = os.path.join(show, str(season), 'data')
    if not os.path.exists(season_dir):
        os.mkdir(season_dir)
    if os.path.exists(season_data_path):
        with open(season_data_path) as season_data_file:
            season_data = cPickle.load(season_data_file)
    else:
        season_data = {}
        h = HTMLParser.HTMLParser()
        pg = urlopen(season_url % (show, season))
        season_data['episodes'] = list((a, h.unescape(b)) for (a, b) in re.findall(r'<a href=".*?" name="episode(.*?)">\W*(.*?)\W*</a>', pg))
        with open(season_data_path, 'wb') as season_data_file:
            cPickle.dump(season_data, season_data_file)
    # print season_data
    for episode in season_data['episodes']:
        get_episode_music(show, season, episode)


def get_show_music(show):
    if not os.path.exists(show):
        os.mkdir(show)
    if os.path.exists(os.path.join(show, 'data')):
        with open(os.path.join(show, 'data')) as show_data_file:
            show_data = cPickle.load(show_data_file)
    else:
        show_data = {}
        slug = show.lower().replace(' ', '-')
        pg = urlopen(show_url % show)
        season_finder_pattern = r'/show/' + slug + r'/season-\d+'
        print season_finder_pattern
        season_links = list(set(re.findall(season_finder_pattern, pg)))
        season_links.sort()
        seasons = list(int(sl[sl.find('season-') + len('season-'):]) for sl in season_links)
        seasons.sort()
        show_data['seasons'] = seasons
        with open(os.path.join(show, 'data'), 'wb') as show_data_file:
            cPickle.dump(show_data, show_data_file)
    # print show_data
    for season in show_data['seasons']:
        get_season_music(show, season)

    os.system("idman /s")

if __name__ == '__main__':
    download_song(["Humme hai hero", "A R Rahman"], "Misc")
   # get_show_music("How I Met Your Mother")
   # get_show_music("Castle")