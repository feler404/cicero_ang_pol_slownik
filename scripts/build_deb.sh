#! /usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

cd ./../
rm -f ./deb/usr/local/bin/clipboard.py
rm -f ./deb/usr/share/cicero/ajt.db
cp ./clipboard.py ./deb/usr/local/bin/clipboard.py
cp ./ajt.db ./deb/usr/share/cicero/ajt.db

cd deb

echo "Build package..."
fakeroot dpkg-deb --build .
rm -f ./../cicero_ang_pol_slownik.deb
mv ./..deb ./../cicero_ang_pol_slownik.deb

echo "Cleanning..."
rm -f ./usr/local/bin/clipboard.py
rm -f ./usr/share/cicero/ajt.db


echo "DONE."