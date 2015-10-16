# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, with_statement

import time
import sys
import os
import sqlite3
import traceback
import logging

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject as gobject
from gi.repository import Notify as notify
from gi.repository import AppIndicator3 as appindicator


#TODO: add install script
#TODO: complete README
#TODO: add logging to file, end log errors for further debug


APP_NAME = "Cicero Słownik Ang-Pol"

if os.path.exists("/usr/share/cicero/ajt.db"):
    DB_FILE = "/usr/share/cicero/ajt.db"
else:
    DB_FILE = "./ajt.db"




class CiceroAngPolDict(gobject.GObject):


    __recent_clipboard = ""
    __exit_signal = False

    shortcut_dict = {
         "s": "rzecz.",
         "S": "rzecz.",
         "M": "rzecz.",
         "v": "czas.",
         "V": "czas.",
         "W": "czas.",
         "a": "przym.",
         "d": "przysł.",
         "c": "spój.",
         "r": "przyim.",
         "o": "zaimek",
         "u": "licz.",
         "k": "skrót",
         "i": "wykrz.",
         "x": "",
        }

    def __init__(self):
        gobject.GObject.__init__(self)
        print("Witamy w {}".format(APP_NAME))
        print("Plik bazy : {}".format(DB_FILE))

        self.logger = logging.getLogger(__name__)
        sh = logging.StreamHandler()
        sh.setLevel(logging.ERROR)
        self.logger.addHandler(sh)

        self.clipboard = gtk.Clipboard.get(gdk.SELECTION_CLIPBOARD)
        notify.init(APP_NAME)
        self.con = sqlite3.connect(DB_FILE)
        gobject.timeout_add(1, self.periodic_check)

        ind = appindicator.Indicator.new("example-simple-client",
                                         "user-away-panel",
                                         appindicator.IndicatorCategory.SYSTEM_SERVICES)
        ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        ind.set_attention_icon("/usr/share/pixmaps/cdetray.png")  # indicator-messages-new

        # create a menu
        menu = gtk.Menu()

        menu_items_exit = gtk.MenuItem("Exit")
        menu_items_exit.connect("activate", self.menuitem_response_exit)
        menu_items_exit.show()
        menu_items_info = gtk.MenuItem("Info")
        menu_items_info.connect("activate", self.menuitem_response_info)
        menu_items_info.show()
        
        menu.append(menu_items_info)
        menu.append(menu_items_exit)
        ind.set_menu(menu)
        gtk.main()

    def send_notification(self, title, text, file_path_to_icon=""):
        n = notify.Notification.new(title, text, file_path_to_icon)
        n.show()

    def menuitem_response_exit(self, *args, **kwargs):
        sys.exit(0)

    def menuitem_response_info(self, *args, **kwargs):
        about = gtk.AboutDialog()
        about.set_program_name(APP_NAME)
        about.set_version("0.1")
        about.set_copyright("(c) Dawid Anioł / AjtSoft")
        about.set_comments(
            """
            Lekki off-line-owy Ang-Pol słownik dla Ubuntu/Debian.


            (Projekt Cicero) - http://feler404-3d.baynow.de/cicero/
            (Strona AjtSoft) - http://www.ajt.com.pl

            """)
        about.set_logo(GdkPixbuf.Pixbuf.new_from_file("/usr/share/pixmaps/gedit-icon.xpm"))
        about.run()
        about.destroy()

    def find_in_sql(self, frase):
        if len(frase) < 2 or len(frase) > 80:
            return [(1, frase, "Warning search len_frase={}".format(len(frase)))]

        with self.con:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM ajt WHERE ang LIKE "{}%"'.format(frase))
            rows = cur.fetchall()
        return rows

    def find_similar_in_sql(self, frase):
        cut_ret = []
        for i, val in enumerate(frase):
            similar_frase = frase[:len(frase)-i]
            ret = self.find_in_sql(similar_frase)
            if ret:
                if ret[0][2].startswith("%"):
                    ret = self.find_in_sql(ret[0][2][1:])
                if ret[0][1] != frase:
                    ret = cut_ret = [(ret[0][0], "{} -> {}".format(frase, ret[0][1]), ret[0][2])]           
                return ret

    def periodic_check(self):
        clipboard_content = self.clipboard.wait_for_text()
        if clipboard_content != self.__recent_clipboard:
            try:
                self.__recent_clipboard = clipboard_content
                ret = self.find_similar_in_sql(clipboard_content)
                self.print_notify(ret)
            except Exception as e:
                more = "(File error={0} : Line number={1} : Line content={3})".format(*traceback.extract_tb(sys.exc_info()[2])[0])
                self.logger.error("Error : Exception={} : Details={}".format(e, more))
                print (clipboard_content, e)
        time.sleep(0.1)
        return True

    def parse_response(self, msg_pol):
        trantab = {43: 59, 
                   60: 39, 
                   62: 39, 
                   64: 32, 
                   37: 32,
                   34: 32}

        msg_pol = msg_pol.translate(trantab)
        while msg_pol.find("$") is not -1:
            tag_pos = msg_pol.find("$")
            tag_name = msg_pol[tag_pos + 1]
            if tag_name.isdigit():
                tag_rep = tag_name
                msg_pol = msg_pol.replace("$"+tag_name, "\n\n"+tag_rep+")")
            else:
                tag_rep = self.shortcut_dict[tag_name]
                msg_pol = msg_pol.replace("$"+tag_name, tag_rep)
        return msg_pol.strip() 


    def print_notify(self, msg):
        first_meaning = msg[0]
        index_id, eng_frase, pol_frase_row = first_meaning
        pol_frase = self.parse_response(pol_frase_row)

        self.send_notification(eng_frase, pol_frase)


if __name__ == "__main__":
    cicero_dict = CiceroAngPolDict()
