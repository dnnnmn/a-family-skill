from os.path import dirname, join
thisPath = dirname(__file__)

#GET FAMILY LISTS FROM FILE
def importFamilies():
    relativesTuple = []
    members = []
    familyFile = (join(thisPath,"family.txt"))
    dataType = 'undefined'
    
    with open(familyFile) as f:
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

# CREATE A FILE OF ALL POSSIBLE RELATIVES
def makeTestFile():
    testMembers = []
    testRelatives = []
    availRelatives = []
    relativesFile = (join(thisPath,"relationsDef.txt"))
    
    with open(relativesFile) as f:
        for line in f:
            if (line == '\n') or (line[0] == '#'): # Don't process blank lines
                pass
            else:
                synonyms = line.split('\t')
                availRelatives.append(synonyms[0].strip('\n'))
    #print (availRelatives)                                     

    families = importFamilies()
    index = -1

    for memberPair in families[0]:
        if memberPair[0] != index:
            testMembers.append(memberPair[1])
            index = memberPair[0]

    for familyMembers in families[1]:
        relatives = []
        relativesType = []
        for relativePairs in familyMembers:
            #print (relativePairs)
            relativesType.append(relativePairs[0])
        for relative in availRelatives:
            #print (availRelatives[i])
            if relative in relativesType:
                relatives.append(relative)
        testRelatives.append(relatives)
    #print (testRelatives)
        
    testFile = [testMembers]
    testFile.append(testRelatives)  
    return testFile
