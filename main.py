import os
import mimetypes
from datetime import datetime
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import pymysql

def getdetails(ob, prop):
	if prop in ob.keys():
		return ob[prop][0]
	else:
		return ''
def getdate(timestamp):
	return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
	
foundfiles = []
for path, subdirs, files in os.walk("PATH_TO_SONGS_DIR"):
	for name in files:
		if name.endswith('.mp3'):
			fullpath = os.path.join(path ,name)
			foundfiles.append([path, name, os.path.getctime(fullpath), os.path.getmtime(fullpath), os.path.getsize(fullpath)])

db = pymysql.connect("HOST","USERNAME","PASSWORD","DB" )

for file in foundfiles:
	fpath = os.path.join(file[0] , file[1])
	
	try:
		audio = EasyID3(fpath)
		mime = mimetypes.guess_type(fpath)
	
		query = "INSERT INTO file_details(name, path, type, create_date, modify_date, size, title, album) VALUES ('{0}','{1}','{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(file[1], file[0], mime[0], getdate(file[2]), getdate(file[3]), file[4], getdetails(audio, 'title'), getdetails(audio, 'album'))
		cursor = db.cursor()
		cursor.execute(query)
		db.commit()
		cursor.close()
	except:
		pass
	
db.close()