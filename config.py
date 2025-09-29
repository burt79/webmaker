### doohickey that reads the config file.
print('initializing conf...')

def declar(str):
    return str.split(":", 1)[1].strip()

with open("conf", "rt") as conf:
    conflines = conf.readlines()

# define defaults
AllowFTP = False
postTitleTag = 'h1'
postDateTag = 'h3'
postContentTag = 'p'
postEditorFontSize = '14'
FTPip = '127.0.0.1'
FTPport = 21
FTPuser = 'user'
FTPpass = 'pass'
HTMLFileName = 'file.html'


# get configs
for x in conflines:
    match x.split(":")[0]:
        case "allowFTP":
            if declar(x) == "true":
                AllowFTP = True
        case "postTitleTag":
            postTitleTag = declar(x)
        case "postDateTag":
            postDateTag = declar(x)
        case "postContentTag":
            postContentTag = declar(x)
        case "postEditorFontSize":
            postEditorFontSize = declar(x)
        case 'FTPip':
            FTPip = declar(x)
        case 'FTPport':
            FTPport = int(declar(x))
        case 'FTPuser':
            FTPuser = declar(x)
        case 'FTPpass':
            FTPpass = declar(x)
        case 'HTMLFileName':
            HTMLFileName = declar(x)


print("allowftp:", AllowFTP)
print('posttitle:', postTitleTag)
print('postEditorFontSize:', postEditorFontSize)
print('FTPip:', FTPip)
print('FTPport:', FTPport)
print('FTPuser:', FTPuser)
print('FTPpass:', FTPpass)
print('HTMLFileName:', HTMLFileName)