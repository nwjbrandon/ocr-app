def get_params(event):
    if "name" not in event:
        return {"status_code": 422, "error": "The field name is missing"}
    if "file" not in event:
        return {"status_code": 422, "error": "The field file is missing"}
    return event["name"], event["file"]
