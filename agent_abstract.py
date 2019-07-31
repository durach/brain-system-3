import configparser
import const
import os


class Configuration:
    config_file_tables = ''

    def __init__(self):
        self.config_file_tables_path = os.path.join(const.CONFIG_DIR, self.config_file_tables)
        self.tables = {}
        self.lamps = {}

        self.cp = configparser.ConfigParser()


class Agent:

    conf = None
    app = False

    def __init__(self):
        pass

    def set_app(self, app):
        self.app = app

    def register_events(self):
        pass

    def lamp_start_on(self):
        pass

    def lamp_false_start_on(self):
        pass

    def lamp_table_on(self, table_no):
        pass

    def all_lamps_off(self):
        pass

    def quit(self):
        pass
