
import facebook

oauth_access_token = "CAACEdEose0cBAMjD9ZBmTxOLdH71GGwY69ZBsDL6tmWeIsBHkorZC4ZBErM1RjDj8izOlBaPduDVqlYfoeI8hZB7RoVo5wF6ao9bSA2SZAPKRyLY7Ceva0ZBa4SPVQZAwXhKzbu06TPVLX5AmgZCdt17u3Nq6fXzi93ZCZAUlM05hQ4e2KKwXgklrvcUzYqZCwM8GPkZD"

graph = facebook.GraphAPI(oauth_access_token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

print "Welcome to Facebook!"
print profile["first_name"]+profile["last_name"]
print profile["gender"]

print "Your friendlist"
for friend in friends["data"]:
	print friend["name"]
	
print "Posting random message on your wall"
#graph.put_object("me", "feed", message="Writing from awesome fbpy!")

