# -*- coding:Utf-8 -*-
###############################################################################
## Lutris
##
## Copyright (C) 2009 Mathieu Comandon strycore@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import gtk
import subprocess
import logging

class MountIsoDialog(gtk.Dialog):
    def __init__(self):

        self.check_fuseiso()

        gtk.Dialog.__init__(self)
        self.set_title("Mount ISO image")
        self.set_size_request(300,200)
        
        self.iso_filechooserbutton = gtk.FileChooserButton("Open an ISO file", backend=None)
        self.iso_label = gtk.Label("ISO file")
        self.iso_label.set_size_request(90,20)
        self.iso_hbox = gtk.HBox()
        self.iso_hbox.pack_start(self.iso_label,False,False)
        self.iso_hbox.pack_start(self.iso_filechooserbutton)
        self.vbox.pack_start(self.iso_hbox,False,False,10)

        self.mount_point_dialog = gtk.FileChooserDialog(title="Select mount point",
                                                        parent=self,
                                                        action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                                        buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                                                 gtk.STOCK_OK, gtk.RESPONSE_ACCEPT),
                                                        backend=None)

        self.mount_point_filechooserbutton = gtk.FileChooserButton(self.mount_point_dialog)
        self.mount_point_label = gtk.Label("Mount point")
        self.mount_point_label.set_size_request(90,20)
        self.mount_point_hbox = gtk.HBox()
        self.mount_point_hbox.pack_start(self.mount_point_label,False,False)
        self.mount_point_hbox.pack_start(self.mount_point_filechooserbutton)
        self.vbox.pack_start(self.mount_point_hbox,False,False,10)

        #Action buttons
        cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
        ok_button = gtk.Button(None, gtk.STOCK_OK)
        self.action_area.pack_start(cancel_button)
        self.action_area.pack_start(ok_button)
        cancel_button.connect("clicked", self.close)
        ok_button.connect("clicked", self.ok_clicked)

        self.show_all()
        self.run()

    def check_fuseiso(self):
        fuseiso_command = subprocess.Popen(["which","fuseiso"],stdout=subprocess.PIPE).stdout
        fuseiso_is_installed = fuseiso_command.readline()
        if "fuseiso" in fuseiso_is_installed:
            logging.debug("fuseiso is installed")
        else:
            logging.debug("fuseiso not here, problems ahead")

    def close(self,widget):
        self.destroy()

    def ok_clicked(self,wigdet):
        #TODO: Check if file is valid
        iso_file = self.iso_filechooserbutton.get_filename()
        mount_point = self.mount_point_filechooserbutton.get_filename()
        fuseiso_command = subprocess.Popen(["fuseiso",iso_file,mount_point],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print "mount done!"
        self.destroy()