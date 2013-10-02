EDFU Erfassen von Szenen
========================

a) Erfassen von Stellen im Edfu-Tempel anhand von Imagemaps und Bilddateien
b) Umrechnung des Koordinatensystem auf Geokoordinaten

scrape.php
==========

allgemein
---------
Das Skript scrape.php hat das Ziel Informationen über die Lage der Textstellen im Tempel verfügbar zu machen.

Es werden zum einen areas aus ImageMaps (welche einzelne Räume bzw. Wände darstellen) und die darin enthaltenen Informationen erfasst und deren Position im Gesamttempelplan berechnet (sowie weitere Information wie etwa der Blickwinkel oder Höhe relativ zur Wandhöhe). Zum anderen können von Räumen zu denen bloß eine Bilddatei vorliegt die areas in das Gesamtkoordinatensystem umgerechnet werden. 

Umgesetzt wird dies halbautomatisiert durch ein PHP-Script. Jedes Dokument (html, gif) wird analysiert, vorhandene Daten extrahiert und die Koordinaten der Felder in ein allgemeines Koordinatensystem übertragen.

In den HTML-Seiten liegen die Informationen derart vor: <area shape="rect" coords="130,521,153,540" href="Chassinat/5_086.jpg" alt="Kaelber treiben - Edfou 5, p. 086, (pl. 113)" title="Kaelber treiben - Edfou 5, p. 086, (pl. 113)">

Die Extraktion der Daten wird Raum für Raum vorgenommen und für eine weitere Verarbeitung zunächst in einer csv Datei pro Raum gespeichert. Die Positionierung der Szenen im Gesamtkoordinatensystem wird teil-automatisiert mit einer manuellen Zuordnung weiterer Informationen vorgenommen (manuell eingetragene Koordinaten der Wände, Bestimmung ob Innen- oder Außenwände illustriert sind , ... siehe Konfiguration/Verwendung)

Um die Bereiche der Szenen aus den jeweiligen GIFs zu extrahieren, wird eine Farbanalyse der einzelnen Pixel des Bildes vorgenommen, da diese Bereiche einheitlich einfarbig markiert sind und von einheitlich gefärbten Rändern begrenzt werden. Auch hier müssen zusätzlich aber Informationen für jeden Raum ergänzt werden.

Schwierigkeiten: Die Szenen sind in der Regel rechtwinklig gezeichnet, zum Teil bestehen sie aber auch komplexe Polygonen. Zur Vereinfachung werden solche Polygone umgerechnet in rechtwinklige Bereiche bzw. bei Bilddateien diese vor der Verarbeitung bearbeitet. Weitere Schwierigkeiten bei der automatisierten Extraktion der Daten, bereitet die nicht stringente Perspektive mancher Pläne. Gelöst wird dies mit einem manuellen Zuschneiden der Bereiche und Aufteilung in mehrere zu bearbeitende Dokumente.

Konfiguration/Verwendung
------------------------
Die gesamte Konfiguration wird in in der Datei config.php vorgenommen, welche kommentiert ist und somit weitesgehend selbsterklärend sein sollte.

Die manuell einzutragenen Daten für die Räume sind in dem $rooms array vorzunehmen. Koordinaten sind dabei zu definieren wie sie in den Imagemaps auch verwendet werden, also 2 Punkte die ein Rechteck beschreiben (Bsp: 153,463,173,485).

Damit die Bilder verarbeitet werden können müssen sie ausschließlich aus Rechtecken bestehen.

Durch Aufruf des Programms werden CSV Dateien geschrieben für alle im array $rooms eingetragenen (bzw. nicht auskommentierten) Bereiche.

Es kann durch den Aufruf der Funktion drawCoords() die Daten auf dem gesamten Tempelplan (drittes Attribut auf true setzen) oder wahlweise auf dem Raum grafisch dargestellt werden.

Spezialfall Türlaibungen u.ä.:
Da das Skript nicht automatisch mit verschiedenen Perspektiven umgehen kann, sind für Türlaibungen extra Bilder erstellt worden, welche danach manuell durch die Ursprungskoordinaten der Bereiche ersetzt werden mussten.

geocoordinates.php
==================

allgemein
---------
Das Skript geocoordinates.php berechnet aus dem verwendeten Koordinaten-System Geokoordinaten in Dezimalgrad.

Das Programm arbeitet dabei mit einem achsensysmetrischen Rechteck beim Ursprung und einem Rechteck beim Ziel der Transformation, so wie es beim Edfu-Tempel gegeben ist.

Das Programm berechnet bisher nur die Koordinaten. Die Berechnung der Breite der einzelnen Bereiche ist  noch nicht implementiert.

Alternativ zu dem Skript kann auch die für das konkrete Modell folgende Formel genutzt werden:

X‘= 24.977378 + (X - 56) * -7.249237701047E-8 +  (775-Y) * 1.6273115220484E-6
Y‘= 32.873111 + (X - 56) * 1.8429173177743E-6 +  (775-Y) * 6.4011379800956E-8


Konfiguration/Verwendung
------------------------
Die Konfiguration erfolgt in der Datei geoconfig.php. Hier sind unter anderem die Koordinaten des Tempels, sowie die Geokoordinaten des Tempels definiert.

Der Aufruf von getGeoCoordinates liefert abhängig von dieser Konfiguration die jeweiligen Geokoordinaten für die eingegebenen Koordinaten.






