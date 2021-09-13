#!/usr/bin/env python3
# -*- coding: utf-8 -*-

FIRST_NAME=""
LAST_NAME=""
LOGIN=""
EMAIL=""
PASSWORD_SSH_KEY="" #optional, if password on ssh key, functionality NOT TESTED


import os
import re
import sys
import urllib.request
import subprocess

VERSION="0.1"

print(""" /$$$$$$$$ /$$$$$$$         /$$$$$$                                                     /$$                        
|__  $$__/| $$__  $$       /$$__  $$                                                   | $$                        
   | $$   | $$  \ $$      | $$  \__/  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
   | $$   | $$$$$$$/      | $$ /$$$$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$|____  $$|_  $$_/   /$$__  $$ /$$__  $$
   | $$   | $$____/       | $$|_  $$| $$$$$$$$| $$  \ $$| $$$$$$$$| $$  \__/ /$$$$$$$  | $$    | $$  \ $$| $$  \__/
   | $$   | $$            | $$  \ $$| $$_____/| $$  | $$| $$_____/| $$      /$$__  $$  | $$ /$$| $$  | $$| $$      
   | $$   | $$            |  $$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$| $$     |  $$$$$$$  |  $$$$/|  $$$$$$/| $$      
   |__/   |__/             \______/  \_______/|__/  |__/ \_______/|__/      \_______/   \___/   \______/ |__/      
                                                                                                    BY Antoine ADAM""")
print("Version:",VERSION)
print("Author: antoine.adam@epita.fr")
print("Description: This program allows to automatically generate the structure, to make a git and push clone.")
print()#print("___________________________________________________________________________________________________________________")
print()

if not FIRST_NAME or not LAST_NAME or not LOGIN or not EMAIL:
    raise Exception("Please configure the executable inside! (FIRST_NAME, LAST_NAME, LOGIN, EMAIL)")

print("TpGenerator update check ...")
lastVersion=urllib.request.urlopen('https://raw.githubusercontent.com/Antoine-ADAM/TpGenerator/main/VERSION').read().decode('utf-8').strip()
if lastVersion != VERSION:
    print("Version installed => Latest version available")
    print(VERSION,"=>",lastVersion)
    print("This code is made of critical actions, it is very important to carry out the update.")
    print("Update link: https://github.com/Antoine-ADAM/TpGenerator")
    raise Exception("Please update TpGenerator !")

print("Downloading the TP list ...")
brutHtmlMain=urllib.request.urlopen('http://www.debug-pro.com/epita/prog/s3/').read().decode('utf-8').replace('\n','')
paterneGetALLTP=re.compile(r"""<li><a href="(pw\/pw_[^"]*\/index\.html)">([^<]*)<\/a><\/li>""")
matches = paterneGetALLTP.finditer(brutHtmlMain, re.MULTILINE)
allTP=[]
print("TP list:")
for matchNum, match in enumerate(matches, start=1):
    print(" -TP"+str(matchNum),"=>",match.group(2))
    allTP.append((match.group(1),match.group(2)))
idTP=-1
max=len(allTP)
while idTP<=0 or idTP>max:
    try:
        br=input(f"What is the number of the tp to process?(1-{max})[{max}]")
        if br == "":
            idTP=max
        else:
            idTP=int(br)
        if idTP <= 0 or idTP > max:
            raise Exception
    except:
        print("Value is not valid !")
(linkTP,nameTP)=allTP[idTP-1]
print("Downloading tp information in progress ...")
brutHtmlTP=urllib.request.urlopen('http://www.debug-pro.com/epita/prog/s3/'+linkTP).read().decode('utf-8').replace('\n','')
paterneGetDeadLine=re.compile(r"""<h3>Due Date<\/h3>\s*<p>By ([^<]*)""")
paterneVerifGit=re.compile(r"""\$ git clone [\.a-z]*@git\.cri\.epita\.fr:p\/2025-s3-tp\/tp([0-9]{2})-[\.a-z]*""")
paterneGetStruct=re.compile(r"""<h3>Directory Hierarchy<\/h3>.*?<ul>(.*?)<\/ul>\s*<p>""")
print("\n\n")
print("---------========={ TP"+str(idTP)+" "+nameTP+" }=========---------")
print("Link: http://www.debug-pro.com/epita/prog/s3/"+linkTP)
match=paterneGetDeadLine.search(brutHtmlTP)
if match:
    print("Deadline:",match.group(1))
else:
    print("Deadline not detected !\n", file=sys.stderr)
match=paterneVerifGit.search(brutHtmlTP)
if match:
    print("The address for git is verified")
    gitAddress=LOGIN+"@git.cri.epita.fr:p/2025-s3-tp/tp"+match.group(1)+"-"+LOGIN
    print("Address GIT: "+gitAddress)
else:
    gitAddress = LOGIN + "@git.cri.epita.fr:p/2025-s3-tp/tp" + ("0" if idTP<10 else "") + str(idTP) + "-" + LOGIN
    print("/!\\ Address git not detected /!\\", file=sys.stderr)
print()
basePath=os.path.dirname(__file__)+"/"
simPath="tp" + ("0" if idTP<10 else "") + str(idTP) + "-" + LOGIN+"/"
pathProject=input(f"Clone location: {basePath}[{simPath}]").strip() or simPath
if pathProject[len(pathProject)-1]!='/':
    pathProject+='/'
if not os.path.exists(pathProject):
 os.mkdir(pathProject)
while True:
    print()
    resGit=input("With which address to clone(no,<address>)?["+gitAddress+"]").strip()
    if not resGit:
        resGit = gitAddress
    if resGit == "no" or subprocess.run(["git","clone",resGit,pathProject], input=PASSWORD_SSH_KEY.encode('utf-8')).returncode==0:
        break
match=paterneGetStruct.search(brutHtmlTP)
if match:
    try:
        print("\n\n")
        print("Directory hierarchy:")
        cibles = {}
        tempo = ""
        isBal = False
        last = ""
        decal = 0
        interne = ""
        ignore = False
        path = []
        res = []
        for e in match.group(1):
            if e == '<':
                isBal = True
            elif e == '>':
                ignore = False
                isBal = False
                if tempo[0] == '/':
                    tempo = tempo[1:]
                    cibles[tempo] -= 1
                    decal -= 1
                    if tempo == "ul":
                        path.pop()
                    if last == tempo:
                        # print((decal+1)*' '+'+'+interne)
                        if tempo == "li" or tempo == "b":
                            p = ""
                            for i in path:
                                p += i
                            print(len(path) * "|  " + '-' + interne)
                            res.append(p + interne)
                        elif tempo == "code":
                            print(len(path) * "|  " + '+' + interne)
                            path.append(interne)
                        last = ""
                    interne = ""
                else:
                    last = tempo
                    if tempo in cibles:
                        cibles[tempo] += 1
                    else:
                        cibles[tempo] = 1
                    # print(decal*' '+'-'+tempo)
                    decal += 1
                    interne = ""
                tempo = ""
            elif isBal:
                if not ignore:
                    if e == ' ':
                        ignore = True
                    else:
                        tempo += e
            else:
                interne += e
        print()

        resInput=input("Write directory hierarchy ?(yes or y,no or n) [yes] ").strip()
        if resInput in ["","y","yes","Y","YES"]:
            testEmptyRep=os.listdir(pathProject)
            if len(testEmptyRep)==0 or (len(testEmptyRep)==1 and testEmptyRep[0]==".git") or input("The directory is not empty! If you continue these files may be overwritten: (yes, no) [no]") == "yes":
                try:
                    if "AUTHORS" in res:
                        res.remove("AUTHORS")
                        with open(pathProject + "AUTHORS", 'w') as f:
                            f.write(FIRST_NAME + '\n' + LAST_NAME + '\n' + LOGIN + '\n' + EMAIL)
                    for e in res:
                        (name, ext) = os.path.splitext(os.path.basename(e))
                        dirE = os.path.dirname(pathProject + e)
                        if not os.path.exists(dirE):
                            os.mkdir(dirE)
                        with open(pathProject + e, 'w') as f:
                            if ext == ".h":
                                f.write("//TpAutoEpitaToulouse " + VERSION + " => " + e + "\n")
                                v = name.upper().replace(' ', '_')
                                f.write("\n#ifndef " + v + "\n#define " + v + "\n\n//PROTOTYPE\n\n#endif")
                            elif name == "main" and ext == ".c":
                                f.write("//TpAutoEpitaToulouse " + VERSION + " => " + e + "\n")
                                if name == "main":
                                    f.write("""#include "stdio.h"
                
                    int main(){
                        //NOT IMPLEMENTED
                        return 0;
                    }""")
                    with open(pathProject + ".gitignore", 'w') as f:
                        f.write("#TpAutoEpitaToulouse " + VERSION + "\n")
                        f.write("""*
                    !*.*
                    !*/
                    !README
                    !AUTHORS
                    .idea/""")
                except Exception:
                    print("ERROR write files", file=sys.stderr)
    except Exception:
        print("ERROR parse directory hierarchy !", file=sys.stderr)
else:
    print("Directory hierarchy not detected !", file=sys.stderr)


print('\ncd "'+os.path.abspath(pathProject)+'"')

nCommit=0
while True:
    print("\n\n")
    input("git add/commit/push ? presses on entry").strip()
    print(subprocess.run(["git", "-C", pathProject, "add", "--all"], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    valid=False
    while not valid:
        print(subprocess.run(["git", "-C", pathProject, "status"], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        print()
        resInput=input('"add <file>" or "rm <file>" or "ok" ? [ok]').strip()
        if resInput == "ok" or resInput == "":
            valid=True
        else:
            cmd=resInput.split(" ",1)
            if len(cmd) == 2:
                if cmd[0] == "add":
                    print(subprocess.run(["git", "-C", pathProject, "add", cmd[1]], stdout=subprocess.PIPE).stdout.decode('utf-8'))
                elif cmd[0] == "rm":
                    print(subprocess.run(["git", "-C", pathProject, "rm", "--cached", cmd[1]], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    print()
    resInput=input(f"Commit name: [v{nCommit}]").strip()
    if resInput == "":
        resInput='v'+str(nCommit)
    print(subprocess.run(["git", "-C", pathProject, "commit", "-m", resInput], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    print(subprocess.run(["git", "-C", pathProject, "push"],stdout=subprocess.PIPE, input=PASSWORD_SSH_KEY.encode('utf-8')).stdout.decode('utf-8'))
    print(subprocess.run(["git", "-C", pathProject, "log"], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    nCommit+=1