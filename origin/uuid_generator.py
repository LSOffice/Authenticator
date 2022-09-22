import uuid, json, random, string, re
from request_exception import request_failure

def uuid_request_success(code, uuid):
    return {
        "status": 0,
        "code": code,
        "uuid": uuid
    }

class UuidRequest:
    def __init__(self, request: dict):
        self.necessary_headers = ["email", "source", "sent"]
        self.request = request
        for a in request:
            if a in self.necessary_headers:
                self.necessary_headers.remove(a)

    def get(self):
        if self.request['source'] not in ['app', 'web']:
            return request_failure(403, "Invalid client")
        if len(self.necessary_headers) != 0:
            return request_failure(400, "Insufficient headers")

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, self.request['email']):
            return request_failure(400, "Invalid email")
        a = json.load(open("data/uuid.json", "r+"))
        if self.request['email'] in a:
            return request_failure(403, "UUID already registered with email")
        uuid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        a[self.request['email']] = uuid
        json.dump(a, open("data/uuid.json", "w"), indent=4)

        return uuid_request_success(200, uuid)