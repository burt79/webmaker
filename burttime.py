### doohickey that tells you what day it is.

from datetime import datetime

def get_date():
    thedamndate = datetime.today().strftime('%B %d, %Y')
    if thedamndate.split(" ")[1].startswith("0"):
        list = thedamndate.split(" ")
        list[1] = list[1].strip("0")
        thedamndate = ""
        for x in list: thedamndate = thedamndate + " " + x
    else: pass
    return thedamndate
    
