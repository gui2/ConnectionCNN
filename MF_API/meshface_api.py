from __future__ import print_function

import base64
import random
import string
import urllib2
import ast
import mimetypes
import random
import string
_BOUNDARY_CHARS = string.digits + string.ascii_letters


'''
Asks to the service to understand an image
path : path of the image to understand
returns : response from the service
'''
def understand(path):
	q_url = 'http://ec2-54-186-158-220.us-west-2.compute.amazonaws.com:8080/api/understand'
	img =  open(path,'rb')
	files = {'source' : {'filename':''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9))+'.jpg' , 'content':img.read()}}
	data, headers = encode_multipart({},files)
	request = urllib2.Request(q_url, data=data, headers=headers)
	f = urllib2.urlopen(request)
	resp = f.read()
	return resp

'''
Each of this 'get_***' parses the response of the service for ***.
'''
def get_classes(resp):
	parsed = []
	d = ast.literal_eval(resp)
	return d['meta']['classify']

def get_words(resp):
	parsed = []
	d = ast.literal_eval(resp)
	return d['meta']['word']

def get_faces(resp):
	parsed = []
	d = ast.literal_eval(resp)
	return d['meta']['face']

def get_pedestrians(resp):
 	parsed = []
	d = ast.literal_eval(resp)
 	return d['meta']['pedestrian']

def get_cars(resp):
 	parsed = []
	d = ast.literal_eval(resp)
 	return d['meta']['car']

'''
Asks and retrieves the latest answer of the query to the server.
'''
def get_last_classes():
	parsed = []
	gRequest = requests.get('http://ec2-54-186-158-220.us-west-2.compute.amazonaws.com:8080/api/latest')
	resp = simplejson.loads(unicodedata.normalize('NFKD', gRequest.text).encode('ascii','ignore'))

 	for kv in resp['meta']['classify']:
		parsed.append((unicodedata.normalize('NFKD', kv['word']).encode('ascii','ignore'),kv['confidence']))

	return parsed

def encode_multipart(fields, files, boundary=None):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """
    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))
    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)