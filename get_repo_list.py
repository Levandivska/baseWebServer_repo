from flask import abort
import requests
import json
import logging


def get_current_dct():
    info_dct = {"name": None, "html_url": None, "description": None, "private": None,
                "created_at": None, "watchers": None}
    return info_dct


def repo_info(url):
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        logging.error('No connection')
        abort(204)

    except requests.exceptions.MissingSchema:
        logging.error('No connection')
        abort(404)

    Jresponse = uResponse.text

    try:
        data = json.loads(Jresponse)
    except json.decoder.JSONDecodeError:
        logging.error('Data not found')
        abort(404)

    result = []
    try:
        for repo in data:
            repo_info_dct = get_current_dct()
            repo_info_dct["name"] = repo["name"]
            repo_info_dct["html_url"] = repo["html_url"]
            repo_info_dct["description"] = repo["description"]
            repo_info_dct["private"] = repo["private"]
            repo_info_dct["created_at"] = repo["created_at"].replace("T"," ").replace("Z"," ")
            repo_info_dct["watchers"] = repo["watchers"]
            result.append(repo_info_dct)
    except TypeError:
        logging.error('Error, Not correct json data')
        abort(404)

    return result

