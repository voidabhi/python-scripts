#!/usr/bin/env python
import sys
import json
import urllib
import urllib2
import argparse

def translate(target, text):
    api = "https://www.googleapis.com/language/translate/v2?"
    api_key = "AIzaSyBgBlJCogk_1Hd_7WaLQgLVbQss0_dvNUc"
    parameters = urllib.urlencode({
        'target': target,
        'key': api_key,
        'q': text
    })

    response = urllib2.urlopen(api + parameters)
    translations = json.loads(response.read())

    translated_text = translations['data']['translations'][0]['translatedText']
    return translated_text.encode('utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', default="en", \
                        help="the language to translate into (default: en)")
    parser.add_argument('text', nargs='*', help="the text to translate")
    args = parser.parse_args()

    if args.text:
        text = ' '.join(args.text)
    else:
        text = sys.stdin.read()
    
    print translate(args.target, text)

if __name__ == "__main__":
    main()
