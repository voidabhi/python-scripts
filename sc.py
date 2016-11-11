#!/usr/bin/env python
import soundcloud
from clize import clize, run
from subprocess import call
 
 
@clize
def sc_load(tracks='', likes='', tags='', group=''):
    opts = {}
    if likes:
        method = 'favorites'
    elif tracks or group:
        method = 'tracks'
    elif tags:
        method = 'tracks'
        opts = {'tags': tags}
    else:
        return
 
    client = soundcloud.Client(client_id='c4c979fd6f241b5b30431d722af212e8')
    if likes or tracks:
        user = likes or tracks
        track = client.get('/resolve', url='https://soundcloud.com/' + user)
        user_id = track.id
        url = '/users/%d/' % user_id
    elif group:
        track = client.get('/resolve', url='https://soundcloud.com/groups/' + group)
        group_id = track.id
        url = '/groups/%d/' % group_id
    else:
        url = '/'
 
    end = '%s%s' % (url, method)
    for i, sound in enumerate(client.get(end, **opts)):
        print("%d Loading %s..." % (i, sound.obj['title']))
        call(['mpc', '-h', '<motdepasse>@entrecote', 'load',
              'soundcloud://url/%s' % sound.obj['permalink_url'].replace('http:', 'https:')])
 
 
if __name__ == '__main__':
    run(sc_load)
