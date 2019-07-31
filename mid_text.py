import pq_gui


class MidText(pq_gui.Widget):
    default_style = {pq_gui.BD_TYPE:pq_gui.BD_NONE}
    widget_name = 'MidText'

    # wrap: none, char, word
    def __init__(self, parent, rect, text, style=None, wrap=pq_gui.WRAP_WORD, state=pq_gui.ENABLED):
        self.wrap = wrap
        pq_gui.Widget.__init__(self, parent, rect, style, state)
        self.settext(text)

    def settext(self, text):
        self.text = text
        self.text_render = pq_gui.restrict_text(text, self.style, self.size, self.wrap)

    def draw(self, screen, position):
        pq_gui.Widget.draw(self, screen, position)

        mid = (self.x + position[0] + self.width/2,self.y + position[1] + self.height/2)
        if self.text_render:
            screen.blit(self.text_render, (mid[0] - self.text_render.get_width()/2, mid[1] - self.text_render.get_height()/2))
            #screen.blit(self.text_render, (self.x + position[0],self.y + position[1]))
