
Cicero Ang-Pol Słownik
**********************

Lekki off-line-owy słownik angielsko-polski dla Ubuntu/Debian. Działa na zasadzie przechwytywania buforu schowka Ctr+C i notyfikacji systemowych do wyświetlania wyników. Aplikacja wymaga do prawidłowej pracy tylko standardowych pakietów z dystrybucji Ubuntu Desktop.

Master developer: Dawid Anioł

Podziękowania dla Andrzeja Tokarskigo z AjtSoft za udostępnienie bazy słów.


Kompatybilność
==============
- Ubuntu Desktop 15
- Ubuntu Desktop 14
- Ubuntu Desktop 13
- Ubuntu Desktop 12


Instalacja / Uruchomienie z pakietu
===================================

- ściągnąć pakiet DEB_ lub ``wget https://github.com/feler404/cicero_ang_pol_slownik/blob/master/build/cicero_ang_pol_slownik.deb?raw=true``
- zainstalować w systemie ``sudo dpkg -i ./cicero_ang_pol_slownik.deb``
- uruchomić program ``python /usr/local/bin/clipboard.py``
- po takiej instalacji program będzie dostępnu również w menu


Instalacja / Uruchomienie ze źródeł
===================================

- ``git clone https://github.com/feler404/cicero_ang_pol_slownik.git`` (ewentualnie zciągnąć i rozpakować zip)
- ``./scripts/run.sh``
- później wystarczy zaznaczyć interesujące słowo i nacisnąć ``Ctrl+C``


Deinstalacja pakietu
====================

- żebu usunąć program wystarczy wpisać ``sudo apt-get remove -y cicer_ang_pol_slownik``


Pomoc
=====
.. image:: static/help.png
    :width: 200px
    :align: center
    :height: 100px
    :alt: alternate text

Linki do projektów źródłowych
=============================
 - (Projekt Cicero) - http://feler404-3d.baynow.de/cicero/
 - (Strona AjtSoft) - http://www.ajt.com.pl


Lista zmian
===========
0.0.1 (05-11-2015)
^^^^^^^^^^^^^^^^^^

- oparcie aplikacji na Gtk/Gdk/Notify/AppIndicator3/sqlite z pliku clipboard.py
- baza danych oparta na bazie AjtSoft (dzięki panie Tomaszu)
- dodane skrypty pomocnicze do edicyji bazy, budowania pakietów oraz testów
- dodana dokumentacja użytkownika
- pakiet został sprawdzony dla Ubuntu v12 do v15

 .. _DEB: https://github.com/feler404/cicero_ang_pol_slownik/blob/master/build/cicero_ang_pol_slownik.deb?raw=true