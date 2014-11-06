#! /usr/bin/env python
#coding=utf-8
"""
Skript zu Import und Normalisierung des Edfu MySQL Dumps
mit Anpassung an das neue Datenbankschema:
    * stärkere Normalisiserung
    * Anpassung an TYPO3 Felder

2013 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
"""

import re
import copy
import time
import pprint
import mysql.connector
import logging
from ConfigParser import SafeConfigParser
import subprocess
from lib import UnicodeReader
import processors

logging.basicConfig(filename='convert.log', filemode='w', level=logging.ERROR)

logger = logging.getLogger(__name__)

parser = SafeConfigParser()
parser.read('settings.ini')

dbUsername = parser.get('database', 'username')
dbPassword = parser.get('database', 'password')
dbHost = parser.get('database', 'host')
dbDatabase = parser.get('database', 'originDatabase')
dbTarget = parser.get('database', 'targetDatabase')

db = mysql.connector.connect(user=dbUsername, password=dbPassword, host=dbHost, database=dbDatabase)
cursor = db.cursor()


proc = subprocess.Popen(["mysql", "--user=%s" % dbUsername, "--password=%s" % dbPassword, dbDatabase],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
out, err = proc.communicate(file("Daten/edfuprojekt.sql").read())


writePrefix = 'edfu`.`tx_edfu_'


def szSplit (s):
    parts = s.replace(' ', '').split(',')
    parts = [int(parts[0]), int(parts[1])]
    return parts


defaultDate = int(time.mktime(time.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')))
defaultFields = {
	'tstamp': int(time.time()),
	'crdate': defaultDate,
	'cruser_id': 0,
	'deleted': 0,
	'hidden': 0,
	'starttime': 0,
	'endtime': 0,
	't3ver_oid': 0,
	't3ver_id': 0,
	't3ver_wsid': 0,
	't3ver_label': '',
	't3ver_state': 0,
	't3ver_stage': 0,
	't3ver_count': 0,
	't3ver_tstamp': 0,
	't3ver_move_id': 0,
	't3_origuid': 0,
	'sys_language_uid': 0,
	'l10n_parent': 0,
	'l10n_diffsource': None,
	'pid': 0
}


def addRecordsToTable (records, tableName):
	global db, cursor
	logger.info(u"\nTabelle »" + tableName + u"«: " + str(len(records)) + u" Datensätze")

	if len(records) > 0:
		for record in records:
			#pprint.pprint(record)
			prefix = writePrefix
			if tableName[-3:] != '_mm':
				prefix += 'domain_model_'
			
				# add default fields to record
				for fieldName in defaultFields:
					if not record.has_key(fieldName):
						record[fieldName] = defaultFields[fieldName]
			
			fieldNames = '(' + ', '.join(record.keys()) + ')'
			values = '(%(' + ')s, %('.join(record.keys()) + ')s)'
			insertStatement = "INSERT INTO `" + prefix + tableName + "` " + fieldNames + " VALUES " + values
			cursor.execute(insertStatement, record)
			
		db.commit()

def getRomanian(number):
	roemisch = {
		'I': 1, 'II':2, 'III':3, 'IV':4, 'V':5, 'VI':6, 'VII':7, 'VIII':8
	}
	return roemisch[number.upper()]




tempel = [
	{'uid': 0, 'name': 'Edfu'}
]

# Einträge für die 8 Chassinat Bände.
bandDict = {
	1: {'uid': 1, 'nummer': 1, 'freigegeben': False, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou I, 1892.', 'tempel_uid': 0},
	2: {'uid': 2, 'nummer': 2, 'freigegeben': False, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou II, 1897.', 'tempel_uid': 0},
	3: {'uid': 3, 'nummer': 3, 'freigegeben': False, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou III, 1928.', 'tempel_uid': 0},
	4: {'uid': 4, 'nummer': 4, 'freigegeben': False, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou IV, 1929.', 'tempel_uid': 0},
	5: {'uid': 5, 'nummer': 5, 'freigegeben': False, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou V, 1930.', 'tempel_uid': 0},
	6: {'uid': 6, 'nummer': 6, 'freigegeben': False, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou VI, 1931.', 'tempel_uid': 0},
	7: {'uid': 7, 'nummer': 7, 'freigegeben': True, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou VII, 1932.', 'tempel_uid': 0},
	8: {'uid': 8, 'nummer': 8, 'freigegeben': True, 'literatur': u'Chassinat, Émile; Le Temple d’Edfou VIII, 1933.', 'tempel_uid': 0}
}
band = []


# Szeneninformation
# Momentan nicht übertragen: Szene 5 (V 011,4-012-4)
szene = []
szene_has_stelle = []
stelle = []
szene_bildDict = {}
szene_bild = []

formularDict = {}
formular = []
suffixe = {}
formular_has_literatur = [
	{'uid_local': 1, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 2, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 3, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 4, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 4, 'uid_foreign': 2, 'detail': '10 (38.), u. n. 40*'},
	{'uid_local': 5, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 6, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 6, 'uid_foreign': 4, 'detail': '309, n. 11'},
	{'uid_local': 6, 'uid_foreign': 5, 'detail': '515, n. 135'},
	{'uid_local': 6, 'uid_foreign': 3, 'detail': '145, n. 676'},
	{'uid_local': 7, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 7, 'uid_foreign': 3, 'detail': '145, n. 676'},
	{'uid_local': 8, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 8, 'uid_foreign': 3, 'detail': '145, n. 676'},
	{'uid_local': 9, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 9, 'uid_foreign': 3, 'detail': '145, n. 676'},
	{'uid_local': 10, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 10, 'uid_foreign': 3, 'detail': '145, n. 676'},
	{'uid_local': 11, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 11, 'uid_foreign': 3, 'detail': '145, n. 676'},
	{'uid_local': 12, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 13, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 14, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 15, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 16, 'uid_foreign': 1, 'detail': '14, n. 51'},
	{'uid_local': 17, 'uid_foreign': 1, 'detail': '14, n. 51'},
]
literatur = [
	{'uid': 1, 'beschreibung': 'Bedier, in: GM 162, 1998'}, 
	{'uid': 2, 'beschreibung': 'Budde/Kurth, in: EB 4, 1994'},
	{'uid': 3, 'beschreibung': 'Labrique, Stylistique'},
	{'uid': 4, 'beschreibung': u'Aufrère, L’univers minéral I'},
	{'uid': 5, 'beschreibung': u'Aufrère, L’univers minéral II'}
]


photosDict = {}
photo = []
photo_typ = []
photoTypDict = {
	'alt': {'uid': 0, 'name': 'SW', 'jahr': 1999},
	'D03': {'uid': 1, 'name': '2003', 'jahr': 2003},
	'D05': {'uid': 2, 'name': '2005', 'jahr': 2005},
	'e': {'uid': 3, 'name': 'e', 'jahr': 1900},
	'G': {'uid': 4, 'name': 'G', 'jahr': 1950},
	'e-o': {'uid': 5, 'name': 'e-o', 'jahr': 1960},
	'Labrique, Stylistique': {'uid': 6, 'name': 'Labrique, Stylistique', 'jahr': 1912},
	'E. XIII': {'uid': 7, 'name': 'Edfou XIII', 'jahr': 1913},
	'E. XIV': {'uid': 8, 'name': 'Edfou XIV', 'jahr': 1914},
} 
formular_has_photoDict = {}
formular_has_photo_collection = []
photo_collection = []
photo_collection_has_photo = []
collectionPrototype = {'items': [], 'stern': False, 'klammern': False, 'kommentar':''}
collection = copy.deepcopy(collectionPrototype)

ort = []
ort_has_stelle = []


def finishCollection (PRIMARY):
	global collection, photo_collection, formular_has_photo_collection
	# Prüfen, ob es diese Sammlung schon gibt
	collectionExists = False
	for c in photo_collection:
		if c['items'] == collection['items'] and c['kommentar'] == collection['kommentar'] and c['klammern'] == collection['klammern'] and c['stern'] == collection['stern']:
			collection = c
			break

	# neue sammlung: ID geben und zur Liste hinzufügen
	if not collection.has_key('uid'):
		collection['uid'] = len(photo_collection)
		photo_collection += [collection]
		#pprint.PrettyPrinter().pprint(collection)

	formular_has_photo_collection += [{
		'uid_local': PRIMARY,
		'uid_foreign': collection['uid']
	}]

	collection = copy.deepcopy(collectionPrototype)

formularProcessor()
ortProcessor()
gottLength = gottProcessor()
wordlistProcessor()

cursor.close()
db.close()

for myCollection in photo_collection:
	for item in myCollection['items']:
		entry = {
			'uid_local': myCollection['uid'],
			'uid_foreign': photosDict[item]['uid']
		}
		if not entry in photo_collection_has_photo:
			photo_collection_has_photo += [entry]
	del myCollection['items']
	

photo = photosDict.values()
photo_typ = photoTypDict.values()
formular = formularDict.values()
band = bandDict.values()
formular_has_photo = formular_has_photoDict.values()

def szenenTool():
	global szene, szene_has_stelle
	# Szeneninformation aus CSV Dateien (aus Imagemap)
	# csv + Unicode Handhabungscode aus der Anleitung
	with open('Daten/tempelplan.csv', 'rb') as bilderListeCSV:
		bilderListeReader = UnicodeReader(bilderListeCSV, delimiter=';')
		bilderColumnDict = {}
		for bildRow in bilderListeReader:
			if bildRow[0] == 'image':
				# Spaltennummern für Felder feststellen
				for index, value in enumerate(bildRow):
					bilderColumnDict[value] = index
			else:
				recordSzeneBild = {
					'uid': len(szene_bildDict),
					'name': bildRow[bilderColumnDict['label']],
					'dateiname': bildRow[bilderColumnDict['image']],
					'imagemap': bildRow[bilderColumnDict['imagemap']],
					'breite': bildRow[bilderColumnDict['new_size_x']],
					'hoehe': bildRow[bilderColumnDict['new_size_y']],
					'breite_original': bildRow[bilderColumnDict['orig_size_x']],
					'hoehe_original': bildRow[bilderColumnDict['orig_size_y']],
					'offset_x': bildRow[bilderColumnDict['offset_x']],
					'offset_y': bildRow[bilderColumnDict['offset_y']],
					'name': bildRow[bilderColumnDict['label']]
				}
				szene_bildDict[recordSzeneBild['dateiname']] = recordSzeneBild
				szene_bild_ID = recordSzeneBild['uid']

				filePath = 'Daten/szenen/' + recordSzeneBild['dateiname'].rstrip('.gif') + '.csv'
				with open(filePath, 'rb') as csvFile:
					logger.info(u'INFO CSV Datei »' + filePath + u'«')
					columnDict = {}

					reader = UnicodeReader(csvFile, delimiter=';')
					for row in reader:
						if row[0] == 'description':
							# Spaltennummern für Felder feststellen
							for index, value in enumerate(row):
								columnDict[value] = index
						elif len(row) >= 12:
							szeneID = len(szene)
							stelleID = len(stelle)

							rSzene = {
								'uid': szeneID,
								'nummer': row[columnDict['plate']],
								'beschreibung': row[columnDict['description']],
								'szene_bild_uid': szene_bild_ID,
								'rect': row[columnDict['polygon']],
								'polygon': '',
								'koordinate_x': row[columnDict['coord-x']],
								'koordinate_y': row[columnDict['coord-y']],
								'blickwinkel': row[columnDict['angleOfView']],
								'breite': row[columnDict['extent-width']],
								'prozent_z': row[columnDict['height-percent']],
								'hoehe': float(row[columnDict['extent-height-percent']]),
								'grau': False
							}

							if columnDict.has_key('areacolor') and row[columnDict['areacolor']] == 2:
								rSzene['grau'] = True
							if columnDict.has_key('polygon_original'):
								rSzene['polygon'] = row[columnDict['polygon_original']]

							szene += [rSzene]
							seiteStart = row[columnDict['page']]
							seiteStop = seiteStart
							zeileStart = 0
							zeileStop = 30
							if len(row) >= 15:
								seiteStop = row[columnDict['page-to']]
								zeileStart = row[columnDict['line']]
								zeileStop = row[columnDict['line-to']]

							if row[columnDict['volume']] != '':
								rStelle = {
									'uid': stelleID,
									'band_uid': row[columnDict['volume']],
									'seite_start': seiteStart,
									'zeile_start': zeileStart,
									'seite_stop': seiteStop,
									'zeile_stop': zeileStop,
									'anmerkung': '',
									'stop_unsicher': 0,
									'zerstoerung': 0
								}
								stelle += [rStelle]

								szene_has_stelle += [{
									'uid_local': szeneID,
									'uid_foreign': stelleID
								}]
						else:
							logger.error(u'Zeile »' + ';'.join(row) + u'« hat weniger als 12 Spalten')

	szene_bild = szene_bildDict.values()

def insertIntoTargetDatabase():

	# In MySQL einfügen
	db = mysql.connector.connect(user=dbUsername, host=dbHost, password=dbPassword, database=dbTarget)
	cursor = db.cursor()

	f = open('Daten/schema.sql')
	schema = f.read()
	f.close()
	schema = re.sub(r'`edfu`.`(.*)`', r'`tx_edfu_domain_model_\1`' , schema)

	typo3Felder = """		tstamp           INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
			crdate           INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
			cruser_id        INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
			deleted          TINYINT(4) UNSIGNED DEFAULT '0' NOT NULL,
			hidden           TINYINT(4) UNSIGNED DEFAULT '0' NOT NULL,
			starttime        INT(11) UNSIGNED DEFAULT '0'    NOT NULL,
			endtime          INT(11) UNSIGNED DEFAULT '0'    NOT NULL,

			t3ver_oid        INT(11) DEFAULT '0'             NOT NULL,
			t3ver_id         INT(11) DEFAULT '0'             NOT NULL,
			t3ver_wsid       INT(11) DEFAULT '0'             NOT NULL,
			t3ver_label      VARCHAR(255) DEFAULT ''         NOT NULL,
			t3ver_state      TINYINT(4) DEFAULT '0'          NOT NULL,
			t3ver_stage      INT(11) DEFAULT '0'             NOT NULL,
			t3ver_count      INT(11) DEFAULT '0'             NOT NULL,
			t3ver_tstamp     INT(11) DEFAULT '0'             NOT NULL,
			t3ver_move_id    INT(11) DEFAULT '0'             NOT NULL,

			t3_origuid       INT(11) DEFAULT '0'             NOT NULL,
			sys_language_uid INT(11) DEFAULT '0'             NOT NULL,
			l10n_parent      INT(11) DEFAULT '0'             NOT NULL,
			l10n_diffsource  MEDIUMBLOB,

			pid              INT(11) DEFAULT '0'             NOT NULL,

			PRIMARY KEY (`uid`)"""

	schema = schema.replace('PRIMARY KEY (`uid`)', typo3Felder)
	schema = re.sub(r'DROP .*`tx_edfu_domain_model_([a-z_]+)_has_([a-z_]+)\`.*\n\n.*tx_edfu_domain_model_\1_has_\2\`',
		r"DROP TABLE IF EXISTS `tx_edfu_\1_\2_mm`;\n\n CREATE TABLE IF NOT EXISTS `tx_edfu_\1_\2_mm`",
		schema)
	# print schema
	for result in cursor.execute(schema, multi=True):
		1

	db.commit()

	addRecordsToTable(tempel, 'tempel')
	addRecordsToTable(band, 'band')
	addRecordsToTable(stelle, 'stelle')
	addRecordsToTable(szene_bild, 'szene_bild')
	addRecordsToTable(szene, 'szene')
	addRecordsToTable(szene_has_stelle, 'szene_stelle_mm')
	addRecordsToTable(literatur, 'literatur')
	addRecordsToTable(gott, 'gott')
	addRecordsToTable(formular, 'formular')
	addRecordsToTable(formular_has_literatur, 'formular_literatur_mm')
	addRecordsToTable(photo_typ, 'photo_typ')
	for p in photo:
		del(p['count'])
	addRecordsToTable(photo, 'photo')
	addRecordsToTable(formular_has_photo, 'formular_photo_mm')

	addRecordsToTable(ort, 'ort')
	addRecordsToTable(ort_has_stelle, 'ort_stelle_mm')

	cursor.close()
	db.close()


def printResult():

	print ""
	print u"FL: Transliteration mit Punkt und Folgebuchstaben:"
	pprint.PrettyPrinter().pprint(suffixe)

	print ""
	print "FL: Datensätze, Stellen, Bilder"
	print "formular: " + str(len(formular))
	print "stelle: " + str(len(stelle))
	print "photo: " + str(len(photo))
	print "formular_has_photo " + str(len(formular_has_photo))

	print ""
	print "OL"
	print "ort: " + str(len(ort))
	print "ort_has_stelle: " + str(len(ort_has_stelle))

	print ""
	print "GL"
	print "gott: " + str(len(gottLength))

	print ""
	print "WL"
	print "wort: " + str(len(wort))
	print "wort_has_stelle: " + str(len(wort_has_stelle))
	print "berlin: " + str(len(berlin))

	print ""
	print "Szenen"
	print "szene: " + str(len(szene))
	print "szene_bild: " + str(len(szene_bild))
	print "szene_has_stelle: " + str(len(szene_has_stelle))
