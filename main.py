import winreg
from urllib import request
import re
import json
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_steam_path():
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(registry_key, "SteamPath")
        return steam_path
    except:
        return 0

res = open(get_steam_path() + "/steamapps/libraryfolders.vdf").read()
rawgGameIds = re.findall(r"[\"]\d{0,}[\"]\t\t", res)
gameIds = []

print(f"""{bcolors.WARNING}
Platinum: Runs perfectly out of the box. 
Gold: Runs perfectly after some tweaks or configuration. 
Silver: Runs with minor issues, but generally playable. 
Bronze: Runs, but often has crashes or other issues that make it uncomfortable to play. 
Borked: The game either won't start or has crucial issues that make it unplayable. 
Native: The game is a native Linux title and doesn't require Proton. 
{bcolors.ENDC}""")

open('steam_proton_checker.txt', 'w').close()
for game in rawgGameIds:
    gameIds.append(game.strip('"\t'))
for gameId in gameIds:
    f = open("steam_proton_checker.txt", "a", encoding="utf-8")
    try:
        gameApi = json.loads(request.urlopen(f"https://store.steampowered.com/api/appdetails?appids={gameId}").read())
        gameName = gameApi[gameId]['data']['name']
        print(f"{bcolors.BOLD + bcolors.HEADER + gameName + bcolors.ENDC}")
        f.write(gameName + "\n")
    except:
        print(f"{bcolors.FAIL}Cannot parse game name! - GameId: {gameId}{bcolors.ENDC}")
        f.write(f"Cannot parse game name! - GameId: {gameId}\n")
    try:
        protonJson = json.loads(request.urlopen(f"https://www.protondb.com/api/v1/reports/summaries/{gameId}.json").read())
        print(f"{bcolors.OKCYAN}gameId: {bcolors.ENDC}{bcolors.BOLD + gameId + bcolors.ENDC}")
        for key, value in reversed(list(protonJson.items())):
            print(f"{bcolors.OKCYAN + key + bcolors.ENDC}: {bcolors.BOLD + str(value) + bcolors.ENDC}")
            f.write(f"\t{key}: {str(value)}\n")
        print(f"https://www.protondb.com/app/{gameId}\n")
        f.write(f"https://www.protondb.com/app/{gameId}\n\n")
    except:
        print(f"{bcolors.FAIL}Cannot parse review!{bcolors.ENDC}\n")
        f.write("Cannot parse review!\n\n")
    f.close()