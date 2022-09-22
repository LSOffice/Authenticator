def request_failure(code, error):
    return {
        "status": 1,
        "code": code,
        "error": error
    }
