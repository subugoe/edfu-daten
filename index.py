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

import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
db2 = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
db3 = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
cursor = db.cursor()
cursor2 = db2.cursor()
cursor3 = db3.cursor() # für szenen



intToRoman = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII'}


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
					bandseiteString = intToRoman[bandNummer] + ' ' + str(stelle['seite_start'])
					doc['bandseite'] += [bandseiteString]
					doc['bandseitezeile'] += [bandseiteString + ', ' + str(stelle['zeile_start'])]
		
				addSzenenForStelleToDocument(stelle, doc)



"""
	Die relevanten Szenen für die Stelle dem Dokument hinzufügen.
"""
szenenQuery = """
SELECT
	szene.uid AS szene_uid,
	szene.nummer AS szene_nummer,
	szene.beschreibung AS szene_beschreibung,
	szene_bild.name AS szene_bild_name,
	szene.rect AS szene_bild_rect,
	szene.polygon AS szene_bild_polygon,
	szene.koordinateX AS szene_koordinateX,
	szene.koordinateY AS szene_koordinateY,
	szene.blickwinkel AS szene_blickwinkel,
	szene.breite AS szene_breite,
	szene.hoehe AS szene_hoehe,
	szene.prozentZ AS szene_prozentZ,
	szene.grau AS szene_grau
FROM
	tx_edfu_domain_model_stelle AS stelle_original,
	tx_edfu_domain_model_szene AS szene,
	tx_edfu_domain_model_szene_bild AS szene_bild,
	tx_edfu_szene_stelle_mm AS szene_stelle,
	tx_edfu_domain_model_stelle AS stelle
WHERE
	stelle_original.uid = %s AND
	stelle_original.band_uid = stelle.band_uid AND
	stelle_original.seite_start <= stelle.seite_stop AND
	stelle_original.seite_stop >= stelle.seite_start AND
	szene.szene_bild_uid = szene_bild.uid AND
	szene_stelle.uid_local = szene.uid AND
	szene_stelle.uid_foreign = stelle.uid 
"""
def addSzenenForStelleToDocument (stelle, document):
	cursor3.execute(szenenQuery, [str(stelle['sql_uid'])])
	for values3 in cursor3:
		docSzene = dict(zip(cursor3.column_names, values3))
		mergeDocIntoDoc(docSzene, document)



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
def submitDocs (name):
	global docs
	#pprint.pprint(docs)
	
	index = solr.Solr('http://localhost:8080/solr/edfu')
	index.add_many(docs)
	index.commit()

	index = solr.Solr('http://vlib.sub.uni-goettingen.de/solr/edfu')
	index.add_many(docs)
	index.commit()
	
	print str(len(docs)) + ' ' + name + u' Dokumente indexiert'
	docs = []
	
	

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
SELECT tx_edfu_domain_model_stelle.uid,seite_start,seite_stop,zeile_start,zeile_stop,anmerkung,stop_unsicher,zerstoerung,nummer,freigegeben
FROM tx_edfu_domain_model_stelle,tx_edfu_domain_model_band
WHERE tx_edfu_domain_model_stelle.band_uid = tx_edfu_domain_model_band.uid
"""
cursor.execute(query)

for (uid,seite_start,seite_stop,zeile_start,zeile_stop,anmerkung,stop_unsicher,zerstoerung,band,freigegeben) in cursor:
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

docs = stellenDict.values()
submitDocs('Stellen')



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
submitDocs('WB Berlin')



# FORMULAR
query = ("SELECT uid,transliteration,uebersetzung,texttyp,stelle_uid FROM tx_edfu_domain_model_formular")
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
	tx_edfu_domain_model_photo.name AS photoName,
	tx_edfu_domain_model_photo_typ.name AS typName,
	tx_edfu_domain_model_photo_typ.jahr AS photoJahr,
	klammern,
	stern,
	kommentar,
	tx_edfu_domain_model_photo_collection.uid AS collectionID
FROM
	tx_edfu_formular_photo_collection_mm,
	tx_edfu_domain_model_photo_collection,
	tx_edfu_photo_collection_photo_mm,
	tx_edfu_domain_model_photo,
	tx_edfu_domain_model_photo_typ
WHERE
	tx_edfu_formular_photo_collection_mm.uid_local = %s
	AND tx_edfu_formular_photo_collection_mm.uid_foreign = tx_edfu_domain_model_photo_collection.uid
	AND tx_edfu_photo_collection_photo_mm.uid_local = tx_edfu_domain_model_photo_collection.uid
	AND tx_edfu_photo_collection_photo_mm.uid_foreign = tx_edfu_domain_model_photo.uid
	AND tx_edfu_domain_model_photo.photo_typ_uid = tx_edfu_domain_model_photo_typ.uid
ORDER BY
	collectionID ASC,
	photoJahr DESC,
	photoName DESC
"""


for (uid,transliteration,uebersetzung,texttyp,stelle_uid) in cursor:
	literatur = []
	cursor2.execute(query2, [str(uid)])
	for (beschreibung, detail) in cursor2:
		literatur += [beschreibung + ' : ' + detail]
	
	photoCollections = {}
	photos = []
	cursor2.execute(query3, [str(uid)])
	for (photoName, typName, photoJahr, klammern, stern, kommentar, collectionID) in cursor2:
		photoPfad = typName + '/' + photoName
		photos += [photoName]
		if not photoCollections.has_key(collectionID):
			photoCollections[collectionID] = {'klammern': klammern, 'stern': stern, 'photos': [], 'photoPfade': [], 'kommentar': kommentar}
		photoCollections[collectionID]['photoPfade'] += [photoPfad]
		photoCollections[collectionID]['photos'] += [photoName]

	
	collectionStrings = []
	collectionPhotos = []
	collectionIDs = []
	collectionKommentare = []
	for collectionID in photoCollections.iterkeys():
		collectionIDs += [collectionID]
		photoCollection = photoCollections[collectionID]
		collectionKommentare += [photoCollection['kommentar']]
		photosString = ','.join(photoCollection['photoPfade'])
		collectionPhotos += [photosString]
		photoBemerkungString = ', '.join(photoCollection['photos'])
		if photoCollection['klammern'] == 1:
			photoBemerkungString = '(' + photoBemerkungString + ')'
		if photoCollection['stern'] == 1:
			photoBemerkungString += '*'
		collectionStrings += [photoBemerkungString]

	
	doc = {
		"id": "formular-" + str(uid),
		"typ": "formular",
		"sql_tabelle": "tx_edfu_domain_model_formular",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"uebersetzung": uebersetzung,
		"texttyp": texttyp,
		"stelle_id": 'stelle-' + str(stelle_uid),
		"literatur": literatur,
		"photo": photos,
		"photo_collection_photos": collectionPhotos,
		"photo_collection_string": collectionStrings,
		"photo_collection_id": collectionIDs,
		"photo_collection_kommentar": collectionKommentare
	}
	addStellenTo([stelle_uid], doc)
	
	docs += [doc]

submitDocs('Formular')



# ORT
query = ("SELECT uid,transliteration,uebersetzung,ortsbeschreibung,anmerkung FROM tx_edfu_domain_model_ort")
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

for (uid,transliteration,uebersetzung,ortsbeschreibung,anmerkung) in cursor:
	stelleIDs = []
	stellen = []
	cursor2.execute(query4, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stelleIDs += ['stelle-' + str(uid_foreign)]
		stellen += [uid_foreign]
	
	doc = {
		"id": "ort-" + str(uid),
		"typ": "ort",
		"sql_tabelle": "tx_edfu_domain_model_ort",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"uebersetzung": uebersetzung,
		"ortsbeschreibung": ortsbeschreibung,
		"anmerkung": anmerkung,
		"stelle_id": stelleIDs
	}
	addStellenTo(stellen, doc)

	docs += [doc]

submitDocs('Ort')



# GOTT
query = ("SELECT uid,transliteration,ort,eponym,beziehung,funktion FROM tx_edfu_domain_model_gott")
cursor.execute(query)

query5 = """
SELECT 
	uid_foreign,
	uid_local
FROM
	tx_edfu_domain_model_stelle AS stelle,
	tx_edfu_domain_model_band AS band,
	tx_edfu_gott_stelle_mm
WHERE
	uid_local = %s AND
	uid_foreign = stelle.uid AND
	stelle.band_uid = band.uid
ORDER BY 
	band.nummer,
	stelle.seite_start,
	stelle.zeile_start
"""

for (uid,transliteration,ort,eponym,beziehung,funktion) in cursor:
	stelleIDs = []
	stellen = []
	cursor2.execute(query5, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stelleIDs += ['stelle-' + str(uid_foreign)]
		stellen += [uid_foreign]
		
	doc = {
		"id": "gott-" + str(uid),
		"typ": "gott",
		"sql_tabelle": "tx_edfu_domain_model_gott",
		"sql_uid": uid,
		"transliteration": transliteration.replace(':', '.'),
		"transliteration_nosuffix": removeSuffix(transliteration),
		"ort": ort,
		"eponym": eponym,
		"beziehung": beziehung,
		"funktion": funktion,
		"stelle_id": stellen
	}
	addStellenTo(stellen, doc)
	
	docs += [doc]

submitDocs('Gott')



# WORT
query = ("SELECT uid,transliteration,weiteres,uebersetzung,anmerkung,hieroglyph,lemma,wb_berlin_uid FROM tx_edfu_domain_model_wort")
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

for (uid,transliteration,weiteres,uebersetzung,anmerkung,hieroglyph,lemma,wb_berlin_uid) in cursor:
	stelleIDs = []
	stellen = []
	cursor2.execute(query6, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stelleIDs += ['stelle-' + str(uid_foreign)]
		stellen += [uid_foreign]
	
	doc = {
		"id": "wort-" + str(uid),
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
		"stelle_id": stellen
	}
	addStellenTo(stellen, doc)
	
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
		
	
	docs += [doc]

submitDocs('Wort')



# MySQL Verbindungen schließen
cursor.close()
cursor2.close()
cursor3.close()
db.close()
db2.close()
db3.close()