#! /usr/bin/env python
#coding=utf-8

import re
import copy
import pprint
import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', database='edfuprojekt')
cursor = db.cursor()


def szSplit (s):
	parts = s.replace(' ', '').split(',')
	parts = [int(parts[0]), int(parts[1])]
	
	return parts
	


roemisch = {
	'I': 1, 'II':2, 'III':3, 'IV':4, 'V':5, 'VI':6, 'VII':7, 'VIII':8
}


# Einträge für die 8 Chassinat Bände.
bandDict = {
	1: {'id': 1, 'nummer': 1, 'freigegeben': False},
	2: {'id': 2, 'nummer': 2, 'freigegeben': False},
	3: {'id': 3, 'nummer': 3, 'freigegeben': False},
	4: {'id': 4, 'nummer': 4, 'freigegeben': False},
	5: {'id': 5, 'nummer': 5, 'freigegeben': True},
	6: {'id': 6, 'nummer': 6, 'freigegeben': True},
	7: {'id': 7, 'nummer': 7, 'freigegeben': False},
	8: {'id': 8, 'nummer': 8, 'freigegeben': False}
}
band = []
# Bislang 5 szenen genutzt, manuell übertragen.
szene = [
	{'id': 1, 'nummer':1, 'beschreibung':''},
	{'id': 2, 'nummer':2, 'beschreibung':''},
	{'id': 3, 'nummer':3, 'beschreibung':''},
	{'id': 4, 'nummer':4, 'beschreibung':''},
	{'id': 5, 'nummer':5, 'beschreibung':''},
]
# Stellenzuweisungen für Szenen.
szene_has_stelle = [
	{'szene_id': 1, 'stelle_id': 0},
	{'szene_id': 2, 'stelle_id': 1},
	{'szene_id': 3, 'stelle_id': 2},
	{'szene_id': 4, 'stelle_id': 3},
	{'szene_id': 5, 'stelle_id': 4},
]
# Eiträge: Stellen für Szenen.
stelle = [
	{'id': 0, 'band_id': 5, 'seite_start': 1, 'zeile_start': 11, 'seite_stop': 4, 'zeile_stop': 6, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 1, 'band_id': 5, 'seite_start': 4, 'zeile_start': 6, 'seite_stop': 7, 'zeile_stop': 4, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 2, 'band_id': 5, 'seite_start': 7, 'zeile_start': 7, 'seite_stop': 9, 'zeile_stop': 8, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 3, 'band_id': 5, 'seite_start': 9, 'zeile_start': 10, 'seite_stop': 10, 'zeile_stop': 16, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 4, 'band_id': 5, 'seite_start': 11, 'zeile_start': 4, 'seite_stop': 12, 'zeile_stop': 4, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
]
formularDict = {}
formular = []
suffixe = {}
formular_has_literatur = [
	{'formular_id': 1, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 2, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 3, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 4, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 4, 'literatur_id': 2, 'detail': '10 (38.), u. n. 40*'},
	{'formular_id': 5, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 6, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 6, 'literatur_id': 4, 'detail': '309, n. 11'},
	{'formular_id': 6, 'literatur_id': 5, 'detail': '515, n. 135'},
	{'formular_id': 6, 'literatur_id': 3, 'detail': '145, n. 676'},
	{'formular_id': 7, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 7, 'literatur_id': 3, 'detail': '145, n. 676'},
	{'formular_id': 8, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 8, 'literatur_id': 3, 'detail': '145, n. 676'},
	{'formular_id': 9, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 9, 'literatur_id': 3, 'detail': '145, n. 676'},
	{'formular_id': 10, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 10, 'literatur_id': 3, 'detail': '145, n. 676'},
	{'formular_id': 11, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 11, 'literatur_id': 3, 'detail': '145, n. 676'},
	{'formular_id': 12, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 13, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 14, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 15, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 16, 'literatur_id': 1, 'detail': '14, n. 51'},
	{'formular_id': 17, 'literatur_id': 1, 'detail': '14, n. 51'},
]
literatur = [
	{'id': 1, 'beschreibung': 'Bedier, in: GM 162, 1998'}, 
	{'id': 2, 'beschreibung': 'Budde/Kurth, in: EB 4, 1994'},
	{'id': 3, 'beschreibung': 'Labrique, Stylistique'},
	{'id': 4, 'beschreibung': u'Aufrère, L’univers minéral I'},
	{'id': 5, 'beschreibung': u'Aufrère, L’univers minéral II'}
]


photosDict = {}
photo = []
photo_typ = []
photoTypDict = {
	'alt': {'id': 0, 'name': 'alt', 'jahr': 1999},
	'D03': {'id': 1, 'name': 'D03', 'jahr': 2003},
	'D05': {'id': 2, 'name': 'D05', 'jahr': 2005},
	'e': {'id': 3, 'name': 'e', 'jahr': 1900},
	'G': {'id': 4, 'name': 'G', 'jahr': 1950},
	'e-o': {'id': 5, 'name': 'e-o', 'jahr': 1960},
	'Labrique, Stylistique': {'id': 6, 'name': 'Labrique, Stylistique', 'jahr': 1912},
	'E. XIII': {'id': 7, 'name': 'Edfou XIII', 'jahr': 1913},
	'E. XIV': {'id': 8, 'name': 'Edfou XIV', 'jahr': 1914},
} 
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
	if not collection.has_key('id'):
		collection['id'] = len(photo_collection)
		photo_collection += [collection]
		#pprint.PrettyPrinter().pprint(collection)

	formular_has_photo_collection += [{
		'formular_id': PRIMARY,
		'photo_collection_id': collection['id']
	}]

	collection = copy.deepcopy(collectionPrototype)



print "\n\n\n\n**** FL *******************************************************************\n"



# Tabelle FL
query = ("SELECT `PRIMARY`, TEXTMITSUF, BAND, SEITEZEILE, TEXTOHNESU, TEXTDEUTSC, TEXTTYP, Photo, SzenenID, SekLit from FL")

cursor.execute(query)

for (PRIMARY, TEXTMITSUF, BAND, SEITEZEILE, TEXTOHNESU, TEXTDEUTSC, TEXTTYP, Photo, SzenenID, SekLit) in cursor:

	myFormular = {}
	myFormular['id'] = PRIMARY
	
	# Felder
	myFormular['uebersetzung'] = TEXTDEUTSC
	myFormular['texttyp'] = TEXTTYP


	# Transliteration
	r = re.findall(r'\.\w+', TEXTMITSUF)
	for i in r:
		if suffixe.has_key(i):
			suffixe[i] += 1
		else:
			suffixe[i] = 1

	myFormular['transliteration'] = re.sub(r'\.([bcdfghjklmnprstvwxyz])', ':\\1', TEXTMITSUF, re.IGNORECASE | re.UNICODE)
	
	
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
		print "FL " + str(PRIMARY) + u" INFO Photo String korrigiert"



	re1 = re.compile(r'[0-9]+a*')
	re2 = re.compile(r'D03_[0-9]+')
	re3 = re.compile(r'D05_[0-9]+a*')
	re4 = re.compile(r'e[0-9]+')
	re5 = re.compile(r'(E. [XVI]+), (pl. [DCLXVI0-9]+)')
	re6 = re.compile(r'\([^)]*\)(\s*\**)')
	re7 = re.compile(r'[DCLXVI]+')
	re8 = re.compile(r'\)\s*\**')
	re9 = re.compile(r'G[0-9]+\s*[f.]*') # Z.B. G30 oder G32 ff.
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
			# Fall 5: name der Form GXXX [ff.]
			name = re9.match(bildString).group(0)
			typ = 'G'
			bildString = bildString[len(name):]
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
			print u"FL " + str(PRIMARY) + u" ** UNKLAR **: »" + bildString + u"«"
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

				
			#print u"FL " + str(PRIMARY) + u" Bild " + typ + u"\t" + str(klammern) + u"\t" + str(stern) + u"\t" + name + u"\t" + kommentar
			
			photoID = typ + '-' + name
			if photosDict.has_key(photoID):
				photosDict[photoID]['count'] += 1
			else:
				if typ == 'D05' or typ == 'D03' or typ == 'alt':
					pfad = typ + '/' + name + '.jpg'
				else:
					pfad = ''
			
				myPhoto = {
					'id': len(photosDict),
					'photo_typ_id': photoTypDict[typ]['id'],
					'name': name,
					'count': 1
				}
				photosDict[photoID] = myPhoto
				
			collection['items'] += [photoID]
			collection['klammern'] = klammern
			collection['stern'] = stern
			collection['kommentar'] = kommentar
				
		bildString = bildString.strip(', ')
	finishCollection(PRIMARY)
	


	# Textposition
	myStelle = {}
	myStelle['band_id'] = bandDict[int(BAND)]['nummer']

	## Sonderfälle
	if PRIMARY == 3416:
		SEITEZEILE = "011, 09 - 012, 01"
		print u"FL "+ str(PRIMARY) + u" ** ÄNDERUNG in »" + SEITEZEILE + u"«"
	if PRIMARY == 9583:
		SEITEZEILE = "078, 14 / Kol. 1"
		print u"FL "+ str(PRIMARY) + u" ** ÄNDERUNG in »" + SEITEZEILE + u"«"
	if PRIMARY == 9584:
		SEITEZEILE = "078, 14 / Kol. 2"
		print u"FL "+ str(PRIMARY) + u" ** ÄNDERUNG in »" + SEITEZEILE + u"«"


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
		
	if len(kommentar) > 0:
		print "FL " + str(PRIMARY) + u" SEITEZEILE »" + SEITEZEILE + u"« KOMMENTAR »" + "; ".join(kommentar) + u"«"
		
 	if len(re.findall("[^0-9, -]", SEITEZEILE)) > 0:
 		print "FL " + str(PRIMARY) + u" SEITEZEILE »" + SEITEZEILE + u"« FEHLER"
 	
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
		print "FL " + str(PRIMARY) + " ** FEHLER SEITEZEILE: " + SEITEZEILE
	
	if result[0][0] > result[1][0]:
		print "FL " + str(PRIMARY) + " ** FEHLER SEITEN absteigend: " + SEITEZEILE
	if result[0][0] == result[1][0] and result[0][1] > result[1][1]:
		print "FL " + str(PRIMARY) + " ** FEHLER ZEILEN absteigend: " + SEITEZEILE
	
	myStelle['seite_start'] = result[0][0]
	myStelle['zeile_start'] = result[0][1]
	myStelle['seite_stop'] = result[1][0]
	myStelle['zeile_stop'] = result[1][1]
	myStelle['stop_unsicher'] = False
	myStelle['zerstoerung'] = False

	myStelle['id'] = len(stelle)
	myFormular['stelle_id'] = len(stelle)

	stelle += [myStelle]
	formularDict[myFormular['id']] = myFormular	
	



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
	elif STELLE == 'VII, 2, 4; 3, 4; 5, 2; 7, 6; 8, 2; 8, 7; 9, 7; 10, 8; 13, 2; 15, 9; 21, 9; 22, 1; 22, 11; 22, 12 (2x); 24, 2; 26, 7; 26, 8; 31, 5; 35, 9; 36, 4; 40, 11; 43, 3; 44, 5; 61, 4; 74, 17; (Gau); 88, 4; 89, 8; 100, 16; 102, 1; 105, 10; 105, 14; 108, 2; 108, 3; 111, 11; 119, 6; 120, 6; 125, 10; 126, 3; 130, 12;':
		# 939
		STELLE = 'VII, 2, 4; 3, 4; 5, 2; 7, 6; 8, 2; 8, 7; 9, 7; 10, 8; 13, 2; 15, 9; 21, 9; 22, 1; 22, 11; 22, 12 (2x); 24, 2; 26, 7; 26, 8; 31, 5; 35, 9; 36, 4; 40, 11; 43, 3; 44, 5; 61, 4; 74, 17 (Gau); 88, 4; 89, 8; 100, 16; 102, 1; 105, 10; 105, 14; 108, 2; 108, 3; 111, 11; 119, 6; 120, 6; 125, 10; 126, 3; 130, 12;'
	elif STELLE == 'VI, 105, 5; 107, 3; 107, 8; 108, 12; 143, 3; 152, 1; 152, 16; 158, 1; 169, 174, 1; 174, 17; 175, 1; 179, 8; 181, 7; 186, 4; 190, 5; 199, 2; 237, 6; 237, 10; 243, 16; 244; 13; 245, 15; 248, 5; 249, 14; 260, 3; 274, 13; 276, 7; 276, 10; 277, 4/5; 277, 14/15;':
		# 1072
		STELLE = 'VI, 105, 5; 107, 3; 107, 8; 108, 12; 143, 3; 152, 1; 152, 16; 158, 1; 169, 174, 1; 174, 17; 175, 1; 179, 8; 181, 7; 186, 4; 190, 5; 199, 2; 237, 6; 237, 10; 243, 16; 244, 13; 245, 15; 248, 5; 249, 14; 260, 3; 274, 13; 276, 7; 276, 10; 277, 4/5; 277, 14/15;'
	elif STELLE == 'VI, 278, 9; 278, 17; 280, 15; 281, 15; 283, 9; 283, 11; 287, 3; 290, 11; 297, 17; 299, 3 ([]); 303, 16; 308, 10; 315; 7; 319, 14; 324, 4; 325, 7; 332, 1; 334, 4; 349, 6; 351, 14; V, 4, 1; 7, 1; 13, 12; 31, 5; 31, 6; 36, 2; 38, 11; 39, 10; 40, 4; 41, 2; 44, 11; 50, 12; 55, 1; 56, 11; 58, 15, 16;':
		# 1073
		STELLE = 'VI, 278, 9; 278, 17; 280, 15; 281, 15; 283, 9; 283, 11; 287, 3; 290, 11; 297, 17; 299, 3 ([]); 303, 16; 308, 10; 315, 7; 319, 14; 324, 4; 325, 7; 332, 1; 334, 4; 349, 6; 351, 14; V, 4, 1; 7, 1; 13, 12; 31, 5; 31, 6; 36, 2; 38, 11; 39, 10; 40, 4; 41, 2; 44, 11; 50, 12; 55, 1; 56, 11; 58, 15, 16;'
	elif STELLE == 'VIII, <23, 2>;':
		# 1198
		STELLE = 'VIII, 23, 2 (<23, 2>)'
	
	if STELLE != originalStelle:
		print "OL " + str(PRIMARY) + u" INFO STELLE String angepaßt"


	myOrt = {
		'id': PRIMARY,
		'transliteration': TRANS,
		'uebersetzung': ORT,
		'ortsbeschreibung': LOK,
		'anmerkung': ANM
	}
	ort += [myOrt]

	
	teile = STELLE.strip('; ').split(';')
	bandNr = 0
	
	for teil in teile:
		if len(teil.strip()) > 0:
			m3 = re3.match(teil)
			if not m3:
				print 'FAIL ' + str(PRIMARY) + ': ' + teil
			else:
				myBand = m3.group(1).strip()
				if len(myBand) > 0:
					bandNr = roemisch[myBand]
				seite = int(m3.group(2).strip())
				z = m3.group(3).replace(' ', '').replace('/', '-')
				zeilen = z.split('-')
				zeileStart = int(zeilen[0])
				if len(zeilen) == 1:
					zeileStop = zeileStart
				else:
					zeileStop = int(zeilen[1])
				
				kommentar = m3.group(4).strip()

				myStelle = {
					'id': len(stelle),
					'band_id': bandNr,
					'seite_start': seite,
					'seite_stop': seite,
					'zeile_start': zeileStart,
					'zeile_stop': zeileStop,
					'stop_unsicher': False,
					'zerstoerung': False,
					'anmerkung': kommentar
				}
				
				stelle += [myStelle]
				ort_has_stelle += [{'ort_id': PRIMARY, 'stelle_id': myStelle['id']}]
			

# Doppelte Einträge in OL zusammenführen
previousO = ort[100]
for o in ort[:]:
	previousTranslit = re.sub(r'[0-9 ]*$', '', previousO['transliteration'])
	translit = re.sub(r'[0-9 ]*$', '', o['transliteration'])

	if translit == previousTranslit and o['uebersetzung'] == previousO['uebersetzung'] and o['ortsbeschreibung'] == previousO['ortsbeschreibung']:
		# Orte stimmen überein: alle links dem o Datensatz zuweisen
		for ohs in ort_has_stelle:
			if ohs['ort_id'] == previousO['id']:
				ohs['ort_id'] = o['id']
		o['transliteration'] = translit
		ort.remove(previousO)	
		print 'OL ' + str(o['id']) + ': DUPLIKAT von ' + str(previousO['id']) + '(' + o['transliteration'] + '/' +previousO['transliteration'] + '); mergen in ' + str(o['id'])
		
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
	if SEITEZEILE == '066, 011ff,;':
		# 84
		SEITEZEILE = '066, 011ff'
	elif SEITEZEILE == '264-269;':
		# 1551
		SEITEZEILE = '264, 0-269, 100;'
	elif SEITEZEILE == '2,7?':
		# 1178
		SEITEZEILE = '2, 7'
		ANM = '2,7?'
	elif SEITEZEILE == '052, 006 und 008;':
		# 2376
		SEITEZEILE = '052, 006; 052, 008'
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
		ANM = '(25)'
	elif SEITEZEILE == '39, 11/f.':
		# 5487
		SEITEZEILE = '39, 11f.'
	elif SEITEZEILE == '90,3 (36)':
		# 5758
		SEITEZEILE = '90,3'
		ANM = '(36)'
	elif SEITEZEILE == '33,14 33,14':
		# 5791
		SEITEZEILE = '33, 14'
	elif PRIMARY == 6335:
		BND = '7'
	elif SEITEZEILE == '114,4 114,7                                                114,4':
		# 7603
		SEITEZEILE = '114,4; 114,7'
	elif SEITEZEILE == '24;4':
		# 7693
		SEITEZEILE == '24, 4'
	elif SEITEZEILE == '75,13 75,13 75,13':
		# 7875
		SEITEZEILE = '75, 13'
	elif SEITEZEILE == '54;3':
		# 8222
		SEITEZEILE = '54, 3'
	elif PRIMARY == 9165:
		BND = '5'
	
	
	myGott = {
		'id': PRIMARY,
		'transliteration': NAME,
		'ort': ORT,
		'eponym': EPON,
		'beziehung': BEZ,
		'funktion': FKT,
	}
	gott += [myGott]
	
	# gelegentlich ist der Inhalt doppelt vorhanden
	szsz = SEITEZEILE.replace(' ', '')
	halbeLaenge = int(round(len(szsz)/2))
	halberString = szsz[halbeLaenge:]
	if halberString + halberString == szsz:
		SEITEZEILE = halberString
	
	SEITEZEILE = SEITEZEILE.replace('.09999999999999', ', 1')
	SEITEZEILE = SEITEZEILE.replace('.30000000000001', ', 3')
	SEITEZEILE = SEITEZEILE.replace('.40000000000001', ', 4')
	SEITEZEILE = SEITEZEILE.replace('.59999999999999', ', 6')
	SEITEZEILE = SEITEZEILE.replace('.69999999999999', ', 7')
	SEITEZEILE = SEITEZEILE.replace('.90000000000001', ', 9')
	SEITEZEILE = SEITEZEILE.replace('.109999999999999', ', 11')
	SEITEZEILE = SEITEZEILE.replace('.119999999999999', ', 12')
	SEITEZEILE = SEITEZEILE.replace('.14000000000001', ', 14')
	SEITEZEILE = SEITEZEILE.replace('.15000000000001', ', 15')
	SEITEZEILE = SEITEZEILE.replace('.18000000000001', ', 18')

	SEITEZEILE = re.sub(r'([0-9]+)\.([0-9]+)', '\\1, \\2', SEITEZEILE)
	SEITEZEILE = re.sub(r'und', ';', SEITEZEILE)
	
	if originalSEITEZEILE != SEITEZEILE:
		print "GL " + str(PRIMARY) + u" INFO STELLE String angepaßt: »" + originalSEITEZEILE + u"« -> »" + SEITEZEILE + u"«"
		
	szs = SEITEZEILE.strip('; ').split(';')
	if len(SEITEZEILE) > 0:
		for sz in szs:
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
					print "GL " + str(PRIMARY) + ": falsche Komponentenzahl " + sz
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
	
			if startSeite:
				myStelle = {
					'id': len(stelle),
					'band_id': int(BND),
					'seite_start': startSeite,
					'seite_stop': stopSeite,
					'zeile_start': startZeile,
					'zeile_stop': stopZeile,
					'stop_unsicher': stopUnsicher,
					'zerstoerung': False,
					'anmerkung': ANM
				}
				stelle += [myStelle]
				
				gott_has_stelle += [{
					'gott_id': PRIMARY,
					'stelle_id': myStelle['id']
				}]


wort = []
wort_has_stelle = []
# Wörterbuch Berlin mit Datensatz für 'nicht belegt'
berlin = [{
	'id': 0,
	'band': 0,
	'seite_start': 0,
	'seite_stop': 0,
	'zeile_start': 0,
	'zeile_stop': 0,
	'zweifel': False
}]



print "\n\n\n\n**** WL *******************************************************************\n"

# Tabelle WL
query = ("SELECT `PRIMARY`, Transliteration, Deutsch, IDS, Weiteres, BelegstellenEdfu, BelegstellenWb, Anmerkungen FROM WL")
cursor.execute(query)

re20 = re.compile(r'^\s*([VI]*)\s*,?\s*(<?)([0-9]*)\s*,\s*([0-9/ -]*)(>?\*?)\s*(.*)$')

for (PRIMARY, Transliteration, Deutsch, IDS, Weiteres, BelegstellenEdfu, BelegstellenWb, Anmerkungen) in cursor:
	bEdfu = BelegstellenEdfu.strip('; ')
	bEdfu = re.sub(r' / V', '; V', bEdfu)

	if bEdfu == 'V, 233. 6':
		# 921
		bEdfu = 'V, 233, 6'
	elif bEdfu == 'VI, 148, <7>; 11':
		# 1023
		bEdfu = 'VI, <148, 7>; 11'
	elif bEdfu == 'VII, 216,10; 217,7; 8; 246,2; VII; 216,9; 217,1; 224,5; VII, 216, 8':
		# 2144
		bEdfu = 'VII, 216,10; 217,7; 8; 246,2; VII, 216,9; 217,1; 224,5; VII, 216, 8'
	elif bEdfu == 'V, 15, 7; VI, 133, 8; 227, 5; VII, 200, 6; /; 284, 4':
		# 2156
		bEdfu = 'V, 15, 7; VI, 133, 8; 227, 5; VII, 200, 6; 284, 4'
	elif bEdfu == 'VI, 112. 1; VII, 122, 9':
		# 2158
		bEdfu = 'VI, 112, 1; VII, 122, 9'
	elif bEdfu == '128, 5/6':
		# 2468
		bEdfu = 'VI, 128, 5/6'
	elif bEdfu == 'VII, 197,7; 198,<2>; 5; 6; 9':
		# 2593
		bEdfu = 'VII, 197,7; <198, 2>; 5; 6; 9'
	elif bEdfu == 'VI, 176,4; 5; 6; 7; ???323,7; 8; 9; 11; 324,1; 4; 5; 329,1???; VII, ???26,7; 257,2???; VI, 118,9; 122,13; 123,9; 127,7; 134,6; V, 37,4; 39,12; 40,7; 10':
		# 2813
		bEdfu = 'VI, 176,4; 5; 6; 7; 323,7 ???; 8 ???; 9 ???; 11; 324,1; 4; 5; 329,1 ???; VII, 26,7 ???; 257,2 ???; VI, 118,9; 122,13; 123,9; 127,7; 134,6; V, 37,4; 39,12; 40,7; 10'
	elif bEdfu == 'V, 130,10; 136,4; 349,3; 4; 8; 350,2; 7; 8; 353,3; 355,6; 359,4; VI, 169, 8; 242, 11; VI, ???18,7; 10; 169,8; 320,12; 321,4; 5; 328,18???; VI, 125, 1; 135, 3; VI, 112, 7; 114, 8; 116, 4; V, 12, 8; 10; 37, 11':
		# 2815
		bEdfu = 'V, 130,10; 136,4; 349,3; 4; 8; 350,2; 7; 8; 353,3; 355,6; 359,4; VI, 169, 8; 242, 11; VI, 18,7 ???; 10; 169,8; 320,12; 321,4; 5; 328,18???; VI, 125, 1; 135, 3; VI, 112, 7; 114, 8; 116, 4; V, 12, 8; 10; 37, 11'
	elif bEdfu == 'V, 130, 1 / kol. 14':
		# 3173
		bEdfu = 'V, 130, 1 (kol. 14)'
	elif bEdfu == 'VIII, 125, 1-4; Z. 14':
		# 3835
		bEdfu = 'VIII, 125, 1-4 (Z. 14)'
	elif bEdfu == u'VII, 107, 17 (Pl.); VI, &344, 16& ???':
		# 3914
		bEdfu = u'VII, 107, 17 (Pl.); VI, %344, 16& ???'
	elif bEdfu == 'V, 100, 7; 251, 6; VIII; 129, 9; 10; 130, 7':
		# 4022
		bEdfu = 'V, 100, 7; 251, 6; VIII, 129, 9; 10; 130, 7'
	elif bEdfu == 'V, <30, 2>; 87, 6; 120, 8; 217, 6; VIII; 37, 2; 38, 4':
		# 4363
		bEdfu = 'V, <30, 2>; 87, 6; 120, 8; 217, 6; VIII, 37, 2; 38, 4'
		

	if BelegstellenEdfu != bEdfu:
		print "WL " + str(PRIMARY) + u" INFO BelegstelleEdfu String angepaßt: »" + BelegstellenEdfu + u"« -> »" + bEdfu + u"«"


	wb = BelegstellenWb
	wbID = None
	anmerkung = None
	if wb == 'nicht im Wb belegt':
		wbID = 0
	elif len(wb) > 0:
		wb = wb.replace('nach Wb I7', 'nach Wb I')
		wb = wb.replace('Wb, I', 'Wb I,').replace(',,', ',')
		wb = wb.replace('X', '10').replace('x', '10')
		wb = wb.replace('o', '0')
		if wb == 'Wb I, 2, 3 - 4':
			# 824
			wb = 'Wb I, 2, 3-4'
		elif wb == 'Wb I, 483, x - 484, 11':
			# 1080
			wb = 'Wb I, 483, 10 - 484, 11'
		elif wb == 'Wb I, 84, 15 - 85, o':
			# 1195
			wb = 'Wb I, 84, 15 - 85, 0'
		elif wb == 'Wb I, 419, 14 - 420, O':
			# 1633
			wb = 'Wb I, 419, 14 - 420, 0'
		elif wb == 'Wb I, 54, (11)-(12)':
			# 2898
			wb = 'Wb I, 54, 11-12'
		elif wb == 'Wb I, 104':
			# 3079-3094
			wb = 'Wb I, 104, 0'
		elif wb == 'Wb I, 344, 7-13???':
			# 4226
			wb = 'Wb I, 344, 7-13'

		if wb != BelegstellenWb:
			anmerkung = u'ursprünglich: ' + BelegstellenWb
			print "WL " + str(PRIMARY) + u" INFO BelegstellenWb String angepaßt: »" + BelegstellenWb + u"« -> »" + wb + u"«"


		zweifel = False
		if wb.find('nach W') == 0:
			zweifel = True
		
		wb = wb.replace('nach Wb I, ', '').replace('Wb I, ', '')
		
		if wb.find(' - ') != -1:
			# Range über mehrere Seiten
			teile = wb.split(' - ')
			start = szSplit(teile[0])
			stop = szSplit(teile[1])
		elif wb.find('-') != -1:
			# Range über mehrere Zeilen
			teile = wb.split(',')
			seite = int(teile[0].strip())
			zeilen = teile[1].strip().split('-')
			start = [seite, int(zeilen[0].strip())]
			stop = [seite, int(zeilen[1].strip())]
		else:
			# Nur eine Stelle
			start = szSplit(wb)
			stop = start
			
		myWB = {
			'id': len(berlin),
			'band': 1,
			'seite_start': start[0],
			'seite_stop': stop[0],
			'zeile_start': start[1],
			'zeile_stop': stop[1],
			'zweifel': zweifel,
			'anmerkung': anmerkung
		}
		
		bereitsVorhanden = False
		for b in berlin:
			if b['seite_start'] == myWB['seite_start'] and b['seite_stop'] == myWB['seite_stop'] and b['zeile_start'] == myWB['zeile_start'] and b['zeile_stop'] == myWB['zeile_stop'] and b['zweifel'] == myWB['zweifel'] and b['anmerkung'] == myWB['anmerkung']:
				myWB['id'] = b['id']
				print 'WL ' + str(PRIMARY) + ' INFO Berlin Datensatz ' + str(b['id']) + ' nachgenutzt'
				bereitsVorhanden = True
		
		if not bereitsVorhanden:
			berlin += [myWB]
		wbID = myWB['id']



	myWort = {
		'id': PRIMARY,
		'transliteration': Transliteration,
		'weiteres': Weiteres,
		'uebersetzung': Deutsch,
		'anmerkung': Anmerkungen,
		'hieroglyph': IDS,
		'berlin_id': wbID
	}
	wort += [myWort]
	
	
	bandNr = 0
	seite = 0
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
				if seite != 0:
					b = str(seite) + ', ' + b
					print 'WL ' + str(PRIMARY) + u' INFO Seitenzahl hinzugefügt »' + b + u'«'
				else:
					print 'WL ' + str(PRIMARY) + u' FEHLER Keine Seitenzahl? »' + b + u'«'

			m20 = re20.match(b)
			if m20:
				if len(m20.group(1)) > 0:
					bandNr = roemisch[m20.group(1).strip()]
				elif bandNr == 0:
					print 'WL ' + str(PRIMARY) + ': fehlende Bandangabe'
				
				seite = int(m20.group(3))
				
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
					print 'WL ' + str(PRIMARY) + u': zu viele Komponenten in Zeilenangabe »' + b + u"«"
		
				anmerkung = m20.group(6).strip()
				
				if m20.group(5) == '>':
					klammer = True
				elif m20.group(5) == '>*':
					stern = True


				myStelle = {
					'id': len(stelle),
					'band_id': bandNr,
					'seite_start': seite,
					'seite_stop': seite,
					'zeile_start': zeileStart,
					'zeile_stop': zeileStop,
					'anmerkung': anmerkung,
					'stop_unsicher': False,
					'zerstoerung': zerstoerung
				}
				stelle += [myStelle]
				
				wort_has_stelle += [{
					'stelle_id': myStelle['id'],
					'wort_id': PRIMARY,
					'schreiber_verbessert': klammer,
					'chassinat_verbessert': stern
				}]
				
			else:
				print 'WL ' + str(PRIMARY) + u': keine erkennbare Seitenzahl »' + b + u'«'

db.close()



for myCollection in photo_collection:
	for item in myCollection['items']:
		entry = {
			'photo_collection_id': myCollection['id'],
			'photo_id': photosDict[item]['id']
		}
		if not entry in photo_collection_has_photo:
			photo_collection_has_photo += [entry]
	del myCollection['items']
	
for myPhoto in photosDict.itervalues():
	photo += [myPhoto]

for myPhotoTyp in photoTypDict.itervalues():
	photo_typ += [myPhotoTyp]
	
for myFormular in formularDict.itervalues():
	formular += [myFormular]
	
for myBand in bandDict.itervalues():
	band += [myBand]


# In MySQL einfügen
db = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
cursor = db.cursor()

add_band = ('INSERT INTO band (`id`, nummer, freigegeben) VALUES (%(id)s, %(nummer)s, %(freigegeben)s)')
for b in band:
	cursor.execute(add_band, b)
db.commit()


add_berlin = ('INSERT INTO berlin (`id`, band, seite_start, zeile_start, seite_stop, zeile_stop, zweifel) VALUES (%(id)s, %(band)s, %(seite_start)s, %(zeile_start)s, %(seite_stop)s, %(zeile_stop)s, %(zweifel)s)')
for b in berlin:
	cursor.execute(add_berlin, b)
db.commit()

add_formular = ('INSERT INTO formular (`id`, stelle_id, transliteration, uebersetzung, texttyp) VALUES (%(id)s, %(stelle_id)s, %(transliteration)s, %(uebersetzung)s, %(texttyp)s)')
for b in formular:
	cursor.execute(add_formular, b)
db.commit()

add_formular_has_literatur = ('INSERT INTO formular_has_literatur (formular_id, literatur_id, detail) VALUES (%(formular_id)s, %(literatur_id)s, %(detail)s)')
for b in formular_has_literatur:
	cursor.execute(add_formular_has_literatur, b)
db.commit()

add_formular_has_photo_collection = ('INSERT INTO formular_has_photo_collection (formular_id, photo_collection_id) VALUES (%(formular_id)s, %(photo_collection_id)s)')
for b in formular_has_photo_collection:
	cursor.execute(add_formular_has_photo_collection, b)
db.commit()

add_gott = ('INSERT INTO gott (`id`, transliteration, ort, eponym, beziehung, funktion) VALUES (%(id)s, %(transliteration)s, %(ort)s, %(eponym)s, %(beziehung)s, %(funktion)s)')
for b in gott:
	cursor.execute(add_gott, b)
db.commit()

add_gott_has_stelle = ('INSERT INTO gott_has_stelle (gott_id, stelle_id) VALUES (%(gott_id)s, %(stelle_id)s)')
for b in gott_has_stelle:
	cursor.execute(add_gott_has_stelle, b)
db.commit()

add_literatur = ('INSERT INTO literatur (`id`, beschreibung) VALUES (%(id)s, %(beschreibung)s)')
for b in literatur:
	cursor.execute(add_literatur, b)
db.commit()

add_ort = ('INSERT INTO ort (`id`, transliteration, uebersetzung, ortsbeschreibung, anmerkung) VALUES (%(id)s, %(transliteration)s, %(uebersetzung)s, %(ortsbeschreibung)s, %(anmerkung)s)')
for b in ort:
	cursor.execute(add_ort, b)
db.commit()

add_ort_has_stelle = ('INSERT INTO ort_has_stelle (ort_id, stelle_id) VALUES (%(ort_id)s, %(stelle_id)s)')
for b in ort_has_stelle:
	cursor.execute(add_ort_has_stelle, b)
db.commit()

add_photo_typ = ('INSERT INTO photo_typ (`id`, name, jahr) VALUES (%(id)s, %(name)s, %(jahr)s)')
for b in photo_typ:
	cursor.execute(add_photo_typ, b)
db.commit()

add_photo = ('INSERT INTO photo (`id`, photo_typ_id, name) VALUES (%(id)s, %(photo_typ_id)s, %(name)s)')
for b in photo:
	cursor.execute(add_photo, b)
db.commit()

add_photo_collection = ('INSERT INTO photo_collection (`id`, klammern, stern, kommentar) VALUES (%(id)s, %(klammern)s, %(stern)s, %(kommentar)s)')
for b in photo_collection:
	cursor.execute(add_photo_collection, b)
db.commit()

add_photo_collection_has_photo = ('INSERT INTO photo_collection_has_photo (photo_collection_id, photo_id) VALUES (%(photo_collection_id)s, %(photo_id)s)')
for b in photo_collection_has_photo:
	cursor.execute(add_photo_collection_has_photo, b)
db.commit()

add_stelle = ('INSERT INTO stelle (`id`, band_id, seite_start, zeile_start, seite_stop, zeile_stop, anmerkung, stop_unsicher, zerstoerung) VALUES (%(id)s, %(band_id)s, %(seite_start)s, %(zeile_start)s, %(seite_stop)s, %(zeile_stop)s, %(anmerkung)s, %(stop_unsicher)s, %(zerstoerung)s)')
for b in stelle:
	cursor.execute(add_stelle, b)
db.commit()

add_szene = ('INSERT INTO szene (`id`, nummer, beschreibung) VALUES (%(id)s, %(nummer)s, %(beschreibung)s)')
for b in szene:
	cursor.execute(add_szene, b)
db.commit()

add_szene_has_stelle = ('INSERT INTO szene_has_stelle (szene_id, stelle_id) VALUES (%(szene_id)s, %(stelle_id)s)')
for b in szene_has_stelle:
	cursor.execute(add_szene_has_stelle, b)
db.commit()

add_wort = ('INSERT INTO wort (`id`, transliteration, weiteres, uebersetzung, anmerkung, hieroglyph, berlin_id) VALUES (%(id)s, %(transliteration)s, %(weiteres)s, %(uebersetzung)s, %(anmerkung)s, %(hieroglyph)s, %(berlin_id)s)')
for b in wort:
	cursor.execute(add_wort, b)
db.commit()

add_wort_has_stelle = ('INSERT INTO wort_has_stelle (wort_id, stelle_id, schreiber_verbessert, chassinat_verbessert) VALUES (%(wort_id)s, %(stelle_id)s, %(schreiber_verbessert)s, %(chassinat_verbessert)s)')
for b in wort_has_stelle:
	cursor.execute(add_wort_has_stelle, b)
db.commit()

db.close()	





"""
print "\n\n**** band ****"
pprint.PrettyPrinter().pprint(band)
print "\n\n**** formular ****"
pprint.PrettyPrinter().pprint(formular)
print "\n\n**** stelle ****"
pprint.PrettyPrinter().pprint(stelle)
print "\n\n**** szene ****"
pprint.PrettyPrinter().pprint(szene)
print "\n\n**** szene_has_stelle ****"
pprint.PrettyPrinter().pprint(szene_has_stelle)
print "\n\n**** formular_has_photo_collection ****"
pprint.PrettyPrinter().pprint(formular_has_photo_collection)
print "\n\n**** photo_collection ****"
pprint.PrettyPrinter().pprint(photo_collection)
print "\n\n**** photo_collection_has_photo ****"
pprint.PrettyPrinter().pprint(photo_collection_has_photo)
print "\n\n**** photo ****"
pprint.PrettyPrinter().pprint(photo)
print "\n\n**** ort ****"
pprint.PrettyPrinter().pprint(ort)
print "\n\n**** ort_has_stelle ****"
pprint.PrettyPrinter().pprint(ort_has_stelle)
print "\n\n**** gott ****"
pprint.PrettyPrinter().pprint(gott)
print "\n\n**** gott_has_stelle ****"
pprint.PrettyPrinter().pprint(gott_has_stelle)
print "\n\n**** wort ****"
pprint.PrettyPrinter().pprint(wort)
print "\n\n**** wort_has_stelle ****"
pprint.PrettyPrinter().pprint(wort_has_stelle)
print "\n\n**** berlin ****"
pprint.PrettyPrinter().pprint(berlin)
"""



print ""
print u"FL: Transliteration mit Punkt und Folgebuchstaben:"
pprint.PrettyPrinter().pprint(suffixe)

print ""
print "FL: Datensätze und Stellen"
print "formular: " + str(len(formular)) 
print "stelle: " + str(len(stelle))
print "szene: " + str(len(szene))
print "szene_has_stelle: " + str(len(szene_has_stelle))

print ""
print "FL: Bilder, Sammlungen und Relationen"
print "photo: " + str(len(photo))
print "photo_collection_has_photo " + str(len(photo_collection_has_photo))
print "photo_collection " + str(len(photo_collection))
print "formular_has_photo_collection " + str(len(formular_has_photo_collection))

print ""
print "OL"
print "ort: " + str(len(ort))
print "ort_has_stelle: " + str(len(ort_has_stelle))

print ""
print "GL"
print "gott: " + str(len(gott))
print "gott_has_stelle: " + str(len(gott_has_stelle))

print ""
print "WL"
print "wort: " + str(len(wort))
print "wort_has_stelle: " + str(len(wort_has_stelle))
print "berlin: " + str(len(berlin))


