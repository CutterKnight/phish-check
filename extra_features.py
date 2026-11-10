"""Extra URL features written by the student (this file is the student's own work).

extra(url, parts) is called for every address, both when training the model and when checking
a URL on the website. It must return a dict {feature name: number}. The names must be new
(different from the ones in urlfeatures.py) and the values must be numbers (True/False also work).

url   = the full address as text, for example "http://paypal.com.login.example.ru/a?x=1"
parts = the same address split by Python's urlsplit: parts.scheme, parts.hostname,
        parts.path, parts.query ...

Example of the shape of a feature (not active):
    "underscores_in_url": url.count("g"),
"""


def extra(url, parts):
    features = {}
    features ["UnderScores"]= url.count('_')
    features ["has_php"]= "php" in url.lower()
    features ["Path_segments"]= url.split('/').count('_') + 1
    return features
