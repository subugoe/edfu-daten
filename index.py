#! /usr/bin/env python
#coding=utf-8

import solr
index = solr.Solr('http://localhost:8983/solr/edfu')

import mysql.connector
db = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
db2 = mysql.connector.connect(user='root', host='127.0.0.1', database='edfu')
cursor = db.cursor()
cursor2 = db2.cursor()

# FORMULAR
query = ("SELECT uid,transliteration,uebersetzung,texttyp,stelle_uid FROM tx_edfu_domain_model_formular")
cursor.execute(query)

query2 = ("SELECT beschreibung, detail "
	"FROM tx_edfu_formular_literatur_mm,tx_edfu_domain_model_literatur "
	"WHERE tx_edfu_formular_literatur_mm.uid_local = %s "
	"AND tx_edfu_formular_literatur_mm.uid_foreign = tx_edfu_domain_model_literatur.uid")

query3 = ("SELECT tx_edfu_domain_model_photo.name AS photoName, tx_edfu_domain_model_photo_typ.name AS typName, tx_edfu_domain_model_photo_typ.jahr AS photoJahr, klammern, stern, kommentar "
	"FROM tx_edfu_formular_photo_collection_mm,tx_edfu_domain_model_photo_collection,tx_edfu_photo_collection_photo_mm,tx_edfu_domain_model_photo,tx_edfu_domain_model_photo_typ "
	"WHERE tx_edfu_formular_photo_collection_mm.uid_local = %s "
	"""AND tx_edfu_formular_photo_collection_mm.uid_foreign = tx_edfu_domain_model_photo_collection.uid
	AND tx_edfu_photo_collection_photo_mm.uid_local = tx_edfu_domain_model_photo_collection.uid
	AND tx_edfu_photo_collection_photo_mm.uid_foreign = tx_edfu_domain_model_photo.uid
	AND tx_edfu_domain_model_photo.photo_typ_uid = tx_edfu_domain_model_photo_typ.uid """
	"ORDER BY photoJahr DESC, photoName DESC")


for (uid,transliteration,uebersetzung,texttyp,stelle_uid) in cursor:
	literatur = []
	cursor2.execute(query2, [str(uid)])
	for (beschreibung, detail) in cursor2:
		literatur += [beschreibung + ' : ' + detail]
	
	photos = []
	cursor2.execute(query3, [str(uid)])
	for (photoName, typName, photoJahr, klammern, stern, kommentar) in cursor2:
		photos += [photoName]
	
	doc = {
		"id": "formular-" + str(uid),
		"typ": "formular",
		"sql_tabelle": "tx_edfu_domain_model_formular",
		"sql_uid": uid,
		"transliteration": transliteration,
		"uebersetzung": uebersetzung,
		"texttyp": texttyp,
		"stelle": stelle_uid,
		"literatur": literatur,
		"photo": photos
	}
	index.add(doc)


# ORT
query = ("SELECT uid,transliteration,uebersetzung,ortsbeschreibung,anmerkung FROM tx_edfu_domain_model_ort")
cursor.execute(query)

query4 = ("SELECT uid_foreign,uid_local "
	"FROM tx_edfu_ort_stelle_mm "
	"WHERE uid_local = %s")

for (uid,transliteration,uebersetzung,ortsbeschreibung,anmerkung) in cursor:
	stellen = []
	cursor2.execute(query4, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stellen += [uid_foreign]
	
	doc = {
		"id": "ort-" + str(uid),
		"typ": "ort",
		"sql_tabelle": "tx_edfu_domain_model_ort",
		"sql_uid": uid,
		"transliteration": transliteration,
		"uebersetzung": uebersetzung,
		"ortsbeschreibung": ortsbeschreibung,
		"anmerkung": anmerkung,
		"stelle": stellen
	}
	index.add(doc)


# GOTT
query = ("SELECT uid,transliteration,ort,eponym,beziehung,funktion FROM tx_edfu_domain_model_gott")
cursor.execute(query)

query5 = ("SELECT uid_foreign,uid_local "
	"FROM tx_edfu_gott_stelle_mm "
	"WHERE uid_local = %s")

for (uid,transliteration,ort,eponym,beziehung,funktion) in cursor:
	stellen = []
	cursor2.execute(query5, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stellen += [uid_foreign]
	
	doc = {
		"id": "gott-" + str(uid),
		"typ": "gott",
		"sql_tabelle": "tx_edfu_domain_model_gott",
		"sql_uid": uid,
		"transliteration": transliteration,
		"ort": ort,
		"eponym": eponym,
		"beziehung": beziehung,
		"funktion": funktion,
		"stelle": stellen
	}
	index.add(doc)


# WORT
query = ("SELECT uid,transliteration,weiteres,uebersetzung,anmerkung,hieroglyph,wb_berlin_uid FROM tx_edfu_domain_model_wort")
cursor.execute(query)

query6 = ("SELECT uid_foreign,uid_local "
	"FROM tx_edfu_wort_stelle_mm "
	"WHERE uid_local = %s")

for (uid,transliteration,weiteres,uebersetzung,anmerkung,hieroglyph,wb_berlin_uid) in cursor:
	stellen = []
	cursor2.execute(query6, [str(uid)])
	for (uid_foreign,uid_local) in cursor2:
		stellen += [uid_foreign]
	
	doc = {
		"id": "gott-" + str(uid),
		"typ": "gott",
		"sql_tabelle": "tx_edfu_domain_model_gott",
		"sql_uid": uid,
		"transliteration": transliteration,
		"uebersetzung": uebersetzung,
		"weiteres": weiteres,
		"anmerkung": anmerkung,
		"hieroglyph": hieroglyph,
		"stelle_berlin": wb_berlin_uid,
		"stelle": stellen
	}
	index.add(doc)


# STELLE
query = ("SELECT tx_edfu_domain_model_stelle.uid,seite_start,seite_stop,zeile_start,zeile_stop,anmerkung,stop_unsicher,zerstoerung,nummer,freigegeben "
	"FROM tx_edfu_domain_model_stelle,tx_edfu_domain_model_band "
	"WHERE tx_edfu_domain_model_stelle.band_uid = tx_edfu_domain_model_band.uid")
cursor.execute(query)

for (uid,seite_start,seite_stop,zeile_start,zeile_stop,anmerkung,stop_unsicher,zerstoerung,band,freigegeben) in cursor:
	
	doc = {
		"id": "stelle-" + str(uid),
		"typ": "stelle",
		"sql_tabelle": "tx_edfu_domain_model_stelle",
		"sql_uid": uid,
		"seite_start": seite_start,
		"seite_stop": seite_stop,
		"zeile_start": zeile_start,
		"zeile_stop": zeile_stop,
		"stelle_anmerkung": anmerkung,
		"stop_unsicher": stop_unsicher,
		"zerstoerung": zerstoerung,
		"band": band,
		"freigegeben": freigegeben
	}
	index.add(doc)

# WB-BERLIN
# WORT
query = ("SELECT uid,band,seite_start,seite_stop,zeile_start,zeile_stop,zweifel FROM tx_edfu_domain_model_wb_berlin")
cursor.execute(query)

for (uid,band,seite_start,seite_stop,zeile_start,zeile_stop,zweifel) in cursor:
	doc = {
		"id": "wb_berlin-" + str(uid),
		"typ": "wb_berlin",
		"sql_tabelle": "tx_edfu_domain_model_wb_berlin",
		"sql_uid": uid,
		"seite_start": seite_start,
		"seite_stop": seite_stop,
		"zeile_start": zeile_start,
		"zeile_stop": zeile_stop,
		"zweifel": zweifel
	}
	index.add(doc)




index.commit()
cursor2.close()	
cursor.close()
db.close()