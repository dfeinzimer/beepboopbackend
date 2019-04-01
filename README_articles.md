# Articles API Usage

## Post article
    URL = "/articles/new"
    Content-Type = "application/json"
    Method = "POST"
    Basic-Auth Required: YES

    Request data format:
        {
            "title": "",
            "headline": "",
            "content": "",
            "author": "",
            "article_date": ""
        }
        title        - Title of the article            (MANDATORY)
        headline     - Article headline                (OPTIONAL, LEAVE VALUE BLANK IF UNUSED)
        content      - Main text/body of the article   (MANDATORY)
        author       - Name of author                  (MANDATORY)
        article_date - Date of article MM/DD/YYYY      (MANDATORY)

    Response header(s):
        Status-Code:    201
        Content-type:   application/json 
        Location:       Will contain the URL to the newly created article

    Response data:
        Empty list - []


## Get article
    URL = "/articles/<ARTICLE_ID>"
    Content-Type = "application/json"
    Method = "GET"
    Basic-Auth Required: NO

    Response header(s):
        Status-Code:    200
        Content-type:   application/json 

    Response data:
        [
            {
                "title": "",
                "headline": "",
                "content": "",
                "author": "",
                "article_date": "",
                "last_modified": ""
            }
        ]


## Modify article
    URL = "/articles/<ARTICLE_ID>"
    Content-Type = "application/json"
    Method = "PATCH"
    Basic-Auth Required: YES

    Request data format:
        {
            "title": "",
            "headline": "",
            "content": "",
            "author": "",
            "article_date": ""
        }

        title        - Title of the article            (OPTIONAL)
        headline     - Article headline                (OPTIONAL)
        content      - Main text/body of the article   (OPTIONAL)
        author       - Name of author                  (OPTIONAL)
        article_date - Date of article MM/DD/YYYY      (OPTIONAL)

    Response header(s):
        Status-Code:    200
        Content-type:   application/json 

    Response data:
        Empty list - []


## Delete article
    URL = "/articles/<ARTICLE_ID>"
    Content-Type = "application/json"
    Method = "DELETE"
    Basic-Auth Required: YES

    Response header(s):
        Status-Code:    200
        Content-type:   application/json 

    Response data:
        Empty list - []


## Get n most recent articles
    URL = "/articles/recent/<n>"
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
                "title": "",
                "headline": "",
                "content": "",
                "author": "",
                "article_date": "",
                "last_modified": ""
            }, 
            ...
        ]


## Get the meta-data for n most recent articles
    URL = "/articles/recent/meta/<n>"
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
                "title": "",
                "author": "",
                "article_date": "",
                "location": "",
                "article_id": ""
            }, 
            ...
        ]