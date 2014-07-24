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
import glob
import csv
import mysql.connector
db = mysql.connector.connect(user='edfu', host='localhost', password='edfu', database='edfuprojekt')
cursor = db.cursor()

writePrefix = 'edfu`.`tx_edfu_'


def szSplit (s):
	parts = s.replace(' ', '').split(',')
	parts = [int(parts[0]), int(parts[1])]

	return parts




# from http://docs.python.org/2/library/csv.html
import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


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
	print u"\nTabelle »" + tableName + u"«: " + str(len(records)) + u" Datensätze"

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



roemisch = {
	'I': 1, 'II':2, 'III':3, 'IV':4, 'V':5, 'VI':6, 'VII':7, 'VIII':8
}


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



print "\n\n\n\n**** FL *******************************************************************\n"



# Tabelle FL
query = ("SELECT ID, TEXTMITSUF, BAND, SEITEZEILE, TEXTOHNESU, TEXTDEUTSC, TEXTTYP, Photo, SzenenID, SekLit from FL")

cursor.execute(query)
re101 = re.compile(r'\wZ')
re102 = re.compile(r'\w\?\w')

for (PRIMARY, TEXTMITSUF, BAND, SEITEZEILE, TEXTOHNESU, TEXTDEUTSC, TEXTTYP, Photo, SzenenID, SekLit) in cursor:

	myFormular = {
		'uid': PRIMARY,
		'id': PRIMARY
	}

	# Felder
	myFormular['texttyp'] = TEXTTYP
	myFormular['uebersetzung'] = (TEXTDEUTSC.strip()
		.replace(u'dZtruit', u'détruit')
		.replace(u'enti?rement', u'entièrement')
		.replace(u'moitiZ', u'moitié')
		.replace(u'premi?re', u'première')
		.replace(u'placZe', u'placée')
		.replace(u'dZesse', u'déesse')
		.replace(u'mutilZs', u'mutilés')
		.replace(u'fen?tre', u'fenêtre')
		.replace(u'ZtZ gravZe', u'été gravée'))

	if myFormular['uebersetzung'] != TEXTDEUTSC:
		print "\t".join(["FL", str(PRIMARY), "INFO", u"Übersetzung String verändert", TEXTDEUTSC, myFormular['uebersetzung']])

	if re101.search(myFormular['uebersetzung']) or re102.search(myFormular['uebersetzung']):
		print "\t".join(["FL", str(PRIMARY), "WARNUNG", u"Vermutlich kaputte Akzente", myFormular['uebersetzung']])


	# Transliteration
	r = re.findall(r'\.\w+', TEXTMITSUF)
	for i in r:
		if suffixe.has_key(i):
			suffixe[i] += 1
		else:
			suffixe[i] = 1

	myFormular['transliteration'] = re.sub(r'\.([^aeiou. ][^.]*)', ':\\1', TEXTMITSUF, re.IGNORECASE | re.UNICODE)


	# Photos
	kommentar = ''

	originalPhoto = Photo
	if Photo == 'D05_5503, D05_5504, D05_5509, D05_5510, D05_5511, D05_5512: D05_5513, D05_5514, ( 2982, 2983, 2984, 2985 )*':
		# 263
		Photo = 'D05_5503, D05_5504, D05_5509, D05_5510, D05_5511, D05_5512, D05_5513, D05_5514, ( 2982, 2983, 2984, 2985 )*'
	elif Photo == 'D05_6555, D06_6556, D05_6557, D05_6558, D05_6559, D05_6560, D05_6561, ( 1605, 1606 )*':
		# 409
		Photo = 'D05_6555, D05_6556, D05_6557, D05_6558, D05_6559, D05_6560, D05_6561, ( 1605, 1606 )*'
	elif Photo == 'D05_4151, D05_4152, D05_4153, D05_4160: D05_4161, D05_4162, D05_4163, D05_4164, D05_4165, D05_4166, D05_4167, D05_4168, D05_4169, ( 1615, 1616 )*':
		# 1137-1138
		Photo = 'D05_4151, D05_4152, D05_4153, D05_4160, D05_4161, D05_4162, D05_4163, D05_4164, D05_4165, D05_4166, D05_4167, D05_4168, D05_4169, ( 1615, 1616 )*'
	elif Photo == 'D05_3779, D05_3780, D05_3787, D05_3788, D05_3789, D05_3790, D05_3791, D05_3792, D05_3793, D05_3794, D05_3795, D05_3796, D05_4094, D05_:4095, D05_4102, D05_4103, D05_4104: D05_4105, D05_4106, D05_4107, D05_4108, D05_4109, ( 1616, 1617 )*':
		# 1155-1156
		Photo = 'D05_3779, D05_3780, D05_3787, D05_3788, D05_3789, D05_3790, D05_3791, D05_3792, D05_3793, D05_3794, D05_3795, D05_3796, D05_4094, D05_4095, D05_4102, D05_4103, D05_4104, D05_4105, D05_4106, D05_4107, D05_4108, D05_4109, ( 1616, 1617 )*'
	elif Photo == 'D05_3771, D05_3772, D05_3773, D05_3774, D05-3775, D05_3776, D05_3777, D05_3778, D05_3779, D05_3780, D05_3783, D05_3784, D05_3786, D05_4085, D05_4086, D05_4087, D05_4088, D05_4089, D05_4090, D05_4091, D05_4092, D05_4093, D05_4094, D05_4095, D05_4099, D05_4100, D05_4101, ( 1616, 1617 )*':
		# 1157-1159
		Photo = 'D05_3771, D05_3772, D05_3773, D05_3774, D05_3775, D05_3776, D05_3777, D05_3778, D05_3779, D05_3780, D05_3783, D05_3784, D05_3786, D05_4085, D05_4086, D05_4087, D05_4088, D05_4089, D05_4090, D05_4091, D05_4092, D05_4093, D05_4094, D05_4095, D05_4099, D05_4100, D05_4101, ( 1616, 1617 )*'
	elif Photo == 'D05_3764, D05_3765, D05_3766, D05_3767, D05_3768, D05_3769, D05_3770, D05_4068, D05_4069, D05_4070, D05_4071, D05_4072, D05_4073, D04_4074, D05_4075, D05_4076, D05_4077, D05_4078, D05_4079, D05_4080, D05_4081, D05_4082, D05_4083, D05_4084, ( 1617, 1618, 1619 )*':
		# 1163-1165
		Photo = 'D05_3764, D05_3765, D05_3766, D05_3767, D05_3768, D05_3769, D05_3770, D05_4068, D05_4069, D05_4070, D05_4071, D05_4072, D05_4073, D05_4074, D05_4075, D05_4076, D05_4077, D05_4078, D05_4079, D05_4080, D05_4081, D05_4082, D05_4083, D05_4084, ( 1617, 1618, 1619 )*'
	elif Photo == 'D05_3764, D05_3765, D05_3766, D05_3767, D05_3768, D05_3769, D05_3770, D05_4068, D05_4069, D05_4070, D05_4071, D05_4072, D05_4073, D04_4074, D05_4075, ( 1618, 1619, 1620 )*':
		# 1167-1169
		Photo = 'D05_3764, D05_3765, D05_3766, D05_3767, D05_3768, D05_3769, D05_3770, D05_4068, D05_4069, D05_4070, D05_4071, D05_4072, D05_4073, D05_4074, D05_4075, ( 1618, 1619, 1620 )*'
	elif Photo == 'D05_3678, D05_3822, D05_3823, D05_3824, D05_3825, D05_3826, D05_3827, D05_3828, D05_3829, D05_3830, D05_3831, D05_3832, D05_3833, D05_4297, D05_4298, D05_4299, D05_4300, D05_4301, D05_4302, D05_4560, D05_4561, D05-4562, D05_4563, D05_4564, D05_4565, ( 3471, 3474 )*':
		# 1381-1382
		Photo = 'D05_3678, D05_3822, D05_3823, D05_3824, D05_3825, D05_3826, D05_3827, D05_3828, D05_3829, D05_3830, D05_3831, D05_3832, D05_3833, D05_4297, D05_4298, D05_4299, D05_4300, D05_4301, D05_4302, D05_4560, D05_4561, D05_4562, D05_4563, D05_4564, D05_4565, ( 3471, 3474 )*'
	elif Photo == 'D05_5391, D05_5395, D05_5396, D05-5397, D05_5398, D05_5399, D05_5400, ( 3112 )*':
		# 1435
		Photo = 'D05_5391, D05_5395, D05_5396, D05_5397, D05_5398, D05_5399, D05_5400, ( 3112 )*'
	elif Photo == 'D05_4954, D05_4955, D05_4956, D05_4957, D05_4958, D05_4959, D05_4983 (Z 6), D05_4984, D05_4985, D05_4986, D05_4987, D05_4988':
		# 1711-1713
		Photo = 'D05_4954, D05_4955, D05_4956, D05_4957, D05_4958, D05_4959, D05_4983, D05_4984, D05_4985, D05_4986, D05_4987, D05_4988'
		kommentar = 'D05_4983 (Z 6)'
	elif Photo == 'D05_6097, D05_6098, D05_6100, D05_6101, D06_6102, D05_6103, D05_6104, D05_6105, D05_6106, D05_6107, D05_6108, D05_6109, D05_6110, D05_6111, D05_6112, D05_6113, D05_6114, D05_6115, D05_6299, D05_6300':
		# 1818-1820
		Photo = 'D05_6097, D05_6098, D05_6100, D05_6101, D05_6102, D05_6103, D05_6104, D05_6105, D05_6106, D05_6107, D05_6108, D05_6109, D05_6110, D05_6111, D05_6112, D05_6113, D05_6114, D05_6115, D05_6299, D05_6300'
	elif Photo == 'D05_6052, D05_6053, D05_6054, D05_6055, D06_6056, D05_6057, D05_6058, D05_6059, D06_6060, D05_6068, D05_6069, D05_6070, D05_6287':
		# 1837,1839
		Photo = 'D05_6052, D05_6053, D05_6054, D05_6055, D05_6056, D05_6057, D05_6058, D05_6059, D05_6060, D05_6068, D05_6069, D05_6070, D05_6287'
	elif Photo == 'D05_6052, D05_6053, D05_6054, D05_6055, D06_6056, D05_6057, D05_6058, D05_6059, D06_6060, D05_6068, D05_6069, D05_6070, D05_6287, 3846, 3847, 3848':
		# 1838
		Photo = 'D05_6052, D05_6053, D05_6054, D05_6055, D05_6056, D05_6057, D05_6058, D05_6059, D05_6060, D05_6068, D05_6069, D05_6070, D05_6287, 3846, 3847, 3848'
	elif Photo == 'D05_6017+, D05_6018, D05_6019, D05_6020, D05_6021, D05_6022, D05_6025, D05_6284+, D05_6285+, ( 1650 )*':
		# 1867-1869
		Photo = 'D05_6017, D05_6018, D05_6019, D05_6020, D05_6021, D05_6022, D05_6025, D05_6284, D05_6285, ( 1650 )*'
	elif Photo == 'D05_4160, D05_4161, D05_4162, D05_4163, D05_4164, D05_4165, D05_4166, D05, 4167, D05_4168, D05_4169':
		# 3097-3099
		Photo = 'D05_4160, D05_4161, D05_4162, D05_4163, D05_4164, D05_4165, D05_4166, D05_4167, D05_4168, D05_4169'
	elif Photo == 'D03_0772, D03_0791, D03_0792, 1146, 1147, e015 ( 1145, 1340, 1341, E. XIII, pl. CCCCXCIV - CCCCXCVI )*':
		# 3745
		Photo = 'D03_0772, D03_0791, D03_0792, 1146, 1147, e015 ( 1145, 1340, 1341, E. XIII, pl. CCCCXCIV, CCCCXCV, CCCXCVI )*'
	elif Photo == 'D05_0388, D05_0389, D05_0390, D05_0391, D05_0392, D05_0393, D05_0394, D05-0395, D03_0622, D03_0623, D03_0624, D03_0625, D03_0618, D03_0619, D03_0620, D03_0621, 1446, 1447 (E. XIV, pl. DLII )*':
		# 4077
		Photo = 'D05_0388, D05_0389, D05_0390, D05_0391, D05_0392, D05_0393, D05_0394, D05_0395, D03_0622, D03_0623, D03_0624, D03_0625, D03_0618, D03_0619, D03_0620, D03_0621, 1446, 1447 (E. XIV, pl. DLII )*'
	elif Photo == u'D05_0539, D05_0540, D05_0541, D05_0542¸ D05_0543, D05_0544, D05_0545, D05_0546, D05_0553, D05_0554, D05_0555, 1449, 1450, e021':
		# 4127
		Photo = 'D05_0539, D05_0540, D05_0541, D05_0542, D05_0543, D05_0544, D05_0545, D05_0546, D05_0553, D05_0554, D05_0555, 1449, 1450, e021'
	elif Photo == 'D05_1876, D05-1877, D05_1878, D05_1893, 1418, 1419, 1420, e087 ( 1415, 1416, 1417, E. XIII, pl. DXX, DXXI )*':
		# 4202
		Photo = 'D05_1876, D05_1877, D05_1878, D05_1893, 1418, 1419, 1420, e087 ( 1415, 1416, 1417, E. XIII, pl. DXX, DXXI )*'
	elif Photo == 'D05_1954, D05_1955, D05_1962, D05_1963, 1409, 1408, e083 (E. XIII, DXXIV, DXXV )*':
		# 4227
		Photo = 'D05_1954, D05_1955, D05_1962, D05_1963, 1409, 1408, e083 (E. XIII, pl. DXXIV, DXXV )*'
	elif Photo == 'D05_1824, D05_1825, D05_1826, D05_1827, D05_1830, D05_1831, D05_1832, D05_1833, D05-1834, D05_1835, D05_1836, D05_1837, 1425, 1426, 1427, e090 (E. XIII, pl. DXXXVI )*':
		# 4420
		Photo = 'D05_1824, D05_1825, D05_1826, D05_1827, D05_1830, D05_1831, D05_1832, D05_1833, D05_1834, D05_1835, D05_1836, D05_1837, 1425, 1426, 1427, e090 (E. XIII, pl. DXXXVI )*'
	elif Photo.find('D05_1061:') != -1:
		# 4772-4795
		Photo = re.sub('D05_1061:', 'D05_1061,', Photo)
	elif Photo.find('D05-0933') != -1:
		# 4817-4823
		Photo = re.sub('D05-0933', 'D05_0933', Photo)
	elif Photo.find('2314 - 2316') != -1:
		# 9316-9323
		Photo = re.sub('2314 - 2316', '2314, 2315, 2316', Photo)
	elif Photo.find('2320 - 2322') != -1:
		# 9332
		Photo = re.sub('2320 - 2322', '2320, 2321, 2322', Photo)
	#elif Photo == '103, 105, 111, 112, 2372, 2387, 2560 ( 103 - 105, 2387 - 2390, E XIV, pl. DCLXXIV )*':
	elif PRIMARY == 10021:
		# 10021
		Photo = '103, 105, 111, 112, 2372, 2387, 2560 ( 103, 104, 105, 2387, 2388, 2389, 2390, E. XIV, pl. DCLXXIV )*'
	elif Photo.find('( 2438, 2439, 2440, 2441, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2449, 2450, 2451 (E. VIII, 96, 3 - 99, 3))*') != -1:
		# 9741-9773
		Photo = re.sub('\(E. VIII, 96, 3 - 99, 3\)', '', Photo)
		kommentar = 'E. VIII, 96, 3 - 99, 3'
	elif PRIMARY == 8399 or PRIMARY == 9011 or PRIMARY == 9012:
		Photo = '3813, 3814, 3815, 3816, 3817, 3818, 3819, 3820, 3821, 3822, 3823, 3824, 3825, 3826, 3827, 3828, 3829, 3830, 3831, 3832, 3833, 3834, 3835, 3836, 3837, 3838'
		kommentar = 'E. VII, 252, 5'
	elif PRIMARY == 9950:
		Photo = re.sub('\(E VIII, 122, 5 - 124, 18\)', '', Photo)
		kommentar = 'E VIII, 122, 5 - 124, 18'
	elif Photo.find('E. E. ') != -1:
		# 5629-5650, 6135
		Photo = re.sub('E. E. ', 'E. ', Photo)
	elif Photo.find('E. XIV. ') != -1:
		# 6249, 6371-6373
		Photo = re.sub('E. XIV. ', 'E. XIV, ', Photo)
	elif Photo.find('E. XIV ') != -1:
		# 10339, 10340
		Photo = re.sub('E. XIV ', 'E. XIV, ', Photo)
	elif Photo.find('E X') != -1:
		# einige mit vergessenem . hinter dem E, z.B. 10203ff
		Photo = re.sub('E X', 'E. X', Photo)
	elif Photo == '( 3909, 3910 ) *':
		# 10348-10372
		Photo = '( 3909, 3910 )*'

	if Photo != originalPhoto:
		print "\t".join(["FL", str(PRIMARY), "INFO", u"Photo String verändert", originalPhoto, Photo])



	re1 = re.compile(r'[0-9]+a*')
	re2 = re.compile(r'D03_[0-9]+')
	re3 = re.compile(r'D05_[0-9]+a*')
	re4 = re.compile(r'e[0-9]+')
	re5 = re.compile(r'(E. [XVI]+), (pl. [DCLXVI0-9]+)')
	re6 = re.compile(r'\([^)]*\)(\s*\**)')
	re7 = re.compile(r'[DCLXVI]+')
	re8 = re.compile(r'\)\s*\**')
	re9 = re.compile(r'(G[0-9]+)\s*([f.]*)') # Z.B. G30 oder G32 ff.
	re10 = re.compile(r'e-onr-[0-9]+')
	re11 = re.compile(r';*\s*Labrique, Stylistique, (pl. [0-9.]*)')
	re12 = re.compile(r'\s*\*') # beginnt mit *
	re13 = re.compile(r'\s*\(teilweise\)')
	re14 = re.compile(r'([^)]*)\s*(\(E. [IVX]+, [0-9]+, [-0-9]+\))(.*)')
	re15 = re.compile(r'[^(]*\((E.[^)]*)')

	bildString = Photo
	klammern = False
	stern = False

	while len(bildString) > 0:
		name = ''
		typ = '---'

		# Sonderfälle
		if PRIMARY == 9562:
			if bildString.find('VIII') != -1:
				m15 = re15.match(bildString)
				kommentar = m15.group(1)
			else:
				kommentar = ''

		if re6.match(bildString):
			finishCollection(PRIMARY)

			# Klammer auf, ggf mit Stern hinter der schließenden Klammer
			klammern = True
			if re6.match(bildString).group(1) == '*':
				stern = True
			bildString = bildString[1:]

			# Spezialfälle mit Kommentaren
			m14 = re14.match(bildString)
			if m14 and PRIMARY < 9000:
				# 6344-6356
				bildString = m14.group(1) + m14.group(3)
				kommentar = m14.group(2)
			elif PRIMARY == 9834:
				bildString = '3911 )*'
				kommentar = 'E. VIII, 108, nach 3'
			elif PRIMARY == 9951:
				bildString = '2374, 2375, 2376 )*'
				kommentar = 'E VIII, 122, 5 - 124, 18'
			elif PRIMARY == 9562 and bildString.find('VIII') != -1:
				bildString = bildString[bildString.find(')') + 1:]
				klammern = False
			elif PRIMARY == 9671:
				kommentar = 'E. VIII, 87, 5'
				bildString = '141, 142, E. XIV, pl. DCLXIX, DCLXX )*'
			elif PRIMARY == 9870:
				kommentar = 'E. VIII, 111, 16'
				bildString = '114, 115, 116, 117)*'

		elif re8.match(bildString):
			# Klammer zu
			klammern = False
			bildString = bildString[len(re8.match(bildString).group(0)):]
		elif re1.match(bildString):
			# Fall 1: Dateiname nur aus Ziffern
			name = re1.match(bildString).group(0)
			typ = 'alt'
			bildString = bildString[len(name):]
		elif re2.match(bildString):
			# Fall 2: Dateiname der Form D03_XXXXX
			name = re2.match(bildString).group(0)
			typ = 'D03'
			bildString = bildString[len(name):]
		elif re3.match(bildString):
			# Fall 3: Dateiname der Form D05_XXXXX
			name = re3.match(bildString).group(0)
			typ = 'D05'
			bildString = bildString[len(name):]
		elif re4.match(bildString):
			# Fall 4: Dateiname der Form eXXX
			name = re4.match(bildString).group(0)
			typ = 'e'
			bildString = bildString[len(name):]
		elif re9.match(bildString):
			# Fall 5: Name der Form GXXX [ff.]
			name = re9.match(bildString).group(1)
			typ = 'G'
			kommentar = re9.match(bildString).group(2)
			bildString = bildString[len(re9.match(bildString).group(0)):]
		elif re10.match(bildString):
			# Fall 6: Name der Form e-onr-XXX
			name = re10.match(bildString).group(0)
			typ = 'e-o'
			bildString = bildString[len(name):]
		elif re11.match(bildString):
			# Fall 7: Labrique, Stylistique
			name = re11.match(bildString).group(1)
			typ = 'Labrique, Stylistique'
			bildString = bildString[len(re11.match(bildString).group(0)):]
		elif re5.match(bildString):
			# Fall (n+1): Verweis auf Tafeln im Edfou Buch
			m = re5.match(bildString)
			typ = m.group(1)
			name = m.group(2)
			# rest = m.group(3)

			bildString = bildString[len(m.group(0)):].strip(', ')
			if re7.match(bildString):
				# Es kommt noch ein Edfou Bild
				bildString = typ + ', pl. ' + bildString

		else:
			print "\t".join(["FL ", str(PRIMARY), u"UNKLAR", bildString])
			bildString = ''

		if len(name) > 0:
			if re12.match(bildString):
				# ist gefolgt von *
				stern = True
				bildString = bildString[len(re12.match(bildString).group(0)):]
			if re13.match(bildString):
				kommentar = 'teilweise'
				bildString = bildString[len(re13.match(bildString).group(0)):]

			if PRIMARY == 9910 and bildString.find('103') == -1:
				kommentar = 'E. VIII, 118, 7'
				bildString = ''

			photoID = typ + '-' + name
			myPhoto = {}
			if photosDict.has_key(photoID):
				myPhoto = photosDict[photoID]
				myPhoto['count'] += 1
			else:
				if typ == 'D05' or typ == 'D03' or typ == 'alt':
					pfad = typ + '/' + name + '.jpg'
				else:
					pfad = ''

				myPhoto = {
					'uid': len(photosDict),
					'photo_typ_uid': photoTypDict[typ]['uid'],
					'name': name,
					'count': 1
				}
				photosDict[photoID] = myPhoto

			collection['items'] += [photoID]
			collection['klammern'] = klammern
			collection['stern'] = stern
			collection['kommentar'] = kommentar

			key = str(PRIMARY) + '-' + str(myPhoto['uid'])
			if not formular_has_photoDict.has_key(key):
				formular_has_photoDict[key] = {
					'uid_local': PRIMARY,
					'uid_foreign': myPhoto['uid'],
					'kommentar': kommentar
				}

		bildString = bildString.strip(', ')
	finishCollection(PRIMARY)



	# Textposition
	myStelle = {}
	myStelle['band_uid'] = bandDict[int(BAND)]['nummer']

	## Sonderfälle
	szOriginal = SEITEZEILE
	if PRIMARY == 3416:
		SEITEZEILE = "011, 09 - 012, 01"
	if PRIMARY == 9583:
		SEITEZEILE = "078, 14 / Kol. 1"
	if PRIMARY == 9584:
		SEITEZEILE = "078, 14 / Kol. 2"


	kommentar = []
	if SEITEZEILE.find('nach ') == 0:
		kommentar += ['nach']
		SEITEZEILE = SEITEZEILE.replace('nach ', '')
	if SEITEZEILE.find(', Z') != -1:
		kommentar += [SEITEZEILE[SEITEZEILE.find(', Z') + 2:]]
		SEITEZEILE = SEITEZEILE[:SEITEZEILE.find(', Z')]
	if SEITEZEILE.find(' / Z') != -1:
		kommentar += [SEITEZEILE[SEITEZEILE.find(' / Z') + 3:]]
		SEITEZEILE = SEITEZEILE[:SEITEZEILE.find(' / Z')]
	if SEITEZEILE.find(', Kol') != -1:
		kommentar += [SEITEZEILE[SEITEZEILE.find(', Kol') + 2:]]
		SEITEZEILE = SEITEZEILE[:SEITEZEILE.find(', Kol')]
	if SEITEZEILE.find(' / kol') != -1:
		kommentar += [SEITEZEILE[SEITEZEILE.find(' / kol') + 3:]]
		SEITEZEILE = SEITEZEILE[:SEITEZEILE.find(' / kol')]
	if SEITEZEILE.find(' / ') != -1:
		kommentar += [SEITEZEILE[SEITEZEILE.find(' / ') + 3:]]
		SEITEZEILE = SEITEZEILE[:SEITEZEILE.find(' / ')]

	if szOriginal != SEITEZEILE:
		print "\t".join(["FL", str(PRIMARY), "INFO", u"Änderung SEITEZEILE", szOriginal, SEITEZEILE])

	if len(kommentar) > 0:
		print "\t".join(["FL", str(PRIMARY), "INFO", "SEITEZEILE + Kommentar", "; ".join(kommentar)])

 	if len(re.findall("[^0-9, -]", SEITEZEILE)) > 0:
		print "\t".join(["FL", str(PRIMARY), "FEHLER", "SEITEZEILE", SEITEZEILE])

 	myStelle['anmerkung'] = '; '.join(kommentar)

	result = []
	if SEITEZEILE.find(' - ') != -1:
		# Form »002, 06 - 003, 02«
		szParts = SEITEZEILE.split(' - ')
		result += [szSplit(szParts[0])]
		result += [szSplit(szParts[1])]
	elif SEITEZEILE.find(',') != -1:
		parts = SEITEZEILE.split(',')
		seite = int(parts[0])
		if parts[1].find('-') != -1:
			zeilen = parts[1].split('-')
			result =[[seite, int(zeilen[0])], [seite, int(zeilen[1])]]
		else:
			zeile = int(parts[1])
			result = [[seite, zeile], [seite, zeile]]
	else:
		result = [[0,0],[0,0]]
		print "\t".join(["FL", str(PRIMARY), "FEHLER", "SEITEZEILE", SEITEZEILE])

	if result[0][0] > result[1][0]:
		print "\t".join(["FL", str(PRIMARY), "FEHLER", "SEITEN absteigend", SEITEZEILE])
	if result[0][0] == result[1][0] and result[0][1] > result[1][1]:
		print "\t".join(["FL", str(PRIMARY), "FEHLER", "ZEILEN absteigend", SEITEZEILE])

	myStelle['seite_start'] = result[0][0]
	myStelle['zeile_start'] = result[0][1]
	myStelle['seite_stop'] = result[1][0]
	myStelle['zeile_stop'] = result[1][1]

	if myStelle['zeile_start'] > 30:
		print "\t".join(["FL", str(PRIMARY), "FEHLER", "zeile_start > 30", SEITEZEILE])
	if myStelle['zeile_stop'] > 30:
		print "\t".join(["FL", str(PRIMARY), "FEHLER", "zeile_stop > 30", SEITEZEILE])

	myStelle['stop_unsicher'] = False
	myStelle['zerstoerung'] = False

	myStelle['uid'] = len(stelle)
	myFormular['stelle_uid'] = len(stelle)

	stelle += [myStelle]
	formularDict[myFormular['uid']] = myFormular




print "\n\n\n\n**** OL *******************************************************************\n"


ort = []
ort_has_stelle = []

# Tabelle OL
query = ("SELECT `PRIMARY`, STELLE, TRANS, ORT, LOK, ANM FROM OL")
cursor.execute(query)

re3 = re.compile(r'^\s*([VI]*)\s*,*\s*([0-9]*)\s*,\s*([0-9/ -]*)\s*(.*)$')

for (PRIMARY, STELLE, TRANS, ORT, LOK, ANM) in cursor:
	originalStelle = STELLE
	if STELLE == 'VIII, 73, 5; 73, 7 (sic; statt   lies wohl  , gegen Anm. 6);':
		# 240
		STELLE = 'VIII, 73, 5; 73, 7 (sic - statt   lies wohl  , gegen Anm. 6)'
	elif STELLE == 'VIII, 42, 9; 42, 15; 77, 1; 125, 10; 126, 13; 133, 16; VII, [54, 16]; 88, 1; 184, 15; 191, 14; VI, 229, 1;':
		# 247
		STELLE = 'VIII, 42, 9; 42, 15; 77, 1; 125, 10; 126, 13; 133, 16; VII, 54, 16 []; 88, 1; 184, 15; 191, 14; VI, 229, 1;'
	elif STELLE == 'V, 8, 10; 10, 5; 31, 5; 33, 12; 35, 3; 46, 1; 98, 13; 100, 7; 127, 2; 128, 2; 158, 1; 168, 1; 170, 3 ( ); 173, 12; 205, 6; 220, 6; 222, 17; 226, 7; 278, 14; 284, 10; 304, 7; 305, 2; 337, 1; 343, 1; 346, 2 (3x); 3 (2x); 4 (2x); 5 (2x); 6 (3x); 347, 1 (2x); 4; 357, 6; 359, 2; 383, 4; 394, 14;':
		# 356
		STELLE = 'V, 8, 10; 10, 5; 31, 5; 33, 12; 35, 3; 46, 1; 98, 13; 100, 7; 127, 2; 128, 2; 158, 1; 168, 1; 170, 3 ( ); 173, 12; 205, 6; 220, 6; 222, 17; 226, 7; 278, 14; 284, 10; 304, 7; 305, 2; 337, 1; 343, 1; 346, 2 (3x); 346, 3 (2x); 346, 4 (2x); 346, 5 (2x); 346, 6 (3x); 347, 1 (2x); 347, 4; 357, 6; 359, 2; 383, 4; 394, 14'
	elif STELLE == u'VIII, 169, 1 (Tempel!); VII, 2, 7; 10, 6; 20, 2 (als Gebieterin u. Herrin der Städte; wohl der Tempel); 20, 10; 20, 14; 22, 6; 23, 10; 25, 1 (die Gebieterin der Städte und Gaue); 25, 11; 39, 7; 40, 13; 52, 7; 60, 11; 61, 10;':
		# 504
		STELLE = u'VIII, 169, 1 (Tempel!); VII, 2, 7; 10, 6; 20, 2 (als Gebieterin u. Herrin der Städte - wohl der Tempel); 20, 10; 20, 14; 22, 6; 23, 10; 25, 1 (die Gebieterin der Städte und Gaue); 25, 11; 39, 7; 40, 13; 52, 7; 60, 11; 61, 10'
	elif STELLE == 'VI, 209 4 (Gau); 209, 5 (Stadt); 216, 9; 217, 2; 224, 11; 237, 6; 242, 16; 243, 6; 244, 4; 245, 5; 247, 5; 249, 13; 261, 11; 263, 10; 270, 2; 273, 8; 273, 10; 276, 11; 278, 16; 282, 8; 282, 11; 283, 7; 283, 13; 284, 15; 285, 11; 288, 4; 288, 7; 290, 4; 291, 5;':
		# 509
		STELLE = 'VI, 209, 4 (Gau); 209, 5 (Stadt); 216, 9; 217, 2; 224, 11; 237, 6; 242, 16; 243, 6; 244, 4; 245, 5; 247, 5; 249, 13; 261, 11; 263, 10; 270, 2; 273, 8; 273, 10; 276, 11; 278, 16; 282, 8; 282, 11; 283, 7; 283, 13; 284, 15; 285, 11; 288, 4; 288, 7; 290, 4; 291, 5;'
	elif PRIMARY == 579:
		ANM = STELLE
		STELLE = ''
	elif STELLE == u'VI, 68, 3; 237, 9; 277, 6; 310, 13; V, 9, 2 ([]; wohl Ägypten); 24, 8 (Ägypten: "das Versiegelte"); 44, 4 (Welt); 59, 5; 63, 1; 64, 7; 70, 3; 80, 6 (Welt); 84, 8 (Welt); 92, 1; 101, 13; 157, 12 (Welt);':
		# 619
		STELLE = u'VI, 68, 3; 237, 9; 277, 6; 310, 13; V, 9, 2 ([], wohl Ägypten); 24, 8 (Ägypten: "das Versiegelte"); 44, 4 (Welt); 59, 5; 63, 1; 64, 7; 70, 3; 80, 6 (Welt); 84, 8 (Welt); 92, 1; 101, 13; 157, 12 (Welt);'
	elif STELLE == 'VIII, 5, 11; (vergleiche auch 8, 9; V, 95, 12 ([]); 324, 5;':
		# 628
		STELLE = 'VIII, 5, 11 (vergleiche auch 8, 9); V, 95, 12 ([]); 324, 5'
	elif STELLE == 'VII, 326, 6; VI, 17, 1; 58, 16; 65, 2; 71, 11; 86, 8; 158, 12; 278, 12; 280, 6; 299, 6; 304, 6; 309, 6; 317, 2; 319, 15;V, 60, 7; 77, 5; 78, 13; 86, 10; 151, 4 ([];<>); 159, 13; 162, 3;':
		# 722
		STELLE = 'VII, 326, 6; VI, 17, 1; 58, 16; 65, 2; 71, 11; 86, 8; 158, 12; 278, 12; 280, 6; 299, 6; 304, 6; 309, 6; 317, 2; 319, 15;V, 60, 7; 77, 5; 78, 13; 86, 10; 151, 4 ([],<>); 159, 13; 162, 3;'
	elif STELLE == 'VI, 36, 11; 208, Anm. 2; 328, 17/18;':
		# 751
		STELLE = 'VI, 36, 11; 208, 0 (Anm. 2); 328, 17/18;'
	elif STELLE == 'VIII, 53, 1; 53, 2; 53, 5; 57, 8; 57, 11; 60, 14-61, 1; 61, 15; 66, 6; 71, 6; 71, 7; VII, 69, 4; 76, 15; 76, 15/16; 106, 13; 131, 2; 131, 6; 190, 1; 204, 7; 204, 10; 204, 15; 211, 6/7; 254, 3; 270, 14; 270, 16; 292, 4; 304, 12; 317, 7; 317, 13;':
		# 892
		STELLE = 'VIII, 53, 1; 53, 2; 53, 5; 57, 8; 57, 11; 60, 14 - 61, 1; 61, 15; 66, 6; 71, 6; 71, 7; VII, 69, 4; 76, 15; 76, 15/16; 106, 13; 131, 2; 131, 6; 190, 1; 204, 7; 204, 10; 204, 15; 211, 6/7; 254, 3; 270, 14; 270, 16; 292, 4; 304, 12; 317, 7; 317, 13;'
	elif STELLE == 'VII, 2, 4; 3, 4; 5, 2; 7, 6; 8, 2; 8, 7; 9, 7; 10, 8; 13, 2; 15, 9; 21, 9; 22, 1; 22, 11; 22, 12 (2x); 24, 2; 26, 7; 26, 8; 31, 5; 35, 9; 36, 4; 40, 11; 43, 3; 44, 5; 61, 4; 74, 17; (Gau); 88, 4; 89, 8; 100, 16; 102, 1; 105, 10; 105, 14; 108, 2; 108, 3; 111, 11; 119, 6; 120, 6; 125, 10; 126, 3; 130, 12;':
		# 939
		STELLE = 'VII, 2, 4; 3, 4; 5, 2; 7, 6; 8, 2; 8, 7; 9, 7; 10, 8; 13, 2; 15, 9; 21, 9; 22, 1; 22, 11; 22, 12 (2x); 24, 2; 26, 7; 26, 8; 31, 5; 35, 9; 36, 4; 40, 11; 43, 3; 44, 5; 61, 4; 74, 17 (Gau); 88, 4; 89, 8; 100, 16; 102, 1; 105, 10; 105, 14; 108, 2; 108, 3; 111, 11; 119, 6; 120, 6; 125, 10; 126, 3; 130, 12;'
	elif STELLE == 'V, 175, 18-176, 1;':
		# 993
		STELLE = 'V, 175, 18 - 176, 1;'
	elif STELLE == 'V, 42, 9; 63, 9 ([]); 71, 13/14 ([]); 86, 7/8; 89, 15; 151, 17-152, 1; 155, 1; 162, 6; 165, 9; 206, 2; 215, 10; 231, 3/4; 244, 14; 288, 16/17; 300, 19; 326, 7; 396, 7;':
		# 1067
		STELLE = 'V, 42, 9; 63, 9 ([]); 71, 13/14 ([]); 86, 7/8; 89, 15; 151, 17 - 152, 1; 155, 1; 162, 6; 165, 9; 206, 2; 215, 10; 231, 3/4; 244, 14; 288, 16/17; 300, 19; 326, 7; 396, 7;'
	elif STELLE == 'VI, 105, 5; 107, 3; 107, 8; 108, 12; 143, 3; 152, 1; 152, 16; 158, 1; 169, 174, 1; 174, 17; 175, 1; 179, 8; 181, 7; 186, 4; 190, 5; 199, 2; 237, 6; 237, 10; 243, 16; 244; 13; 245, 15; 248, 5; 249, 14; 260, 3; 274, 13; 276, 7; 276, 10; 277, 4/5; 277, 14/15;':
		# 1072
		STELLE = 'VI, 105, 5; 107, 3; 107, 8; 108, 12; 143, 3; 152, 1; 152, 16; 158, 1; 169, 1; 174, 17; 175, 1; 179, 8; 181, 7; 186, 4; 190, 5; 199, 2; 237, 6; 237, 10; 243, 16; 244, 13; 245, 15; 248, 5; 249, 14; 260, 3; 274, 13; 276, 7; 276, 10; 277, 4/5; 277, 14/15;'
	elif STELLE == 'VI, 278, 9; 278, 17; 280, 15; 281, 15; 283, 9; 283, 11; 287, 3; 290, 11; 297, 17; 299, 3 ([]); 303, 16; 308, 10; 315; 7; 319, 14; 324, 4; 325, 7; 332, 1; 334, 4; 349, 6; 351, 14; V, 4, 1; 7, 1; 13, 12; 31, 5; 31, 6; 36, 2; 38, 11; 39, 10; 40, 4; 41, 2; 44, 11; 50, 12; 55, 1; 56, 11; 58, 15, 16;':
		# 1073
		STELLE = 'VI, 278, 9; 278, 17; 280, 15; 281, 15; 283, 9; 283, 11; 287, 3; 290, 11; 297, 17; 299, 3 ([]); 303, 16; 308, 10; 315, 7; 319, 14; 324, 4; 325, 7; 332, 1; 334, 4; 349, 6; 351, 14; V, 4, 1; 7, 1; 13, 12; 31, 5; 31, 6; 36, 2; 38, 11; 39, 10; 40, 4; 41, 2; 44, 11; 50, 12; 55, 1; 56, 11; 58, 15, 16;'
	elif STELLE == 'VIII, <23, 2>;':
		# 1198
		STELLE = 'VIII, 23, 2 (<23, 2>)'

	if STELLE != originalStelle:
		print "\t".join(["OL", str(PRIMARY), "INFO", u"Änderung STELLE", originalStelle, STELLE])


	myOrt = {
		'uid': PRIMARY,
		'id': PRIMARY,
		'transliteration': TRANS,
		'ort': ORT,
		'lokalisation': LOK,
		'anmerkung': ANM
	}
	ort += [myOrt]


	teile = STELLE.strip('; ').split(';')
	bandNr = 0

	for teil in teile:
		if len(teil.strip()) > 0:
			m3 = re3.match(teil)
			if not m3:
				print "\t".join(["OL", str(PRIMARY), "FEHLER", u"STELLE", teil])
			else:
				myBand = m3.group(1).strip()
				if len(myBand) > 0:
					bandNr = roemisch[myBand]
				seiteStart = int(m3.group(2).strip())
				seiteStop = seiteStart
				zeileStart = 100
				zeileStop = 100
				if m3.group(3).find(' - ') != -1:
					seiteStop = int(m3.group(3).split(' - ')[1])
					zeileStart = int(m3.group(3).split(' - ')[0])
					zeileStop = int(m3.group(4).strip(' ,'))
					kommentar = ''
				else:
					z = m3.group(3).replace(' ', '').replace('/', '-')
					zeilen = z.split('-')
					zeileStart = int(zeilen[0])
					if len(zeilen) == 1:
						zeileStop = zeileStart
					else:
						zeileStop = int(zeilen[1])

					kommentar = m3.group(4).strip()

				myStelle = {
					'uid': len(stelle),
					'band_uid': bandNr,
					'seite_start': seiteStart,
					'seite_stop': seiteStop,
					'zeile_start': zeileStart,
					'zeile_stop': zeileStop,
					'stop_unsicher': False,
					'zerstoerung': False,
					'anmerkung': kommentar
				}

				if myStelle['zeile_start'] > 30:
					print "\t".join(["OL", str(PRIMARY), "FEHLER", "zeile_start > 30: " + str(myStelle['zeile_start']), teil])
				if myStelle['zeile_stop'] > 30:
					print "\t".join(["OL", str(PRIMARY), "FEHLER", "zeile_stop > 30: " + str(myStelle['zeile_stop']), teil])

				stelle += [myStelle]
				ort_has_stelle += [{'uid_local': PRIMARY, 'uid_foreign': myStelle['uid']}]


# Doppelte Einträge in OL zusammenführen
previousO = ort[100]
for o in ort[:]:
	previousTranslit = re.sub(r'[0-9 ]*$', '', previousO['transliteration'])
	translit = re.sub(r'[0-9 ]*$', '', o['transliteration'])

	if translit == previousTranslit and o['ort'] == previousO['ort'] and o['lokalisation'] == previousO['lokalisation']:
		# Orte stimmen überein: alle links dem o Datensatz zuweisen
		for ohs in ort_has_stelle:
			if ohs['uid_local'] == previousO['uid']:
				ohs['uid_local'] = o['uid']
		o['transliteration'] = translit
		ort.remove(previousO)
		print "\t".join(["OL", str(PRIMARY), "INFO", str(o['uid']) + u" Duplikat von " + str(previousO['uid']) + u": mergen", o['transliteration'], previousO['transliteration']])

	previousO = o




print "\n\n\n\n**** GL *******************************************************************\n"


gott = []
gott_has_stelle = []

# Tabelle GL
query = ("SELECT `PRIMARY`, NAME, ORT, EPON, BEZ, FKT, BND, SEITEZEILE, ANM from GL")
cursor.execute(query)

re3 = re.compile(r'^\s*([VI]*)\s*,*\s*([0-9]*)\s*,\s*([0-9/ -]*)\s*(.*)$')

for (PRIMARY, NAME, ORT, EPON, BEZ, FKT, BND, SEITEZEILE, ANM) in cursor:

	originalSEITEZEILE = SEITEZEILE
	stelleAnmerkung = ''
	if SEITEZEILE == '066, 011ff,;':
		# 84
		SEITEZEILE = '066, 011ff'
	elif SEITEZEILE == '264-269;':
		# 1551
		SEITEZEILE = '264, 0 - 269, 30;'
	elif SEITEZEILE == '2,7?':
		# 1178
		SEITEZEILE = '2, 7'
		stelleAnmerkung = '2,7?'
	elif SEITEZEILE == '052, 006 und 008;':
		# 2376
		SEITEZEILE = '052, 6-8'
	elif SEITEZEILE == '215, 11 (2x)-216, 1 (1':
		# 2463
		SEITEZEILE = '215, 11 - 216, 1'
	elif SEITEZEILE == '159':
		# 3266
		SEITEZEILE = '159, 0'
	elif SEITEZEILE == '149, 3:':
		# 3654
		SEITEZEILE = '149, 3'
	elif SEITEZEILE == '90, 3 (25);':
		# 4093
		SEITEZEILE = '90, 3;'
		stelleAnmerkung = '(25)'
	elif SEITEZEILE == '39, 11/f.':
		# 5487
		SEITEZEILE = '39, 11f.'
	elif SEITEZEILE == '90,3 (36)':
		# 5758
		SEITEZEILE = '90,3'
		stelleAnmerkung = '(36)'
	elif SEITEZEILE == '33,14 33,14':
		# 5791
		SEITEZEILE = '33, 14'
	elif PRIMARY == 6335:
		BND = '7'
	elif SEITEZEILE == '331,6 und 332,1':
		# 6420
		SEITEZEILE = '331, 6 - 332, 1'
	elif SEITEZEILE == '331,9 und 332,5':
		# 6421
		SEITEZEILE = '331, 9 - 332, 5'
	elif SEITEZEILE == '114,4 114,7                                                114,4':
		# 7603
		SEITEZEILE = '114, 4-7'
	elif SEITEZEILE == '47,5 47,5- 47,5':
		# 7616
		SEITEZEILE = '47, 5'
	elif SEITEZEILE == '24;4':
		# 7693
		SEITEZEILE = '24, 4'
	elif SEITEZEILE == '75,13 75,13 75,13':
		# 7875
		SEITEZEILE = '75, 13'
	elif SEITEZEILE == '54;3':
		# 8222
		SEITEZEILE = '54, 3'
	elif SEITEZEILE == '137, 008-138':
		# 8337
		SEITEZEILE = '137, 008 - 138, 10'
	elif SEITEZEILE == '201; 008':
		# 8853
		SEITEZEILE = '201, 008'
	elif SEITEZEILE == '067; 004':
		# 8918
		SEITEZEILE = '067, 004'
	elif SEITEZEILE == '018; 009':
		# 8939
		SEITEZEILE = '018, 009'
	elif PRIMARY == 9165:
		BND = '5'


	myGott = {
		'uid': PRIMARY,
		'id': PRIMARY,
		'transliteration': NAME,
		'ort': ORT,
		'eponym': EPON,
		'beziehung': BEZ,
		'funktion': FKT,
		'anmerkung': ANM
	}
	gott += [myGott]

	# gelegentlich ist der Inhalt doppelt vorhanden
	szsz = SEITEZEILE.replace(' ', '')
	halbeLaenge = int(round(len(szsz)/2))
	halberString = szsz[halbeLaenge:]
	if halberString + halberString == szsz:
		SEITEZEILE = halberString

	SEITEZEILE = SEITEZEILE.replace('.09999999999999', ', 1')
	SEITEZEILE = SEITEZEILE.replace('.300000000000001', ', 3')
	SEITEZEILE = SEITEZEILE.replace('.30000000000001', ', 3')
	SEITEZEILE = SEITEZEILE.replace('.40000000000001', ', 4')
	SEITEZEILE = SEITEZEILE.replace('.59999999999999', ', 6')
	SEITEZEILE = SEITEZEILE.replace('.699999999999999', ', 7')
	SEITEZEILE = SEITEZEILE.replace('.69999999999999', ', 7')
	SEITEZEILE = SEITEZEILE.replace('.90000000000001', ', 9')
	SEITEZEILE = SEITEZEILE.replace('.109999999999999', ', 11')
	SEITEZEILE = SEITEZEILE.replace('.119999999999999', ', 12')
	SEITEZEILE = SEITEZEILE.replace('.140000000000001', ', 14')
	SEITEZEILE = SEITEZEILE.replace('.14000000000001', ', 14')
	SEITEZEILE = SEITEZEILE.replace('.15000000000001', ', 15')
	SEITEZEILE = SEITEZEILE.replace('.18000000000001', ', 18')

	SEITEZEILE = re.sub(r'([0-9]+)\.([0-9]+)', '\\1, \\2', SEITEZEILE)
	SEITEZEILE = re.sub(r'und', ';', SEITEZEILE)

	if originalSEITEZEILE != SEITEZEILE:
		print "\t".join(["GL", str(PRIMARY), "INFO", u"Änderung SEITEZEILE", originalSEITEZEILE, SEITEZEILE])

	szs = SEITEZEILE.strip('; ').split(';')
	if len(szs) == 1 and len(szs[0]) > 1:
		sz = szs[0]
		stopUnsicher = False
		sz = sz.strip(' ,')
		komponenten = sz.split(',')
		if len(komponenten) == 1:
			# nur eine Komponente: nur eine Seitenzahl vorhanden, mit Zeile 0 ergänzen
			sz = re.sub('([0-9]*)(.*)', '\\1,0\\2', sz)
			komponenten = sz.split(',')

		if len(komponenten) > 2:
			sz = sz.replace(' ', '')
			sz = sz.replace('/', '-')
			sy = sz.split('-')
			if len(sy) == 2:
				start = szSplit(sy[0])
				stop = szSplit(sy[1])
				startSeite = start[0]
				startZeile = start[1]
				stopSeite = stop[0]
				stopZeile = stop[1]
			else:
				print "\t".join(["GL", str(PRIMARY), "FEHLER", u"SEITEZEILE, falsche Komponentenzahl", sz])
		else:
			startSeite = int(komponenten[0])
			stopSeite = startSeite
			zeilen = komponenten[1].strip()
			if zeilen.find('f') != -1:
				stopUnsicher = True
				zeilen = re.sub(r'\s*f+\.*', '', zeilen)

			zeilen = re.sub(r'[ /-]+', '-', zeilen)
			zs = zeilen.split('-')

			startZeile = int(zs[0])
			if len(zs) > 1:
				stopZeile = int(zs[1])
			else:
				stopZeile = startZeile

		band = int(BND)
		if startSeite > 0 and band > 0:
			myStelle = {
				'uid': len(stelle),
				'band_uid': band,
				'seite_start': startSeite,
				'seite_stop': stopSeite,
				'zeile_start': startZeile,
				'zeile_stop': stopZeile,
				'stop_unsicher': stopUnsicher,
				'zerstoerung': False,
				'anmerkung': stelleAnmerkung
			}
			stelle += [myStelle]

			if myStelle['zeile_start'] > 30:
				print "\t".join(["GL", str(PRIMARY), "FEHLER", "zeile_start > 30", sz])
			if myStelle['zeile_stop'] > 30:
				print "\t".join(["GL", str(PRIMARY), "FEHLER", "zeile_stop > 30", sz])

			myGott['stelle_uid'] = myStelle['uid']
		else:
			print "\t".join(["GL", str(PRIMARY), "FEHLER", u"startSeite oder Band nicht ermittelbar: Datensatz verwerfen", sz])
	else:
		print "\t".join(["GL", str(PRIMARY), "FEHLER", u"nicht genau eine Stelle in SEITEZEILE: Datensatz verwerfen", SEITEZEILE])


wort = []
wort_has_stelle = []
# Wörterbuch Berlin mit Datensatz für 'nicht belegt'
berlin = [{
	'uid': 0,
	'band': 0,
	'seite_start': 0,
	'seite_stop': 0,
	'zeile_start': 0,
	'zeile_stop': 0,
	'notiz': None
}]



print "\n\n\n\n**** WL *******************************************************************\n"

# Tabelle WL
query = ("SELECT `PRIMARY`, Transliteration, Deutsch, IDS, Weiteres, BelegstellenEdfu, BelegstellenWb, Anmerkungen FROM WL")
cursor.execute(query)

re20 = re.compile(r'^\s*([VI]*)\s*,?\s*(<?)([0-9]*)\s*,\s*([0-9/ -]*)(>?\*?)\s*(.*)$')

for (PRIMARY, Transliteration, Deutsch, IDS, Weiteres, BelegstellenEdfu, BelegstellenWb, Anmerkungen) in cursor:
	anmerkungWL = ''

	bEdfu = BelegstellenEdfu
	if bEdfu.find('zum Beispiel') == 0:
		# 1266, 1296, 2781, 2811
		bEdfu = bEdfu.replace('zum Beispiel', '')
		anmerkungWL = '(Beispiele) '
	elif bEdfu.find('<VIII, ') == 0:
		# 732, 797, 804, 816, 2247, 2312, 2319, 2331
		bEdfu = 'VIII, <' + bEdfu[7:]
	elif bEdfu == 'E VIII, 0,31, 07; 060, 07':
		# 1089, 2604
		bEdfu = 'E VIII, 031, 07; 060, 07'
	elif bEdfu == 'E VIII, 033, 01; 068, 02; 098, 02; 103; 18; 162, 05':
		# 1415, 2930
		bEdfu = 'E VIII, 033, 01; 068, 02; 098, 02; 103, 18; 162, 05'
	elif bEdfu == 'E VIII, 026, 07; 041, 05; 053, 06; 156,l 15':
		# 1491
		bEdfu = 'E VIII, 026, 07; 041, 05; 053, 06; 156, 15'

	bEdfu = bEdfu.strip('EPON; ')
	bEdfu = re.sub(r' / V', '; V', bEdfu)

	if BelegstellenEdfu != bEdfu:
		print "\t".join(["WL", str(PRIMARY), "INFO", u"Änderung BelegstellenEdfu", BelegstellenEdfu, bEdfu])

	wb = BelegstellenWb
	wbID = None
	anmerkungWB = None
	notiz = None

	if wb == 'nicht im Wb belegt':
		wbID = 0
	elif len(wb) > 0:
		if wb == 'nach II, 123, 12 - 124*':
			wb = 'nach II, 123, 12 - 124, 1'
			anmerkungWB = '*'
		elif wb == 'I, 171, 03 - 12; 18 - 21':
			# 356
			wb = 'I, 171, 03 - 12'
		elif wb == 'II, 429 - 432, 05':
			# 1358-1361
			wb = 'II, 429, 01 - 432, 05'
		elif wb == 'II, 498 - 500, 24':
			# 1418-1420
			wb = 'II, 498, 01 - 500, 24'
		elif wb == 'III, 026 - 027, 19':
			# 1441
			wb = 'III, 026,01 - 027, 19'

		if wb != BelegstellenWb:
			anmerkungWB = u'ursprünglich: ' + BelegstellenWb
			print "\t".join(["WL", str(PRIMARY), "INFO", u"Änderung BelegstellenWb", BelegstellenWb, wb])

		vornach = 0
		if wb.find('nach ') == 0 :
			vornach = 1
			wb = wb.replace('nach ', '')
		elif wb.find('vor ') == 0:
			vornach = -1
			wb = wb.replace('vor ', '')

		roemischBand = wb[0:wb.index(',')]
		wb = wb[wb.index(',') + 1:].strip()
		band = roemisch[roemischBand]

		wb = wb.replace(' -', '-').replace('- ', '-')

		if wb.find('-') != -1:
			# Range
			teile = wb.split('-')
			if len(teile) == 2:
				seiteZeile = teile[0].split(',')
				seiteStart = int(seiteZeile[0].strip())
				seiteStop = seiteStart
				zeileStart = int(seiteZeile[1].strip())

				if teile[1].find(',') != -1:
					# Komma im zweiten Teil: unterschiedliche Seiten
					seiteZeile2 = teile[1].split(',')
					seiteStop = int(seiteZeile2[0].strip())
					zeileStop = int(seiteZeile2[1].strip())
				else:
					# Range innerhalb einer Seite
					zeileStop = int(teile[1].strip())

				start = [seiteStart, zeileStart]
				stop = [seiteStart, zeileStop]

			else:
				print "\t".join(["WL", str(PRIMARY), "FEHLER", u"BelegstellenWb Formatfehler", BelegstellenWb, wb])

		else:
			# Nur eine Stelle
			start = szSplit(wb)
			stop = start

		myWB = {
			'uid': len(berlin),
			'band': band,
			'seite_start': start[0],
			'seite_stop': stop[0],
			'zeile_start': start[1],
			'zeile_stop': stop[1],
			'vornach': vornach,
			'notiz': notiz,
			'anmerkung': anmerkungWB
		}

		bereitsVorhanden = False
		for b in berlin:
			if b['seite_start'] == myWB['seite_start'] and b['seite_stop'] == myWB['seite_stop'] and b['zeile_start'] == myWB['zeile_start'] and b['zeile_stop'] == myWB['zeile_stop'] and b['notiz'] == myWB['notiz'] and b['anmerkung'] == myWB['anmerkung']:
				myWB['uid'] = b['uid']
				bereitsVorhanden = True

		if not bereitsVorhanden:
			berlin += [myWB]
		wbID = myWB['uid']



	myWort = {
		'uid': PRIMARY,
		'id': PRIMARY,
		'transliteration': Transliteration,
		'weiteres': Weiteres,
		'uebersetzung': Deutsch,
		'anmerkung': (anmerkungWL + Anmerkungen).strip(),
		'hieroglyph': IDS,
        'lemma': None,
		'wb_berlin_uid': wbID
	}
	wort += [myWort]


	bandNr = 0
	seiteStart = 0
	zerstoerung = False

	if len(bEdfu) > 0:
		belegstellen = bEdfu.split(';')
		for b in belegstellen:
			b = b.strip()

			klammer = False
			stern = False

			if b.find('%') != -1:
				zerstoerung = True
				b = b.replace('%', '').replace('&', '')

			if b.find(',') == -1:
				if seiteStart != 0:
					b = str(seiteStart) + ', ' + b
#					print "\t".join(["WL", str(PRIMARY), "INFO", u"Seitenzahl hinzugefügt", b])
				else:
					print "\t".join(["WL", str(PRIMARY), "FEHLER", u"keine Seitenzahl", b])

			m20 = re20.match(b)
			if m20:
				if len(m20.group(1)) > 0:
					bandNr = roemisch[m20.group(1).strip()]
				elif bandNr == 0:
					print "\t".join(["WL", str(PRIMARY), "FEHLER", u"fehlende Bandangabe", b])

				seiteStart = int(m20.group(3))
				seiteStop = seiteStart
				anmerkung = ''

				if m20.group(4).find(' - ') != -1:
					zeileStart = int(m20.group(4).split(' - ')[0])
					zeileStop = int(m20.group(4).split(' - ')[1])
				else:
					zeilenString = m20.group(4)
					zeilenString = zeilenString.replace('/', '-').replace(' ', '')
					zeilen = zeilenString.split('-')
					if len(zeilen) == 1:
						zeileStart = int(zeilen[0])
						zeileStop = zeileStart
					elif len(zeilen) == 2:
						zeileStart = int(zeilen[0])
						zeileStop = int(zeilen[1])
					else:
						print "\t".join(["WL", str(PRIMARY), "FEHLER", u"zu viele Komponenten in Zeilenangabe", b])

					anmerkung = m20.group(6).strip()

				if m20.group(5) == '>':
					klammer = True
				elif m20.group(5) == '>*':
					stern = True
				elif len(m20.group(5)) > 2:
						print "\t".join(["WL", str(PRIMARY), "FEHLER", u"m20.group(5) zu lang", b])

				myStelle = {
					'uid': len(stelle),
					'band_uid': bandNr,
					'seite_start': seiteStart,
					'seite_stop': seiteStop,
					'zeile_start': zeileStart,
					'zeile_stop': zeileStop,
					'anmerkung': anmerkung,
					'stop_unsicher': False,
					'zerstoerung': zerstoerung
				}
				stelle += [myStelle]

				if myStelle['zeile_start'] > 30:
					print "\t".join(["WL", str(PRIMARY), "FEHLER", "zeile_start > 30", b])
				if myStelle['zeile_stop'] > 30:
					print "\t".join(["WL", str(PRIMARY), "FEHLER", "zeile_stop > 30", b])

				wort_has_stelle += [{
					'uid_local': PRIMARY,
					'uid_foreign': myStelle['uid'],
					'schreiber_verbessert': klammer,
					'chassinat_verbessert': stern
				}]

			else:
				print "\t".join(["WL", str(PRIMARY), "FEHLER", u"keine erkennbare Seitenzahl", b])

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
				print u'INFO CSV Datei »' + filePath + u'«'
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
						print u'Zeile »' + ';'.join(row) + u'« hat weniger als 12 Spalten'

szene_bild = szene_bildDict.values()



# In MySQL einfügen
db = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
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

addRecordsToTable(berlin, 'wb_berlin')

addRecordsToTable(formular, 'formular')
addRecordsToTable(formular_has_literatur, 'formular_literatur_mm')
addRecordsToTable(photo_typ, 'photo_typ')
for p in photo:
	del(p['count'])
addRecordsToTable(photo, 'photo')
addRecordsToTable(formular_has_photo, 'formular_photo_mm')

addRecordsToTable(gott, 'gott')

addRecordsToTable(ort, 'ort')
addRecordsToTable(ort_has_stelle, 'ort_stelle_mm')

addRecordsToTable(wort, 'wort')
addRecordsToTable(wort_has_stelle, 'wort_stelle_mm')

cursor.close()
db.close()


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
print "gott: " + str(len(gott))

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
