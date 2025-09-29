### doohickey that handles data storage and interfaces with external text files. 

print("initializing parser...")

from config import *

postlist = []
marks = []

with open("data.txt", "rt") as blog:
     bloglines = blog.readlines()

class post:
     def __init__(self, id, pushed, title, content, date):
          self.id = id
          self.pushed = pushed
          self.title = title
          self.content = content
          self.date = date
          self.marked = False
          self.online = False
          print(f"post initialized: ID {self.id} | {self.title}")
     def get_state(self):
          if self.pushed == False: star = "*"
          else: star = "-"
          if self.marked == True: mark = "!"
          else: mark = "-"
          return f"{star}{mark}"

def post_get(id):
     for x in postlist:
          if x.id == id:
               return x
     print("post_get failed: post not found")
     

def id_gen(list): # finds the next available post id
     takens = []
     counter = 1
     for x in list:
          takens.append(x.id)
     while takens.__contains__(counter):
          for x in list:
               if x.id == counter:
                    counter += 1
     return counter

def post_write(x):
     bloglines.append("\n")
     bloglines.append(f"{x.id}#!|{x.title}")
     bloglines.append(f"{x.id}#>|{x.content}")
     bloglines.append("\n")
     bloglines.append(f"{x.id}#d|{x.date}")

def save():
     print("saving posts...")
     with open("data.txt", "w") as blog:
          pass
     
     with open("data.txt", "w") as blog:
          global bloglines
          bloglines = []
          for x in postlist:
               if x.marked == True:
                    print(f"post {x.id} is marked for removal. removing from postlist.")
               else:
                    x.pushed = True
                    print(f"writing post {x.id} to file.")
                    post_write(x)
          blog.writelines(bloglines)

          do = True
          while do:
               do = False
               for x in postlist:
                    if x.marked == True:
                         do = True
                         postlist.remove(x)
                    else: pass

### inits of things

print("=== init says: ===")
for x in bloglines:
     if x.__contains__("#!"):
          alpha = x.split("|")
          id = int(alpha[0].strip("0").rstrip("#!"))
          title = alpha[1]
          for x in bloglines:
               if x.__contains__(f"{alpha[0].rstrip("#!")}#>"): content = x.split("|")[1]
          for x in bloglines:
               if x.__contains__(f"{alpha[0].rstrip("#!")}#d"): date = x.split("|")[1] 

          postlist.insert(0, post(id, True, title, content, date))
          

          id = None
          title = None
          content = None

postlist.sort(key=lambda x: x.id, reverse=True)
    
