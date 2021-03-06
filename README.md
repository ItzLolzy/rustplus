![Rust+.py](https://github.com/olijeffers0n/rustplus/blob/main/icon.png?raw=true)

<p align="center">
<a href="https://pypi.org/project/rustplus/"><img src="https://img.shields.io/pypi/v/rustplus?style=plastic" alt="pypi"/></a>
</p>

A lot of code and ideas have come from the JavaScript version of a wrapper, so I will credit him now:
[Liam Cottle's RustPlus.js](https://github.com/liamcottle/rustplus.js)
I have used his Protocol Buffer file for this, as well as instructions on how to use his command line tool to get the information you need.

## Installation:
Install the package with:
```
pip install rustplus
```
It should also install all the dependencies, but if not you will have to install them yourself

## Usage:
```py
from  rustplus  import  RustSocket

rust_socket = RustSocket("IPADDRESS", "PORT", 64BITSTEAMID, PLAYERTOKEN)
#See below for more information on the above ^^

#Connects to the server's websocket
rust_socket.connect()

"""
For information on the following see below
"""
#Get mapMarkers:
markers = rust_socket.getMarkers()

#Get Server Info:
info = rust_socket.getInfo()

#Get Current time:
time = rust_socket.getTime()

#Getting Team info
team_info = rust_socket.getTeamInfo()

#Getting Team Chat:
team_chat = rust_socket.getTeamChat()

#Sending a Team Chat message:
status = rust_socket.sendTeamMessage("Yo! I sent this with Rust+.py")

#Get Camera Image:
camera_image = rust_socket.getCameraFrame("CAMID",FRAMENO)

#Get Map Image:
rust_map = rust_socket.getMap(addIcons = True)

#Get Entity Information
entity_info = rust_socket.getEntityInfo(ENTITYID)

#Turning On/Off a Smart Switch
rust_socket.turnOffSmartSwitch(ENTITYID)
rust_socket.turnOnSmartSwitch(ENTITYID)

rust_socket.closeConnection()
```
### Information on Usage:
##### Initialising a `RustSocket`:
```py
rust_socket = RustSocket("IPADDRESS",  "PORT", 64BITSTEAMID, PLAYERTOKEN)
```
Simply creates the `RustSocket` object, however it does not actually ping the server, or have any actions in any way. To connect to the server you must call:
```py
rust_socket.connect()
```
Which will ping the server and open the connection.

##### Getting the map:
```py
rustMap = rust_socket.getMap(addIcons = bool)
```
This returns an image which the module has formatted with the images of each monument after it has parsed the bytes. If you do not want the icons, and instead just want the empty map, add the parameter `addIcons = False`. If you want to save the image file, just call `rustMap.save("name.png")` which will save it to the current directory. You can also call `rustMap.show()` which will open the map as a picture file.

##### Getting server Info:
```py
info = rust_socket.getInfo()
```
This method returns a dictionary with the following data:
```
{
	'url': Server URL - String, 
	'name': Server Name - String, 
	'map': Map Type - String, 
	'size': Map Size - Integer, 
	'currentPlayers': CurrentPlayers - Integer, 
	'maxPlayers': MaxPlayers - Integer, 
	'queuedPlayers': QueuedPlayers - Integer, 
	'seed': Map Seed - Integer
}
```
##### Getting server time:
```py
time = rust_socket.getTime()
```
The method returns a string of the current time, in the format `"HOURS:MINUTES"` in 24Hr format. The method has already parsed the raw data to a human-readable string.
##### Getting the Team Chat
```py
team_chat = rust_socket.getTeamChat()
```
This returns an iterable list of `ChatMessage` objects, with the entries:

 - SteamID
 - SenderName
 - Message
 - Colour
 
So, you could print out the messages like this:
```py
for message in team_chat:
	print(message.message)
```
##### Sending a message to the Team Chat:
```py
status = rust_socket.sendTeamMessage("Yo! I sent this with Rust+.py")
```
This method returns a status, however this can be ignored if you would like. The message will be sent as if you are sending it.
##### Getting team info:
```py
team_info = rust_socket.getTeamInfo()
```
This returns a list of the players in your team, as well as a lot of data about them such as: `x`,`y`,`dead`,`online`,`name` etc etc
##### Getting a camera frame:
```py
cam_picture = rust_socket.getCameraFrame("CAMID",FRAMENO)
```
Returns a very low resolution image from the camera. There are some caveats:
 - A player must be near the camera for it to work
 - This is disabled on servers by default. An admin must run the convar: `cctvrender.enabled true` in console to enable it
 - The image returned often looks terrible

The codes of cameras can be found [here](https://www.corrosionhour.com/rust-cctv-camera-codes-list/)

##### Getting Entity Information:
```py
entity_info = rust_socket.getEntityInfo(ENTITYID)
```
Returns some information on the entity you provided. See __below__ on how to get the Entity ID
Works on many entities like Smart Switches and Storage Monitors

##### Turning On/Off a Smart Switch:
```py
rust_socket.turnOffSmartSwitch(ENTITYID)
rust_socket.turnOnSmartSwitch(ENTITYID)
```
Both return some data on the action fullfilled. See __below__ on how to get the Entity ID

##### Closing the connection:
```py
rust_socket.closeConnection()
```
This can be called in order to close the websocket, however it does not destroy the object you made. This means that you can close and reopen the websocket effectively infinitely.

### Getting the Entity ID
- If you are an Admin:
The Entity ID Can be obtained by looking at the entity in game and typing `entity.debug_lookat` into the `F1` console . This will display the entity ID on the screen. 
Please Note:  the Entity ID is the numbers at the beginning

- If you are not an Admin:
You can use the tool that [Liam Cottle](https://github.com/liamcottle/rustplus.js#using-the-command-line-tool) has made. 
 1. Run `npx @liamcottle/rustplus.js fcm-register` (If it is the first Time)
	Note: You must have Google Chrome installed to use `fcm-register`
 2. You will be prompted to log into your steam account via the facepunch website
 3. Run `npx @liamcottle/rustplus.js fcm-listen`
 4. Leave this window open, then go onto the server you would like information for and send a pairing notification from in-game. You should get a response like this:
	```
	{
	  img: '',
	  entityType: '',
	  ip: 'ServerIP',
	  entityId: 'EntityID',         <--- Entity ID
	  type: 'EntityType',
	  url: 'ServerURL',
	  playerToken: 'PlayerToken',
	  port: 'port',
	  entityName: 'EntityName',
	  name: 'Name',
	  logo: '',
	  id: '',
	  desc: 'Description',
	  playerId: 'PlayerID'
	}
	```
You can see the Entity ID Here

### Getting Your Steam ID and PlayerToken:
This is where it gets a bit finnicky. The Steam ID is unique to your steam account, so can be used for any server you connect to. However, the `PlayerToken` is unique to each server. There are two ways to get this data:

#### As a server Admin / Owner:
You can go to the server files where you will find a database called `player.tokens.db` containing all of these codes. You can use a tool such as [this](https://sqlitebrowser.org/) to get the codes, or access them programmatically.
#### As a player.
You can use the tool that [Liam Cottle](https://github.com/liamcottle/rustplus.js#using-the-command-line-tool) made to get the Player Token When you pair a server. This also gives you the IP address and the port. You must have `npm` installed and run this, which is annoying, however his tool is very effective:

 1. Run `npx @liamcottle/rustplus.js fcm-register` (If it is the first Time)
	Note: You must have Google Chrome installed to use `fcm-register`
 2. You will be prompted to log into your steam account via the facepunch website
 3. Run `npx @liamcottle/rustplus.js fcm-listen`
 4. Leave this window open, then go onto the server you would like information for and send a pairing notification from in-game. You should get a response like this:
	```
	{
	  img: '',
	  port: 'port',                       <-----Server Port
	  ip: 'your-server-ip',               <-----Server IP
	  name: "your-server-name",
	  id: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
	  type: 'server',
	  url: '',
	  desc: 'your-server-description',
	  playerId: 'your-steam-id',          <-----Steam ID
	  playerToken: 'your-player-token'    <-----Player Token
	}
	```
	
 5. You can then use these details in the Python Wrapper here:
	 ```py
	 rust_socket = RustSocket("IPADDRESS",  "PORT", 64BITSTEAMID, PLAYERTOKEN)
	 ```
### Rate Limiting 
The server uses a '[Token Bucket](https://en.wikipedia.org/wiki/Token_bucket)' approach meaning that you should be careful how many requests you send, however if you are sensible, this should be a non-issue...

You get:
`50 tokens max per IP address with 15 replenished per second`
`25 tokens max per PlayerID with 3 replenished per second`

And these are the costs:
```
Info : 1
Map : 5
Camera Frame: 2
Map Markers : 1
Time : 1
SendTeamChat : 2
GetTeamInfo : 1
EntityInfo: 1
SetEntityValue: 1
```

### Support:
If you need help, or you think that there is an issue feel free to open an issue. If you think you have made some improvements, open a PR! 

I have tried to explain this a well as possible, but if you should need further clarification, as i said open an issue. If not: `Ollie#0175` on discord

There is more data that can be accessed with this API, such as the following:
- Setting Team Leader

I may add some of this functionality soon, depends on the interest :-)

Have Fun! 
