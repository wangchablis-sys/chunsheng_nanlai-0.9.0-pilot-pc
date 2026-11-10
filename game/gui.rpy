## 红卫的春天 — GUI base
init offset = -2

init python:
    gui.init(1920, 1080)

define config.check_conflicting_properties = True

define gui.accent_color = "#D64532"
define gui.idle_color = "#6A4A32"
define gui.idle_small_color = "#8C6A48"
define gui.hover_color = "#E0892D"
define gui.selected_color = "#C45C26"
define gui.insensitive_color = "#8A7A6A88"
define gui.text_color = "#2B2420"
define gui.interface_text_color = "#2B2420"

define gui.text_font = "fonts/SourceHanSansLite.ttf"
define gui.name_text_font = "fonts/SourceHanSansLite.ttf"
define gui.interface_text_font = "fonts/SourceHanSansLite.ttf"

define gui.text_size = 32
define gui.name_text_size = 38
define gui.interface_text_size = 26
define gui.label_text_size = 30
define gui.notify_text_size = 22
define gui.title_text_size = 76

define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"
define gui.main_menu_text_color = "#F3E7D3"

define gui.textbox_height = 300
define gui.textbox_yalign = 1.0
define gui.name_xpos = 300
define gui.name_ypos = 18
define gui.name_xalign = 0.0
define gui.namebox_width = None
define gui.namebox_height = None
define gui.namebox_borders = Borders(24, 12, 24, 12)
define gui.namebox_tile = False
define gui.dialogue_xpos = 320
define gui.dialogue_ypos = 96
define gui.dialogue_width = 1280
define gui.dialogue_text_xalign = 0.0

define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(18, 10, 18, 10)
define gui.button_tile = False
define gui.button_text_font = gui.interface_text_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.0

define gui.choice_button_width = 1400
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(40, 20, 40, 20)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = 30
define gui.choice_button_text_xalign = 0.0
define gui.choice_button_text_idle_color = "#3A2218"
define gui.choice_button_text_hover_color = "#C44522"

define gui.quick_button_borders = Borders(10, 4, 10, 4)
define gui.quick_button_text_size = 20
define gui.quick_button_text_idle_color = "#D9C9B8"
define gui.quick_button_text_selected_color = "#D99A4E"

define gui.about = _("""《红卫的春天》0.9.0-pilot

一个凤阳青年的十七年。
1978—1995，从红手印到春声收音机。

剧本：基于《红卫的春天》优化稿与支线数值文档改编
引擎：Ren'Py 8.5
美术：纸雕/水彩概念美术版
音乐/音效：程序化环境音

这是一个虚构故事，人物与事件为艺术创作。""")
