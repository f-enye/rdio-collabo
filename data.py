import json

def newPlaylist(name):
    raw_json = open('static/data.json')
    data = json.load(raw_json)
    data["playlists"].append({"name": name})

    raw_json = open('static/data.json', 'w')
    raw_json.write(json.dumps(data, sort_keys=True, indent=2))
    raw_json.close()

def nearby():
    raw_json = open('static/data.json')
    data = json.load(raw_json)
    raw_json.close()  

    return json.dumps(data, sort_keys=True, indent=2)
