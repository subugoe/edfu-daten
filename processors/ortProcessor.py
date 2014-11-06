def ortProcessor():
	global stelle, logger, cursor
	logger.name = 'ortProcessor'

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
			logger.info("\t".join(["OL", str(PRIMARY), u"Änderung STELLE", originalStelle, STELLE]))


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
					logger.error("\t".join(["OL", str(PRIMARY), u"STELLE", teil]))
				else:
					myBand = m3.group(1).strip()
					if len(myBand) > 0:
						bandNr = getRomanian(myBand)
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
						logger.error("\t".join(["OL", str(PRIMARY), "zeile_start > 30: " + str(myStelle['zeile_start']), teil]))
					if myStelle['zeile_stop'] > 30:
						logger.error("\t".join(["OL", str(PRIMARY), "FEHLER", "zeile_stop > 30: " + str(myStelle['zeile_stop']), teil]))

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
			logger.info("\t".join(["OL", str(PRIMARY), str(o['uid']) + u" Duplikat von " + str(previousO['uid']) + u": mergen", o['transliteration'], previousO['transliteration']]))

		previousO = o