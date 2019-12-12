from flask import Flask, jsonify
import psycopg2
from get_repo_list import *
import sys

database = sys.argv[1]
password = sys.argv[2]


def get_url_by_name(name):
    return "https://api.github.com/orgs/{}/repos".format(name)


def db(database, password):
    conn = psycopg2.connect(host="localhost", database=database, password=password)
    return conn


app = Flask(__name__)


@app.route('/<name>', methods=['GET'])
def get_repos_info(name):

    repos = repo_info(get_url_by_name(name))

    global database
    global password
    res = []
    try:
        conn = db(database, password)
        cursor = conn.cursor()
        for repo in repos:
            cursor.execute(
            "INSERT INTO repo_info (username, name, html_url, description, private, created_at, watchers) SELECT %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS(SELECT 1 FROM repo_info where name = %s)",
            (name, repo["name"], repo["html_url"], repo["description"], repo["private"], repo["created_at"], repo["watchers"],repo["name"] ))

            cursor.execute("SELECT id FROM repo_info WHERE name = %s",(repo["name"], ) )
            id_info = cursor.fetchall()
            res.append({"repo_name": repo["name"], "repo_id": id_info[0][0]})
        conn.commit()

    except psycopg2.Error as error:
        logging.error(error)
        raise

    finally:
        conn.close()
        cursor.close()
    return jsonify(res), 201


if __name__ == '__main__':
    app.run(debug=True)