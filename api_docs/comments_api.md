## Post a comment
    URL = "http://localhost/comments"
    Content-Type = "application/json"
    Method = "POST"
    Basic-Auth Required: YES

    Request data format:
        {
            "user_display_name": "",
            "comment": "",
            "article_url": ""
        }
        article_url in format: "articles/<article_id>"

        Status-Code:    201
        Content-type:   application/json


    Response data:
        Empty list - []


## Delete comment
    URL = "http://localhost/comments/<comment_ID>"
    Content-Type = "application/json"
    Method = "DELETE"
    Basic-Auth Required: YES

    Response header(s):
        Status-Code:    201
        Content-type:   application/json

    Response data:
        Empty list - []


##Get comment count on a article
    URL = "http://localhost/comments/count/<article_url>
    Content-Type = "application/json"
    Method = "GET"
    Basic-Auth Required: YES

    <article_url> in format of articles=<article_id>
    ex: /comments/count/articles=1

    Response header(s):
        Status-Code:    200
        Content-type:   application/json 

    Response data:
        Response data:
        [
            {
                "count": ""
            }
        ]


## Get n most recent comments on article
    URL = "http://localhost/comments/<n>/<article_url>
    Content-Type = "application/json"
    Method = "GET"
    Basic-Auth Required: YES

    <n> is the number of most recent articles to retrieve
    <article_url> in format of articles=<article_id>
    ex: /comments/n/articles=1

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
                "user_display_name": "",
                "article_url": ""
            }, 
            ...
        ]
    
    
    