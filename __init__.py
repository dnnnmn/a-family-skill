from mycroft import MycroftSkill, intent_file_handler


class AFamily(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('family.a.intent')
    def handle_family_a(self, message):
        self.speak_dialog('family.a')


def create_skill():
    return AFamily()

