from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

cur_file = ''
def_ext='.txt'
file_type=[('Text','*.txt'),('HTML','.html')]
fresh = True

root = Tk("Text Editor")

#---Text Area---
text = Text(root,wrap=NONE)
vert_scroll = Scrollbar(root)

vert_scroll.pack(side=RIGHT, fill=Y)

text.pack(side=LEFT, fill=BOTH,expand = YES)
vert_scroll.config(command=text.yview)
text.config(yscrollcommand=vert_scroll.set)

#---Selection Tag---
text.tag_config('select', background='gray')

#---Default Tag---
text.tag_config('default', background='white')

#---Menu Commands---

#<-File I/O->
def open_file():
    file = filedialog.askopenfilename(parent=root,title = "Select file")
    try:
        with open(file,'r') as file_obj:
            global cur_file,fresh
            fresh = False
            cur_file = ''
            cur_file += file
            text.delete('1.0',END)
            text.insert('1.0',file_obj.read())
    except:
        messagebox.showerror('Error', 'File not Found')

def save_file():
    if fresh:
        save_file_as()
    else:
        with open(cur_file,'w') as file_obj:
            data = text.get('1.0', END + '-1c')
            file_obj.write(data)


def save_file_as():
    file = filedialog.asksaveasfilename(parent=root,title = "Select file",defaultextension=def_ext,filetypes=file_type)
    with open(file,'w') as file_obj:
        data = text.get('1.0', END + '-1c')
        file_obj.write(data)

#<-Edit->
def find(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)

def replace_all(text_widget, keyword1, keyword2):
    data = text_widget.get('1.0',END + '-1c')
    ndata = data.replace(keyword1,keyword2)
    text_widget.delete('1.0',END)
    text.insert('1.0', ndata)

def replace_next(text_widget, keyword1, keyword2):
    data = text_widget.get('1.0', END + '-1c')
    ndata = data.replace(keyword1, keyword2, 1)
    text_widget.delete('1.0', END)
    text.insert('1.0', ndata)

def findwin():
    find_w = Toplevel(height=100,width=500)
    
    entry = Entry(find_w)
    entry.pack(side=RIGHT)

    b = Button(find_w, text='Find', command=lambda: find(text, entry.get(), 'select'))
    b.pack(side=RIGHT)
    find_w.mainloop()

def replacewin():
    replace_w = Toplevel(height=58,width=205)
    
    entry1 = Entry(replace_w)
    entry2 = Entry(replace_w)
    entry1.place(x=80,y=5)
    entry2.place(x=80,y=35)

    b1 = Button(replace_w, text='Replace All ', command=lambda: replace_all(text, entry1.get(), entry2.get()))
    b2 = Button(replace_w, text='Replace Next', command=lambda: replace_next(text, entry1.get(), entry2.get()))
    b1.place(x=0,y=0)
    b2.place(x=0,y=30)
    replace_w.mainloop()

#---Menu Bar---
menubar = Menu(root)

#---Adding File Menu---
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(labe='Open', command=open_file)
filemenu.add_command(label='Save', command=save_file)
filemenu.add_command(label='Save As...', command=save_file_as)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=lambda:exit())

#---Adding Edit Menu---
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label='Cut', command=lambda: root.focus_get().event_generate('<<Cut>>'))
editmenu.add_command(label='Copy', command=lambda: root.focus_get().event_generate('<<Copy>>'))
editmenu.add_command(label='Paste', command=lambda: root.focus_get().event_generate('<<Paste>>'))
editmenu.add_separator()
editmenu.add_command(label='Undo', command=text.edit_undo)
editmenu.add_command(label='Redo', command=text.edit_redo)
editmenu.add_separator()
editmenu.add_command(label='Find', command=findwin)
editmenu.add_command(label='Replace', command=replacewin)

#---Adding Everything Together---
menubar.add_cascade(label='File', menu=filemenu)
menubar.add_cascade(label='Edit', menu=editmenu)

#---main---
root.config(menu=menubar)
root.mainloop()

























