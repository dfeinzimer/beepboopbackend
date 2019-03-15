## Post a comment

    URL = "comments/post"

    Content-Type = "application/json"

    Method = "POST"
    Basic-Auth Required: NO

    Request data format:
        {
            "user_id": "",
            "comment": "",
        }
        Status-Code:    201
        Content-type:   application/json
    Response data:
        Empty list - []


## Delete comment
    URL = "/comments/delete/<int:comment_ID>"
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

## Get nth comment
    URL = "/comments/nth_comment/<int:nth>
    Content-Type = "application/json"
    Method = "GET"
    Basic-Auth Required: NO

    Response header(s):
        Status-Code:    200
        Content-type:   application/json 

    Response data:
        Response data:
        [
            {
                "comment": "",
                "comment_data": "",
                "comment_id": "",
                "user_id": ""
            }, 
            ...
        ]
    
    
    
