import sys
import os
from os.path import dirname, isfile, join
#relativesTuple = []
#members = []

toolsPath = dirname(__file__)
sys.path.append(os.path.abspath(toolsPath))

# GET SYNONYMS LIST FROM FILE
def importSynonyms():
    synonyms = []
    with open(join(toolsPath,'synonyms.txt')) as f:
        for line in f:
            line = line.split(',')
            pair = [line[0].strip('\n')]
            pair.append(line[1].strip('\n'))
            synonyms.append(pair)
    return synonyms

#GET FAMILY LISTS FROM FILE
def importFamilies():
    relativesTuple = []
    members = []
    constantsFile = (join(toolsPath,"family.txt"))
    dataType = 'undefined'
    
    with open(constantsFile) as f:
        for line in f:
            if (line == '\n') or (line[0] == '#'): # Don't process blank lines
                pass
            elif '*MEMBERS*' in line:
                dataType = 'members'
            elif '*RELATIVES*' in line:
                dataType = 'relatives'
            else:
                line = line.strip('\n')
                if dataType == 'members':
                    line = line.split(',')
                    pair = [line[0]]
                    pair.append(line[1])                               
                    members.append(pair)
                if dataType == 'relatives':
                    if '****' in line:
                        memberTuples = []
                        relativesTuple.append(memberTuples)
                    else:
                        line = line.split(',')
                        pair = [line[0]]
                        pair.append(line[1])                               
                        memberTuples.append(pair)
    f.close #not sure this is necessary
    lists = [members]
    lists.append(relativesTuple)
    return lists

#MAKE MEMBERS & RELATIVES LISTS AND SAVE TO FILE
def make_lists():
    print ("Making Family Files and storing as family.txt\n")
    relativesTuple = []
    members = []

    familyFile =(join(toolsPath,"familyDef.txt"))
    index = -1
    dataType = 'undefined'

    # Generate list for members and list of relatives of members
    with open(familyFile) as f:
        for line in f:
            if (line == '\n') or (line[0] == '#'): # Don't process blank lines
                pass
            elif '*MEMBER*' in line:
                dataType = 'member'
                index += 1
                membersRelatives = []
            elif '*RELATIVES*' in line:
                dataType = 'relatives'
                relativesTuple.append(membersRelatives) #membersRelatives is empty here initially but as it gets populated below it appears here
            else:
                line = line.strip('\n')
                if dataType == 'relatives':
                    line = line.split('\t')
                    membersRelatives.append(line)
                elif dataType == 'member':
                    pair = [str(index)]
                    pair.append(line)
                    members.append(pair)
                else:
                    print ('UNDEFINED ENTRY')
    f.close #not sure this is necessary

    # Save above lists to a file
    membersStr = convert_lists(members)

    relationsStrngs = []
    i=0
    for member in relativesTuple:
        relationsStrngs.append(convert_lists(relativesTuple[i]))
        i += 1

    path = (join(toolsPath,'family.txt'))        
    f = open(path, "w")
    f.write('*MEMBERS*\n')
    f.write(membersStr)
    f.write('*RELATIVES*\n')
    for members in relationsStrngs:   
        f.write('****\n')
        f.write(members)
    f.close()

#THIS FILE RETURNS A SYNONYM LIST BUILT FROM RELATIONSHIPS DEFINED IN relativesDef.txt
# ALSO CREATES A FILE OF THEM SINCE THE DO NOT CHANGE OFTEN
def makeSynonyms():
    print ("Making Synonyms File and storing as synonyms.txt\n")
    synonyms = [] # list of synonyms for above relations

    # Generate synonyms list
    with open(join(toolsPath,'relationsDef.txt')) as f:
        for line in f:
            line = line.split('\t')
            
            i = 0                       
            while i < len(line):
                pair = [line[0].strip('\n')]
                pair.append(line[i].strip('\n'))
                synonyms.append(pair)
                i+=1
    # Save synonyms to file
    relationshipsStr = convert_lists(synonyms)
    path = (join(toolsPath,'synonyms.txt'))        
    f = open(path, "w")
    f.write(relationshipsStr)
    f.close()               
                            
    return synonyms

#THIS FILE CONVERTS A LIST OF LISTS TO A STRING
def convert_lists(listOfLists):
    listOneDim = []
    for pairs in listOfLists:
        pairsStr = ','.join(pairs) + '\n'
        listOneDim += pairsStr
        #print (pairs)
    #print ('list1d')
    #print (list1d)

    listOfListsStr = ''.join(listOneDim)
    #print ('listOfListsStr')
    #print (listOfListsStr)

    return listOfListsStr

#THIS FILE CREATES RelationKeyword.voc THAT SHOULD BE INSERTED IN DIR FOR KEYWORDS  
def makeRelationKeyword():
    print ("Making RelationKeyword File and storing as RelationKeyword.voc\n")
    #relations = "" # allowable relations to use for relationship file
    keywords = "" # synonyms for above relations
    
    with open(join(toolsPath,'relationsDef.txt')) as f:
        for line in f:
            line = line.split("\t")
            
            i = 0                       
            while i < len(line):
                keywords += (line[i].strip('\n')) +'\n' # have exactly 1 /n at end
                i+=1

            #relation = line[0].strip('\n') +'\n' # have exactly 1 /n at end
            #relations += relation           
   
    f = open(join(toolsPath,'RelationKeyword.voc'), "w")
    f.write(keywords)
    f.close()

#THIS FILE CREATES  familyDefBlank.txt TO USE AS AS TEMPLATE FOR familyDef.txt    
def makeFamilyBlank():
    print ("Making a template File and storing as familyBlank.txt\n")
    #relationFile = open(join(toolsPath,'RelationKeyword.voc'))
    #relations = relationFile.read()
    
    relations = ''
    with open(join(toolsPath,'relationsDef.txt')) as f:
        for line in f:
            line = line.split("\t")
            relation = line[0].strip('\n') +'\n' # have exactly 1 /n at end
            relations += relation           
    

    f = open(join(toolsPath,'familyDefBlank.txt'), "w")
    f.write('*MEMBER*\n')
    f.write('# USE ONLY LOWER CASE FOR ALL ENTRIES\n')
    f.write('# insert member name\n')
    f.write('# insert other ways Mycroft might hear your name\n')
    f.write('# Each on their own line\n\n')
    f.write('*RELATIVES*\n')
    f.write('# The following are all defined relations\n')
    f.write('# Enter the appopriate name with a tab after each applicable relation\n')        
    f.write('# A line may be duplicated if more than one relation of that type exists\n')
    f.write('# Delete unused lines including these comments\n')
    f.write(relations)
    f.write('\n# Add the above for each member\n')
    f.write('# When complete save as familyDef.txt in this directory')
    f.write('# Then run makeFiles to generate new files')
    f.close()
       
# THIS FILE CREATES PersonKeyword.voc THAT SHOULD BE INSERTED IN DIR FOR KEYWORDS
# IT SHOULD BE RUN WHENEVER FamiltDef.txt IS CHANGED
def makePersonKeword():
    print ("Making PersonKeyword File and storing as PersonKeyword.voc\n")
    dataType = ''
    keywords = ''
    with open(join(toolsPath,'familyDef.txt')) as f:
        for line in f:
            txt = line     
            if (txt == '\n') or (txt[0] == '#'): # Don't process blank lines
                pass
            elif '*MEMBER*' in txt:
                dataType = 'member'
            elif '*RELATIVES*' in txt:
                dataType = 'relatives'
            else:
                if dataType == 'member':
                    keywords += txt
    f = open(join(toolsPath,'PersonKeyword.voc'), "w")
    f.write(keywords)
    f.close()

#THIS IS A DEBUG FILE TO SHOW SYNONYM RELATIONSHIPS
def show_synonyms():
    relations = "" # allowable relations to use for relationship file

    with open(join(toolsPath,'relationsDef.txt')) as f:
        for line in f:
            line = line.split('\t')
            relation = line[0].strip('\n') +'\n' # have exactly 1 /n at end
            relations += relation
                     
    synonyms = importSynonyms()
    
    relationName = relations.split('\n')
    for name in relationName:
        for relation, aka in synonyms:
            if relation == name:
                print (name +' AKA ' + aka)                  

