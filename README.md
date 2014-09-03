enigma2-plugin-extensions-moviearchiver
============================

![Screenshot](https://raw.github.com/MovieArchiver/enigma2-plugin-extensions-moviearchiver/master/src/plugin.png)


Archivieren:
--------
Der MovieArchiver archiviert automatisch Aufnahmen von beispielsweise der eingebauten Festplatte auf eine externen USB Festplatte.
Hat man mehrere Festplatten ist so sichergestellt das die Platte auf der aufgenommen wird Platz für neue Aufnahmen hat.

Ist "Automatische Archivieren" aktiviert wird nach jeder Aufnahme geprüft ob das eingestellte Limit erreicht wurde und ggf. so viel alte Aufnahme in das Archiv
verschoben bis das Limit an Festplattenplatz wieder frei ist.

Folgende Dateienendungen werden archiviert:
.ts, .avi, .mkv, .mp4, .iso

Inkl. der entsprechenden Metadateien wie z.B.:
.ts.cuts und .ts.meta
--------


Backup:
--------
Alternativ kann er auch als Backup Programm genutzt werden (über die Einstellungen einstellbar).
Zum Backup werden alle Dateien (es gibt keine Dateiendungs-Einschränkung) hinzugefügt die sich im angegebenen Verzeichnis (inkl. aller Unterverzeichnisse) befinden.
--------

Deaktiviert kann der MovieArchiver auch manuel über die Einstellungsseite gestartet werden.


Wichtig:
- Nutzung des Scripts auf eigene Gefahr!

Zu Testen:
- Was passiert wenn der EMC offen ist während eine Archivierung im Hintergrund gestartet wird?
- Was passiert wenn eine Aufnahme gerade abgespielt wird die im Hintergrund archiviert werden soll?

Bisher getestet auf folgenden Images/Receivern:
- openATV / Gigablue Quad
- HDF / ET9000

Screenshot:
![Screenshot](https://raw.github.com/MovieArchiver/enigma2-plugin-extensions-moviearchiver/master/screenshots/MovieArchiver.jpg)