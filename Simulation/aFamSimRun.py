class self(object):
    dbn = "me"
    relativesTuple = []
    members = []
    synonyms = []
    
import aFamSim
from aFamSimMakTstFile import makeTestFile

aFamSim.__init__(self)        
while 1 == 1:
    answer = input ("enter your question (or ? to see all relationships, quit to exit)  ")
    
    if answer == '?':
        family = makeTestFile()
        testMembers = family[0]
        testRelatives = family[1]
        
        i=0
        for member in testMembers:
            for membersRelatives in testRelatives[i]:
                message = member + ' ' + membersRelatives
                answer = aFamSim.handle_family_intent(self, message)
                print (message + ' is ' + answer)
            i += 1
    elif answer == 'quit':
        break
    elif len(answer.split()) < 2:
        print ('You need to give me more to work with')
    else:  # this is PersonKeyword screen
        valid = False
        for index, name in self.members:
            if name in answer:
                personIndex = int(index)
                valid = True
                break
        if not valid:
            print ('No member found by that name')          
        else:
            print (aFamSim.handle_family_intent(self, answer))


