import json
import requests
import argparse
import sys


class GUrlShorten():
    def __init__(self, key):
        self.API_KEY = key

    def google_url_shorten(self, url):
        req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + self.API_KEY
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(req_url, json=payload, headers=headers)
        resp = json.loads(r.text)
        return resp['id']

    def google_url_expand(self, url):
        req_url = 'https://www.googleapis.com/urlshortener/v1/url'
        payload = {'key': self.API_KEY, 'shortUrl': url}
        r = requests.get(req_url, params=payload)
        resp = json.loads(r.text)
        return resp['longUrl']


def main():
    desc = "A python script to shorten or expand urls using Google Url Shortener API"

    parser = argparse.ArgumentParser(description=desc, prog='GoogleUrlShortener.py')
    parser.add_argument('-e', '--expand', action='store_true', help='Short Url will be expanded.')
    parser.add_argument('-s', '--shorten', action='store_true', help='Long Url will be shortened.')
    req_key = parser.add_argument_group("Required named arguments")
    req_key.add_argument('-k', '--key', type=str, help='Browser API key. Get it from Google Developer Console', required=True)
    req_key.add_argument('-u', '--url', type=str, help='URL which you want to shorten or expand.', required=True)
    args = parser.parse_args()

    if args.expand and args.shorten:
        print('\n--expand/--shorten are mutually exclusive\n')
        parser.parse_args(['--help'])
    if not (args.shorten or args.expand):
        print('\n--expand/--shorten is required\n')
        parser.parse_args(['--help'])
    else:
        obj = GUrlShorten(args.key)
        if args.expand:
            print(obj.google_url_expand(args.url))
        elif args.shorten:
            print(obj.google_url_shorten(args.url))
        else:
            raise Exception('Magical Exception')

if __name__ == '__main__':
    sys.exit(main())
