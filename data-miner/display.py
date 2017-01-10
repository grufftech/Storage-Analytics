import os, sys, datetime, time
import elasticsearch
from stat import *

if __name__ == '__main__':
    es = elasticsearch.Elasticsearch('elasticsearch')  # use default of localhost, port 920
    es.indices.create(index='files', ignore=400)
    res = es.search(index="files", body={"query": {"match": {"name":"/code/data-miner"}}})
    print("Got %d Hits:" % res['hits']['total'])
    totalsize = 0
    for hit in res['hits']['hits']:
        print("%(name)s: %(filesize)s" % hit["_source"])
