#!/usr/bin/env bash

# download and install
echo "Prepare..."
rm -f /tmp/cicero_ang_pol_slownik.deb
wget "https://github.com/feler404/cicero_ang_pol_slownik/blob/master/build/cicero_ang_pol_slownik.deb?raw=true" -P /tmp/
mv /tmp/cicero_ang_pol_slownik.deb?raw=true /tmp/cicero_ang_pol_slownik.deb
sudo dpkg -i /tmp/cicero_ang_pol_slownik.deb


# run and wait on exit
echo "Run..."
python /usr/local/bin/clipboard.py

# cleanup
echo "Cleanup..."
sudo apt-get remove -y cicero-ang-pol-slownik
rm -f /tmp/cicero_ang_pol_slownik.deb

echo "Done."