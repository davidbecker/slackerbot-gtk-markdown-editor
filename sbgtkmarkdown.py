#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# sbgtkmarkdown.py - main application file
#
# Open markdown text files or create a new one.
# Edit and see results in webkit preview window.
# Save or Export as HTML files.
#
# Copyright (C) 2010  Ahmet Özdemir web3pointzero@gmail.com
#
# Code Base: http://code.google.com/p/slackerbot-gtk-markdown-editor/
# Documentation : http://www.slackerbot.com/slackerbot-gtk-markdown-editor/
#
# Acknowledgements:
#
# Thanks Jezra. (For whole idea)
# http://www.jezra.net/blog/A_markdown_editorviewer_in_Python
#
# Thanks Tudor Barbu (For get_html function) 
# http://blog.motane.lu/2009/06/18/pywebkitgtk-execute-javascript-from-python/
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gtk
import webkit
import markdown

class SbGtkMarkdown:

    def close(self,widget,event,data = None):
        gtk.main_quit()
        return False

    def __init__(self):
        self.file_name = "New File"
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event",self.close)
        self.window.set_title("Slackerbot Markdown Editor - " + self.file_name)
        self.window.set_size_request(400,300)
        self.window.set_border_width(0)
        #self.window.maximize()
        self.window.add_events(gtk.gdk.KEY_RELEASE_MASK)

        self.window.connect("key-release-event", self.keyrelease_event)

        container_main = gtk.VBox(False,0)
        self.window.add(container_main)
        container_main.show()

        menu_file = gtk.Menu()
        item_new =  gtk.MenuItem("New")
        item_open = gtk.MenuItem("Open")
        item_save = gtk.MenuItem("Save")
        item_save_as = gtk.MenuItem("Save As")
        item_save_as_html = gtk.MenuItem("Export As HTML")
        item_quit = gtk.MenuItem("Quit")

        menu_file.append(item_new)
        menu_file.append(item_open)
        menu_file.append(item_save)
        menu_file.append(item_save_as)
        menu_file.append(item_save_as_html)
        menu_file.append(item_quit)

        item_new.connect("activate",self.file_new)
        item_open.connect("activate",self.file_open)
        item_save.connect("activate",self.file_save)
        item_save_as.connect("activate",self.file_save_as)
        item_save_as_html.connect("activate",self.file_export_as_html)
        item_quit.connect ("activate",self.close , "quit")

        item_new.show()
        item_open.show()
        item_save.show()
        item_save_as.show()
        item_save_as_html.show()
        item_quit.show()

        menu_help = gtk.Menu()
        item_about = gtk.MenuItem("About")
        menu_help.append(item_about)

        item_about.connect("activate",self.help_about)
        item_about.show()

        file_item = gtk.MenuItem("File")
        file_item.show()

        file_item.set_submenu(menu_file)

        help_item = gtk.MenuItem("Help")
        help_item.show()
        help_item.set_submenu(menu_help)

        menu_bar = gtk.MenuBar()
        container_inner = gtk.HPaned()

        container_main.pack_start(menu_bar,False,False,0)
        container_main.pack_start(container_inner)
        self.tb = gtk.TextBuffer()
        editor = gtk.TextView(self.tb)
        editor.set_wrap_mode(gtk.WRAP_WORD)

        input_scroll = gtk.ScrolledWindow()
        adj = input_scroll.get_vadjustment()
        input_scroll.add_with_viewport(editor)
        input_scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        input_scroll.get_vadjustment().connect("changed", self.changed)
        input_scroll.get_vadjustment().connect("value-changed", self.value_changed)
        container_inner.pack1(input_scroll,True)

        self.preview = webkit.WebView()
        preview_settings = self.preview.get_settings()
        preview_settings.set_property('enable-plugins',False)
        preview_settings.set_property('default-font-size', 9)
        preview_settings.set_property('default-monospace-font-size', 8)

        self.preview.set_settings(preview_settings)
        self.out_scroll = gtk.ScrolledWindow()
        self.out_scroll.add(self.preview)
        self.out_scroll.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
        self.out_scroll.get_vadjustment().connect("changed", self.changed)
        self.out_scroll.get_vadjustment().connect("value-changed", self.value_changed)
        container_inner.add2(self.out_scroll)

        self.out_scroll.show()
        input_scroll.show()
        editor.show()
        self.preview.show()
        container_inner.show()
        menu_bar.show()

        menu_bar.append(file_item)
        menu_bar.append(help_item)
        self.window.show()

    def markdown(self,widget):
        text = self.get_buffer_text()
        mdtext = markdown.markdown(text)
        self.preview.load_html_string(mdtext,"file:///")

    def get_buffer_text(self):
        start_iter = self.tb.get_start_iter()
        end_iter = self.tb.get_end_iter()
        text=self.tb.get_text(start_iter,end_iter)
        return text

    def keyrelease_event(self, widget, event):
        self.markdown(widget)

    def changed(self, vadjust):
        if not hasattr(vadjust, "need_scroll") or vadjust.need_scroll:
            vadjust.set_value(vadjust.upper-vadjust.page_size)
            vadjust.need_scroll = True

    def value_changed(self, vadjust):
        vadjust.need_scroll = abs(vadjust.value + vadjust.page_size - \
                                  vadjust.upper) \
                              < vadjust.step_increment

    def help_about(self, widget):
        self.file_name = "New File"
        self.window.set_title("About Slackerbot Markdown Editor")
        self.tb.set_text(self.about_text)
        self.markdown(widget)

    def file_new(self, widget):
        self.file_name = "New File"
        self.tb.set_text("")
        self.window.set_title("Slackerbot Markdown Editor - " + self.file_name)
        self.markdown(widget)

    def file_open(self,widget):
        dialog = gtk.FileChooserDialog("Open file..",None,gtk.FILE_CHOOSER_ACTION_OPEN,
                                      (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                       gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)

        txt_filter=gtk.FileFilter()
        txt_filter.set_name("Text files")
        txt_filter.add_mime_type("text/*")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")

        dialog.add_filter(txt_filter)
        dialog.add_filter(all_filter)

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            file_name = dialog.get_filename()
            self.tb.set_text(open(dialog.get_filename()).read())
            self.file_name = file_name
            self.window.set_title("Slackerbot Markdown Editor - " + self.file_name)

        elif response == gtk.RESPONSE_CANCEL:
            dialog.destroy()

        dialog.destroy()
        self.markdown(widget)

    def file_save(self, widget):
        if  self.file_name == "New File":
            self.file_save_as(widget)
        else:
            textbuffer = self.tb
            file = open(self.file_name,"w")
            file.write(textbuffer.get_text(textbuffer.get_start_iter(),
                                        textbuffer.get_end_iter()))
            file.close()
            self.window.set_title("Slackerbot Markdown Editor - " + self.file_name)

    def file_save_as(self, widget):
        dialog = gtk.FileChooserDialog("Save..",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_SAVE,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                          gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        txt_filter=gtk.FileFilter()
        txt_filter.set_name("Text files")
        txt_filter.add_mime_type("text/*")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")

        dialog.add_filter(txt_filter)
        dialog.add_filter(all_filter)

        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            self.file_name = dialog.get_filename()
            textbuffer = self.tb
            file = open(dialog.get_filename(),"w")
            file.write(textbuffer.get_text(textbuffer.get_start_iter(),
                                        textbuffer.get_end_iter()))
            file.close()
            self.window.set_title("Slackerbot Markdown Editor - " + self.file_name)

        elif response == gtk.RESPONSE_CANCEL:
            dialog.destroy()

        dialog.destroy()

    def file_export_as_html(self, widget):
        dialog = gtk.FileChooserDialog("Save..",
                                         None,
                                         gtk.FILE_CHOOSER_ACTION_SAVE,
                                         (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                          gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        txt_filter=gtk.FileFilter()
        txt_filter.set_name("Html files")
        txt_filter.add_mime_type("text/html")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")

        dialog.add_filter(txt_filter)
        dialog.add_filter(all_filter)

        response = dialog.run()
        file_name = dialog.get_filename()

        if response == gtk.RESPONSE_OK:
            textbuffer = self.get_html(self.preview)
            file = open(file_name,"w")
            file.write(textbuffer)
            file.close()
        elif response == gtk.RESPONSE_CANCEL:
            dialog.destroy()

        dialog.destroy()

    def get_html(self, preview):
        preview.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
        html = preview.get_main_frame().get_title()
        preview.execute_script('document.title=oldtitle;')
        if html:
            return "<html>" + html + "</html>"
        else:
            return "<html><body>" + self.about_text + "</body></html>"

    def main(self):
        gtk.main()

    about_text = """
Slackerbot GTK+ Markdown Editor
---
Open markdown text files or create a new one. Edit and see results in webkit preview window. Save or Export as HTML files.

Copyright (C) 2010 **Ahmet Ozdemir** 

[http://www.slackerbot.com][web]

[web3pointzero@gmail.com][email]

[email]: web3pointzero@gmail.com
[web]: http://www.slackerbot.com

**Documentation :**
[http://www.slackerbot.com/slackerbot-gtk-markdown-editor/][docs]
**Code Base :**
[http://code.google.com/p/slackerbot-gtk-markdown-editor/][code]

[docs]: http://www.slackerbot.com/slackerbot-gtk-markdown-editor/
[code]: http://code.google.com/p/slackerbot-gtk-markdown-editor/

**Acknowledgements:**

Thanks ***Jezra***. (For whole idea) [http://www.jezra.net/blog/A_markdown_editorviewer_in_Python][jezra]

[jezra]: http://www.jezra.net/blog/A_markdown_editorviewer_in_Python

Thanks ***Tudor Barbu*** (For get_html function) [http://blog.motane.lu/2009/06/18/pywebkitgtk-execute-javascript-from-python/][tudor]

[tudor]: http://blog.motane.lu/2009/06/18/pywebkitgtk-execute-javascript-from-python/ 
"""

if __name__ == "__main__":
    widget = SbGtkMarkdown()
    widget.main()

