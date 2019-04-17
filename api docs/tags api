## Add tag to url
    URL = "http://localhost/tags"
    Content-Type = "application/json"
    Method = "POST"
    Basic-Auth Required: YES

    Request data format:
        {
            "tag": "",
            "url": ""
        }

        tag            - article tag               (MANDATORY)
        url            - corresponding url         (MANDATORY)

        Status-Code:    201
        Content-type:   application/json
    Response data:
        Empty list - []

##TODO
## Delete tag from a specific URL
    URL = "http://localhost/tags"
    Content-Type = "application/json"
    Method = "DELETE"
    Basic-Auth Required: YES

    Request data format:
        {
            "tag": "",
            "url": ""
        }
    
    tag is a plain string: ex "apples"
    url is the articlue url: ex "articles/1"

    Response header(s):
        Status-Code:    201
        Content-type:   application/json

    Response data:
        Empty list - []


## Get tag by URL
    URL = "http://localhost/tags/url/<article_url>"
    Content-Type = "application/json"
    Method = "GET"
    Basic-Auth Required: YES

    <article_url> in format of articles=<article_id>
    ex: /tags/url/articles=1

    Response header(s):
        Status-Code:    201
        Content-type:   application/json

    Response data:
        [
            {
                "tag": "",
                "url": "",
                "tag_id": ""
            }
        ]


## Get URLs by tag
    URL = "http://localhost/tags/tag/<tag>"
    Content-Type = "application/json"
    Method = "GET"
    Basic-Auth Required: YES

    <tag> is the string tag
    ex: /tags/tag/apples

    Response header(s):
        Status-Code:    201
        Content-type:   application/json

    Response data:
        [
            {
                "tag": "",
                "url": "",
                "tag_id": ""
            },
            ...
        ]

