#!/usr/bin/python
import urllib2
import sys

def main(argv):
    remote_url = None
    local_file = None
    f_size_unknown = True
    file_size = 0
    file_size_dl = 0
    block_sz = 8 * 1024
    if not isinstance(argv, list):
        print('pywget: Wrong main() arguments');
        return 1
    if len(argv) < 2:
        print('pywget: Need at least one remote url as argument')
        showUsage()
        return 1
    remote_url = argv[1]
    if len(argv) > 2:
        local_file = argv[2]
    else:
        try:
            local_file = remote_url.split('/')[-1]
        except:
            local_file = remote_url 

    print("pywget Downloading: %s -> %s"%(remote_url, local_file))
    u = urllib2.urlopen(remote_url)
    f = open(local_file, 'wb')
    meta = u.info()
    try:
        file_size = int(meta.getheaders("Content-Length")[0])
        f_size_unknown = False
    except:
        file_size = 1

    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        
        if not f_size_unknown:
            status = r"%10d of %10d  [%3.2f%%]" % (file_size_dl,
                                                   file_size,
                                                   file_size_dl * 100 / file_size)
        else:
            status = r"%10d of Unknown " % file_size_dl
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()
    u.close()

    return 0

def showUsage():
    print('pywget -- A wget(1) written in Python')
    print('Usage: wget <remote_url> [local_file_patch]')

if __name__=='__main__':
    exit(main(sys.argv))

