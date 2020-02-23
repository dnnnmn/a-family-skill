import sys
import os
from os.path import dirname, isfile, join

#toolsPath =(join(dirname(__file__),"FamilyTools"))
toolsPath =dirname(__file__)
sys.path.append(os.path.abspath(toolsPath))

import aFamilyTools

fontDefault = "\033[0;36;40m"
fontAnswer = "\033[0;31;47m"
fontAction = "\033[0;34;47m"
fontDisplay = "\033[0;34;40m"

print (fontAnswer)
answer = input("Did you change the relationsDef.txt file (y or n)  ")
if answer == 'y':
    print (fontDefault)
    aFamilyTools.makeRelationKeyword()
    aFamilyTools.makeFamilyBlank()
    print (fontAction)
    print ("Copy file RelationKeyword.voc to Dir for Keywords")   
    print (fontDefault)
    print ("A new familyDefBlank.txt file has beem created")
    print (fontAction)
    print ("Create a new familyDef.txt file from familyDefBlank.txt before continuing")       
    
print (fontAnswer)
answer = input("\nIs a new family.txt file avialable (y or n)  ")
if answer == 'y':
    answer = input("\nPress y to remake all files  ")
    if answer == 'y':
        print (fontDefault)
        aFamilyTools.makeSynonyms()
        aFamilyTools.make_lists()
        aFamilyTools.makePersonKeword()
        print (fontAction)
        print ("Copy file PersonKeyword.voc to Dir for Keywords")
        print ("\nCopy file family.txt to Dir for skill")
        print ("\nCopy file synonyms.txt to Dir for skill")
       
print (fontAnswer)
answer = input("\nPress y to show synonyms  ")
if answer == 'y':
    print (fontDisplay)
    aFamilyTools.show_synonyms()
print (fontAnswer)
answer = input("\nPress y to show members  ")
if answer == 'y':
    print (fontDisplay)
    family = aFamilyTools.importFamilies()
    print (family[0], '\n')
print (fontAnswer)
answer = input("\nPress y to show relationships  ")
if answer == 'y':
    print (fontDisplay)
    family = aFamilyTools.importFamilies()
    print (family[1], '\n')
    #print (family[1][0], '\n')
    #print (family[1][0][2], '\n')
    #print (family[1][0][2][1], '\n')
print (fontDefault)
