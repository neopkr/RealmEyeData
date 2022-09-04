from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

MAIN = 'neopkr'

class RealmEyeDir:
    PLAYER = "https://www.realmeye.com/player/"
    GRAVEYARD = "https://www.realmeye.com/graveyard-of-player/"
    EXALTATIONS = "https://www.realmeye.com/exaltations-of/"
    PETS = "https://www.realmeye.com/pets-of/"
    HISTORY = {
        "Fame": "https://www.realmeye.com/fame-history-of-player/",
        "Rank": "https://www.realmeye.com/rank-history-of-player/",
        "Name": "https://www.realmeye.com/name-history-of-player/",
        "Guild": "https://www.realmeye.com/guild-history-of-player/"
    }
dir = RealmEyeDir()

# Main Reqs

def getRequestAllText(playerIGN) -> str:
    pUrl = f"https://www.realmeye.com/player/{playerIGN}"
    req = Request(pUrl, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    return soup.get_text()
def getRequestList(playerIGN):
    pUrl = f"https://www.realmeye.com/player/{playerIGN}"
    req = Request(pUrl, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return str(BeautifulSoup(page, "html.parser"))
def getSoup(playerIGN):
    pUrl = f"https://www.realmeye.com/player/{playerIGN}"
    req = Request(pUrl, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    return BeautifulSoup(page, "html.parser")

servers = ["USWest", "USWest3", "USWest4", "USSouthWest", "USSouth3", "USSouth", "USNorthWest", "USMidWest2", "USMidWest", "USEast", "USEast2", "EUWest2", "EUWest", "EUSouthWest", "EUNorth", "EUEast", "Australia", "Asia"]
ouputFileError = {
    'playerNotFound': 'Sorry, the player you entered does not exist or is not registered in RealmEye, please try again.',
    'QueryError': "Sorry... the query was not successful. You can send this error to the repository to fix it as quickly as possible: https://github.com/neopkr/RealmEyeData/issues"
}

# Http Req Info
def getRealmEyeData(ign):
    main = getRequestAllText(ign)
    try:
        guild = main.split("Rank")[2].split(" ")[2].split("Guild")[1]
        guildLevel = main.split("Rank")[3].split(" ")[0]
        if guildLevel.find("Initiate") != -1:
            guildLevel = "Initiate"
        elif guildLevel.find("Member") != -1:
            guildLevel = "Member"
        elif guildLevel.find("Officer") != -1:
            guildLevel = "Officer"
        elif guildLevel.find("Leader") != -1:
            guildLevel = "Leader"
        elif guildLevel.find("Founder") != -1:
            guildLevel = "Founder"
    except:
        guild = "None"
        guildLevel = "None"
    try:
        player = main.split(" ")[5]
        charAlive = main.split(ign)[2].split(" ")[0].replace("Characters", "").split("Skins")[0]
        skins = main.split("Skins")[1].split(" ")[0]
        exalt = main.split("Exaltations")[3].split(" ")[0].split("Fame")[0]
        rank = main.split("Rank")[2].split(" ")[0].replace("Account", "")
    except IndexError:
        return ouputFileError["QueryError"]
    last = main.split("Last")[1].split(" ")
    FoundServer = []
    for i in range(len(last)):
        if last[i] in servers:
            FoundServer.append(last[i])
    try:
        return player, charAlive, skins, exalt, rank, [guild, guildLevel], FoundServer[0]
    except IndexError: 
        return player, charAlive, skins, exalt, rank, [guild, guildLevel], 'Hidden'


# GetCharacters
def getCharacters(ign):
    ls = getRequestList(ign).split(" ") # list
    classes = []
    filter = "</td><td>"
    id = []
    for e in getSoup(ign).find_all(class_ = "character"):
        classes.extend(e['class'])
        id.extend(e['id'])
    # id.index : 0 - ?, 0 = first char . . . last char
    charList = []
    fixList = []
    for i in range(len(id)):
        charList.append(ls[ls.index(f'id="{id[i]}"') + 3].split(filter)) # FIX HERE, View test (Fixed 4:49AM)
    for i in range(len(charList)):
        if charList[i][-1] == "<a":
            # search item and change it for the right one
            for e in range(len(id)):
                fixList.append(ls[ls.index(f'id="{id[e]}"') + 4].split(">")[1].replace("</a", ""))
            item = fixList[i]
            charList[i][6] = item
            charList[i].pop(0)
            charList[i].pop(2)
        else:
            charList[i].pop(0)
            charList[i].pop(-1)
            charList[i].pop(2)
    itemClassParser = []
    for i in getSoup(ign).find_all(class_ = "item"):
        itemClassParser.append(i)
    itemParser = []
    itemList = []
    for i in range(len(itemClassParser)):
        itemParser.append(str(itemClassParser[i]).split("title"))
    for i in range(len(itemParser)):
        itemList.append(str(itemParser[i][1]).replace("></span>", "").replace('"', "").replace("=", ""))
    # Fill list
    for i in range(len(charList)):
        for e in range(0, 4):
            charList[i].append(itemList[e])
        itemList.pop(0)
        itemList.pop(0)
        itemList.pop(0)
        itemList.pop(0)
    return charList

class ReadHistory:
    def fame(self):
        print(dir.HISTORY['fame'])
# igm, alive, skins, exalt, rank
#   1,     2,     3,     4,    5

def ReturnRealmEyeData(MASTER, char):
    if MASTER == ouputFileError["QueryError"]:
        return ouputFileError["QueryError"]
    base = {
        "player": MASTER[0],
        "skins": MASTER[2],
        "aliveCharacters": MASTER[1],
        "exaltations": MASTER[3],
        "rank": MASTER[4],
        "guild": f"{MASTER[5][0]}, {MASTER[5][1]}",
        'lastSeen': MASTER[6],
        "characters": {

        }
    }
    for a in range(len(char)):
        base["characters"][a] = {
            "class": char[a][0],
            "level": char[a][1],
            "basefame": char[a][2],
            "experience": char[a][3],
            "placement": char[a][4],
            "items": {
                "weapon": char[a][5],
                "ability": char[a][6],
                "armor": char[a][7],
                "ring": char[a][8]
            },
        }
    return base
