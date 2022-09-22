import uuid, json, random, string, re, time
from request_exception import request_failure

def token_request_success(code, token):
    return {
        "status": 0,
        "code": code,
        "token": token
    }

class TokenRequest:
    def __init__(self, request: dict):
        self.request = request
        self.necessary_headers = ["uuid", "email", "source", "sent"]
        for a in request:
            if a in self.necessary_headers:
                self.necessary_headers.remove(a)

    def get(self):
        b = json.load(open("data/auth_token.json", "r+"))
        count = 0

        #token expiring
        if self.request['uuid'] in b:
            for a2 in b[self.request['uuid']]:
                if int(time.time()) > (int(a2['signature']) + (5*60)):
                    b[self.request['uuid']].pop(count)
                count += 1

        #No need to remind
        #regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        #if not re.fullmatch(regex, self.request['email']):
        #    return request_failure(400, "Invalid email format")
        if self.request['source'] not in ['app', 'web']:
            return request_failure(403, "Invalid client")
        a = json.load(open("data/uuid.json", "r+"))
        if self.request['email'] not in a:
            return request_failure(403, "Forbidden request")
        if self.request['uuid'] != a[self.request['email']]:
            return request_failure(403, "Forbidden request")
        if len(self.necessary_headers) != 0:
            return request_failure(400, "Insufficient headers")

        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        if self.request['uuid'] not in b:
            b[self.request['uuid']] = []
        b[self.request['uuid']].append({
            "token": token,
            "signature": time.time()
        })
        json.dump(b, open("data/auth_token.json", "w"), indent=4)
        return token_request_success(200, token)