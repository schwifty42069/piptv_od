from bs4 import BeautifulSoup as Soup
import urllib.request
import requests
import json
import time
import tqdm


class ImdbQuery(object):
    def __init__(self, search, media_type):
        self.search = search
        self.media_type = media_type
        self.search_words = self.search.split()
        self.formatted_search = self.format_search_words()
        self.search_address = "https://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=all".format(self.formatted_search)
        self.titles = []
        self.title_codes = []

    def format_search_words(self):
        formatted_words = ''
        for word in self.search_words:
            formatted_words += word + "+"
        return formatted_words[:len(formatted_words) - 1]

    def scrape_title_codes(self):
        req = requests.get(self.search_address).text
        results = Soup(req, 'html.parser').findAll("td", {"class": "result_text"})
        for result in results:
            self.title_codes.append(str(result.parent).split("href=")[1].split(">")[0].strip("\"").split("/")[2])

    def scrape_media_titles(self):
        req = requests.get(self.search_address).text
        results = Soup(req, 'html.parser').findAll("td", {"class": "result_text"})
        for result in results:
            self.titles.append("{}. {}".format(results.index(result) + 1, str(result.contents[1]).split(">")[1]
                                               .split("</")[0] + result.contents[2]))
        return

    @staticmethod
    def get_series_seasons(title_code):
        series_page = "https://www.imdb.com/title/{}/episodes?season=1&ref_=tt_eps_sn_1".format(title_code)
        bsoup = Soup(requests.get(series_page).text, 'html.parser')
        num = 0
        for i in bsoup.find("select", id="bySeason").contents:
            if "<option value=" in str(i):
                if num < int(str(i).split("<option value=")[1].split(">")[0].strip("\"")):
                    num = int(str(i).split("<option value=")[1].split(">")[0].strip("\""))
        return num

    @staticmethod
    def get_season_episodes(title_code, season):
        season_series_page = "https://www.imdb.com/title/{}/episodes?season={}&ref_=tt_eps_sn_1"\
            .format(title_code, season)
        bsoup = Soup(requests.get(season_series_page).text, 'html.parser')
        num = 0
        for d in bsoup.findAll("div"):
            if "S" in d.text and "Ep" in d.text and "\n" not in d.text:
                if num < int(d.text.split("Ep")[1]):
                    num = int(d.text.split("Ep")[1])
        return num

    @staticmethod
    def scrape_episode_titles(title_code, season):
        titles = []
        season_series_page = "https://www.imdb.com/title/{}/episodes?season={}&ref_=tt_eps_sn_1"\
            .format(title_code, season)
        bsoup = Soup(requests.get(season_series_page).text, 'html.parser')
        x = 0
        for s in bsoup.findAll("strong"):
            if "title=" in str(s):
                x += 1
                titles.append("{}. {}".format(x, str(s).split("title=\"")[1].split("\">")[0]))
        return titles


class VsApiWrapper(object):
    def __init__(self, title_code, media_type, **kwargs):
        self.api_req_root = "https://www.vidsource.me/api/source/"
        self.title_code = title_code
        self.media_type = media_type
        try:
            if self.media_type == "tv" and "s" not in kwargs.keys() or self.media_type == "tv" \
                    and "e" not in kwargs.keys():
                raise MissingArgsException
        except MissingArgsException:
            print("Missing required keyword arguments for media_type {}".format(self.media_type))
        if "s" in kwargs.keys() and "e" in kwargs.keys() and media_type == "tv":
            s = kwargs.get("s")
            e = kwargs.get("e")
            self.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate,br', 'Host': 'vidsrc.me', 'Referer':
                            'https://vidsrc.me/server1/{}/{}-{}/'.format(self.title_code, s, e), 'User-Agent':
                            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
            self.media_code_url = "https://vidsrc.me/yeye?i={}&s={}&e={}&srv=1".format(self.title_code, s, e)
        else:
            self.headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate,br', 'Host': 'vidsrc.me', 'Referer':
                            'https://vidsrc.me/server1/{}/'.format(self.title_code), 'User-Agent':
                            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
            self.media_code_url = "https://vidsrc.me/yeye?i={}&srv=1".format(self.title_code)
        self.media_code = self.fetch_media_code()

    def fetch_media_code(self):
        req = requests.post(self.media_code_url, headers=self.headers).content
        return str(req, 'utf-8')

    def api_request(self):
        return json.loads(requests.post(self.api_req_root + self.media_code).text)


class ApiMassQuery(object):
    def __init__(self, title_code, imdb_query):
        self.title_code = title_code
        self.imdb_query = imdb_query
        self.media_type = self.imdb_query.media_type
        self.link_list = []

    def find_media_sources(self):
        if self.media_type == "tv":
            for s in range(self.imdb_query.get_series_seasons(self.title_code)):
                for e in range(self.imdb_query.get_season_episodes(self.title_code, s)):
                    try:
                        api = VsApiWrapper(self.title_code, "tv", s=s, e=e)
                        if api.media_code != '':
                            print("Season {} - Episode {}\n{}\n".format(s, self.imdb_query.scrape_episode_titles
                                                                        (self.title_code, s)[e - 1], api.api_request()
                                                                        ['data']))
                            self.link_list.append(api.api_request()['data'][len(api.api_request()['data']) - 1]['file'])
                            time.sleep(1.5)

                    except json.decoder.JSONDecodeError:
                        continue
        else:
            api = VsApiWrapper(self.title_code, "movie")
            if api.media_code != '':
                print("{}\n{}".format(self.imdb_query.titles[0], api.api_request()['data']))
            else:
                api.media_code_url = api.media_code_url[:len(api.media_code_url) - 2] + "2"
                api.media_code = api.fetch_media_code()
                print(api.media_code)
                print("{}\n{}".format(self.imdb_query.titles[0], api.api_request()['data']))
        return


class MediaDownloader(object):
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        site = urllib.request.urlopen(self.url)
        meta = site.info()
        self.size = int(int(meta._headers[3][1]) / 16384)

    def download_media(self):
        print("\nDownloading {}..\n".format(self.filename))
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            with open(self.filename, 'wb') as f:
                bar = tqdm.tqdm(total=self.size)
                for chunk in r.iter_content(chunk_size=16384):
                    if chunk:
                        f.write(chunk)
                        bar.update(1)
        return


class MissingArgsException(Exception):
    """Missing required keyword args for selected media type"""
    pass
