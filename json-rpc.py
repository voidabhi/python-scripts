# This is an example for panager json-rpc
# you may copy/redistribute/whatever this file
import json # manipulation of json
import socket # for server connection
import getpass # for password input

PORT = 8888 # Port that json-rpc server runs
HOST = 'localhost' # Host that the server runs
BUFF = 2048 # Number of bytes to receive from the server socket
# (will never be reached, but just in case...)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialise our socket
sock.connect((HOST, PORT)) # connect to host <HOST> to port <PORT>

# We will store all the input at a dictionary,
# for easier json formatting
input_data = {}
# DO NOT USE THE SCRIPT AS-IS. IT REQUIRES INPUT SANITIZATION!!!
input_data['website'] = raw_input('Website: ') # Read input for "website"
input_data['username'] = raw_input('Username: ') # Read input for "username"
input_data['password'] = getpass.getpass('Password: ') # Read hidden input for "password"

dumped_data = json.dumps(input_data) # Dump the input dictionary to proper json
# Note: dumps faction was imported from json module, remember?

sock.send(dumped_data) # Send the dumped data to the server
server_response = sock.recv(BUFF) # Receive the results (if any) from the server
decoded_response = json.loads(server_response) # decode the data received
sock.close() # close the socket connection
print decoded_response['passphrase'] # spit the decoded data
