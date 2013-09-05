#! /usr/bin/env python
#coding=utf-8
"""
Skript zur Indexierung der Edfu Daten.
Liest die Daten aus MySQL,
denormalisiert sie in Solr Dokumente
und spielt sie in Solr Index(e).

2013 Sven-S. Porst, SUB Göttingen <porst@sub.uni-goettingen.de>
"""

import re
import copy
import solr
import pprint
import time

import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
db2 = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
cursor = db.cursor()
cursor2 = db2.cursor()



intToRoman = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII'}


"""
	Konversion Römischer Zahlen von:
	http://code.activestate.com/recipes/81611-roman-numerals/
"""
numeral_map = zip(
	(1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
	('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
)

def int_to_roman(i):
	result = []
	for integer, numeral in numeral_map:
	    count = int(i / integer)
	    result.append(numeral * count)
	    i -= integer * count
	return ''.join(result)

def roman_to_int(n):
	n = unicode(n).upper()

	i = result = 0
	for integer, numeral in numeral_map:
		while n[i:i + len(numeral)] == numeral:
			result += integer
			i += len(numeral)
	return result
	
	
	

def addValueForKeyToDict (value, key, myDict):
	if not myDict.has_key(key):
		myDict[key] = []
	insertValue = value
	if value == None:
		insertValue = ''
	myDict[key] += [value]


def mergeDocIntoDoc (new, target):
	for key in new.keys():
		value = new[key]
		if type(value) == list:
			for item in value:
				addValueForKeyToDict(item, key, target)
		else:
			addValueForKeyToDict(value, key, target)



"""
	Die übergebenen Stellen dem Dokument hinzufügen.
"""
def addStellenTo (stellen, doc):
	global stellenDict, intToRoman

	for feld in ['seite_start', 'seite_stop', 'zeile_start', 'zeile_stop', 'band', 'stelle_anmerkung', 'stelle_unsicher', 'zerstoerung', 'freigegeben']:
		if not feld in doc:
			doc[feld] = []
			if feld == 'band':
				doc['bandseite'] = []
				doc['bandseitezeile'] = []
			
		for stelleID in stellen:
			stelle = stellenDict[stelleID]
			stelle['besitzer'] = doc['id']
			doc[feld] += [stelle[feld]]
			
			if feld == 'band':
				bandNummer = stelle['band']
				if intToRoman.has_key(bandNummer):
					bandSeite = intToRoman[bandNummer] + ' ' + ("%03d" % (stelle['seite_start']))
					doc['bandseite'] += [bandSeite]
					bandSeiteZeile = bandSeite + ', '
					if stelle['seite_stop'] == stelle['seite_start']:
						bandSeiteZeile += str(stelle['zeile_start'])
						if stelle['zeile_stop'] != stelle['zeile_start']:
							bandSeiteZeile += '-' + str(stelle['zeile_stop'])
					else:
						bandSeiteZeile += str(stelle['zeile_start']) + ' - ' + ("%03d" % (stelle['seite_stop'])) + ', ' + str(stelle['zeile_stop'])
					
					doc['bandseitezeile'] += [bandSeiteZeile]
		
				addSzenenForStelleToDocument(stelle, doc)



def addSzenenForStelleToDocument (stelle, doc):
	global stelleSzene, szenenDict
	if stelleSzene.has_key(stelle['sql_uid']):
		szenen = stelleSzene[stelle['sql_uid']]
		for szeneID in szenen:
			szene = copy.deepcopy(szenenDict[szeneID])
			del szene['stelle_uid']
			mergeDocIntoDoc(szene, doc)
		


"""
	Szeneninformationen laden und zwischenspeichern.
"""
szenenQuery = """
SELECT
	stelle_original.uid AS stelle_uid,
	szene.uid AS szene_uid,
	szene.nummer AS szene_nummer,
	szene.beschreibung AS szene_beschreibung,
	szene_bild.name AS szene_bild_name,
	szene_bild.dateiname AS szene_bild_dateiname,
	szene_bild.breite AS szene_bild_breite,
	szene_bild.hoehe AS szene_bild_hoehe,
	szene_bild.offset_x AS szene_bild_offset_x,
	szene_bild.offset_y AS szene_bild_offset_y,
	szene.rect AS szene_bild_rect,
	szene.polygon AS szene_bild_polygon,
	szene.koordinate_x AS szene_koordinate_x,
	szene.koordinate_y AS szene_koordinate_y,
	szene.blickwinkel AS szene_blickwinkel,
	szene.breite AS szene_breite,
	szene.hoehe AS szene_hoehe,
	szene.prozent_z AS szene_prozent_z,
	szene.grau AS szene_grau
FROM
	tx_edfu_domain_model_stelle AS stelle_original,
	tx_edfu_domain_model_szene AS szene,
	tx_edfu_domain_model_szene_bild AS szene_bild,
	tx_edfu_szene_stelle_mm AS szene_stelle,
	tx_edfu_domain_model_stelle AS stelle
WHERE
	stelle_original.band_uid = stelle.band_uid AND
	stelle_original.seite_start <= stelle.seite_stop AND
	stelle_original.seite_stop >= stelle.seite_start AND
	szene.szene_bild_uid = szene_bild.uid AND
	szene_stelle.uid_local = szene.uid AND
	szene_stelle.uid_foreign = stelle.uid 
"""

szenenDict = {}
stelleSzene = {}
currentSzeneID = None
cursor.execute(szenenQuery)
for values in cursor:
	docSzene = dict(zip(cursor.column_names, values))
	szeneUID = docSzene['szene_uid']
	stelleUID = docSzene['stelle_uid']
	if currentSzeneID != szeneUID:
		# Neue Szene
		currentSzeneID = szeneUID
		docSzene['stelle_uid'] = [stelleUID]
		szenenDict[currentSzeneID] = docSzene
	else:
		szenenDict[currentSzeneID]['stelle_uid'] += [stelleUID]
	
	if not stelleSzene.has_key(stelleUID):
		stelleSzene[stelleUID] = []
	stelleSzene[stelleUID] += [szeneUID]
	
	# Arrgh! (Ohne kleine Pause bricht die MySQL Verbindung zusammen. Unklar, warum.)
	time.sleep(0.001)




"""
	Entfernen des Suffix in Transliterationen.
	Ist bereits durch : markiert.
	: danach durch den normalen . ersetzen.
"""
suffixremover = re.compile(r'(:[^aeiou][^ ]*)')
def removeSuffix (transliteration):
	return suffixremover.sub('', transliteration).replace(':', '.')



"""
	Dokumente im Array doc an den Index schicken und den Array leeren.
"""
def submitDocs (docs, name):
	#pprint.pprint(docs)
	
	index = solr.Solr('http://localhost:8080/solr/edfu')
	index.add_many(docs)
	index.commit()

	index = solr.Solr('http://vlib.sub.uni-goettingen.de/solr/edfu')
	index.add_many(docs)
	index.commit()
	
	print str(len(docs)) + ' ' + name + u' Dokumente indexiert'
	
	

"""
	Indexe leeren.
"""
index = solr.Solr('http://localhost:8080/solr/edfu')
index.delete_query('*:*')
index = solr.Solr('http://vlib.sub.uni-goettingen.de/solr/edfu')
index.delete_query('*:*')




"""
	Erstellen von Indexdokumenten für die verschiedenen SQL Tabellen.
"""



# STELLE
stellenDict = {}

query = """
SELECT
	stelle.uid, seite_start, seite_stop, zeile_start, zeile_stop,
	anmerkung, stop_unsicher, zerstoerung,
	band.nummer, band.freigegeben,
	tempel.name
FROM
	tx_edfu_domain_model_stelle AS stelle,
	tx_edfu_domain_model_band AS band,
	tx_edfu_domain_model_tempel AS tempel
WHERE
	stelle.band_uid = band.uid AND
	band.tempel_uid = tempel.uid
"""
cursor.execute(query)

for (uid,seite_start,seite_stop,zeile_start,zeile_stop,anmerkung,stop_unsicher,zerstoerung,band,freigegeben,tempel) in cursor:
	zeile_start2 = zeile_start
	if not zeile_start:
		zeile_start2 = 0
	zeile_stop2 = zeile_stop
	if not zeile_stop:
		zeile_stop2 = 100

	doc = {
		"id": "stelle-" + str(uid),
		"typ": "stelle",
		"sql_tabelle": "tx_edfu_domain_model_stelle",
		"sql_uid": uid,
		"tempel": tempel,
		"band": band,
		"seite_start": seite_start,
		"seite_stop": seite_stop,
		"zeile_start": zeile_start2,
		"zeile_stop": zeile_stop2,
		"stelle_anmerkung": anmerkung,
		"stelle_unsicher": stop_unsicher,
		"start": band * 1000000 + seite_start * 1000 + zeile_start2,
		"stop": band * 1000000 + seite_stop * 1000 + zeile_stop2,
		"zerstoerung": zerstoerung,
		"freigegeben": freigegeben
	}
	
	stellenDict[doc['sql_uid']] = doc



# WB-BERLIN
berlinDict = {}

query = ("SELECT uid,band,seite_start,seite_stop,zeile_start,zeile_stop,notiz FROM tx_edfu_domain_model_wb_berlin")
cursor.execute(query)

for (uid,band,seite_start,seite_stop,zeile_start,zeile_stop,notiz) in cursor:
	doc = {
		"id": "wb_berlin-" + str(uid),
		"typ": "wb_berlin",
		"sql_tabelle": "tx_edfu_domain_model_wb_berlin",
		"sql_uid": uid,
		"band": band,
		"seite_start": seite_start,
		"seite_stop": seite_stop,
		"zeile_start": zeile_start,
		"zeile_stop": zeile_stop,
		"notiz": notiz
	}
	
	berlinDict[uid] = doc
	
docs = berlinDict.values()
submitDocs(docs, 'WB Berlin')
docs = []



# FORMULAR
query = ("SELECT uid,id,transliteration,uebersetzung,texttyp,stelle_uid FROM tx_edfu_domain_model_formular")
cursor.execute(query)

query2 = """
SELECT
	beschreibung, detail
FROM
	tx_edfu_formular_literatur_mm,
	tx_edfu_domain_model_literatur
WHERE
	tx_edfu_formular_literatur_mm.uid_local = %s AND
	tx_edfu_formular_literatur_mm.uid_foreign = tx_edfu_domain_model_literatur.uid
"""

query3 = """
SELECT
	formular_photo.kommentar AS kommentar,
	photo.name AS photoName,
	photo_typ.name AS typName,
	photo_typ.jahr AS photoJahr
FROM
	tx_edfu_formular_photo_mm AS formular_photo,
	tx_edfu_domain_model_photo AS photo,
	tx_edfu_domain_model_photo_typ AS photo_typ
WHERE
	formular_photo.uid_local = %s
	AND formular_photo.uid_foreign = photo.uid
	AND photo.photo_typ_uid = photo_typ.uid
"""

for (uid,id,transliteration,uebersetzung,texttyp,stelle_uid) in cursor:
	literatur = []
	cursor2.execute(query2, [str(uid)])
	for (beschreibung, detail) in cursor2:
		literatur += [beschreibung + ' : ' + detail]
	
	cursor2.execute(query3, [str(uid)])
	
	# Photos sortieren: erst nach Jahr, dann nach Nummer, dabei auch nicht offensichtlich numerische richtig handhaben
	photosDict = {}
	for (kommentar, photoName, typName, photoJahr) in cursor2:
		key = str('%04d' % photoJahr) + '-'
		try:
			key += ('%04d' % int(photoName))
		except ValueError:
			if photoName[0] == 'G':
				key += ('%04d' % int(photoName[1:]))
			elif photoName[0:4] == 'pl. ':
				try:
					key += ('%04d' % int(photoName[4:]))
				except ValueError:
					key += ('%04d' % roman_to_int(photoName[4:]))
			else:
				key += photoName
		
		photosDict[key] = {
			"typName": typName,
			"photoName": photoName,
			"photoJahr": photoJahr,
			"kommentar": kommentar
		}
	
	sortedKeys = sorted(photosDict.keys(), reverse=True)
	
	photo = []
	photo_pfad = []
	photo_kommentar = []
	for key in sortedKeys:
		photoInfo = photosDict[key]
		photo += [photoInfo["photoName"]]
		photo_pfad += [photoInfo["typName"] + '/' + photoInfo["photoName"]]
		photo_kommentar += [photoInfo["kommentar"]]
	
	doc = {
		"id": "formular-" + str(id),
		"typ": "formular",
		"sql_tabelle": "tx_edfu_domain_model_formular",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"uebersetzung": uebersetzung,
		"texttyp": texttyp,
		"stelle_id": 'stelle-' + str(stelle_uid),
		"literatur": literatur,
		"photo": photo,
		"photo_pfad": photo_pfad,
		"photo_kommentar": photo_kommentar
	}
	addStellenTo([stelle_uid], doc)
	
	doc['sort'] = stellenDict[stelle_uid]['start']
	
	docs += [doc]

submitDocs(docs, 'Formular')
docs = []



# ORT
query = ("SELECT uid,id,transliteration,ort,lokalisation,anmerkung FROM tx_edfu_domain_model_ort")
cursor.execute(query)

query4 = """
SELECT 
	uid_foreign,
	uid_local
FROM
	tx_edfu_domain_model_stelle AS stelle,
	tx_edfu_domain_model_band AS band,
	tx_edfu_ort_stelle_mm
WHERE
	uid_local = %s AND
	uid_foreign = stelle.uid AND
	stelle.band_uid = band.uid
ORDER BY 
	band.nummer,
	stelle.seite_start,
	stelle.zeile_start
"""

for (uid,id,transliteration,ort,lokalisation,anmerkung) in cursor:
	stelleIDs = []
	stellen = []
	cursor2.execute(query4, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stelleIDs += ['stelle-' + str(uid_foreign)]
		stellen += [uid_foreign]
	
	doc = {
		"id": "ort-" + str(id),
		"typ": "ort",
		"sql_tabelle": "tx_edfu_domain_model_ort",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"ort": ort,
		"lokalisation": lokalisation,
		"anmerkung": anmerkung,
		"stelle_id": stelleIDs
	}
	addStellenTo(stellen, doc)

	doc['sort'] = doc['transliteration']
	if len(stellen) > 0:
		doc['sort'] += '--' + str(stellenDict[stellen[0]]['start'])

	docs += [doc]

submitDocs(docs, 'Ort')
docs = []



# GOTT
query = ("""
SELECT
	uid,id,stelle_uid,transliteration,ort,eponym,beziehung,funktion,anmerkung
FROM
	tx_edfu_domain_model_gott
""")
cursor.execute(query)

for (uid,id,stelle_uid,transliteration,ort,eponym,beziehung,funktion,anmerkung) in cursor:
	stellen = []
	stelleIDs = []
	if stelle_uid:
		stellen = [stelle_uid]
		stelleIDs = ['stelle-' + str(stelle_uid)]
		
	doc = {
		"id": "gott-" + str(id),
		"typ": "gott",
		"sql_tabelle": "tx_edfu_domain_model_gott",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"ort": ort,
		"eponym": eponym,
		"beziehung": beziehung,
		"funktion": funktion,
		"anmerkung": anmerkung,
		"stelle_id": stelleIDs
	}
	addStellenTo(stellen, doc)
	
	doc['sort'] = doc['transliteration']
	if len(stellen) > 0:
		doc['sort'] += '--' + str(stellenDict[stelle_uid]['start'])
	
	docs += [doc]

submitDocs(docs, 'Gott')
docs = []



# WORT
query = ("SELECT uid,id,transliteration,weiteres,uebersetzung,anmerkung,hieroglyph,lemma,wb_berlin_uid FROM tx_edfu_domain_model_wort")
cursor.execute(query)

query6 = """
SELECT 
	uid_foreign,
	uid_local
FROM
	tx_edfu_domain_model_stelle AS stelle,
	tx_edfu_domain_model_band AS band,
	tx_edfu_wort_stelle_mm
WHERE
	uid_local = %s AND
	uid_foreign = stelle.uid AND
	stelle.band_uid = band.uid
ORDER BY 
	band.nummer,
	stelle.seite_start,
	stelle.zeile_start
"""

for (uid,id,transliteration,weiteres,uebersetzung,anmerkung,hieroglyph,lemma,wb_berlin_uid) in cursor:
	stelleIDs = []
	stellen = []
	cursor2.execute(query6, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stelleIDs += ['stelle-' + str(uid_foreign)]
		stellen += [uid_foreign]
	
	doc = {
		"id": "wort-" + str(id),
		"typ": "wort",
		"sql_tabelle": "tx_edfu_domain_model_wort",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"uebersetzung": uebersetzung,
		"weiteres": weiteres,
		"anmerkung": anmerkung,
		"hieroglyph": hieroglyph,
		"lemma": lemma,
		"stelle_berlin_id": wb_berlin_uid,
		"stelle_id": stelleIDs
	}
	addStellenTo(stellen, doc)
	
	doc['sort'] = doc['transliteration']
	
	# WB Berlin Daten hinzufügen
	if berlinDict.has_key(wb_berlin_uid):
		berlin = berlinDict[wb_berlin_uid]
		berlinStart = str(berlin['seite_start']) + '.' + str(berlin['zeile_start'])
		berlinStop = str(berlin['seite_stop']) + '.' + str(berlin['zeile_stop'])
		berlinString = str(berlin['band']) + ', ' + berlinStart
		if berlinStart != berlinStop:
			berlinString += '-' + berlinStop
		doc['berlin_display'] = berlinString
		copyFields = ['band', 'seite_start', 'zeile_start', 'seite_stop', 'zeile_stop', 'notiz']
		for fieldName in copyFields:
			doc['berlin_' + fieldName] = berlin[fieldName]
			
		doc['sort'] += '--' +  str(berlin['band'] * 1000000 + berlin['seite_start'] * 1000 + berlin['zeile_start'])
	
	docs += [doc]

submitDocs(docs, 'Wort')
docs = []

submitDocs(stellenDict.values(), 'Stellen')


# MySQL Verbindungen schließen
cursor.close()
cursor2.close()
db.close()
db2.close()