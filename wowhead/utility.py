import uuid
import json
from db import get_db

def get_new_token():
    #return str(uuid.uuid4())
    return "76add84-d749-4faa-896a-fda7b050978d"

def get_data_list():
    db = get_db()
    data_qry = db.execute(
        "SELECT id, author_id, created, data from post ORDER BY created ASC"
    ).fetchall()
    data_list = []
    for idx, item in enumerate(data_qry):
        id, author_id, created, data = item
        try:
            data = json.loads(data)
        except ValueError:
            print(">>>> WARN can't parse post id={} data='{}'".format(id, data))
            continue
        for key, value in data.items():
            data_list.append(
                {
                    "key": key,
                    "value": str(value),
                    "index": str(idx),
                }
            )
    return data_list