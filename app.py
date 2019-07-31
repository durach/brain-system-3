import time
import math
import pygame.locals
import pq_gui
import const
import mid_text


class App(pq_gui.pqApp):

    timer_value = 0
    system_status = const.STATUS_WAITING
    snd_10sec_played = False
    agent_list = False
    btn_reset = None
    btn_start60 = None
    btn_start20 = None
    lb_timer_text = None
    lb_status = None
    snd_start = None
    snd_false_start = None
    snd_win = None
    snd_10sec = None
    snd_timeout = None
    timer_target_value = None
    timestamp_start_value = None

    def main(self, agent_list):

        # Agent
        self.agent_list = agent_list
        for agent in self.agent_list:
            agent.set_app(self)

        # GUI
        self.draw_gui()
        self.update_timer_label()

        # Events
        for agent in self.agent_list:
            agent.register_events()

        # KeyBoard
        self.init_keyboard()

        # Sounds
        self.init_sounds()

        # Lamps
        self.all_lamps_off()

    def draw_gui(self):
        self.btn_reset = pq_gui.Button(self, ((20, 15), (140, 50)), const.MSG[const.MSG_RESET], self.do_reset, const.STYLE_BUTTON)
        self.btn_reset.pack()

        self.btn_start60 = pq_gui.Button(self, ((20, 80), (140, 50)), const.MSG[const.MSG_START60], self.do_start60, const.STYLE_BUTTON)
        self.btn_start60.pack()

        self.btn_start20 = pq_gui.Button(self, ((20, 145), (140, 50)), const.MSG[const.MSG_START20], self.do_start20, const.STYLE_BUTTON)
        self.btn_start20.pack()

        pq_gui.Box(self, ((185, 21), (220, 75)), const.MSG[const.MSG_TIMER], const.STYLE_TIMER_BOX).pack()
        self.lb_timer_text = mid_text.MidText(self, ((185, 21), (219, 74)), '', const.STYLE_TIMER_TEXT)
        self.lb_timer_text.pack()

        self.lb_status = mid_text.MidText(self, ((185, 110), (220, 85)), const.MSG[const.MSG_WAITING], const.STYLE_STATUS)
        self.lb_status.pack()

        self.bind(const.DBRAIN_TIMER_EVENT, self.do_timer_tick)

    def init_sounds(self):
        self.snd_start = pygame.mixer.Sound(const.SOUND_START)
        self.snd_false_start = pygame.mixer.Sound(const.SOUND_FALSESTART)
        self.snd_win = pygame.mixer.Sound(const.SOUND_WIN)
        self.snd_10sec = pygame.mixer.Sound(const.SOUND_10SEC)
        self.snd_timeout = pygame.mixer.Sound(const.SOUND_TIMEOUT)

    def init_keyboard(self):
        self.bind((pq_gui.KEYDOWN, pq_gui.K_z), self.do_reset)
        self.bind((pq_gui.KEYDOWN, pq_gui.K_x), self.do_start60)
        self.bind((pq_gui.KEYDOWN, pq_gui.K_c), self.do_start20)

    def do_reset(self, e):
        self.lb_status.style[pq_gui.BG_COLOR] = const.COLOR_GREEN
        self.lb_status.settext(const.MSG[const.MSG_WAITING])
        self.reset_timer()
        self.system_status = const.STATUS_WAITING
        self.snd_10sec_played = False
        self.all_lamps_off()

    def do_start60(self, e):
        if self.system_status == const.STATUS_WAITING:
            self.timer_target_value = 60
            self.timestamp_start_value = time.time()
            self.system_status = const.STATUS_STARTED
            self.start_timer()
            self.play_start()
            self.lamp_start_on()

    def do_start20(self, e):
        if self.system_status == const.STATUS_WAITING:
            self.timer_target_value = 20
            self.timestamp_start_value = time.time()
            self.system_status = const.STATUS_STARTED
            self.start_timer()
            self.play_start()
            self.lamp_start_on()

    def start_timer(self):
        pygame.time.set_timer(const.DBRAIN_TIMER_EVENT, 5)
        self.lb_status.settext(const.MSG[const.MSG_STARTED] % self.timer_target_value)

    def stop_timer(self):
        pygame.time.set_timer(const.DBRAIN_TIMER_EVENT, 0)

    def reset_timer(self):
        pygame.time.set_timer(const.DBRAIN_TIMER_EVENT, 0)
        self.timer_value = 0
        self.update_timer_label()

    def finalize_timer(self):
        pygame.time.set_timer(const.DBRAIN_TIMER_EVENT, 0)
        self.timer_value = self.timer_target_value
        self.update_timer_label()

    def do_timer_tick(self, e):
        if self.system_status == const.STATUS_WAITING:  # Sometimes timer can do one tick after reset_timer
            return

        timestamp_current_value = time.time()
        self.timer_value = timestamp_current_value - self.timestamp_start_value

        if (0 < (self.timer_target_value - self.timer_value) <= 10) and (not self.snd_10sec_played):
            self.snd_10sec_played = True
            self.play_10sec()

        if (self.timer_target_value - self.timer_value) < 0:
            self.lb_status.settext(const.MSG[const.MSG_TIMEOUT])
            self.system_status = const.STATUS_STOPPED
            self.finalize_timer()
            self.play_timeout()
        self.update_timer_label()

    def exit(self, event=None):
        # print("Before quit")
        
        for agent in self.agent_list:
            agent.all_lamps_off()
            agent.quit()

        pq_gui.pqApp.exit(self, event)

    def update_timer_label(self):
        if self.timer_value == 0:
            self.lb_timer_text.settext('00:00')
            self.lb_timer_text.style[const.TEXT_COLOR] = const.COLOR_BLACK
        else:
            (milliseconds, seconds) = math.modf(self.timer_value)
            if 0 < (self.timer_target_value - self.timer_value) <= 10:
                self.lb_timer_text.style[const.TEXT_COLOR] = const.COLOR_RED
            else:
                self.lb_timer_text.style[const.TEXT_COLOR] = const.COLOR_BLACK
            self.lb_timer_text.settext('%02d:%02d' % (seconds, milliseconds * 100))

    def table_pressed(self, table_no):
        if self.system_status == const.STATUS_STARTED:
            self.process_win(table_no)

        elif self.system_status == const.STATUS_WAITING:
            self.process_false_start(table_no)
            self.system_status = const.STATUS_STOPPED

    def process_win(self, table_no):
        self.lb_status.style[const.BG_COLOR] = const.COLOR_RED
        self.lb_status.settext(const.MSG[const.MSG_PRESSED] % (table_no))
        self.system_status = const.STATUS_STOPPED
        self.stop_timer()
        self.play_win(table_no)
        self.lamp_table_on(table_no)

    def process_false_start(self, table_no):
        self.lb_status.style[const.BG_COLOR] = const.COLOR_BLUE
        self.lb_status.settext(const.MSG[const.MSG_FALSESTART] % (table_no))
        self.system_status = const.STATUS_STOPPED
        self.play_falsestart(table_no)
        self.lamp_falsestart_on()
        self.lamp_table_on(table_no)

    # Sounds

    def play_start(self):
        self.snd_start.play()

    def play_falsestart(self, table_no):
        self.snd_false_start.play()

    def play_win(self, table_no):
        self.snd_win.play()

    def play_10sec(self):
        self.snd_10sec.play()

    def play_timeout(self):
        self.snd_timeout.play()

    # Lamps

    def lamp_start_on(self):
        for agent in self.agent_list:
            agent.lamp_start_on()

    def lamp_falsestart_on(self):
        for agent in self.agent_list:
            agent.lamp_false_start_on()

    def lamp_table_on(self, table_no):
        for agent in self.agent_list:
            agent.lamp_table_on(table_no)

    def all_lamps_off(self):
        for agent in self.agent_list:
            agent.all_lamps_off()
