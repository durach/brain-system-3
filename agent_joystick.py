import re
import agent_abstract
import pygame


class Configuration(agent_abstract.Configuration):
    config_file_tables = 'agentJoystick.ini'

    def __init__(self):
        agent_abstract.Configuration.__init__(self)
        self.import_data()

    def import_data(self):
        self.cp.read(self.config_file_tables_path)
        for k, v in self.cp.items('tables'):
            res = re.search(r'tables\.(?P<table>\d+)\.(?P<type>joystick|button)', k)
            if res:
                matches = res.groupdict()
                try:
                    table_no = int(matches['table'])

                    if table_no not in self.tables:
                        self.tables[table_no] = {'joystick': 0, 'button': 0}

                    self.tables[table_no][matches['type']] = int(v)
                except ValueError:
                    print("Error parsing config key %s" % k)

    def get_table_by_event(self, joy, button):
        for key in self.tables:
            table = self.tables[key]
            if table['joystick'] == joy and table['button'] == (button + 1):  # we add +1 here since pyGame joystick button numbers start from 0
                return key
        return None


class Agent(agent_abstract.Agent):

    def __init__(self):
        agent_abstract.Agent.__init__(self)
        self.init_configuration()
        self.init_joysticks()

    def init_configuration(self):
        self.conf = Configuration()

    def init_joysticks(self):
        joysticks = []
        for joystick_no in range(pygame.joystick.get_count()):
            stick = pygame.joystick.Joystick(joystick_no)
            stick.init()
            joysticks.append(stick)

    def register_events(self):
        self.app.bind(pygame.JOYBUTTONDOWN, self.do_joy_button_down)

    def do_joy_button_down(self, e):
        table_no = self.conf.get_table_by_event(e.joy, e.button)
        if table_no:
            self.app.table_pressed(table_no)
