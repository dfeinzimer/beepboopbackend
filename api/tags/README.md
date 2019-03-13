## Create new tag
URL = "tag/new"
Content-Type = "application/json"
Method = "POST"
Basic-Auth Required: YES

Request data format:
    {
        "tag": "",
        "url": "",
        "email": "",
        "password": ""
    }

    email            - Email used for login               (MANDATORY)
    password         - Current password used to login     (MANDATORY)

    Status-Code:    201
    Content-type:   application/json
Response data:
    Empty list - []

## Delete post
URL = "/tags/delete/<url>"
Content-Type = "application/json"
Method = "DELETE"
Basic-Auth Required: YES

Request data format:
    {
        "email": "",
        "password": ""
    }

    email            - Email used for login               (MANDATORY)
    password         - Current password used to login     (MANDATORY)

Response header(s):
    Status-Code:    201
    Content-type:   application/json

Response data:
    Empty list - []
