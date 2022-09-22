keys = {
    "uuid": 0,
    "email": 1
}

def get_setting(key):
    if key not in keys:
        return {"success": False, "code": 0}

    a = open("data/settings.txt", "r+").readlines()
    data = {}
    count = 0
    for a2 in a:
        changeda2 = a2.replace("\n", "")
        prefix = changeda2[:changeda2.index(":")]
        suffix = changeda2[changeda2.index(":")+2:]
        data[prefix] = suffix

        count += 1

    for key1 in keys:
        if not key1 in data: return {"success": False, "code": 1}

    if data[key] == "": return {"success": False, "code": 2}

    return {"success": True, "data": data[key]}

def set_setting(key, setting):
    if key not in keys:
        return {"success": False, "code": 0}

    a = open("data/settings.txt", "r+").readlines()
    data = {}
    count = 0
    for a2 in a:
        changeda2 = a2.replace("\n", "")
        prefix = changeda2[:changeda2.index(":")]
        suffix = changeda2[changeda2.index(":")+2:]
        data[prefix] = suffix

        count += 1

    for key1 in keys:
        if not key1 in data: return {"success": False, "code": 1}

    if setting == "": return {"success": False, "code": 2}

    data[key] = setting

    string = ""
    for d in data:
        string += f"{d}: {data[d]}\n"

    open("data/settings.txt", "w").write(string)
    return {"success": True}
