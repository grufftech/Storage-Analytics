import os, sys, ntpath
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
from stat import *

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
        'folder': pathbuilder(pathname,[]),
        'file': filename,
        'size': size,
        'timestamp': datetime.now(),
    }
    res = es.index(index='file-index', doc_type='files', body=doc)
    print(res['created'])
    print("indexing file:", pathname, filename, size)

def pathbuilder(path,listvalues = []):
    pathname, foldername = os.path.split(path)
    if pathname == "/":
        return listvalues
    else:
        listvalues.append(pathname+"/")
        return pathbuilder(pathname,listvalues)

if __name__ == '__main__':
    es = Elasticsearch('elasticsearch')
    es.indices.delete(index='file-index', ignore=[400, 404])
    es.indices.delete(index='folder-index', ignore=[400, 404])
    walktree(sys.argv[1], visitfile)
