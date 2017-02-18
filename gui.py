# This file is part of MacroJudge.
#
# MacroJudge is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MacroJudge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import pygtk
import gtk
import pango
import urllib
import compile
import scan
import xmlreader
from names import COMPILERS_INFO, COMPILERS_DISPLAY_NAMES

if __name__ != "__main__":
    print ("This should only be used as the entry script for the client side application.")
    sys.exit(0)
pygtk.require('2.0')

CURRENT_PROBLEM = None
REPOSITORY = "http://128.199.122.193/macrojudge/repository/"
COMPILER = "gcc"


window = gtk.Window(gtk.WINDOW_TOPLEVEL)
window.connect("delete-event", gtk.main_quit)
window.resize(500, 500)

main_vbox = gtk.VBox()

text_hbox = gtk.HBox()
text_hbox.set_homogeneous(True)

description_text = gtk.TextView()
description_text.set_wrap_mode(True)
description_text.modify_font(pango.FontDescription("monospaced 10"))

description_scroll = gtk.ScrolledWindow()
description_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
description_scroll.add(description_text)

code_text = gtk.TextView()
code_text.modify_font(pango.FontDescription("monospaced 10"))

code_scroll = gtk.ScrolledWindow()
code_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
code_scroll.add(code_text)

right_vbox = gtk.VBox()

compile_button = gtk.Button("_Run")
list_button = gtk.Button("Repository")
choose_button = gtk.Button("Choose Problem")
compiler_button = gtk.Button("Choose Compiler")

code_info = gtk.Label("Compiler: gcc, Language: c")

toolbar = gtk.HBox()
toolbar.set_homogeneous(True)

def show_prompt(message, title=None):
    dialog = gtk.Dialog(title=title, parent=window, flags=gtk.DIALOG_MODAL,
                        buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    label = gtk.Label(message)
    dialog.vbox.pack_start(label)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()

def download_xml_by_id(id):
    request = urllib.urlopen(REPOSITORY + "{}.{}.{}.xml".format(id[0], id[1], id[2]))
    str = request.read()
    request.close()
    return str

def compile_onclick(btn, text):
    if CURRENT_PROBLEM is None:
        show_prompt("Please Choose a Prroblem to Solve.", "Error")
        return
    sum = 0
    errcount = 0
    try:
        results = compile.excecute_source(text.get_text(text.get_start_iter(), text.get_end_iter()), COMPILER, map(lambda x : x.stdin, CURRENT_PROBLEM.tests), timeout=1)
        for i in range(len(results)):
            if CURRENT_PROBLEM.check_whitespace:
                if scan.formatted_scan(CURRENT_PROBLEM.tests[i].stdout) == scan.word_scan(results[i][0]):
                    sum += 1
            else:
                if scan.word_scan(CURRENT_PROBLEM.tests[i].stdout) == scan.word_scan(results[i][0]):
                    sum += 1
        show_prompt("Number of currect answers: " + str(sum) + "/" + str(len(CURRENT_PROBLEM.tests)),"output")
    except compile.CompileTimeError:
        show_prompt("Compile Time Error!", "Error")
    except compile.CompilerNotFoundError:
        show_prompt("Compiler Not Found On This Computer!", "Error")
    except Exception:
        show_prompt("Error!", "Error")

def choose_problem_onclick(btn, data):
    global description_text
    problem_id = [1,1,1]
    dialog = gtk.Dialog(title="Choose Problem", parent=window, flags=gtk.DIALOG_MODAL, buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    hbox = gtk.HBox()
    field1 = gtk.Entry(1)
    field2 = gtk.Entry(1)
    field3 = gtk.Entry(1)
    hbox.pack_start(field1)
    hbox.pack_start(field2)
    hbox.pack_start(field3)
    hbox.show_all()
    dialog.vbox.pack_start(hbox)
    if dialog.run() != gtk.RESPONSE_ACCEPT:
        dialog.destroy()
        return
    try:
        problem_id = [int(field1.get_text()),int(field2.get_text()),int(field3.get_text())]
    except ValueError:
        dialog.destroy()
        show_prompt("Please type in a valid id number.")
        return
    dialog.destroy()
    name = "{}.{}.{}.xml".format(problem_id[0],problem_id[1],problem_id[2])
    global CURRENT_PROBLEM
    try:
        str = download_xml_by_id(problem_id)
    except Exception:
        show_prompt("Cannot download this file.")
        return
    try:
        if not os.path.exists(os.path.expanduser("~/.macrojudge")):
            os.system("mkdir ~/.macrojudge")
        f = open(os.path.expanduser("~/.macrojudge/" + name), 'w')
        f.write(str)
        f.close()
        CURRENT_PROBLEM = xmlreader.parse(os.path.expanduser("~/.macrojudge/" + name))
    except Exception:
        show_prompt("Error loading this file.")     # Loaded a html page for error is a typical exception here
        return
    buffer = gtk.TextBuffer()
    buffer.set_text(CURRENT_PROBLEM.description + "\n\nExample Input:\n" + CURRENT_PROBLEM.example_in + "\n\nExample OutPut:\n" + CURRENT_PROBLEM.example_out)
    description_text.set_buffer(buffer)

def choose_compiler_onclick(btn, data):
    global COMPILER, code_info
    dialog = gtk.Dialog(title="Choose Compiler", parent=window, flags=gtk.DIALOG_MODAL , buttons=(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    dialog.set_default_size(300,100)
    combobox = gtk.combo_box_new_text()
    for compiler_name in COMPILERS_DISPLAY_NAMES:
        combobox.append_text(compiler_name)
    dialog.vbox.pack_start(combobox, expand=True, fill=False)
    dialog.vbox.show_all()
    if dialog.run() == gtk.RESPONSE_ACCEPT and combobox.get_active_text() is not None:
        info = COMPILERS_INFO[combobox.get_active_text()]
        COMPILER = info[0]
        code_info.set_text("Compiler: {}, Language: {}".format(info[0], info[1]))
    dialog.destroy()

choose_button.connect("clicked", choose_problem_onclick, None)
compiler_button.connect("clicked", choose_compiler_onclick, None)
compile_button.connect("clicked", compile_onclick, code_text.get_buffer())

toolbar.pack_start(compile_button)
toolbar.pack_start(list_button)
toolbar.pack_start(choose_button)
toolbar.pack_start(compiler_button)

right_vbox.pack_start(code_scroll)
right_vbox.pack_start(code_info, expand=False, fill=False)

text_hbox.pack_start(description_scroll, padding=3)
text_hbox.pack_start(right_vbox, padding=3)

main_vbox.pack_start(toolbar, expand=False, fill=False)
main_vbox.pack_start(text_hbox)

window.add(main_vbox)
window.show_all()
gtk.main()