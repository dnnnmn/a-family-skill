from mycroft import MycroftSkill, intent_file_handler

from os.path import dirname, isfile, join

from adapt.intent import IntentBuilder

import sys
import os
#from mycroft.util.log import getLogger
#toolsPath =(join(dirname(__file__),"FamilyTools"))
#sys.path.append(os.path.abspath(toolsPath))
#from aFamilyTools import makeRelationships

thisPath = dirname(__file__)

__author__ = 'is it Tachie'


class AFamily(MycroftSkill):
    def __init__(self):
        super(AFamily, self).__init__(name="AFamily")
        self.myKeywords = []
        self.synonyms = importSynonyms()
        families = importFamilies()
        self.members = families[0]
        self.relativesTuple = families[1]
        
    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        family_intent = IntentBuilder("familyIntent").\
            require("PersonKeyword").\
            one_of("RelationKeyword", "AnimalKeyword").build()
        self.register_intent(family_intent, self.handle_family_intent)
 
    def handle_family_intent(self, message):
        msg = str(message.data.get('utterance'))
         
        # Determine which member is chosen 
        for index, name in self.members:
            if name in msg:
                personIndex = int(index)
                break        
         
        # Search msg for which kind of relative is being sought
        relationSought = []
        words = msg.split()
        for relativeKind, synonym in self.synonyms:
            for word in words:
                if word == synonym:
                    relationSought.append(relativeKind)
                    break
 
        # Find the names of all relatives of this type for the selected member
        relativeChosen = ''
        for relation, name in self.relativesTuple[personIndex]:
             for relative in relationSought: 
                if relation == relative:
                    relativeChosen = name + ' and ' + relativeChosen
                
        if relativeChosen == '':
            relativeChosen = 'no ' + word + ' found'
        else:
            relativeChosen = relativeChosen[0:-5] # remove last ' and '
      
        self.speak_dialog(relativeChosen)
        
# GET SYNONYMS LIST FROM FILE
def importSynonyms():
    synonyms = []
    with open(join(thisPath,'synonyms.txt')) as f:
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

def create_skill():
    return AFamily()

