#!/bin/sh

TMP_PATH=/tmp/tmpMovieArchiver
TMP_SRC_PATH="${TMP_PATH}/usr/lib/enigma2/python/Plugins/Extensions/MovieArchiver"


echo "Kopiere Plugin MovieArchiver aus aktuellen Verzeichnis nach ${TMP_PATH}"

#rm -r $TMP_PATH
mkdir -p $TMP_SRC_PATH
cp -r ../src/* $TMP_SRC_PATH
cp -r ../CONTROL ${TMP_PATH}/CONTROL
cp -r ../po/de.mo ${TMP_SRC_PATH}/locale/de/LC_MESSAGES
mv ${TMP_SRC_PATH}/locale/de/LC_MESSAGES/de.mo ${TMP_SRC_PATH}/locale/de/LC_MESSAGES/MovieArchiver.mo

echo "Zugriffsrechte der CONTROL Scripte zur Ausfuehrung bereit machen"
chmod 0755 ${TMP_PATH}/CONTROL/*

echo "Erstelle ipk in /tmp"
ipkg-build ${TMP_PATH} /tmp