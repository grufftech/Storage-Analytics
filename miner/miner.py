import os, sys, ntpath
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from stat import *
from time import sleep

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        if os.listdir(top) == ".fcpbundle":
            continue

        try:
            mode = os.stat(pathname).st_mode
        except OSError as e:
            continue
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            callback(pathname)
        else:
            # Unknown file type, Skipping
            continue

def visitfile(file):
    size = os.stat(file).st_size
    path = ntpath.basename(file)
    pathname, filename = os.path.split(file)
    es = Elasticsearch('elasticsearch')
    doc = {
        'path': file,
        'size': size,
        'timestamp': datetime.now(),
    }
    res = es.index(index='file-index', doc_type='files', body=doc)
    print(res['created'])
    print("indexing file:", pathname, filename, size)

if __name__ == '__main__':
    es = Elasticsearch('elasticsearch')

    if sys.argv[2].lower() == "nuke":
        es.indices.delete(index='file-index', ignore=[400, 404])
        es.indices.delete(index='.kibana', ignore=[400, 404])
        print("nuked cache")
        sys.exit(1)

    walktree(sys.argv[1], visitfile)
