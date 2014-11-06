def gottProcessor():
	global stelle, logger, cursor

	logger.name = 'gottProcessor'
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
			logger.info("\t".join(["GL", str(PRIMARY), u"Änderung SEITEZEILE", originalSEITEZEILE, SEITEZEILE]))

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
					logger.error("\t".join(["GL", str(PRIMARY), u"SEITEZEILE, falsche Komponentenzahl", sz]))
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
					logger.error("\t".join(["GL", str(PRIMARY), "zeile_start > 30", sz]))
				if myStelle['zeile_stop'] > 30:
					logger.error("\t".join(["GL", str(PRIMARY), "zeile_stop > 30", sz]))

				myGott['stelle_uid'] = myStelle['uid']
			else:
				logger.error("\t".join(["GL", str(PRIMARY), u"startSeite oder Band nicht ermittelbar: Datensatz verwerfen", sz]))
		else:
			logger.error( "\t".join(["GL", str(PRIMARY), u"nicht genau eine Stelle in SEITEZEILE: Datensatz verwerfen", SEITEZEILE]))

	return gott
