#! /usr/bin/env python
#coding=utf-8

import re
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
band = {
	1: {'nummer': 1, 'freigegeben': False},
	2: {'nummer': 2, 'freigegeben': False},
	3: {'nummer': 3, 'freigegeben': False},
	4: {'nummer': 4, 'freigegeben': False},
	5: {'nummer': 5, 'freigegeben': True},
	6: {'nummer': 6, 'freigegeben': True},
	7: {'nummer': 7, 'freigegeben': False},
	8: {'nummer': 8, 'freigegeben': False}
}
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
	{'id': 0, 'band': 5, 'seite_start': 1, 'zeile_start': 11, 'seite_stop': 4, 'zeile_stop': 6, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 1, 'band': 5, 'seite_start': 4, 'zeile_start': 6, 'seite_stop': 7, 'zeile_stop': 4, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 2, 'band': 5, 'seite_start': 7, 'zeile_start': 7, 'seite_stop': 9, 'zeile_stop': 8, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 3, 'band': 5, 'seite_start': 9, 'zeile_start': 10, 'seite_stop': 10, 'zeile_stop': 16, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
	{'id': 4, 'band': 5, 'seite_start': 11, 'zeile_start': 4, 'seite_stop': 12, 'zeile_stop': 4, 'anmerkung': '', 'stop_unsicher': 0, 'zerstoerung': 0},
]
formular = {}
suffixe = {}
formular_has_photo = []
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
photos = {}




# Tabelle FL
query = ("SELECT `PRIMARY`, TEXTMITSUF, BAND, SEITEZEILE, TEXTOHNESU, TEXTDEUTSC, TEXTTYP, Photo, SzenenID, SekLit from FL WHERE 1=0")

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

	if Photo != originalPhoto:
		print "FL " + str(PRIMARY) + u" INFO Photo geändert: »" + originalPhoto + u"« -> »" + Photo + u"«"



	re1 = re.compile(r'[0-9]+a*')
	re2 = re.compile(r'D03_[0-9]+')
	re3 = re.compile(r'D05_[0-9]+a*')
	re4 = re.compile(r'e[0-9]+')
	# groups: 1 -> edfou, 2 -> plate, 3 -> weitere plate
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
			if photos.has_key(photoID):
				photos[photoID]['count'] += 1
			else:
				if typ == 'D05' or typ == 'D03' or typ == 'alt':
					pfad = typ + '/' + name + '.jpg'
				else:
					pfad = ''
			
				myPhoto = {
					'id': len(photos),
					'typ': typ,
					'name': name,
					'pfad': pfad,
					'count': 1
				}
				photos[photoID] = myPhoto
				
			photoRelation = {
				'formular_id': PRIMARY,
				'photo_id': photos[photoID]['id'],
				'klammern': klammern,
				'stern': stern,
				'kommentar': kommentar
			}
			formular_has_photo += [photoRelation]
		

		bildString = bildString.strip(', ')
		


	# Textposition
	myStelle = {}
	myStelle['band_id'] = band[int(BAND)]['nummer']

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
	myStelle['stop_unsicher'] = None
	myStelle['zerstoerung'] = None

	myStelle['id'] = len(stelle)
	myFormular['stelle_id'] = len(stelle)

	stelle += [myStelle]
	formular[myFormular['id']] = myFormular	
	



ort = []
ort_has_stelle = []

# Tabelle OL
query = ("SELECT `PRIMARY`, STELLE, TRANS, ORT, LOK, ANM FROM OL")
cursor.execute(query)

re1 = re.compile(r'\s*([VI]+)\s*')

for (PRIMARY, STELLE, TRANS, ORT, LOK, ANM) in cursor:
	text = TRANS
	uebersetzung = ORT
	ortsbeschreibung = LOK
	anmerkung = ANM
	
	teile = STELLE.split(';')
	band = 0
	
	for teil in teile:
		komponenten = teil.split(',')
		m1 = re1.match(komponenten[0])
		if m1:
			roem = m1.group(1)
			if roemisch.has_key(roem):
				band = roemisch[roem]



print ""
print u"FL: Transliteration mit Punkt und Folgebuchstaben:"
pprint.PrettyPrinter().pprint(suffixe)

print ""
print "FL: " + str(len(formular)) + u" Datensätze mit verlinkten Stellen"
# pprint.PrettyPrinter().pprint(formular)
# pprint.PrettyPrinter().pprint(stelle)

print ""
print "FL: " + str(len(photos)) + u" Bilder mit " + str(len(formular_has_photo)) + u" Relationen"
#pprint.PrettyPrinter().pprint(photos)
#pprint.PrettyPrinter().pprint(formular_has_photo)

db.close()