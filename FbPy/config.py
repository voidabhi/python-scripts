
import ConfigParser

config  = ConfigParser.ConfigParser()
config.read("settings.cfg")
username  = config.get("auth","username")
password  = config.get("auth","password")
print username 
print password