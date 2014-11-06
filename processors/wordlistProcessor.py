def wordlistProcessor():
	global stelle, logger, cursor
	logger.name = 'wordlistProcessor'

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
			logger.info("\t".join(["WL", str(PRIMARY), u"Änderung BelegstellenEdfu", BelegstellenEdfu, bEdfu]))

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

			if "," not in wb:
				logger.error('WL ID: %s Zeichen "," in %s nicht enthalten. Bitte Belegstelle korrigieren', str(PRIMARY), wb)
				wb = 'I, 171, 03 - 12'

			if wb != BelegstellenWb:
				anmerkungWB = u'ursprünglich: ' + BelegstellenWb
				logger.info("\t".join(["WL", str(PRIMARY), u"Änderung BelegstellenWb", BelegstellenWb, wb]))

			vornach = 0
			if wb.find('nach ') == 0 :
				vornach = 1
				wb = wb.replace('nach ', '')
			elif wb.find('vor ') == 0:
				vornach = -1
				wb = wb.replace('vor ', '')

			roemischBand = wb[0:wb.index(',')]

			wb = wb[wb.index(',') + 1:].strip()
			band = getRomanian(roemischBand)

			wb = wb.replace(' -', '-').replace('- ', '-')

			if wb.find('-') != -1:
				# Range
				teile = wb.split('-')
				if len(teile) == 2:
					try:
						seiteZeile = teile[0].split(',')
						seiteStart = int(seiteZeile[0].strip())
						seiteStop = seiteStart
						zeileStart = int(seiteZeile[1].strip())
					except IndexError:
						logger.error("\t".join(['WB', 'list index out of range', str(wbID), teile[0]]))
					except ValueError:
						logger.error("\t".join(['WB', 'invalid literal', str(wbID), teile[0]]))

					if teile[1].find(',') != -1:
						# Komma im zweiten Teil: unterschiedliche Seiten
						try:
							seiteZeile2 = teile[1].split(',')
							seiteStop = int(seiteZeile2[0].strip())
							zeileStop = int(seiteZeile2[1].strip())
						except IndexError:
							logger.exception("\t".join([teile[1]]))
					else:
						# Range innerhalb einer Seite
						zeileStop = int(teile[1].strip())

					start = [seiteStart, zeileStart]
					stop = [seiteStart, zeileStop]

				else:
					logger.error("\t".join(["WL", str(PRIMARY), u"BelegstellenWb Formatfehler", BelegstellenWb, wb]))

			else:
				# Nur eine Stelle
				try:
					start = szSplit(wb)
				except IndexError:
					logger.error("\t".join(['WB', 'list index out of range', wb, str(PRIMARY)]))
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
						logger.error("\t".join(["WL", str(PRIMARY), u"keine Seitenzahl", b]))

				m20 = re20.match(b)
				if m20:
					if len(m20.group(1)) > 0:
						bandNr = getRomanian(m20.group(1).strip())
					elif bandNr == 0:
						logger.error("\t".join(["WL", str(PRIMARY), u"fehlende Bandangabe", b]))

					if (m20.group(3)):
						seiteStart = int(m20.group(3))
					else:
						logger.error("\t".join(["WL", str(PRIMARY), u"Irgendwas kaputt in m20", b]))


					seiteStop = seiteStart
					anmerkung = ''

					if m20.group(4).find(' - ') != -1:
						zeileStart = int(m20.group(4).split(' - ')[0])
						zeileStop = int(m20.group(4).split(' - ')[1])
					else:
						zeilenString = m20.group(4)
						zeilenString = zeilenString.replace('/', '-').replace(' ', '')
						zeilen = zeilenString.split('-')
						if len(zeilen) == 1 and zeilen is not u'':
							try:
								zeileStart = int(zeilen[0])
							except ValueError:
								logger.error('invalid literal for int() with base 10 %s', zeilen[0])
							zeileStop = zeileStart
						elif len(zeilen) == 2:
							zeileStart = int(zeilen[0])
							zeileStop = int(zeilen[1])
						else:
							logger.error("\t".join(["WL", str(PRIMARY), u"zu viele Komponenten in Zeilenangabe", b]))

						anmerkung = m20.group(6).strip()

					if m20.group(5) == '>':
						klammer = True
					elif m20.group(5) == '>*':
						stern = True
					elif len(m20.group(5)) > 2:
						logger.error("\t".join(["WL", str(PRIMARY), u"m20.group(5) zu lang", b]))

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
						logger.error("\t".join(["WL", str(PRIMARY), "zeile_start > 30", b]))
					if myStelle['zeile_stop'] > 30:
						logger.error("\t".join(["WL", str(PRIMARY), "zeile_stop > 30", b]))

					wort_has_stelle += [{
						'uid_local': PRIMARY,
						'uid_foreign': myStelle['uid'],
						'schreiber_verbessert': klammer,
						'chassinat_verbessert': stern
					}]

				else:
					logger.error("\t".join(["WL", str(PRIMARY), u"keine erkennbare Seitenzahl", b]))
	addRecordsToTable(berlin, 'wb_berlin')
	addRecordsToTable(wort, 'wort')
	addRecordsToTable(wort_has_stelle, 'wort_stelle_mm')
