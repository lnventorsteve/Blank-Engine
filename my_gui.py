import json
import math
import os
import time
import pyperclip
import pygame

pygame.init()
default_font = pygame.font.SysFont(pygame.font.get_default_font(), 24)

# lookup tables
shift_table = {
    32: 32,
    33: 33,
    34: 34,
    35: 35,
    36: 36,
    37: 37,
    38: 38,
    39: 34,
    40: 40,
    41: 41,
    42: 42,
    43: 43,
    44: 44,
    45: 95,
    46: 46,
    47: 63,
    48: 41,
    49: 33,
    50: 64,
    51: 35,
    52: 36,
    53: 37,
    54: 94,
    55: 38,
    56: 42,
    57: 40,
    58: 58,
    59: 58,
    60: 60,
    61: 43,
    62: 62,
    63: 63,
    64: 64,
    65: 65,
    66: 66,
    67: 67,
    68: 68,
    69: 69,
    70: 70,
    71: 71,
    72: 72,
    73: 73,
    74: 74,
    75: 75,
    76: 76,
    77: 77,
    78: 78,
    79: 79,
    80: 80,
    81: 81,
    82: 82,
    83: 83,
    84: 84,
    85: 85,
    86: 86,
    87: 87,
    88: 88,
    89: 89,
    90: 90,
    91: 123,
    92: 124,
    93: 125,
    94: 126,
    95: 95,
    96: 126,
    97: 65,
    98: 66,
    99: 67,
    100: 68,
    101: 69,
    102: 70,
    103: 71,
    104: 72,
    105: 73,
    106: 74,
    107: 75,
    108: 76,
    109: 77,
    110: 78,
    111: 79,
    112: 80,
    113: 81,
    114: 82,
    115: 83,
    116: 84,
    117: 85,
    118: 86,
    119: 87,
    120: 88,
    121: 89,
    122: 90,
    123: 91,
    124: 92,
    125: 93,
    126: 126}


class Input:
    def __init__(self):
        self.Keys_pressed = {}  # raw key info
        self.keys = []  # key info with filter for button input
        self.unicode = []  # key info with filter for text input
        self.cursor_state = False
        self.mouse_info = (0, 0, 0)
        self.mouse_button = 0
        self.mouse_position = (0, 0)
        self.p_mouse_position = (0, 0)
        self.c_time = 0
        self.scroll_amount = 0
        self.mods = []
        self.CAPS = False
        self.looked_x = 0
        self.looked_y = 0
        self.capture_mouse = False

    def get_input(self, event, frame):
        if event.type == pygame.MOUSEMOTION:
            mx, my = self.mouse_position = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button = event.button

        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button = 0
            mb = event.button
            scroll = mb
            if mb > 7:
                if mb % 2 == 0:
                    scroll -= 3
                    self.scroll_amount = -scroll
                else:
                    scroll -= 7
                    self.scroll_amount = scroll
            else:
                if mb == 4:
                    self.scroll_amount = -1
                if mb == 5:
                    self.scroll_amount = 1

        if event.type == pygame.KEYDOWN:
            key = event.key
            self.Keys_pressed[key] = [frame, time.perf_counter() + 0.5]
            if key > 1000000000:
                if key == 1073742049:
                    self.mods.append("SHIFT")
                elif key == 1073742048:
                    self.mods.append("CTRL")
                elif key == 1073742050:
                    self.mods.append("ALT")
                elif key == 1073742051:
                    self.mods.append("WIN")
                elif key == 1073742053:
                    self.mods.append("SHIFT")
                elif key == 1073742054:
                    self.mods.append("ALT")
                elif key == 1073742052:
                    self.mods.append("CTRL")
                elif key == 1073742881:
                    if "Caps" in self.mods:
                        self.mods.remove("Caps")
                    else:
                        self.mods.append("Caps")

        if event.type == pygame.KEYUP:
            key = event.key
            self.Keys_pressed.pop(key)

            if key > 1000000000:
                if key == 1073742049:
                    self.mods.remove("SHIFT")
                elif key == 1073742048:
                    self.mods.remove("CTRL")
                elif key == 1073742050:
                    self.mods.remove("ALT")
                elif key == 1073742051:
                    self.mods.remove("WIN")
                elif key == 1073742053:
                    self.mods.remove("SHIFT")
                elif key == 1073742054:
                    self.mods.remove("ALT")
                elif key == 1073742052:
                    self.mods.remove("CTRL")

    def update(self, frame):

        self.mouse_info = (self.mouse_position[0], self.mouse_position[1], self.mouse_button)
        if self.capture_mouse:
            pygame.mouse.set_visible(False)
            self.looked_x = self.p_mouse_position[0] - self.mouse_position[0]
            self.looked_y = self.p_mouse_position[1] - self.mouse_position[1]
            self.p_mouse_position = self.mouse_position
        else:
            pygame.mouse.set_visible(True)

        ct = time.perf_counter()
        self.keys = []
        for key in self.Keys_pressed:
            kf, kt = self.Keys_pressed[key]
            if kf == frame:
                self.keys.append(key)
            if ct > kt:
                self.keys.append(key)
                self.Keys_pressed[key] = [kf, kt + 0.05]
        self.unicode = []
        for key in self.keys:
            if key in shift_table:
                if "SHIFT" in self.mods or "CAPS" in self.mods:
                    self.unicode.append(chr(shift_table[key]))
                else:
                    self.unicode.append(chr(key))

    def cursor(self):
        if time.perf_counter() >= self.c_time:
            self.c_time = time.perf_counter() + 0.5
            self.cursor_state = not self.cursor_state
        return self.cursor_state

    def Keys_pressedraw(self):
        return self.Keys_pressed

    def mouse(self):
        return self.mouse_info

    def clicked(self):
        self.mouse_button = -abs(self.mouse_button)
        mx, my = self.mouse_position
        self.mouse_info = (mx, my, self.mouse_button)

    def scroll(self):
        scroll_amount = self.scroll_amount
        self.scroll_amount = 0
        return scroll_amount
class Theme:
    def __init__(self, screen_info=(None, (0, 0), 0), font=default_font, font_size=12,
                 font_name=pygame.font.get_default_font(), text_color=(255, 255, 255), border_color=(128, 128, 128),
                 background_color=(64, 64, 64)):
        self.display = screen_info[0]
        self.screen = screen_info[1]
        self.width = self.screen[0] * 2
        self.height = self.screen[1] * 2
        self.scale = screen_info[2]
        self.font_name = font_name
        self.font = font
        self.font_size = font_size
        self.Colors = {text_color, border_color, background_color}
        self.tcolor = text_color
        self.bcolor = border_color
        self.bgcolor = background_color
        self.Sounds = {}
        self.sound_info = {}
        self.border = 3
        self.path = str(os.path.dirname(__file__))

    def save_Theme(self):
        Theme = {}
        Theme["Colors"] = self.Colors
        Theme["Sounds"] = self.sound_info
        Theme["Fonts"] = {}
        Theme["Fonts"][self.font_name] = self.font_size
        Theme["Properties"] = {}
        Theme["Properties"]["Border Thickness"] = self.border

        return Theme

    def load_Theme(self, config, Theme=False):
        if Theme == False:
            file = config["theme"]
        else:
            file = Theme

        with open(f"{self.path}/Themes/{file}.json", "r") as Theme:
            Theme = json.loads(Theme.read())
            Fonts = []
            for font in Theme["Fonts"]:
                Fonts.append(font)
            self.font = pygame.font.SysFont(Fonts[0], Theme["Fonts"][Fonts[0]] * config["scale"])
            self.font_size = Theme["Fonts"][Fonts[0]]
            self.font_name = Fonts[0]
            for sound in Theme["Sounds"]:
                try:
                    self.Sounds[sound] = pygame.mixer.Sound(f"{self.path}/sounds/{Theme['Sounds'][sound]['name']}")
                    self.Sounds[sound].set_volume(Theme["Sounds"][sound]["volume"])
                except:
                    self.Sounds[sound] = []
                    for name in Theme['Sounds'][sound]['names']:
                        temp = pygame.mixer.Sound(f"{self.path}/sounds/{name}")
                        temp.set_volume(Theme["Sounds"][sound]["volume"])
                        self.Sounds[sound].append(temp)
            self.sound_info = Theme["Sounds"]
            self.Colors = Theme["Colors"]
            self.tcolor = Theme["Colors"]['Text color']
            self.bcolor = Theme["Colors"]['Border color']
            self.bgcolor = Theme["Colors"]['Background color']
            self.border = Theme["Properties"]["Border Thickness"]

    def change_Theme(self, new_theme):
        with open(f"{self.path}/Themes/{new_theme}.json", "r") as Theme:
            Theme = json.loads(Theme.read())
            Fonts = []
            for font in Theme["Fonts"]:
                Fonts.append(font)
            self.font = pygame.font.SysFont(Fonts[0], Theme["Fonts"][Fonts[0]] * self.scale)
            self.font_size = Theme["Fonts"][Fonts[0]]
            self.Sounds = {}
            for sound in Theme["Sounds"]:
                try:
                    self.Sounds[sound] = pygame.mixer.Sound(f"{self.path}/sounds/{Theme['Sounds'][sound]['name']}")
                    self.Sounds[sound].set_volume(Theme["Sounds"][sound]["volume"])
                except:
                    self.Sounds[sound] = []
                    for name in Theme['Sounds'][sound]['names']:
                        temp = pygame.mixer.Sound(f"{self.path}/sounds/{name}")
                        temp.set_volume(Theme["Sounds"][sound]["volume"])
                        self.Sounds[sound].append(temp)
            self.sound_info = Theme["Sounds"]
            self.Colors = Theme["Colors"]
            self.tcolor = Theme["Colors"]['Text color']
            self.bcolor = Theme["Colors"]['Border color']
            self.bgcolor = Theme["Colors"]['Background color']
            self.border = Theme["Properties"]["Border Thickness"]

    def fonts(self, font_name=False, font_size=False):
        if font_name != False:
            self.font_name = font_name
        if font_size != False:
            self.font_size = font_size

        if font_name != False or font_size != False:
            self.font = pygame.font.SysFont(self.font_name, self.font_size * self.scale)

        return self.font

    def screen_info(self, screen_info=False, display=False, screen=False, scale=False):
        if screen_info != False:
            self.display = screen_info[0]
            self.screen = screen_info[1]
            self.width = self.screen[0] * 2
            self.height = self.screen[1] * 2
            self.scale = screen_info[2]
            self.font = pygame.font.SysFont(self.font_name, self.font_size * self.scale)
        if display != False:
            self.display = display
        if screen != False:
            self.screen = screen
        if scale != False:
            self.scale = scale
            self.font = pygame.font.SysFont(self.font_name, self.font_size * self.scale)
        return (self.display, self.screen, self.scale)

    def colors(self, colors=False, text_color=False, border_color=False, background_color=False):
        if colors != False:
            self.tcolor = colors[0]
            self.bcolor = colors[1]
            self.bgcolor = colors[2]
            self.Colors = {}
            self.Colors["Text color"] = self.tcolor
            self.Colors["Border color"] = self.bcolor
            self.Colors["Background color"] = self.bgcolor
        if text_color != False:
            self.tcolor = text_color
            self.Colors["Text color"] = self.tcolor
        if border_color != False:
            self.bcolor = border_color
            self.Colors["Border color"] = self.bcolor
        if background_color != False:
            self.bgcolor = background_color
            self.Colors["Background color"] = self.bgcolor

        return (self.tcolor, self.bcolor, self.bgcolor)

    def sounds(self, name=False, sound=False, volume=False):
        if name != False:
            if name in self.Sounds:
                if sound != False:
                    self.Sounds[name] = pygame.mixer.Sound("sounds/" + sound)
                    self.sound_info[name]["name"] = sound
                if volume != False:
                    if type(self.Sounds[name]) != list:
                        self.Sounds[name].set_volume(volume / 100)
                        self.sound_info[name]["volume"] = volume
                return self.Sounds[name]
        else:
            if volume != False:
                for sound in self.Sounds:
                    if type(self.Sounds[sound]) != list:
                        self.Sounds[sound].set_volume((volume / 100) * (self.sound_info[sound]["volume"] / 100))
            return self.Sounds
class Renderer:
    def __init__(self, theme):
        self.theme = theme
        self.windows = []
        self.base_window = []

    def add_window(self, window):
        self.windows.append(window)

    def remove_window(self, window):
        print(self.windows.index(window))

    def sort_windows(self, window):
        return window.last_click

    def render(self):
        self.windows.sort(key=self.sort_windows, reverse=True)
        for window in self.windows:
            window.render()

def box(renderer, pos, size, border_color=False, background_color=False):
    theme = renderer.theme
    display, screen, scale = theme.screen_info()
    tcolor, bcolor, bgcolor = theme.colors()
    if border_color:
        bcolor = border_color
    if background_color:
        bgcolor = background_color
    sx, sy = screen
    px, py = pos = pos
    x, y = sx + px * scale, sy + py * scale
    x2, y2 = size = size
    x2, y2 = x2 * scale, y2 * scale

    pygame.draw.rect(display, bcolor, (x - x2 / 2, y - y2 / 2, x2, y2))
    pygame.draw.rect(display, bgcolor, (
    (x - x2 / 2) + theme.border, (y - y2 / 2) + theme.border, x2 - theme.border * 2, y2 - theme.border * 2))

    return x - x2 / 2, y - y2 / 2, x + x2 / 2, y + y2 / 2
def button(renderer, pos, size, _text, input):
    theme = renderer.theme
    display, screen, scale = theme.screen_info()
    tcolor, bcolor, bgcolor = theme.colors()
    sound = theme.sounds("button")
    sx, sy = screen
    x, y = pos
    x, y = sx + x * scale, sy + y * scale
    x2, y2 = size
    x2, y2 = x2 * scale, y2 * scale
    mx, my, mb = input.mouse()
    if x - x2 / 2 < mx < x + x2 / 2 and y - y2 / 2 < my < y + y2 / 2:
        r, g, b = bgcolor
        if r - 16 < 0:
            r = 0
        else:
            r -= 16
        if g - 16 < 0:
            g = 0
        else:
            g -= 16
        if b - 16 < 0:
            b = 0
        else:
            b -= 16
        bgcolor = r, g, b
        if mb == 1:
            if sound != False:
                pygame.mixer.Sound.play(sound)
            input.clicked()
            return True
    Text(renderer, pos, _text, True, size, background_color=bgcolor).render()
    return False
def get_center(center, scale, pos, tx=0, ty=0, size=(0, 0)):
    x, y = pos
    sx, sy = size
    sx = sx / 2 * scale
    sy = sy / 2 * scale
    if center == "left":
        pos = (x + tx / 2 - sx, y)
    elif center == "right":
        pos = (x - tx / 2 + sx, y)
    elif center == "top":
        pos = (x, y - ty / 2 - sy)
    elif center == "bottom":
        pos = (x, y + ty / 2 + sy)
    elif center == "top_left":
        pos = (x + tx / 2 - sx, y + ty / 2 - sy)
    elif center == "top_right":
        pos = (x - tx / 2 + sx, y + ty / 2 - sy)
    elif center == "bottom_left":
        pos = (x + tx / 2, y - ty / 2 + sy)
    elif center == "bottom_right":
        pos = (x - tx / 2 + sx, y - ty / 2 + sy)
    return pos
def switch(renderer, pos, state, input):
    theme = renderer.theme
    display, screen, scale = theme.screen_info()
    tcolor, bcolor, bgcolor = theme.colors()
    sound = theme.sounds("button")
    sx, sy = screen
    x, y = pos
    x, y = sx + x * scale, sy + y * scale
    mx, my, mb = input.mouse()
    if mx != 0 and my != 0 and mb == 1:
        if x - 10 * scale < mx < x + 10 * scale:
            if y - 4 * scale < my < y + 4 * scale:
                if sound != False:
                    pygame.mixer.Sound.play(sound)
                state = not state
                input.clicked()
    if state:
        pygame.draw.circle(display, (0, 200, 0), (x - 6 * scale, y), 4 * scale)
        pygame.draw.rect(display, (0, 200, 0), (x - 6 * scale, y - 4 * scale, 13 * scale, 8 * scale))
        pygame.draw.circle(display, tcolor, (x + 6 * scale, y), 4 * scale)
    else:
        pygame.draw.circle(display, (255, 0, 0), (x + 6 * scale, y), 4 * scale)
        pygame.draw.rect(display, (255, 0, 0), (x - 6 * scale, y - 4 * scale, 13 * scale, 8 * scale))
        pygame.draw.circle(display, tcolor, (x - 6 * scale, y), 4 * scale)
    return (state)
def hit_box(renderer, pos, size, input):
    theme = renderer.theme
    display, screen, scale = theme.screen_info()
    sound = theme.sounds("button")
    sx, sy = screen
    x, y = pos
    x, y = sx + x * scale, sy + y * scale
    x2, y2 = size
    mx, my, mb = input.mouse()
    if mx != 0 and my != 0 and mb == 1:
        if x - (x2 / 2) * scale < mx < x + (x2 / 2) * scale:
            if y - (y2 / 2) * scale < my < y + (y2 / 2) * scale:
                if sound != False:
                    pygame.mixer.Sound.play(sound)
                input.clicked()
                return True
    return False
def hover(renderer, pos, size, input):
    theme = renderer.theme
    display, screen, scale = theme.screen_info()
    sx, sy = screen
    x, y = pos
    x, y = sx + x * scale, sy + y * scale
    x2, y2 = size
    mx, my, mb = input.mouse()
    if x - (x2 / 2) * scale < mx < x + (x2 / 2) * scale:
        if y - (y2 / 2) * scale < my < y + (y2 / 2) * scale:
            return True
    return False
def update(self, input, maxTextLength=False):
    sound = self.sound
    sx, sy = self.screen
    x, y = self.pos
    x, y = sx + x * self.scale, sy + y * self.scale
    size_x, size_y = self.size
    x2, y2 = size_x * self.scale, size_y * self.scale
    mx, my, mb = input.mouse()
    centerX, centerY = get_center(self.center, self.scale, self.pos, size=self.size)
    mods = input.mods
    bgcolor = self.bgcolor
    if x - x2 / 2 < mx < x + x2 / 2 and y - y2 / 2 < my < y + y2 / 2:
        r, g, b = bgcolor
        if r - 16 < 0:
            r = 0
        else:
            r -= 16
        if g - 16 < 0:
            g = 0
        else:
            g -= 16
        if b - 16 < 0:
            b = 0
        else:
            b -= 16
        bgcolor = r, g, b
        if mb == 1:
            input.clicked()
            if self.text == self.default_text:
                self.text = ""
            if sound != False:
                pygame.mixer.Sound.play(sound)
            self.in_text = True
    else:
        if mb != 0:
            self.in_text = False
            if self.text == "":
                self.text = self.default_text

    if self.in_text:
        # split text at cursor
        if self.pointer == 0:
            text1 = self.text
            text2 = ""
        else:
            text1 = self.text[:-self.pointer]
            text2 = self.text[-self.pointer:]
        for key in input.keys:
            # backsapce
            if key == 8:
                text1 = text1[:-1]
                self.text = text1 + text2
                max = len(self.text)
                if self.pointer > max:
                    self.pointer = max
                #print(self.pointer)
            # delete
            elif key == 127:
                text2 = text2[1:]
                self.text = text1 + text2
                if self.pointer > 0:
                    self.pointer -= 1
                #print(self.pointer)
            # enter
            elif key == 13 or key == 27:
                self.in_text = False
                if self.text == "":
                    self.text = self.default_text

            # left arrow
            elif key == 1073741904:
                max = len(self.text)
                self.pointer += 1
                if self.pointer > max:
                    self.pointer = max
                #print(self.pointer)
            # right arrow
            elif key == 1073741903:
                if self.pointer > 0:
                    self.pointer -= 1
                #print(self.pointer)
            # ctrl-v
            elif key == 118 and "CTRL" in mods:
                print("ctrl-v")
                data = pyperclip.paste()
                self.text = text1 + data + text2
            # ctrl-c
            elif key == 99 and "CTRL" in mods:
                print("ctrl-c")
                pyperclip.copy(self.text)
            # ctrl-x
            elif key == 120 and "CTRL" in mods:
                print("ctrl-x")
                pyperclip.copy(self.text)
                self.text = ""
            # ctrl-delete
            elif key == 127 and "CTRL" in mods:
                self.text = ""

            # add key to text
            else:
                for key in input.unicode:
                    textX, textY = self.font.size(self.text)
                    if maxTextLength != False:
                        if textX + 20 < maxTextLength:
                            text1 = text1 + key
                            textX, textY = self.font.size(text1 + text2)
                            if textX + 10 > maxTextLength:
                                text1 = text1[:-1]
                            self.text = text1 + text2
                    else:
                        self.text = text1 + key + text2

        _text = self.text
        textX, textY = self.font.size(_text)
        textOffset = self.font.size(self.text[:-len(_text)])
        Text(self.window, self.pos, _text, self.in_box, self.size, background_color=bgcolor, cut_dir=True,
             center=self.center).render()

        if input.cursor():
            t1x, t1y = self.font.size(text1)
            t1x -= (textX + textOffset[0]) / 2 + textOffset[0] / 2
            if t1x > (self.size[0] * self.scale) / 2 - self.theme.border * self.scale:
                t1x = (self.size[0] * self.scale) / 2 - self.theme.border * self.scale

            pygame.draw.line(self.display, self.tcolor, (x + t1x, y + t1y / 2.5), (x + t1x, y - t1y / 2.5), self.scale)

        #set pointer on mouse click
        if x - x2 / 2 < mx < x + x2 / 2 and y - y2 / 2 < my < y + y2 / 2 and mb == 1:
            clicked = True
            mx = mx - self.screen[0] - centerX * self.scale
    else:
        _text = self.text
        tx, ty = self.font.size(_text)
        if maxTextLength != False:
            while tx + 10 > x2:
                _text = _text[1:]
                tx, ty = self.font.size(_text)
        Text(self.window, (centerX, centerY), _text, self.in_box, self.size, background_color=bgcolor).render()
def get_text(self):
    return str(self.text)
def change_text(self, text):
    p_text = self.text
    self.text = str(text)
    return str(p_text)
def button_list(renderer, pos, size, options, max, Input):
    for each in options:
        if Button(renderer, pos, size, each, Input).render():
            return each
        pos += size[1] + 5
def alert(renderer, pos, size, name, button1, button2, Input, frame, timer=False, center="center"):
    name = str(name)
    button1 = str(button1)
    button2 = str(button2)
    x, y = pos
    sx, sy = size
    theme = renderer.theme
    scale = theme.scale
    text_x, text_y = theme.font.size(name)
    name_list = name.split(" ")
    if timer != False:
        timer = time.perf_counter() + timer
    while True:
        for event in pygame.event.get():
            Input.get_input(event, frame)
        Input.update(frame)
        if timer != False:
            if timer < time.perf_counter():
                return False
        box(renderer, pos, size)
        line = ""
        Pos = 0
        for each in name_list:
            line += each + " "
            text_x, text_y = theme.font.size(line)
            if text_x > (sx * scale) / 2 + 20:
                Label(renderer, (x, y - sy / 2 + 15 + Pos), line).render()
                line = ""
                Pos += 15
        Label(renderer, (x, y - sy / 2 + 15 + Pos), line)
        if button(renderer, (x - sx / 2 + sx / 4, y + sy / 2 - 20), (sx / 3, 15), button1, Input):
            return True
        if button(renderer, (x + sx / 2 - sx / 4, y + sy / 2 - 20), (sx / 3, 15), button2, Input):
            return False
        if timer != False:
            Label(renderer, (x, y + sy / 2 - 20), round(timer - time.perf_counter())).render()
        frame += 1
        pygame.display.update()
        time.sleep(0.05)
"""
def graph(theme, pos, size, values, name):
    display, screen, scale = theme.screen_info()
    tcolor,bcolor,bgcolor = theme.colors()
    sx, sy = screen
    px, py = pos
    x, y = sx + px * scale, sy + py * scale
    sx, sy = size
    x2, y2 = sx * scale, sy * scale
    gx, gy = x + x2 / 2, y + y2 / 2
    box(theme, pos, size)

    text(theme, (px, py + sy / 1.7), name, tcolor)
    p_point = None
    total_x = len(values) - 1
    p_time = total_x
    for point in values:
        if point > 100:
            point = 100
        py = point * (y2 / 100)
        if p_point != None:
            ppx, ppy = p_point
            pygame.draw.line(display, tcolor, ((gx - p_time * (x2 / total_x)), gy - py),
                             (gx - ppx * (x2 / total_x), gy - ppy), 2)
        p_point = (p_time, py)
        p_time -= 1


def vertical_bar_graph(theme, pos, size, value,max_value = 100,min_value = 0, name = ""):
    display, screen, scale = theme.screen_info()
    color,bcolor,bgcolor = theme.colors()
    sx, sy = screen
    px, py = pos
    x, y = sx + px * scale, sy + py * scale
    sx, sy = size
    x2, y2 = sx * scale, sy * scale
    box(theme, pos, size)
    if value > max_value:
        pygame.draw.rect(display, bcolor, (x - x2 / 2, (y + y2 / 2) - y2, x2, y2))
    else:
        fill = (y2 / max_value) * value
        pygame.draw.rect(display, color, (x - x2 / 2, (y + y2 / 2) - fill, x2, fill))
    text(theme,(px, py - sy / 1.7), name)


def horizontal_bar_graph(theme, pos, size, value, name):
    display, screen, scale = theme.screen_info()
    color,bcolor,bgcolor = theme.colors()
    sx, sy = screen
    px, py = pos
    x, y = sx + px * scale, sy + py * scale
    sx, sy = size
    x2, y2 = sx * scale, sy * scale
    box(theme, pos, size)
    if value > 100:
        pygame.draw.rect(display, bcolor, (x - x2 / 2, (y + y2 / 2) - y2, x2, y2))
    else:
        fill = (x2 / 100) * value
        pygame.draw.rect(display, color, ((x - x2 / 2), (y - y2 / 2), fill, y2))
    text(theme, (px, py + y2 / 3), name)


def multi_graph(theme, pos, size, time, values, name):
    display, screen, scale = theme.screen_info()
    sx, sy = screen
    px, py = pos
    x, y = sx + px * scale, sy + py * scale
    sx, sy = size
    x2, y2 = sx * scale, sy * scale
    gx, gy = x + x2 / 2, y + y2 / 2
    box(theme, pos, size)
    text(theme, (px, py + sy / 1.85), name)
    for value in values:
        color = value[:3]
        print(color)
        value = value[3:]
        p_point = None
        p_time = len(time) - 1
        max_time = time[-1]
        print(max_time)
        for _ in value:
            point = value[p_time]
            if point > 100:
                point = 100
            py = point * ((y2 - 2) / 100)
            if p_point != None:
                ppx, ppy = p_point
                pygame.draw.line(display, color, ((gx - (time[-p_time - 1] * (x2 / max_time))), (gy - py - 2)),
                                 ((gx - (ppx * (x2 / max_time))), (gy - ppy - 2)), 2)
            p_point = (time[-p_time - 1], py)
            p_time -= 1
"""


class Box:
    def __init__(self, window, pos, size, border_color=False, background_color=False, resize=False):
        self.window = window
        self.renderer = window.renderer
        self.theme = self.renderer.theme
        self.display, self.screen, self.scale = self.theme.screen_info()
        self.tcolor, self.bcolor, self.bgcolor = self.theme.colors()
        if border_color != False:
            self.bcolor = border_color
        if background_color != False:
            self.bgcolor = background_color

        self.init_pos = pos
        self.resize = resize
        self.sx, self.sy = self.screen
        self.px, self.py = self.pos = pos
        self.x, self.y = self.sx + self.px * self.scale, self.sy + self.py * self.scale
        self.x2, self.y2 = self.size = size
        self.x2, self.y2 = self.x2 * self.scale, self.y2 * self.scale

        self.rect = (self.x - self.x2 / 2, self.y - self.y2 / 2, self.x + self.x2 / 2, self.y + self.y2 / 2)
    def get_rect(self):
        return self.rect
    def update(self, window):
        self.pos = (self.init_pos[0] + window.pos[0], self.init_pos[1] + window.pos[1])
        if self.resize:
            scale = (window.size[0] / window.init_size[0], window.size[1] / window.init_size[1])
        else:
            scale = (1, 1)

        self.px, self.py = self.pos
        self.x, self.y = self.sx + self.px * self.scale, self.sy + self.py * self.scale
        self.x2, self.y2 = self.size
        self.x2, self.y2 = self.x2 * self.scale * scale[0], self.y2 * self.scale * scale[1]
    def render(self):
        pygame.draw.rect(self.display, self.bcolor, (self.x - self.x2 / 2, self.y - self.y2 / 2, self.x2, self.y2))
        pygame.draw.rect(self.display, self.bgcolor, ((self.x - self.x2 / 2) + self.theme.border,
                                                      (self.y - self.y2 / 2) + self.theme.border,
                                                      self.x2 - self.theme.border * 2, self.y2 - self.theme.border * 2))
class Text:
    def __init__(self, window, pos, text, in_box=False, size=(0, 0), text_color=False
                 , border_color=False, background_color=False, center="center"
                 , cut_dir=False, resize=False):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme = self.renderer.theme
        self.pos = pos
        self.in_box = in_box
        self.resize = resize
        self.display, self.screen, self.scale = theme.screen_info()
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.center = center
        self.cut_dir = cut_dir

        if text_color:
            self.tcolor = text_color
        if border_color:
            self.bcolor = border_color
        if background_color:
            self.bgcolor = background_color
        self.size = size
        sx, sy = self.screen
        x, y = self.pos
        self.x, self.y = sx + x * self.scale, sy + y * self.scale
        self.init_pos = (self.x, self.y)
        tx, ty = self.font.size(str(text))

        if in_box:
            self.box = Box(self.window, self.pos, size, self.bcolor, self.bgcolor, resize=resize)
            while tx > size[0] * self.scale:
                if cut_dir:
                    text = text[1:]
                else:
                    text = text[:-1]
                tx = self.font.size(str(text))[0]

        self.text = text
        self.text_pos = (tx, ty)
        self.tx, self.ty = tx, ty
        self.text_text = self.font.render(str(text), True, self.tcolor)


    def update(self, window):

        if self.resize:
            scale = (window.size[0] / window.init_size[0], window.size[1] / window.init_size[1])
        else:
            scale = (1, 1)

        if self.in_box:
            self.box.update(window)
        #print(scale)

        self.x, self.y = (self.init_pos[0] * scale[0] + window.pos[0] * self.scale,
                          self.init_pos[1] * scale[1] + window.pos[1] * self.scale)

    def change_text(self,text):
        tx, ty = self.font.size(str(text))

        if self.in_box:
            self.box = Box(self.window, self.pos, self.size, self.bcolor, self.bgcolor, resize=self.resize)
            while tx > self.size[0] * self.scale:
                if self.cut_dir:
                    text = text[1:]
                else:
                    text = text[:-1]
                tx = self.font.size(str(text))[0]

        self.text = text
        self.text_pos = (tx, ty)
        self.tx, self.ty = tx, ty
        self.text_text = self.font.render(str(text), True, self.tcolor)

    def render(self):
        if self.in_box:
            self.box.render()

        self.display.blit(self.text_text,
                          get_center(self.center, self.scale,
                                     (self.x - self.tx / 2, self.y - self.ty / 2),
                                     self.tx,self.ty, self.size))
class Button:
    def __init__(self, window, pos, size, text, input, resize=False):
        self.window = window
        self.renderer = window.renderer
        self.theme = self.renderer.theme
        self.display, self.screen, self.scale = self.theme.screen_info()
        self.tcolor, self.bcolor, self.bgcolor = self.theme.colors()
        self.sound = self.theme.sounds("button")
        self.pos = pos
        self.size = size
        self.input = input
        self.resize = resize
        self.name = text
        self.text = Text(window, pos, text, True, size)
        self.state = False

    def update(self, window):
        pos = window.pos
        self.text.update(window)
        if self.resize:
            scale = (window.size[0] / window.init_size[0], window.size[1] / window.init_size[1])
        else:
            scale = (0, 0)

        sx, sy = self.screen
        x, y = self.pos
        x, y = (pos[0] + x) * self.scale + sx, (pos[1] + y) * self.scale + sy
        x2, y2 = (self.size[0] * scale[0], self.size[1] * scale[1])
        x2, y2 = x2 * self.scale, y2 * self.scale
        mx, my, mb = self.input.mouse()
        if x - x2 / 2 < mx < x + x2 / 2 and y - y2 / 2 < my < y + y2 / 2:
            r, g, b = self.bgcolor
            if r - 16 < 0:
                r = 0
            else:
                r -= 16
            if g - 16 < 0:
                g = 0
            else:
                g -= 16
            if b - 16 < 0:
                b = 0
            else:
                b -= 16
            self.bgcolor = r, g, b
            if mb == 1:
                if self.sound != False:
                    pygame.mixer.Sound.play(self.sound)
                self.input.clicked()
                self.state = True
                return self.name
        self.text.bgcolor = self.bgcolor
        self.state = False

    def render(self):
        self.text.render()
class TextBox:
    def __init__(self, render_window, pos, size, text, text_center="center", center="center", in_box=True, default_text="",
                 resizeable=False, window=None):
        self.window = render_window
        self.renderer = render_window.renderer
        self.theme = theme = self.renderer.theme
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.sound = theme.sounds("button")
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.in_text = False
        self.name = ""
        self.default_text = default_text
        self.text = str(text)
        self.start_pos = pos
        if window is not None:
            self.pos = window.pos[0] + pos[0], window.pos[1] + pos[1]
        else:
            self.pos = pos
        self.size = size
        self.font = theme.fonts()
        self.pointer = 0
        self.in_box = in_box
        self.center = center
        self.text_center = text_center
        self.resizeable = resizeable
        self.window = window

    def update(self, input, maxTextLength=False):
        if self.window is not None:
            self.pos = self.window.pos[0] + self.start_pos[0], self.window.pos[1] + self.start_pos[1]

        update(self, input, maxTextLength)

    def get_text(self):
        return str(self.text)

    def change_text(self, text):
        p_text = self.text
        self.text = str(text)
        return str(p_text)

class ValueLabel:
    def __init__(self, window, pos, value, name, center="center", in_box=False, size=(0,0), text_color=False,
                 border_color=False, background_color=False):
        name = str(value) + str(name)
        self.text = Text(renderer, pos, name, in_box, size, center=center, text_color=text_color,
                         border_color=border_color, background_color=background_color)

    def render(self):
        self.text.render()
class LabelValue:
    def __init__(self, window, pos, name, value, center="center", in_box=False, size=(0,0), fixed=True,
                 text_color=False
                 , border_color=False, background_color=False):

        self.name = name
        self._text = str(name) + str(value)
        self.text = Text(window, pos, self._text, in_box, size, center=center, text_color=text_color
                         , border_color=border_color, background_color=background_color)
        window.add_element(name,self)
    def change_value(self,new_value):
        self.text.change_text(str(self.name) + str(new_value))


    def render(self):
        self.text.render()
class Label:
    def __init__(self, window, pos, name, center="center", in_box=False, size=(0,0), fixed=True, text_color=False
                 , border_color=False, background_color=False, resize=False):
        name = str(name)
        self.text = Text(window, pos, name, in_box, size, center=center, text_color=text_color
                         , border_color=border_color, background_color=background_color, resize=resize)

    def update(self, window):
        self.text.update(window)

    def render(self):
        self.text.render()
class Label_text:
    def __init__(self, window, pos, size, name, value, text_center="center", center="center", in_box=True,
                 resizeable=False):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme = self.renderer.theme
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.sound = theme.sounds("button")
        self.in_text = False
        self.name = name
        self.text = str(value)
        self.default_text = str(value)
        self.pos = pos
        self.mousePos = (0, 0)
        self.size = size
        self.pointer = 0
        self.in_box = in_box
        self.center = center
        self.text_center = text_center
        self.resizeable = resizeable
        posx, posy = pos
        sizex, sizey = size
        self.text_object = Text(window, (posx - sizex - 20, posy), self.name, self.in_box, self.size)

    def update(self, input):
        return update(self, input)

    def render(self):
        self.text_object.render()
class color_picker:
    def __init__(self, window, pos, size, name="", color=(0, 0, 0), center="center"):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme = self.renderer.theme
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.sound = theme.sounds("button")
        self.pos = pos
        self.color = (color[0], color[1], color[2])
        self.size = size
        self.name = str(name)
        self.center = center
        self.text_center = "center"
        self.update()

    def update(self):
        sx, sy = self.theme.screen_info()[1]
        scale = self.theme.screen_info()[2]
        px, py = self.pos
        px, py = px * scale, py * scale
        x, y = sx + px, sy + py
        sx, sy = self.size
        sx, sy = sx * scale, sy * scale
        self.Spectrum = pygame.transform.scale(pygame.image.load("images/spectrum_chart.jpg"), (sx - 4, sy - 4))

        if self.center == "center":
            x, y = x - sx / 2, y - sy / 2
        elif self.center == "left":
            x, y = x - sx / 2, y
        self.rect = (x + 2, y + 2)

    def get_color(self, input):
        self.update()
        box = Box(self.renderer, self.pos, self.size)
        box.render()
        self.display.blit(self.Spectrum, self.rect)
        px, py = self.pos
        x, y = self.rect
        sx, sy = self.size
        x2, y2 = sx * self.scale, sy * self.scale
        mx, my, mb = input.mouse()
        mb = abs(mb)
        if x < mx < x + x2 and y < my < y + y2 and mb == 1:
            input.clicked()
            self.color = (self.display.get_at((int(mx), int(my)))[:3])

        R, G, B = self.color
        luminance = R * 0.2126 + G * 0.7152 + B * 0.0722
        if luminance > 120:
            C = 0
        else:
            C = 255
        text_color = (C, C, C)

        text = Text(self.renderer, (px - (sx + 20), py), self.name, True, self.size, text_color=text_color,
                    background_color=self.color)
        text.render()
        return self.color
class multiple_choice_input:
    def __init__(self, window, pos, size, name, current_value, values, max_values, center="center", pointer=0):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme = self.renderer.theme
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.sound = theme.sounds("button")
        self.selected = False
        self.name = name
        self.text = str(current_value)
        self.values = values
        self.max_values = max_values
        self.pos = pos
        self.size = size
        self.pointer = pointer
        self.in_box = True
        scale = self.scale
        x, y = self.screen
        px, py = pos
        sx, sy = size
        x2, y2 = self.scaled = sx * scale, sy * scale
        self.rect = ((x + px * scale) - (x2 / 2), (y + py * scale) - (y2 / 2), (x + px * scale) + (x2 / 2),
                     (y + py * scale) + (y2 / 2))

    def update(self, input):
        px, py = self.pos
        x, y, x2, y2 = self.rect
        text_x, text_y = self.font.size("pd")
        text_y = text_y * (2 / self.scale)
        mx, my, mb = input.mouse()
        bgcolor = self.theme.bgcolor
        if self.selected:
            if len(self.values) > self.max_values:
                values = self.values[self.pointer:self.max_values + self.pointer]
                start_pos = len(values) * text_y
                box_rect = Box(self.window, (px + 120, py), (100, (start_pos / 2) + 10))
                pos = - math.floor(len(values) / 2)
                if len(values) % 2 == 0:
                    pos += 0.5
                for each in values:
                    Text(self.window, (px + 120, py + pos * (text_y / 2)), each).render()
                    pos += 1
            else:
                start_pos = len(self.values) * text_y
                box_rect = Box(self.window, (px + 120, py), (100, (start_pos / 2) + 10))
                values = self.values
                pos = - math.floor(len(self.values) / 2)
                if len(self.values) % 2 == 0:
                    pos += 0.5
                for each in values:
                    Text(self.window, (px + 120, py + pos * (text_y / 2)), each).render()
                    pos += 1

            bx, by, bx2, by2 = box_rect.get_rect()

            if bx < mx < bx2 and by < my < by2 and mb == 1:
                input.clicked()
                if self.sound != False:
                    pygame.mixer.Sound.play(self.sound)
                click = my - by
                self.text = values[math.floor(click / ((by2 - by) / len(values)))]

            self.pointer += input.scroll()

            if self.pointer < 0:
                self.pointer = 0
            if self.pointer > len(self.values) - self.max_values:
                self.pointer = len(self.values) - self.max_values

        if x < mx < x2 and y < my < y2:
            r, g, b = bgcolor
            if r - 16 < 0:
                r = 0
            else:
                r -= 16
            if g - 16 < 0:
                g = 0
            else:
                g -= 16
            if b - 16 < 0:
                b = 0
            else:
                b -= 16
            bgcolor = r, g, b
            if mb == 1:
                input.clicked()
                self.selected = True
                if self.sound != False:
                    pygame.mixer.Sound.play(self.sound)
        elif mb != 0:
            self.selected = False

        size_x, size_y = self.size
        Text(self.window, (px - (size_x + 20), py), self.name, self.in_box, self.size).render()
        Text(self.window, self.pos, self.text, self.in_box, self.size, background_color=bgcolor).render()
class pop_up:
    def __init__(self, window, pos1, pos2, speed, delay, size, text, center="center"):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme =  self.renderer.theme
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.text = str(text)
        self.pos1 = pos1
        self.pos2 = pos2
        self.pos = pos1
        self.speed = speed
        self.delay = delay
        self.size = size
        if size[0] == -1:
            self.size = (self.font.size(self.text)[0] / self.scale + 10, self.size[1])
        self.start = False
        self.delay_time = 0
        self._return = False
        self.pop_up = True
        self.last_frame = time.perf_counter()

    def update(self):
        self.frame_time = (time.perf_counter() - self.last_frame) * 100
        self.last_frame = time.perf_counter()
        if self.pop_up:
            posx, posy = self.pos
            posx1, posy1 = self.pos1
            posx2, posy2 = self.pos2

            if self.pos == self.pos2:
                if not self.start:
                    self.delay_time = time.perf_counter() + self.delay
                    self.start = True
                if time.perf_counter() > self.delay_time:
                    self.start = False
                    self._return = True
                    if posx > posx1: posx -= self.speed * (self.frame_time / 4)
                    if posx < posx1: posx += self.speed * (self.frame_time / 4)
                    if posy > posy1: posy -= self.speed * (self.frame_time / 4)
                    if posy < posy1: posy += self.speed * (self.frame_time / 4)

            else:
                if self._return:
                    if self.pos == self.pos1:
                        self._return = False
                        self.pop_up = False
                    else:
                        if posx > posx1:
                            posx -= self.speed * (self.frame_time / 4)
                            if posx < posx1:
                                posx = posx1
                        if posx < posx1:
                            posx += self.speed * (self.frame_time / 4)
                            if posx > posx1:
                                posx = posx1
                        if posy > posy1:
                            posy -= self.speed * (self.frame_time / 4)
                            if posy < posy1:
                                posy = posy1
                        if posy < posy1:
                            posy += self.speed * (self.frame_time / 4)
                            if posy > posy1:
                                posy = posy1

                else:
                    if posx > posx2:
                        posx -= self.speed * (self.frame_time / 4)
                        if posx < posx2:
                            posx = posx2
                    if posx < posx2:
                        posx += self.speed * (self.frame_time / 4)
                        if posx > posx2:
                            posx = posx2
                    if posy > posy2:
                        posy -= self.speed * (self.frame_time / 4)
                        if posy < posy2:
                            posy = posy2
                    if posy < posy2:
                        posy += self.speed * (self.frame_time / 4)
                        if posy > posy2:
                            posy = posy2

            self.pos = (posx, posy)
            Text(self.window, self.pos, self.text, in_box=True, size=self.size).render()
class file:
    def __init__(self, window, pos, size, file_name, input, mode="Open"):
        self.window = window
        self.renderer = window.renderer
        self.Input = input
        self.theme = theme = self.renderer.theme
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.sound = theme.sounds("button")
        size_x, size_y = size
        self.file_name = TextBox(renderer, (15, -size_y / 2 + 12), (size_x - 108, 15), file_name, in_box=True)
        self.file_history = [file_name]
        self.selected = "No file selected"
        self.size = size
        self.pos = pos
        self.browsing = False
        self.pointer = 0
        self.filters = False
        self.mode = mode

    def browse(self):
        sound = self.sound
        color = (64, 64, 64)
        file_name = self.file_name.text
        mx, my, mb = self.Input.mouse()
        px, py = self.pos
        size_x, size_y = self.size
        sx, sy = self.screen_info[1]
        scale = self.screen_info[2]
        row = 17
        stuff = []

        if self.filters:
            box(self.renderer, self.pos, self.size)
            Text(self.renderer, (px, -size_y / 2 + 12), "Filters")
            Text(self.renderer, (px, py), "Sorry no filters are avaiLabel.")

            if button(self.renderer, (px + size_x / 2 - 25, -size_y / 2 + 12), (30, 15), "Exit", self.Input):
                self.Input.clicked()
                print("Exit")
                self.filters = False
                self.browsing = False
                if sound != False:
                    pygame.mixer.Sound.play(sound)

            if button(self.renderer, (px + size_x / 2 - 60, py + size_y / 2 - 15), (80, 15), "Apply", self.Input):
                self.Input.clicked()
                print("Apply")
                self.filters = False
                if sound != False:
                    pygame.mixer.Sound.play(sound)

            if button(self.renderer, (px - size_x / 2 + 60, py + size_y / 2 - 15), (80, 15), "Cancel", self.Input):
                self.Input.clicked()
                print("Cancel")
                self.filters = False
                if sound != False:
                    pygame.mixer.Sound.play(sound)

        else:
            box(self.renderer, self.pos, self.size)
            self.file_name.update(self.Input)
            Text(self.renderer, (-size_x / 2 + 40, -size_y / 2 + 12), "Search", in_box=True, size=(60, 15))
            if button(self.renderer, (px + size_x / 2 - 25, -size_y / 2 + 12), (30, 15), "Exit", self.Input):
                self.Input.clicked()
                print("Exit")
                self.browsing = False
                if sound != False:
                    pygame.mixer.Sound.play(sound)

            if button(self.renderer, (px - size_x / 2 + 60, py + size_y / 2 - 15), (80, 15), "Back",
                      self.Input) or mb == 6:
                self.Input.clicked()
                print("back")
                self.pointer = 0
                path = file_name.split("/")
                if "" in path:
                    path = path[:-1]
                path = path[:-1]
                file_name = ''
                for folder in path:
                    print(file_name)
                    file_name += folder + "/"
                self.file_name.change_text(file_name)
                self.selected = ""
                if sound != False:
                    pygame.mixer.Sound.play(sound)

            if button(self.renderer, (px, py + size_y / 2 - 15), (80, 15), "Filters", self.Input):
                self.Input.clicked()
                print("Filters")
                self.filters = True
                if sound != False:
                    pygame.mixer.Sound.play(sound)

            self.pointer -= self.Input.scroll()
            if self.pointer > len(stuff) / 2:
                self.pointer = len(stuff) / 2

            _file_name = file_name

            try:
                if len(file_name) > 1:
                    while not os.path.isdir(_file_name):
                        _file_name = _file_name[:-1]
                        if _file_name == "":
                            break

                    name = file_name.strip(_file_name)
                    for each in os.listdir(_file_name):
                        if each.lower().startswith(name.lower()):
                            stuff.append(each)

                else:
                    for drive in range(26):
                        drive += 65
                        drive = chr(drive)
                        if os.path.isdir(drive + ":"):
                            stuff.append(drive + ":")
            except:
                pass

            top = -size_y / 2 + 13 + self.pointer * row
            line = -75
            if 10 < len(stuff) < 20:
                column1 = stuff[:9]
                column2 = stuff[9:]
            elif len(stuff) > 10:
                split = math.ceil(len(stuff) / 2)
                column1 = stuff[:split]
                column2 = stuff[split:]
            else:
                column1 = stuff
                column2 = []

            columns = [column1, column2]
            for column in columns:
                for each in column:
                    try:
                        if file_name.find("Blueprints/"):
                            with open(file_name + each + '/description.json', "r") as description:
                                description = json.loads(description.read())
                                name = description["name"]
                        else:
                            name = each
                    except:
                        name = each

                    tx, ty = self.font.size(name)
                    if tx > 130 * scale:
                        name += "..."
                        while tx > 130 * scale:
                            name = name[:-4]
                            name += "..."
                            tx, ty = self.font.size(name)

                    top += row
                    if top > -size_y / 2 + row:
                        if hover(self.renderer, (line, top), (130, 15), self.Input) or each == self.selected:
                            r, g, b = self.bgcolor
                            if r - 16 < 0:
                                r = 0
                            else:
                                r -= 16
                            if g - 16 < 0:
                                g = 0
                            else:
                                g -= 16
                            if b - 16 < 0:
                                b = 0
                            else:
                                b -= 16
                            bgcolor = r, g, b
                        else:
                            bgcolor = self.bgcolor
                        Label(self.renderer, (line, top), name, in_box=True, size=(130, 15), background_color=bgcolor)
                        if hit_box(self.renderer, (line, top), (130, 15), self.Input):
                            self.selected = each
                            path = file_name.split("/")
                            path = path[:-1]
                            file_name = ''
                            for folder in path:
                                file_name += folder + "/"
                            file_name += each + "/"
                            if not os.path.isdir(file_name):
                                file_name = file_name + '/' + each + '/'
                            if os.path.isdir(file_name):
                                self.file_name.change_text(file_name)
                                self.pointer = 0
                            if sound != False:
                                pygame.mixer.Sound.play(sound)

                    if top > py + size_y / 2 - row * 3:
                        break
                top = -size_y / 2 + 13 + self.pointer * row
                line += 150

            if button(self.renderer, (px + size_x / 2 - 60, py + size_y / 2 - 15), (80, 15), self.mode, self.Input):
                self.Input.clicked()
                print(self.mode)
                if sound != False:
                    pygame.mixer.Sound.play(sound)
                if self.mode == "Open":
                    self.browsing = False
                elif self.mode == "Save as":
                    x, y = pos = (0, 0)
                    sx, sy = size = (200, 100)
                    save_name = TextBox(self.renderer, (x, y), (sx / 1.2, 15), "", default_text="File name")
                    Label(self.theme, (px + size_x / 2 - 60, py + size_y / 2 - 15), self.mode, in_box=True,
                          size=(80, 15))
                    while True:
                        for event in pygame.event.get():
                            self.Input.get_input(event)
                        self.Input.update()
                        box(self.renderer, pos, size)
                        Label(self.renderer, (x, y - sy / 2 + 20), "Save file as", in_box=True, size=(sx / 2, 15))
                        save_name.update(self.Input)
                        if button(self.renderer, (x - sx / 2 + sx / 4, y + sy / 2 - 20), (sx / 3, 15), "Cancel",
                                  self.Input):
                            break
                        if button(self.renderer, (x + sx / 2 - sx / 4, y + sy / 2 - 20), (sx / 3, 15), "Save", self.Input):
                            try:
                                shutil.copy("temp", self.file_name.text + save_name.text + ".xml")
                            except Exception as e:
                                print(e)
                            break
                            self.browsing = False
                        pygame.display.update()
                        time.sleep(0.05)

                elif self.mode == "Set Path":
                    self.browsing = False
class Slider:
    def __init__(self, window, pos, size, direction, Input, value=0, audio=False):
        self.window = window
        self.renderer = window.renderer
        self.Input = Input
        self.theme = theme = self.renderer.theme
        self.screen_info = theme.screen_info()
        self.display, self.screen, self.scale = self.screen_info
        self.tcolor, self.bcolor, self.bgcolor = theme.colors()
        self.font = theme.fonts()
        self.sound = theme.sounds("button")
        self.pos = pos
        self.size = size
        self.direction = direction
        self.value = value
        self.center = "center"
        self.selected = False
        self.p_mouse = self.Input.mouse()
        self.p_value = self.value
        self.audio = audio

    def update(self):
        sx, sy = self.size
        sx, sy = sx * self.scale, sy * self.scale
        self.x, self.y = self.pos
        self.screenx, self.screeny = self.screen
        self.box = Box(self.window, self.pos, self.size)
        if hover(self.renderer, self.pos, self.size, self.Input):
            self.value -= self.Input.scroll() / 100
            if self.value > 1:
                self.value = 1
            if self.value < 0:
                self.value = 0

        if hit_box(self.renderer, self.pos, self.size, self.Input):
            self.selected = True
            mx, my, mb = self.p_mouse = self.Input.mouse()

            if self.direction == "up":
                self.value = 1 - (my - self.y - sy / 2) / sy
                #print(self.value)
            elif self.direction == "right":
                self.value = (mx - (self.screenx - self.x - sx / 2)) / sx
            elif self.direction == "down":
                self.value = (my - self.y - sy / 2) / sy
            elif self.direction == "left":
                self.value = 1 - (mx - (self.screenx - self.x - sx / 2)) / sx

        if self.selected:
            mx, my, mb = self.Input.mouse()
            pmx, pmy, pmb = self.p_mouse
            if mb == -1:
                if self.direction == "up":
                    self.value += (pmy - my) / sy
                elif self.direction == "right":
                    self.value += (mx - pmx) / sx
                elif self.direction == "down":
                    self.value += (my - pmy) / sy
                elif self.direction == "left":
                    self.value += (pmx - mx) / sx
                self.p_mouse = self.Input.mouse()
                if self.value > 1:
                    self.value = 1
                if self.value < 0:
                    self.value = 0

            else:
                self.selected = False

        if self.direction == "up":
            spy = sy / 2 - sy * self.value
            if spy > sy / 2 - sx / 4:
                spy = sy / 2 - sx / 4
            elif spy < -sy / 2 + sx / 4:
                spy = -sy / 2 + sx / 4
            slider_pos = (self.x, spy)
            size = (sx, sx / 2)

        elif self.direction == "right":
            spx = -sx / 2 + sx * self.value
            if spx > sx / 2 - sy / 4:
                spx = sx / 2 - sy / 4
            elif spx < -sx / 2 + sy / 4:
                spx = -sx / 2 + sy / 4
            slider_pos = (spx, 0)
            size = (sy / 2, sy)

        elif self.direction == "down":
            spy = sy / 2 + sy * self.value
            if spy > sy / 2 - sx / 4:
                spy = sy / 2 - sx / 4
            elif spy < -sy / 2 + sx / 4:
                spy = -sy / 2 + sx / 4
            slider_pos = (self.x, spy)
            size = (sx, sx / 2)

        elif self.direction == "left":
            spx = sx / 2 - sx * self.value
            if spx > sx / 2 - sy / 4:
                spx = sx / 2 - sy / 4
            elif spx < -sx / 2 + sy / 4:
                spx = -sx / 2 + sy / 4
            slider_pos = (spx, 0)
            size = (sy / 2, sy)
        self.spx, self.spy = slider_pos
        sizex, sizey = size
        self.sizex, self.sizey = sizex - self.theme.border * 2, sizey - self.theme.border * 2
        self.cx, self.cy = get_center(self.center, self.scale, self.pos, size=self.size)

        if int(self.value * 100) == int(self.value * 10) * 10 and self.value != self.p_value:
            if self.audio:
                pygame.mixer.Sound.play(self.sound)

        self.p_value = self.value

    def render(self):
        self.box.render()
        pygame.draw.rect(self.display, self.tcolor,
                         (self.cx + self.screenx + self.x + self.spx - self.sizex / 2,
                          self.cy + self.screeny + self.y + self.spy - self.sizey / 2, self.sizex, self.sizey))
class window:
    def __init__(self, renderer, pos, size, name, Input, resizeable=False, min=(10, 10), max=(0, 0), set_order= False):
        self.renderer = renderer
        self.theme = theme = renderer.theme
        self.display = theme.display
        self.screen = theme.screen
        self.scale = theme.scale
        self.Input = Input
        self.pos = pos
        self.size = size
        self.init_size = size
        self.name = name
        self.resizeable = resizeable
        self.min = min
        self.max = max
        self.resizing = False
        self.smx = 0
        self.smy = 0
        self.dir = 0
        self.selected = True
        self.elements = {}
        self.last_click = self.Input.c_time
        self.set_order = set_order
        if self.set_order != False:
            self.last_click = self.set_order

        x, y = size

        self.main_box = Box(self, self.pos, self.size, resize=True)
        self.title = Label(self, (0, -y / 2 + 7.5), self.name, in_box=True, size=(x, 15), resize=True)
        self.back = Button(self, (x / 2 - 22.5, -y / 2 + 7.5), (15, 15), "←", self.Input, resize=True)
        self.close = Button(self, (x / 2 - 7.5, -y / 2 + 7.5), (15, 15), "X", self.Input, resize=True)

        self.elements["main_box"] = self.main_box
        self.elements["title"] = self.title
        self.elements["back"] = self.back
        self.elements["close"] = self.close

        self.renderer.add_window(self)

    def add_element(self, name, element):
        self.elements[name] = element

    def remove_element(self, name):
        self.elements.pop(name)

    def clear(self):
        self.elements = {}

    def update(self):
        for element in self.elements:
            self.elements[element].update(self)

    def render(self):
        for element in self.elements:
            self.elements[element].render()
class analog_stick:
    def __init__(self, window, pos, size, name, Input, resizeable=False, min=(0, 0), max=(0, 0)):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme = self.renderer.theme
        self.display = theme.display
        self.screen = theme.screen
        self.scale = theme.scale
        self.Input = Input
        self.pos = pos
        self.size = size
        self.name = name
        self.resizeable = resizeable
        self.min = min
        self.max = max
        self.resizing = False
        self.smx = 0
        self.smy = 0
        self.dir = 0
        self.x = 128
        self.y = 128

class display_window:
    def __init__(self, window, pos, size):
        self.window = window
        self.renderer = window.renderer
        self.theme = theme = self.renderer.theme
        self.display = theme.display
        self.screen = theme.screen
        self.scale = theme.scale
        self.pos = pos
        self.size = size
        size_x, size_y = self.size
        x2, y2 = size_x * self.scale, size_y * self.scale
        self.surface = pygame.Surface((x2 - 4, y2 - 4))
        self.surface.fill((0, 0, 0))

    def update(self):
        sx, sy = self.screen
        x, y = self.pos
        x, y = sx + x * self.scale, sy + y * self.scale
        size_x, size_y = self.size
        x2, y2 = size_x * self.scale, size_y * self.scale
        x = x - x2 / 2
        y = y - y2 / 2
        box(self.renderer, self.pos, self.size)
        self.display.blit(self.surface, (x + 2, y + 2))
        self.surface.fill((0, 0, 0))

class Layer:
    def __init__(self,renderer, Input, set_order= False):
        self.renderer = renderer
        self.theme = theme = renderer.theme
        self.display = theme.display
        self.screen = theme.screen
        self.scale = theme.scale
        self.Input = Input
        self.elements = {}
        self.last_click = set_order

        self.renderer.add_window(self)

    def add_element(self, name, element):
        self.elements[name] = element

    def remove_element(self, name):
        self.elements.pop(name)

    def clear(self):
        self.elements = {}

    def update(self):
        for element in self.elements:
            self.elements[element].update(self)

    def render(self):
        for element in self.elements:
            self.elements[element].render()



class line:
    def __init__(self, window, name, color, start_pos, end_pos, width = 1):
        self.window = window
        self.name = name
        self.surface = window.renderer.theme.display
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width

        window.add_element(name,self)

    def render(self):
        pygame.draw.line(self.surface,self.color,self.start_pos,self.end_pos,self.width)