from flask import Flask, request
import logging
import os
import json

import elastic.elastic
import elasticsearch.exceptions

app = Flask(__name__)


def make_response(inf, code):
    return json.dumps({"data": inf, "code": code})


@app.route("/")
def root():
    return "You shall not pass!\n少女前线天下第一"


@app.route("/search")
def search():
    if True:  # try:
        args = request.args
        index = "project_for_search_engine"
        doc_type = "data"

        if "size" in args:
            size = int(args["size"])
        else:
            size = 10

        if "from" in args:
            from_ = int(args["from"])
        else:
            from_ = 0

        where = "content"
        if "where" in args:
            where = args["where"]

        arr = []
        if "query" in args.keys():
            q = args["query"]
        else:
            q = ""

        '''
        if "gte" in args.keys():
            gte = args["gte"]
        else:
            gte = "1926-08-17"
        if "lte" in args.keys():
            lte = args["lte"]
        else:
            lte = "2026-08-17"
        '''

        body = {
            "query": {
                "function_score":{
                    "query":{
                        "bool": {
                            "should": [
                                {
                                    "match": {
                                        "title":{
                                            "query": q,
                                            "boost": 3
                                        }
                                    }
                                },
                                {
                                    "match":{
                                        "content":{
                                            "query": q
                                        }
                                    }
                                }
                            ]
                        }
                    },
            
                "field_value_factor":{
                    "field": "pageRank",
                    "factor": 0.3
                },
                "boost_mode": "sum",
                }
            }

        }
        try:
            result = elastic.elastic.search(index, doc_type, body, size=size, from_=from_)
        except elasticsearch.exceptions.ConnectionTimeout:
            return make_response("timeout", 1)

        arr = []
        for item in result["hits"]["hits"]:
            arr.append(item)

        return make_response(arr, 0)
    # except Exception as e:
    #    return make_response(str(e), -1)


@app.route("/doc")
def fetch_doc():
    try:
        args = request.args
        index = "law"
        doc_type = "data"
        if not ("id" in args):
            return make_response("id is needed", 1)

        if "timeout" in args:
            timeout = int(args["timeout"])
        else:
            timeout = 30

        try:
            return make_response(
                elastic.elastic.fetch_doc(args["index"], args["doc_type"], args["id"], timeout)["_source"], 0)
        except elasticsearch.exceptions.NotFoundError:
            return make_response("not found", 2)
        except elasticsearch.exceptions.ConnectionTimeout:
            return make_response("timeout", 3)
    except Exception as e:
        return make_response(str(e), -1)


if __name__ == "__main__":
    app.run(host="166.111.5.246", port=20086, debug=True, threaded=True)
