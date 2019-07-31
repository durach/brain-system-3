import re
import agent_abstract
import interface_keusb24b
import threading
import queue

QUEUE_IN_CMD_RELAY_TURN_ON = 1
QUEUE_IN_CMD_RELAY_TURN_OFF = 2
QUEUE_IN_CMD_ALL_RELAYS_TURN_OFF = 3
QUEUE_IN_CMD_QUIT = 4


class Configuration(agent_abstract.Configuration):

    config_file_tables = 'agentKEUSB24R.ini'
    tables = {}
    stand = {'start': {'relay': 0}, 'falsestart': {'relay': 0}}

    def __init__(self):
        agent_abstract.Configuration.__init__(self)
        self.import_data()

    # print self.tables
    # print self.stand

    def import_data(self):
        self.cp.read(self.config_file_tables_path)
        for k, v in self.cp.items('lamps'):
            # Tables
            res = re.search(r'tables\.(?P<table>\d+)\.relay', k)
            if res:
                matches = res.groupdict()
                try:
                    table_no = int(matches['table'])
                    if table_no not in self.tables:
                        self.tables[table_no] = {'relay': 0, 'input': 0}
                    self.tables[table_no]['relay'] = int(v)
                except ValueError:
                    print("Error parsing config key %s" % k)
                continue
            # Start
            res = re.search(r'stand\.(?P<type>start|falsestart)\.relay', k)
            if res:
                matches = res.groupdict()
                try:
                    self.stand[matches['type']]['relay'] = int(v)
                except ValueError:
                    print("Error parsing config key %s" % k)
                continue

        for k, v in self.cp.items('inputs'):
            # Tables
            res = re.search(r'tables\.(?P<table>\d+)\.input', k)
            if res:
                matches = res.groupdict()
                try:
                    table_no = int(matches['table'])
                    if table_no not in self.tables:
                        self.tables[table_no] = {'relay': 0, 'input': 0}
                    self.tables[table_no]['input'] = int(v)
                except ValueError:
                    print("Error parsing config key %s" % k)
                continue

    def get_lamp_by_table(self, table_no):
        if table_no in self.tables:
            return self.tables[table_no]['relay']
        else:
            return False

    def get_lamp_start(self):
        return self.stand['start']['relay']

    def get_lamp_falsestart(self):
        return self.stand['falsestart']['relay']

    def get_all_inputs(self):
        inputs = []
        for table in self.tables.values():
            if table['input'] > 0:
                inputs.append(table['input'])
        return inputs


class Agent(agent_abstract.Agent):
    thread = False
    queue_in = False
    queue_out = False

    def __init__(self):
        agent_abstract.Agent.__init__(self)
        self.init_configuration()

        self.queue_in = queue.Queue()
        self.queue_out = queue.Queue()

        self.thread = ThreadKEUSB24R(self.conf, self.queue_in, self.queue_out)
        self.thread.start()

    def init_configuration(self):
        self.conf = Configuration()

    def register_events(self):
        pass

    def is_initialized(self):
        return self.thread.is_alive()

    def lamp_start_on(self):
        if self.is_initialized():
            self.queue_in.put({'cmd': QUEUE_IN_CMD_RELAY_TURN_ON, 'param': self.conf.get_lamp_start()})

    def lamp_falsestart_on(self):
        # print "lamp_false_start_on"
        if self.is_initialized():
            self.queue_in.put({'cmd': QUEUE_IN_CMD_RELAY_TURN_ON, 'param': self.conf.get_lamp_falsestart()})

    def lamp_table_on(self, table_no):
        # print "lamp_table_on %d"  % table_no
        if self.is_initialized():
            self.queue_in.put({'cmd': QUEUE_IN_CMD_RELAY_TURN_ON, 'param': self.conf.get_lamp_by_table(table_no)})

    def all_lamps_off(self):
        # print "all_lamps_off"
        if self.is_initialized():
            self.queue_in.put({'cmd': QUEUE_IN_CMD_ALL_RELAYS_TURN_OFF, 'param': None})

    def quit(self):
        # print("quit")
        if self.is_initialized():
            self.queue_in.put({'cmd': QUEUE_IN_CMD_QUIT, 'param': None})


class ThreadKEUSB24R(threading.Thread):
    device = False
    queue_in = False
    queue_out = False

    def __init__(self, conf, queue_in, queue_out):
        threading.Thread.__init__(self)
        self.conf = conf
        self.queue_in = queue_in
        self.queue_out = queue_out

    def init_port(self):
        self.device = interface_keusb24b.InterfaceKEUSB24R()
        if self.is_initialized():
            self.device.config_io(self.conf.get_all_inputs())
            return True
        else:
            return False

    def is_initialized(self):
        return self.device.is_initialized()

    def run(self):
        if not self.init_port():
            return

        while True:
            try:
                # Get cmd
                in_cmd = self.queue_in.get(timeout=0.01)

                # Dispatch
                # print in_cmd
                cmd = in_cmd['cmd']
                param = in_cmd['param']
                if cmd == QUEUE_IN_CMD_RELAY_TURN_ON:
                    self.relay_turn_on(param)
                elif cmd == QUEUE_IN_CMD_RELAY_TURN_OFF:
                    self.relay_turn_off(param)
                elif cmd == QUEUE_IN_CMD_ALL_RELAYS_TURN_OFF:
                    self.all_relays_turn_off()
                elif cmd == QUEUE_IN_CMD_QUIT:
                    self.queue_in.task_done()
                    return

                # Task done
                self.queue_in.task_done()
            except queue.Empty:
                pass

            # self.device.get_inputs_state()

    def relay_turn_on(self, lamp):
        # print "relay turn on %d" % lamp
        self.device.relay_turn_on(lamp)

    def relay_turn_off(self, lamp):
        # print "relay turn off %d" % lamp
        self.device.relay_turn_off(lamp)

    def all_relays_turn_off(self):
        for lamp in self.device.lamps:
            self.relay_turn_off(lamp)
