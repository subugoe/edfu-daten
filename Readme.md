# Edfu Daten
Dateien und Skripte zur Bearbeitung der Edfu-Daten


## Ziel
Die Edfu Daten liegen in einer MySQL Datenbank bei der GWDG vor. Ziel ist es, sie auf der TYPO3 Website der AdW im Web verfüg- und bearbeitbar zu machen. Schritte dazu:

* Export des Dumps bei der GWDG
* lokales Einlesen des Dumps in MySQL und:
	* Korrektur der bekannten Fehler im Dump
	* Normalisierung
	* Anpassung an die Tabellenformate von TYPO3
* Erstellung eines Solr Index aus den Daten
* Darstellung der Solr Dokumente durch TYPO3


## Unterordner
* [Daten](Daten):
	* edfuprojekt.sql: SQL Dump (nicht im Repository)
	* edfu.mwb (MySQL Workbench Dokument erzeugt die folgenden Dateien), Edfu DB.pdf (Graphik), schema.sql: SQL Schema des normalisierten Datenmodells
	* szenen: CSV Exporte der Szeneninformationen erzeugt durch das [szenentool Skript](szenentool)
	* tempelplan.csv: CSV Datei mit den verschiedenen Teilstücken des gesamten Tempelplans
* [solr/config](solr/config): Konfiguration für den Solr Index
* [szenentool](szenentool): Skript zum Extrahieren der Szenenrechtecke aus dem Tempelplan
* [tempelplan](tempelplan): Graphiken vom Tempelplan; original und beschnitten
* [Fonts](Fonts): Verschiedene Transliterationsfonts zum Testen
* [emf](emf): Versuche, die EMF Dateien mit den Hieroglyphen gut zu konvertieren (erfolglos: jetzt werden vom Projekt SVGs geliefert)



## Konversion der Daten
Das Konversionsskript [convert.py](convert.py) bereitet die Daten aus dem MySQL Dump für das verbesserte Datenschema auf.

Es benötigt:

* einige Python Module, z.B. mysql.connector (siehe die imports am Anfang des Skripts)
* den importierten MySQL Dump in der Datenbank »edfuprojekt« in MySQL (host:127.0.0.1, user:root, einstellbar am Anfang des Skripts)
* die Möglichkeit, das Konversionsergebnis in die Tabelle »edfu« des lokalen MySQL Servers zu schreiben
* das SQL Schema der Zieldatenbank in [Daten/schema.sql](Daten/schema.sql)


### Zielschema
Das Zieldatenbankschema wurde mit MySQLWorkbench erstellt. Zugehörige Dateien sind:

* [Daten/edfu.mwb](Daten/edfu.mwb) – MySQLWorkbench Datei
* [Daten/schema.sql](Daten/schema.sql) – SQL Schema, vom Importskript benötigt
* [Daten/schema.pdf](Daten/schema.pdf) – graphische Darstellung des SQL Schemas

Die TYPO3 spezifischen Felder sind nicht in dem Datenbankschema enthalten. Wegen ihrer großen Zahl und Redundanz fügt das Konversionsskript sie zu den Tabellen hinzu und wandelt dabei die verschiedenen Namenskonventionen für Tabellen ineinander um (Präfix `tx_gs_` und ggf `model_domain`, bzw. Suffix `_mm`).


### Seiten-/Zeilenangaben
Die verschiedenen Tabellen des Edfu-Datenbestands enthalten Seiten-/Zeilenangaben von Stellen in den Chassinat Bänden. Sie haben Formen wie »VII, 123, 08« oder »VIII, 017, 12 - 018, 03«. Während die Angaben für das menschliche Auge meist verständlich sind, sind sie nicht regelmäßig formatiert und haben viele kleine Variationen zwischen den Tabellen und auch einzelnen Datensätzen.

Das Konversionsskript versucht die vorhandenen Daten so gut wie möglich zu lesen und häufig auftretende Unregelmäßigkeiten zu korrigieren. Weiterhin enthält es viele Korrekturen von Tippfehlern in den Daten, die bei Importversuchen aufgefallen sind. Diese Korrekturen funktionieren, indem der Feldinhalt mit dem als falsch bekannten String verglichen wird und ersetzen den String dann durch die richtige Version. (Dieses etwas komplizierte Vorgehen im Vergleich zur Verwendung der Datensatz ID stellt sicher, daß bei künfigten Importen ein möglicherweise vom Projekt inzwischen korrigierter Feldinhalt nicht überschrieben wird.) In diesem Rahmen durchgeführte Korrekturen werden als Lognachrichten ausgegeben.

Das Resultat sind Seiten- und Zeilenangaben als Daten, die sich für weitere Suchen verwenden lassen und nicht als Freitext für das menschliche Auge. Diese Aufwertung der Datenqualität ist zentral für die neuen Suchmöglichkeiten, die die Seiten- und Zeilenangaben von Textstellen und Szenen zusammenbringen.


### Bildnamenlisten
Ein ähnliches Problem beim Import stellt das Feld FL/Photo dar. Auch hier sind die Angaben teilweise nicht regelmäßig formatiert und werden wenn nötig bereinigt und Änderungen an den Daten als Lognachricht ausgegeben.

Das Konversionsskript enthält noch Code für das Beibehalten der Bildgruppierungen. Die Gruppierungsdaten werden aber nicht mehr exportiert, da sie mit der Verfügbarkeit von Vorschaubildern auf der Website für das Projekt an Wert verloren haben und das Datenmodell in der technischen Umsetzung sehr kompliziert gemacht hätten.


### Logging
Das Importskript loggt Importprobleme, Feldänderungen und allgemeine Informationen zum Datenimport in die Konsole. Das Log liegt als [convert.log](convert.log) vor. Importprobleme sind je nach Schwere mit INFO, WARNUNG oder FEHLER versehen.




## Indexierung der Daten
Das Indexierungsskrip ist [index.py](index.py). Es erzeugt einen [Solr](http://lucene.apache.org/solr/) Index aus den konvertierten MySQL Daten.

Es benötigt:
* einige Python Module, z.B. mysql.connector (siehe die Imports am Anfang des Skripts)
* Zugriff auf MySQL mit den konvertierten Daten in der Datenbank »edfu« (host:127.0.0.1, user:root, einstellbar am Anfang des Skripts)
* Schreibzugriff auf den Ziel Solr Index (konfiguriert am Ende des Skriptes, es wird in zwei Index indexiert)


### Solr Konfiguration
Das Schema für den Solr Index liegt unter [solr/conf/schema.xml](solr/conf/schema.xml).


### Dokumente
Zur Indexierungszeit werden Dokumente für die Datensatztypen »formular«, »wort«, »ort« und »gott« erstellt, die IDs der Form »TYP-X« haben, wobei TYP der Name des Datensatztyps ist und X die ID des Datenasatzes, z.B. »formular-1«.

Die Dokumente werden mit Information zu den zugehörigen Szenen angereichert, um die Anzeige des Tempelplans mit den hervorgehobenen Szenen zu ermöglichen. Dieser Schritt macht viele SQL Abfragen, die die Indexierung relativ langsam machen.

Zusätzlich erstellt das Skript Dokumente vom Typ »stelle«, »szene« und »wb_berlin«. 


### Automatische Indexierung
Dieses Skript erstellt den Index vollständig neu. Für den regulären Betrieb, in dem Daten in TYPO3 bearbeitet werden und sofort im Index abfragbar sein sollen ist es nötig, die Konversion granularer auszuführen und nur das neue/geänderte/gelöschte Dokument, sowie die davon abhängigen Dokumente im Index zu aktualisieren. Die Überprüfung der Abhängigkeiten und die Löschfunktion ist in diesem Skript noch nicht vorhanden.


### Logging
Das Indexierungsskript loggt Probleme in die Konsole. Das Log liegt als [index.log](index.log) vor und soll Informationen über die Anzahl der Dokumente nach Typ enthalten.



