#! /bin/python
# -*- coding: utf-8 -*-

import os, json, time, hashlib

class Cache(object):
    def __init__(self, cache_path=None, cache_name=None, cache_extension="cache", expired=3600):
        extension = cache_extension.lstrip(".") or "cache"
        self.extension = "." + extension

        self.expired = expired
        self.cache_name = cache_name or hashlib.md5(".").hexdigest()

        if cache_path and os.path.exists(cache_path) == True:
            self.cache_path = cache_path
        else:
            self.cache_path = os.path.abspath("./cache")

    '''
    Get cache file point and data, if file not exist, data = {}
    '''
    def __get_cache(self):
        path = self.cache_path+"/"+self.cache_name+self.extension
        try:
            fp = open(path, "r+")
            data = fp.read()
            return (fp, data)
        except IOError as e:
            fp = open(path, "w+")
            data = "{}"
            return (fp, data)
    '''
    Set cache file by string data, data json format likes {"key": {"expired": 3600, "data": "value", "time": 1443578308}}
    :param string data
    '''
    def __set_cache(self, data):
        path = self.cache_path+"/"+self.cache_name+self.extension
        fp = open(path, "w+")
        fp.write(data)

    '''
    Set expired length
    :param int expired  expired time
    '''
    def set_exipired(self, expired=3600):
        self.expired = expired or self.expired
        return self.expired

    '''
    Get cache file name in md5 hash
    '''
    def get_cache_name(self):
        return self.cache_name

    '''
    Set cache file name by string
    :param string name  cache file name
    '''
    def set_cache_name(self, name):
        self.cache_name = hashlib.md5(name).hexdigest()
        return self.cache_name

    '''
    Set cache file extension without "."
    :param string extension without "."
    :return
    '''
    def set_extension(self, extension):
        extension = extension.lstrip(".") or "cache"
        self.extension = "." + extension

    '''
    Get cache file extension name
    :return extension
    '''
    def get_extension(self):
        return self.extension

    '''
    Set cahce file save directory, with check exist, please make sure directory has write competencec
    :param string dir
    :return cache_path
    '''
    def set_cache_dir(self, dir):
        if os.path.exists(dir) == True:
            self.cache_path = dir
        return self.cache_path

    '''
    Clear expired keys in cache file
    :return null
    '''
    def clear_expired(self):
        fp, data = self.__get_cache()
        data = json.loads(data)
        for key, value in data.items():
            if value["time"] + value["expired"] < int(time.time()):
                del data[key]
        self.__set_cache(json.dumps(data))

    '''
    Check if key is cahce in cahce file and check expired
    :return True/False
    '''
    def is_cache(self, key):
        fp, data = self.__get_cache()
        data = json.loads(data)
        if data.has_key(key):
            item = data[key]
            if item["time"] + item["expired"] < int(time.time()):
                del data[key]
                self.__set_cache(json.dumps(data))
                return False
            else:
                return True
        return False

    '''
    Get cahce value, with check expired
    :param string key
    '''
    def get(self, key):
        fp, data = self.__get_cache()
        data = json.loads(data)
        if data.has_key(key):
            item = data[key]
            if item["time"] + item["expired"] < int(time.time()):
                '''data expired'''
                del data[key]
                self.__set_cache(json.dumps(data))
                return None
            else:
                return item
        return None

    '''
    Set cache
    :param string key
    :param string value in json format
    :param int expired
    '''
    def set(self, key, value, expired=None):
        expired = expired or self.expired
        fp, data = self.__get_cache()

        try:
            data = json.loads(data)
        except:
            data = {}

        store_value = {
            "time": int(time.time()),
            "expired": expired,
            "data": value
        }
        data[key] = store_value
        m = json.dumps(data)
        self.__set_cache(m.strip(""))

if __name__ == "__main__":
    cache = Cache(cache_extension=".cache", cache_name="py-cache", expired=3600)
    cache.set("key", "value", 1)
    cache.clear_expired()
    print cache.is_cache("key")
    print cache.get("key")
