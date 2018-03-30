# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   parseData
   Description:
        1)分析云图，抽取职位要求
   Author:      LOVE
   Date:        2018/3/28 21:06
-------------------------------------------------
   Change Activity:
                2018/3/28: 
-------------------------------------------------
"""

from config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
database = client[MONGO_DB]
collection = database[MONGO_TABLE]


query = {}
query["requirement"] = {
    u"$ne": None
}


projection = {}
projection["_id"] = 0
projection["name"] = 1
projection["requirement"] = 1
projection["company"] = 1
projection["salary"] = 1

sort = [ (u"company", 1) ]

cursor = collection.find(query, projection = projection, sort = sort)


def save_job_requirement(cursor, filename):
    try:
        for doc in cursor:
            with open(filename, 'a', encoding="utf-8") as f:
                print("suc append text>>>>>>>>>>>>>>>")
                f.write(doc["requirement"])
    finally:
        client.close()

if __name__ == "__main__":
    save_job_requirement(cursor, MONGO_TABLE + ".txt")