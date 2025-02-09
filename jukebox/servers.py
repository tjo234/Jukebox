#!/usr/bin/env
import json
from time import sleep
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

JSON_PATH = "servers.json"
MPD_PATH = "_mpd._tcp.local."
zeroconf = Zeroconf()

def load_servers():
    print("Loading Jukebox Servers from JSON....")
    try:
        with open(JSON_PATH, 'r') as f:
            return json.load(f)
    except:
        return {
            "last_used": "",
            "discovered": []
        }

def listen_for_servers():
    listener = JukeboxServerListener()
    browser = ServiceBrowser(zeroconf, MPD_PATH, listener)

class JukeboxServerListener(ServiceListener):
    '''
    Listens for MDP servers and adds them to a local JSON file. 
    '''
    def __init__(self):
        self.servers = load_servers()

    def save_json(self):
        with open(JSON_PATH, 'w') as f:
            json.dump(self.servers, f)
            print(f"server.json - SAVED")

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        #print(f"Service - {name} updated")
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        #print(f"Service - {name} removed")
        pass
        
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info and info.server:
            server = info.server.rstrip('.') # Remove closing '.'
            if server not in self.servers['discovered']:
                self.servers['discovered'].append(server)
                self.save_json()
            print(f"Server - {server} added")

if __name__ == "__main__":
    listen_for_servers()
    try:
        input("Press enter to exit...\n")
    finally:
        zeroconf.close()