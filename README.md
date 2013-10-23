enigma2-plugin-extensions-moviearchiver
============================

![Screenshot](https://raw.github.com/MovieArchiver/enigma2-plugin-extensions-moviearchiver/master/src/plugin.png)

Der MovieArchiver archiviert automatisch Aufnahmen von beispielsweise der eingebauten Festplatte auf eine externen USB Festplatte.
Ist er aktiviert wird nach jeder Aufnahme geprüft ob das eingestellte Limit erreicht wurde und ggf. so viel alte Aufnahme in das Archiv
verschoben bis das Limit an Festplattenplatz wieder frei ist.

Deaktiviert kann der MovieArchiver auch manuel über die Einstellungsseite gestartet werden.



Hinweise:
- Es handelt sich um eine Beta Version. Getestet wurde das Plugin bisher NUR auf einer Gigablue Quad mit openATV. Ob andere Images und
Receiver funktionieren ist daher nicht bekannt
- Ob eingebundene Netzwerklaufwerke damit funktionieren ist ebenfalls bisher unbekannt
- Nach der Installation ist der MovieArchiver deaktiviert


Wichtig:
- Nutzung des Scripts auf eigene Gefahr!


Known Issues:
- Nach drücken der gelben Taste in den Einstellungen:
	- Archivierung wird im Hintergrund gestartet, bisher fehlt noch ein User-Feedback das es gestartet wurde
- Wenn der MovieArchiver aktiviert ist, wird nach jeder Aufnahme geprüft ob der Speicher noch ausreicht oder ob das Limit erreicht wurde.
Wurde das Limit erreicht wird die älteste Aufnahme sofort verschoben. Es gibt also bisher keine Prüfung ob noch eine weitere Aufnahme läuft.
Habt ihr also eine langsame Festplatte, sollte das Automatische Archivieren erst mal deaktiviert sein und das archivieren manuel über die
Settings vorgenommen werden.


Zu Testen:
- Nach Aufnahme aus dem Deepstandby und anschließender automatischer Archivierung:
	- geht der Receiver korrekt in den Deepstandby obwohl eine Archivierung gestartet wurde?
	- wird die Archivierung evtl. einfach abgebrochen und keine Aufnahmen verschoben?

- Was passiert wenn der EMC offen ist während eine Archivierung im Hintergrund gestartet wird?
	- aktualisiert sich die Ansicht von alleine?

- Was passiert wenn eine Aufnahme gerade abgespielt wird die im Hintergrund archiviert werden soll?
	- bricht die Archivierung ab?

- Wie ist das Verhalten auf anderen Receivern (bisher nur auf Gigablue Quad getestet)?

- Funktioniert das Plugin auch mit anderen Images wie beispielsweise openMips?


Screenshot:

![Screenshot](https://raw.github.com/MovieArchiver/enigma2-plugin-extensions-moviearchiver/master/screenshots/MovieArchiver.jpg)