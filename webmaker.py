### main doohickey. runs gui and interfaces with all modules.

import tkinter as tk
from tkinter import ttk
import parser
import maker
import burttime
import web
import config

print("initializing guy...")

postWindowWidth = config.postEditorFontSize * 2
postWindowHeight = 500
postWindowGeo = f"{postWindowWidth}x{postWindowHeight}"

root = tk.Tk()

# p1 = tk.PhotoImage(file = 'favicon.ico')
root.geometry("1360x550")
root.title("burt's webmaker")
# root.iconphoto(True, p1)

editid = None
cmdHistory = ["R"]
cmdList = ['edit', 'statreset', 'help', 'setid', 'addpost', 'delpost']
arm = False
 
conf = {"bg": "black",
        "fg": "white",
        "font": "monospace 14 bold",
        "padx": "5",
        "pady": "5"}

def statout(arg):
    status.config(fg='black',text=arg)

def staterr(arg):
    status.config(fg='red', text=f"ERR: {arg}")

def quit():
    root.destroy()
    exit(0)

def cmd_help():
    help = tk.Tk()
    help.geometry("600x500")
    help.title("help")
    maintext = tk.Label(help, None, font="monospace 14", justify="left", wraplength=550, text='''
help: display this page.
addpost: display the add post interface
delpost [id]: mark specified post for deletion.
setid [id] [new id]: manually set the id number of a post object.
statreset: reset status bar to default state.
exit: close the program without pushing.
'''
    )
    maintext.pack(anchor=tk.NW)

def addpost():
    def pushpost():
        global table
        title = titlebox.get(1.0, tk.END)
        content = box.get(1.0, tk.END).replace('\n', '\\n')
        id = parser.id_gen(parser.postlist)
        date = burttime.get_date()
        post = parser.post(id, False, title, content, date)
        parser.postlist.insert(0, post)
        parser.post_write(post)
        push_table_posts()
        addpost.destroy()
        statout(f"post {id} added! push to apply.")
    global conf
    addpost = tk.Tk()
    addpost.geometry(postWindowGeo)
    addpost.title("new post")
    addbtn = tk.Button(addpost, conf, text="add", command=pushpost, anchor=tk.NW)
    addbtn.pack(side='left', anchor=tk.NW)
    titlebox = tk.Text(addpost, None, width=50, height=1, font="monospace 14 bold")
    titlebox.pack(anchor=tk.CENTER, ipady=3)
    box = tk.Text(addpost, None, width=75, height=20, wrap="word", font=f"courier {config.postEditorFontSize}")
    box.pack(anchor=tk.CENTER, ipady=3)

def delpost():
    def post_mark():
        try: delid = int(text.get(1.0, tk.END).strip())
        except ValueError: lbl.config(text="put in a number, stupid.")
        for x in parser.postlist:
            if x.id == delid:
                x.marked = not x.marked
                statout(f"post {x.id} marked for deletion. push to apply.")
            else: pass
        push_table_posts()
        delpost.destroy()
    delpost = tk.Tk()
    delpost.geometry("150x150")
    delpost.title("delete post")
    lbl = tk.Label(delpost, None, text="id of post to delete:")
    text = tk.Text(delpost, None, width=5, height=2)
    btn = tk.Button(delpost, conf, text="delete", command=post_mark)
    lbl.pack()
    text.pack()
    btn.pack()
    delpost.focus()
    text.focus()

def editpost(x):
    def pushpost():
        global table
        x.title = titlebox.get(1.0, tk.END)
        x.content = box.get(1.0, tk.END).replace('\n', '\\n')
        x.pushed = False
        parser.post_write(x)
        push_table_posts()
        editpost.destroy()
        statout(f"post {x.id} edited! push to apply.")
    global conf
    editpost = tk.Tk()
    editpost.geometry(postWindowGeo)
    editpost.title(f"edit post {x.id}")
    addbtn = tk.Button(editpost, conf, text="edit", command=pushpost, anchor=tk.NW)
    addbtn.pack(side='left', anchor=tk.NW)
    titlebox = tk.Text(editpost, None, width=50, height=1, font="monospace 14 bold")
    titlebox.pack(anchor=tk.CENTER, ipady=3)
    box = tk.Text(editpost, None, width=75, height=20)
    box.pack(anchor=tk.CENTER, ipady=3)
    titlebox.insert(1.0, x.title)
    box.insert(1.0, x.content.replace("\\n", "\n"))

def push_table_posts():
    global table
    parser.postlist.sort(key=lambda x: x.id, reverse=True)
    table.tag_configure('row', background='#FFFFFF', font="monospace 14 bold")
    table.tag_configure('oddrow', background="#E8E8E8", font="monospace 14 bold")
    ping = True
    for i in table.get_children():
        table.delete(i)
    for x in reversed(parser.postlist):
        if ping:
            table.insert(parent='', index=0, values=(x.get_state(), x.id, x.title, x.date), tags=('row',))
        elif not ping:
            table.insert(parent='', index=0, values=(x.get_state(), x.id, x.title, x.date), tags=('oddrow',))
        ping = not ping

# blog table ---------------------

table = ttk.Treeview(root, height=20)

table['columns'] = ('state', 'ID', 'title', 'date')

table.column('#0', width=0, stretch=tk.NO)
table.column('state', anchor=tk.W, width=50)
table.column('ID', anchor=tk.W, width=30)
table.column('title', anchor=tk.W, width=300)
table.column('date', anchor=tk.W, width=300)

table.heading('#0', text='', anchor=tk.W)
table.heading('state', text='*', anchor=tk.W)
table.heading('ID', text='ID', anchor=tk.W)
table.heading('title', text='title', anchor=tk.W)
table.heading('date', text='date', anchor=tk.W)

push_table_posts()

def save():
    parser.save()
    push_table_posts()
    statout("changes saved!")

def maker_main():
    maker.main()
    statout("html made and deployed in output.")

def toggle_arm():
    global arm
    arm = not arm
    if arm == True:
        statout('FTP armed.')
    else: statout('FTP disarmed.')
    print('arm:', arm) 

def send():
    global arm
    if config.AllowFTP == False:
        staterr("FTP is disabled.")
        return 1
    elif arm == False:
        staterr("program is not armed to make FTP connections.")
        return 1
    else:
        web.send()
        statout("files uploaded to server successfully.")
        return 0 

# buttons

btnframe = tk.Frame(root)

if config.AllowFTP == True:
    box = tk.Checkbutton(root, text='arm FTP', command=toggle_arm)
    box.pack(anchor=tk.NW)

btn = tk.Button(btnframe, conf, command=addpost, text="new post")
btn.pack(anchor=tk.NW, side='left')

btn = tk.Button(btnframe, conf, command=delpost, text="del post")
btn.pack(anchor=tk.NW, side='left')

btn = tk.Button(btnframe, conf, command=save, text="save")
btn.pack(anchor=tk.NW, side='left')

btn = tk.Button(btnframe, conf, command=maker_main, text="make html")
btn.pack(anchor=tk.NW, side='left')

if config.AllowFTP == True:
    btn = tk.Button(btnframe, conf, command=send, text="push to server")
    btn.pack(anchor=tk.NW, side='left')

btn = tk.Button(btnframe, conf, command=quit, text="exit")
btn.pack(anchor=tk.NW, side='left')

cmdframe = tk.Frame(root, None)
status = tk.Label(cmdframe, None, text="ready!", font="TkDefaultFont 12")
status.grid(column=0, row=0, sticky=tk.W)
cmdlin = tk.Entry(cmdframe, None, width=115, font="monospace 14 bold", takefocus="",)
cmdlin.grid(column=0, row=1)
#gobtn = tk.Button(cmdframe, conf, text='enter', height=0, width=0)
gobtn = tk.Entry(cmdframe, width=0)
gobtn.grid(column=1, row=1)

btnframe.pack()
cmdframe.pack(anchor=tk.SW, side='bottom', padx=10, pady=10)
table.pack()


def handleReturn(thing):
    thing = None
    global cmdHistory, upIndex
    cmdHistory.insert(1, cmdlin.get()); upIndex = 0
    string = cmdlin.get().split(" ")
    cmdlin.delete(0, 'end')
    cmd = string[0].strip().lower()
    string.remove(string[0])
    args = []
    for x in string:
        args.append(x)
        
    match cmd:
        case "addpost":
            addpost()
        
        case "delpost":
            for i in args:
                for x in parser.postlist:
                    if x.id == int(i):
                        x.marked = not x.marked
            statout(f"posts marked for deletion. push to apply.")
            push_table_posts()

        case "edit":
            try: editpost(parser.post_get(int(args[0])))
            except AttributeError: statout("usage: edit [id]")
            except IndexError: staterr("post not found.")
        

        case "setid":
            try:
                x = parser.post_get(int(args[0]))
                for i in parser.postlist:
                    if i.id == int(args[1]):
                        staterr("id already taken.")
                        return 1
                x.id = int(args[1])
                x.pushed = False
                push_table_posts()
                statout("id set successfully!")
            except IndexError:
                statout("usage: setid [id] [new id]")

        case "save":
            save()
        
        case "statreset":
            print(arm)
            statout("ready!")
        
        case "help":
            cmd_help()
        
        case _:
            staterr("invalid command.")



upIndex = 0

def handleUp(thing):
    thing = None
    global upIndex, cmdHistory
    if upIndex == 0: cmdHistory[0] = cmdlin.get()
    else: pass
    try:
        if upIndex == len(cmdHistory) - 1:
            return 1
        else:
            cmdlin.delete(0, tk.END)
            upIndex += 1
            cmdlin.insert(0, cmdHistory[upIndex]); 
            return 0
    except IndexError: return 1

def handleTab(thing):
    thing = None
    statout("lol")

def handleDown(thing):
    thing = None
    global upIndex, cmdHistory
    if upIndex == 0: cmdHistory[0] = cmdlin.get()
    else: pass
    try:
        if not upIndex == 0: 
            cmdlin.delete(0, tk.END)
            upIndex -= 1
            cmdlin.insert(0, cmdHistory[upIndex])
            return 0
        else: return 1
    except IndexError: return 1

def handleTab(thing):
    global prev
    thing = None
    str = cmdlin.get()
    cmdlin.focus_set()
    for x in cmdList:
        if x.startswith(str) and x != prev.strip():
            cmdlin.delete(0, tk.END)
            cmdlin.insert(0, x + " ")
            cmdlin.focus_force()
            prev = x
            return 0
    cmdlin.focus(); return 1

prev = ""

def bs(thing):
    thing = None
    # i am stupid
    cmdlin.focus_set()

cmdlin.focus_set()
cmdlin.bind("<Return>", handleReturn)
cmdlin.bind("<Up>", handleUp)
cmdlin.bind("<Down>", handleDown)
cmdlin.bind("<Tab>", handleTab)
gobtn.bind("<FocusIn>", bs)



root.mainloop()