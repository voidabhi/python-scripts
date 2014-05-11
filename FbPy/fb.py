
import facebook

oauth_access_token = "CAACEdEose0cBAO04waCG0vfZCOIfloedhMHzMZBZB56FBhv52GwTZCMAer4kZAiSdxz5Ap66fLjX18erhGHwUm5qx2ZBtVVt4LZA4YqpDoLP8XKJq9PVGArUmZBqcZAu2eQz2UdqObnFxI3thDN5TCDTarkZA3sQblWN1ZAEbCot2QT6JICw4btpQB8Q2PjvZCmnDU8ZD"

graph = facebook.GraphAPI(oauth_access_token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

print "Welcome to Facebook!"
print profile["first_name"]+profile["last_name"]
print profile["gender"]

print "Your friendlist"
for friend in friends["data"]:
	print friend["name"]

