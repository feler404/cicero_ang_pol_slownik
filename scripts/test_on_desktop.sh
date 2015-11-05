#!/usr/bin/env bash

# download and install
rm -f cicer_ang_pol_slownik.dev
wget https://github.com/feler404/cicero_ang_pol_slownik/blob/master/build/cicero_ang_pol_slownik.deb
sudo dpkg -i ./cicer_ang_pol_slownik.deb

# run and wait on exit
python /usr/local/bin/clipboard.py

# cleanup
sudo apt-get remove -y cicer_ang_pol_slownik
rm -f cicer_ang_pol_slownik.deb