#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse
import urllib
import json
from game import game

PORT_NUMBER = 8080

users = []		#userID is index {name:name, gameID:gameID}
games = []		#gameID is index

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):

	def getValue(self, key):
		value = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get(key, None)
		if(not value == None):
			return value[0]
		return None

	def writeJSON(self, dict):
		b=json.dumps(dict)
		self.wfile.write(b.encode())
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		func = self.getValue('func')

		if(func == 'requestUserID'):
			name = self.getValue("name")
			if(not name == None):
				userID = len(users)
				users.append({"name":name, "gameID":-1})

				dict = {"userID":userID}
				self.writeJSON(dict)
				return
			else:
				#return API error for no name given
				return
		if(func == "createGame"):
			userID = self.getValue("userID")
			if(not userID == None):
				password = self.getValue("password")
				if(password == None):
					password = -1
				gameID = len(games)
				newGame = game(gameID, password)

				newGame.users.append(userID)
				games.append(newGame)

				dict = {"gameID":gameID, "password":password}
				self.writeJSON(dict)
				return
			else:
				#return API error for no userID given
				return

		elif(func == "joinGame"):
			userID = self.getValue("userID")
			if(not userID == None):
				gameID = self.getValue("gameID")
				if(not gameID == None):
					password = self.getValue("password")
					if(not password == None):
						joinGame = games[int(gameID)]
						if(joinGame.password == password):
							if(len(joinGame.users) < joinGame.maxUsers):
								joinGame.users.append(userID)
								dict = {"gameID":gameID, "password":password, "users:":joinGame.users}
								self.writeJSON(dict)
								return
							else:
								#return API error for game full
								return
						else:
							#return API error for password incorrect
							return
					else:
						#return API error for no password given
						return
				else:
					#return API error for no gameID given
					return 
			else:
				#return API error for no userID given
				return 
		elif(func == "findGame"):
			userID = self.getValue("userID")
			if(not userID == None):
				for findGame in games:
					if(len(findGame.users) < findGame.maxUsers and findGame.password == "-1"):
						findGame.users.append(userID)
						dict = {"gameID":findGame.gameID, "password":findGame.password, "users:":findGame.users}
						self.writeJSON(dict)
						return
				#return API error for no games found
				return
			else:
				#return API error for no userID given
				return






		else:
			#return API error for not a valid function
			return

		

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
	