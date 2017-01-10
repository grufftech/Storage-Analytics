import os, sys, datetime, time
import elasticsearch
from stat import *

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)

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
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def visitfile(file):
    size = os.stat(file).st_size
    ts = time.time()
    es.index(index='files', doc_type='data', body={
        'name': file,
        'filesize': size,
        'timestamp': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    })

    print 'indexing', file, size

if __name__ == '__main__':
    es = elasticsearch.Elasticsearch('elasticsearch')  # use default of localhost, port 920
    es.indices.create(index='files', ignore=400)
    walktree(sys.argv[1], visitfile)
    
