#!/bin/sh

echo "Kopiere Plugin MovieArchiver nach /tmp/tmpMovieArchiver/"
#rm -r /tmp/tmpMovieArchiver
mkdir -p /tmp/tmpMovieArchiver/usr/lib/enigma2/python/Plugins/Extensions/MovieArchiver
cp -r ../src/* /tmp/tmpMovieArchiver/usr/lib/enigma2/python/Plugins/Extensions/MovieArchiver
cp -r ../CONTROL /tmp/tmpMovieArchiver/CONTROL

echo "Zugriffsrechte der CONTROL Scripte zur Ausfuehrung bereit machen"
chmod 0755 /tmp/tmpMovieArchiver/CONTROL/*

echo "Erstelle ipk in /tmp"
ipkg-build /tmp/tmpMovieArchiver /tmp