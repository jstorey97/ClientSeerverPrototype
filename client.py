import requests
import json

URL = "http://127.0.0.1:8080"
PARAMS = {"function":"newPlayer", "name":"james"}

def request(dict):
	r = requests.get(url = URL, params = dict)
	try:
		return r.json()
	except ValueError:
		return {}

def requestUserID(name):		
	dict = {"func":"requestUserID", "name":name}
	return request(dict)

def createGame(userID, password = -1):
	dict = {"func":"createGame", "userID":userID, "password":password}
	return request(dict)

def joinGame(userID, gameID, password = -1):
	dict = {"func":"joinGame", "userID":userID, "gameID":gameID, "password":password}
	return request(dict)

def findGame(userID):
	dict = {"func":"findGame", "userID":userID}
	return request(dict)

'''
Client 1 connects
Client 2 connects
Client 1 creates game
Client 2 joins game
'''

userID1 = requestUserID("James")["userID"]
print("Recieved User ID:", userID1, "for client 1")

userID2 = requestUserID("Cameron")["userID"]
print("Recieved User ID:", userID2, "for client 2")

userID3 = requestUserID("Ava")["userID"]
print("Recieved User ID:", userID3, "for client 3")

gameCreate = createGame(userID1)
gameID1 = gameCreate["gameID"]
password1 = gameCreate["password"]
print("Client 1 created game with ID:", gameID1, "and password", password1)

gameJoin = joinGame(userID2, gameID1, password1)
gameID2 = gameJoin["gameID"]
password2 = gameJoin["password"]
print("Client 2 joined game with ID:", gameID2, "and password", password2)

gameFind = findGame(userID3)
gameID3 = gameFind["gameID"]
password3 = gameFind["password"]
print("Client 3 found game with ID:", gameID3, "and password", password3)