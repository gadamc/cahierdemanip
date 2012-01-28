#!/usr/bin/env python
from dropbox import client, rest, session
import os,sys, pickle



#
#
#______________________________

def main(*argv):
    '''
       Usage:  ./get.py /path/to/folder
       or
             ./get.py 
       will save the CaheirDeManip.doc in your current directory
    '''
    if len(argv) > 0:
        sendToThisDir = argv[0]
    else:
        sendToThisDir = '.'

    akey = '5p5o73o3r35uz8g'
    asecret = 'hz7ffxbyqa1pql9'
    atyp = 'dropbox'
    homedir = os.path.expanduser('~')
    rcfile = os.path.join(homedir, '.cahierdemanip')
    sess = session.DropboxSession(akey, asecret, atyp)  

    access_token = ''
    
    if os.path.isfile( rcfile ):
        f = open( rcfile , 'r')
        access_token = pickle.load(f)
        sess.set_token(access_token.key, access_token.secret)
    else:
        reqtok = sess.obtain_request_token()
        url = sess.build_authorize_url(reqtok)
        print 'you must authenticate this app. Please click on the following URL.'
        print url
        print 'When you are finished, press Return'
        raw_input()
        try:    
            f = open(rcfile, 'w')
            access_token = sess.obtain_access_token(reqtok)
            pickle.dump(access_token, f)
        except:
            print "authentication failed, try again."
            os.remove(rcfile)
            sys.exit(0)
            
    print 'connecting to account...'
    try:
        cl = client.DropboxClient(sess)
        info = cl.account_info()
        print "linked account:", info['display_name'], info['email']
    except:
        print 'authentication failed somehow. delete the file %s and try again' % rcfile
        sys.exit(0)
        
    print 'downloading Cahier de Manip to', sendToThisDir    
    out = open(os.path.join(sendToThisDir, 'CAHIER_DE_MANIP.doc'), 'w')
    out.write(cl.get_file('/cahierdemanip/CAHIER_DE_MANIP.doc').read())


if __name__ == '__main__':
    main(*sys.argv[1:])
