### doohickey that makes the html files.

import os
import parser
import config

def newpost(x):
    global document
    contentList = x.content.split("\\n")
    document.write('\n')
    document.write('<div class="post">\n')
    document.write(f'<{config.postTitleTag}>{x.title}</{config.postTitleTag}>\n')
    document.write(f'<{config.postDateTag}>{x.date}</{config.postDateTag}>\n')
    for i in contentList: document.write(f'<{config.postContentTag}>{i}</{config.postContentTag}>\n')
    document.write('</div>\n')
    document.write('\n')


def main():
    global document
    try:
        os.remove(f"output/{config.HTMLFileName}")
    except FileNotFoundError:
        pass

    with open(f"template/{config.HTMLFileName}", "rt") as document:# read the current blog.html for reference
        lines = document.readlines()
        lines.insert(0, '<!--PLACEHOLDER-->')
    
    document = open(f"output/{config.HTMLFileName}", "xt") # create output file

    for x in lines:
        if x.__contains__("<!--blog-->"): # make blog posts in blog.html
            bcursor = lines.index(x)
            print(f"writing blog posts @ line {bcursor}...")
            document.write(x)
            for x in parser.postlist:
                newpost(x)
        else:
            document.write(x)

    document.close()
    return 0

# old shit from when this was a command line utility. you could uncomment it and run maker/parser on their own if u really wanted to. 

'''
loop = True


while loop:
    cmd = input("push these changes? [y/n] > ")
    if cmd.lower().strip() == "y":
        print("pushing changes...")
        print(index.name)
        send(index.name)
        print("changes pushed.")
        loop = False
        break
    elif cmd.lower().strip() == "n":
        print("changes saved locally, no changes pushed.")
        loop = False
        break
    else:
        print("ERR: invalid input.")


'''