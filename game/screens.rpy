## 红卫的春天 — screens and styles

default quick_menu = True


screen say(who, what):
    if renpy.get_screen("choice") is None:
        use play_hud

    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                hbox:
                    spacing 16
                    yalign 0.5
                    text "名" style "name_mark"
                    text who id "who"

        text what id "what"

    if who in portrait_map:
        add portrait_map[who] xpos 72 ypos 712 xysize (196, 196)


screen choice(items):
    use play_hud

    vbox:
        style_prefix "choice"

        for i in items:
            $ choice_locked = ("（拿不出）" in i.caption) or ("（还做不到）" in i.caption)
            textbutton i.caption:
                action i.action
                sensitive (not choice_locked)


screen stat_strip():
    zorder 400

    if not main_menu:
        $ pulse_on = any(stat_pulse.values())
        if pulse_on:
            timer 2.4 action Function(clear_stat_pulse)

        frame:
            xpos 22
            ypos 16
            background Solid("#1A1024D0")
            padding (10, 8, 12, 8)

            vbox:
                spacing 3

                for key, label, icon in (
                    ("money", "资金", "gui/stat_money.png"),
                    ("rep", "信誉", "gui/stat_rep.png"),
                    ("tech", "技术", "gui/stat_tech.png"),
                    ("family", "亲情", "gui/stat_family.png"),
                    ("thought", "思想", "gui/stat_thought.png"),
                ):
                    hbox:
                        spacing 8
                        ysize 30

                        add icon:
                            xysize (26, 26)
                            yalign 0.5
                        text label:
                            size 16
                            yalign 0.5
                            color ("#FFF1A8" if stat_pulse[key] else "#F3E6D0")
                        text str(getattr(store, key)):
                            size 20
                            bold True
                            xminimum 34
                            yalign 0.5
                            color ("#FFF6D0" if stat_pulse[key] else "#FFFFFF")
                        if stat_pulse[key]:
                            text ("+" if stat_pulse[key] > 0 else "") + str(stat_pulse[key]):
                                size 16
                                yalign 0.5
                                color ("#7DFFB2" if stat_pulse[key] > 0 else "#FF8A7A")

                if stat_conflict():
                    text "钱是有了，招牌开始被人躲开。":
                        size 15
                        color "#E07A72"
                        xmaximum 168


screen play_hud():
    zorder 500
    use quick_menu


screen quick_menu():
    zorder 500

    frame:
        background Solid("#1A1024F2")
        padding (8, 6)
        xpos 1910
        xanchor 1.0
        ypos 10

        hbox:
            spacing 4

            textbutton "回退" action Rollback() style "quick_button" text_style "quick_button_text"
            textbutton "历史" action ShowMenu("history") style "quick_button" text_style "quick_button_text"
            textbutton "自动" action Preference("auto-forward", "toggle") style "quick_button" text_style "quick_button_text"
            textbutton "快进" action Skip() alternate Skip(fast=True, confirm=True) style "quick_button" text_style "quick_button_text"
            textbutton "存档" action ShowMenu("save") style "quick_button" text_style "quick_button_text"
            textbutton "读档" action ShowMenu("load") style "quick_button" text_style "quick_button_text"
            textbutton "状态" action ShowMenu("stats") style "quick_button" text_style "quick_button_text"
            textbutton "情节" action ShowMenu("plot_tree") style "quick_button" text_style "quick_button_text"
            textbutton "人物" action ShowMenu("people_gallery") style "quick_button" text_style "quick_button_text"
            textbutton "设置" action ShowMenu("preferences") style "quick_button" text_style "quick_button_text"


screen main_menu():
    tag menu

    add "hist_cover"
    add Solid("#140E18AA")
    add "gui/logo.png" xalign 0.5 ypos 36 xysize (980, 320)

    text "互动视觉小说，1978—1995" style "main_menu_tagline" xalign 0.5 ypos 390

    vbox:
        style_prefix "main_menu"
        xalign 0.5
        yalign 0.58
        spacing 4

        textbutton "开始游戏" action Start()
        textbutton "读取存档" action ShowMenu("load")
        textbutton "结局图鉴" action ShowMenu("endings_gallery")
        textbutton "设置" action ShowMenu("preferences")

    text "v0.9.0-pilot" style "main_menu_version" xalign 0.99 yalign 0.985

    use quick_menu


screen navigation():
    vbox:
        style_prefix "nav"
        xpos 110
        ypos 180
        spacing 2

        if not main_menu:
            textbutton "返回游戏" action Return()

        textbutton "保存" action ShowMenu("save")
        textbutton "读取" action ShowMenu("load")
        textbutton "状态" action ShowMenu("stats")
        textbutton "情节" action ShowMenu("plot_tree")
        textbutton "人物" action ShowMenu("people_gallery")
        textbutton "历史" action ShowMenu("history")
        textbutton "设置" action ShowMenu("preferences")
        textbutton "结局图鉴" action ShowMenu("endings_gallery")
        textbutton "制作名单" action ShowMenu("about")
        textbutton "回到标题" action MainMenu(confirm=True)
        textbutton "退出" action Quit(confirm=True)


screen game_menu(title):
    tag menu

    add "gui/game_menu.png"
    add "gui/overlay/game_menu.png"
    use navigation

    frame:
        style "game_menu_frame"
        xpos 470
        ypos 90
        xsize 1360
        ysize 880

        vbox:
            spacing 18
            text title style "game_menu_title"
            transclude

    textbutton "返回" action Return() style "nav_button" xpos 110 ypos 980

    use quick_menu


screen save():
    tag menu
    use file_slots("保存")


screen load():
    tag menu
    use file_slots("读取")


screen file_slots(title):
    use game_menu(title):
        grid 3 2:
            xalign 0.5
            yalign 0.5
            spacing 20

            for i in range(1, 7):
                button:
                    style "slot_button"
                    action FileAction(i)

                    vbox:
                        spacing 4

                        text "存档 [i]" style "slot_number"
                        text FileTime(i, format="%Y-%m-%d %H:%M", empty="空存档") style "slot_time"
                        text FileSaveName(i) style "slot_name"


screen preferences():
    tag menu

    use game_menu("设置"):
        vbox:
            spacing 12

            text "显示" style "pref_header"
            hbox:
                spacing 12
                textbutton "窗口" action Preference("display", "window")
                textbutton "全屏" action Preference("display", "fullscreen")

            text "文字速度" style "pref_label"
            bar value Preference("text speed") style "pref_slider"

            text "自动前进等待" style "pref_label"
            bar value Preference("auto-forward time") style "pref_slider"

            text "音乐音量" style "pref_label"
            bar value Preference("music volume") style "pref_slider"

            text "音效音量" style "pref_label"
            bar value Preference("sound volume") style "pref_slider"

            text "BGM说明" style "pref_header"
            text "序章　《北京记忆》纪录片片头曲\n第一章　沙沙\n第二章　《我不想说》\n第三章　daylight\n第四章　ocean\n第五章·南巡现场　浮光\n第六章·卷土重来　沙沙\n正向结局·共同富裕／质造立身／薪火基层　《在希望的田野上》纯音乐\n中性结局　Moonglow\n坏结局　阳光洒在树隙" style "pref_bgm"

            text "快进" style "pref_header"
            hbox:
                spacing 12
                textbutton "跳过已读" action Preference("skip", "seen")
                textbutton "跳过全部" action Preference("skip", "all")


screen history():
    tag menu

    use game_menu("历史"):
        viewport:
            yinitial 1.0
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 14

                if not _history_list:
                    text "还没有历史记录。" style "history_text"

                for h in _history_list:
                    vbox:
                        spacing 2

                        if h.who:
                            text h.who style "history_who"

                        text h.what style "history_text"


screen stats():
    tag menu

    use game_menu("状态"):
        viewport:
            ysize 740
            scrollbars "vertical"
            mousewheel True

            vbox:
                spacing 12

                text "孙红卫，1978—1995" style "stats_title"
                text "这五项会改后面的话，也会关掉还做不到的选择。" style "route_text"

                for label, value, blurb in (
                    ("资金", money, money_blurb()),
                    ("信誉", rep, rep_blurb()),
                    ("技术", tech, tech_blurb()),
                    ("亲情", family, family_blurb()),
                    ("思想", thought, thought_blurb()),
                ):
                    vbox:
                        spacing 2
                        hbox:
                            spacing 14
                            text label style "stat_label"
                            bar value StaticValue(value, 100) style "stat_bar"
                            text "[value]" style "stat_value"
                        text blurb style "thought_text"

                if stat_conflict():
                    text "钱是有了，招牌开始被人躲开。" style "stat_conflict"

                text "路线" style "pref_header"

                if not flag_wu_decided:
                    text "吴国强，尚未选择" style "route_text"
                elif flag_wu:
                    text "吴国强，资助了。推高信誉、思想" style "route_text"
                else:
                    text "吴国强，没有资助。信誉下去了" style "route_text"

                if not flag_watch_decided:
                    text "质量路线，尚未选择" style "route_text"
                elif flag_watch == 2:
                    text "质量路线，逐台维修。推高技术、信誉" style "route_text"
                elif flag_watch == 1:
                    text "质量路线，降价说明。守住信誉" style "route_text"
                else:
                    text "质量路线，直接售卖。资金上来，信誉受损" style "route_text"

                if not flag_accident_decided:
                    text "事故处理，尚未发生" style "route_text"
                elif flag_recall:
                    text "事故处理，全面召回。推高信誉、思想" style "route_text"
                elif flag_gray:
                    text "事故处理，灰色填补。资金上来，信誉大跌" style "route_text"
                else:
                    text "事故处理，隐瞒出货。信誉、思想大跌" style "route_text"

                if not flag_tour_decided:
                    text "南巡，尚未到达" style "route_text"
                elif flag_tour == 1:
                    text "南巡，去了现场。思想抬得最多" style "route_text"
                elif flag_tour == 2:
                    text "南巡，站在边缘。思想抬了一点" style "route_text"
                else:
                    text "南巡，没有去。思想往下掉" style "route_text"

                if not flag_end_decided:
                    text "终局，尚未选择" style "route_text"
                elif flag_fengyang:
                    text "终局，回凤阳建厂。亲情、思想" style "route_text"
                else:
                    text "终局，留在深圳。资金" style "route_text"


screen plot_tree():
    tag menu
    default picked = ""

    $ geo = plot_geometry()
    $ card = plot_card(picked)
    $ prog_done, prog_total = plot_progress()
    $ prog_pct = int(100.0 * prog_done / prog_total)

    add Solid("#EEF1FA")

    textbutton "返回":
        xpos 250
        ypos 16
        xsize 92
        ysize 44
        background Solid("#FFFFFF")
        hover_background Solid("#F4E6C4")
        text_size 22
        text_color "#5C4EA8"
        action Return()

    text "左右拖动，点一个节点看分支" xpos 360 ypos 24 size 22 color "#6E6790" font gui.interface_text_font

    use quick_menu

    viewport:
        xpos 0
        ypos 68
        xsize 1920
        ysize 760
        mousewheel "horizontal"
        draggable True
        arrowkeys True

        fixed:
            xsize geo["width"]
            ysize 760

            for band in geo["bands"]:
                add Solid(band["color"]) xpos band["x"] ypos 0 xysize (band["w"], 760)

            for seg in geo["lines"]:
                add Solid(seg["color"]):
                    xpos seg["x"]
                    ypos seg["y"]
                    xanchor 0.5
                    yanchor 0.5
                    xysize (seg["w"], 7)
                    rotate seg["angle"]

            for node in geo["nodes"]:
                if node["kind"] == "chapter":
                    button:
                        xpos node["x"]
                        ypos node["y"]
                        xanchor 0.5
                        yanchor 0.42
                        background Solid("#00000000")
                        action SetScreenVariable("picked", "" if picked == node["id"] else node["id"])

                        vbox:
                            spacing 6
                            xalign 0.5

                            if node["locked"]:
                                add "gui/plot_key.png" xalign 0.5 xysize (78, 78)
                            else:
                                frame:
                                    background Solid("#F0C24A" if node["here"] else "#FFFFFF")
                                    padding (7, 7)
                                    add node["face"] xysize (132, 132)

                            text node["title"]:
                                xalign 0.5
                                size 22
                                color "#3A315C"
                                font gui.interface_text_font
                            text node["sub"]:
                                xalign 0.5
                                size 16
                                color "#6E6790"
                                text_align 0.5
                                font gui.interface_text_font
                else:
                    button:
                        xpos node["x"]
                        ypos node["y"]
                        xanchor 0.0
                        yanchor 0.5
                        background Solid("#00000000")
                        action SetScreenVariable("picked", "" if picked == node["id"] else node["id"])

                        hbox:
                            spacing 8
                            yalign 0.5

                            if node["locked"]:
                                add "gui/plot_key.png" yalign 0.5 xysize (34, 34)
                            elif node["picked"]:
                                frame:
                                    yalign 0.5
                                    xysize (26, 26)
                                    background Solid("#7C6AE0")
                            elif node["seen"]:
                                frame:
                                    yalign 0.5
                                    xysize (26, 26)
                                    background Solid("#FFFFFF")
                                    padding (5, 5)
                                    add Solid("#7C6AE0") xysize (16, 16)
                            else:
                                frame:
                                    yalign 0.5
                                    xysize (26, 26)
                                    background Solid("#FFFFFF")

                            text node["title"]:
                                yalign 0.5
                                size 18
                                color ("#3A315C" if node["seen"] or not node["locked"] else "#8E88A8")
                                font gui.interface_text_font

    frame:
        xpos 24
        ypos 848
        xsize 420
        ysize 78
        background Solid("#FFFFFFEE")
        padding (16, 12)

        vbox:
            spacing 6
            text "走过 " + str(prog_done) + " / " + str(prog_total):
                size 18
                color "#6E6790"
                font gui.interface_text_font
            fixed:
                xsize 380
                ysize 16
                add Solid("#E4DDF8") xysize (380, 16)
                add Solid("#7C6AE0") xysize (max(8, int(380 * prog_pct / 100.0)), 16)
            text str(prog_pct) + "%":
                size 16
                color "#5C4EA8"
                font gui.interface_text_font

    if card:
        frame:
            xpos 470
            ypos 836
            xsize 1420
            ysize 220
            background Solid("#FFFFFFEE")
            padding (22, 14)

            hbox:
                spacing 28

                vbox:
                    spacing 8
                    xsize 640
                    text card["title"] size 26 color "#3A315C" font gui.interface_text_font
                    text card["body"]:
                        xmaximum 620
                        size 18
                        color "#5C5678"
                        font gui.interface_text_font

                    if picked.startswith("c:") and card["chapter"] == "ending" and not card["locked"]:
                        textbutton "去看结局":
                            xsize 220
                            ysize 48
                            background Solid("#7C6AE0")
                            text_size 22
                            text_color "#FFFFFF"
                            action Confirm(plot_confirm("ending"), [Function(prepare_plot_jump, "ending"), Jump(PLOT_JUMP["ending"])])
                    elif picked.startswith("c:") and card["chapter"] != plot_here():
                        textbutton ("从头开始" if card["chapter"] == "south" else ("跳到这里" if stage_index(card["chapter"]) > stage_index(plot_here()) else "回到这里")):
                            xsize 220
                            ysize 48
                            background Solid("#7C6AE0")
                            text_size 22
                            text_color "#FFFFFF"
                            action Confirm(plot_confirm(card["chapter"]), [Function(prepare_plot_jump, card["chapter"]), Jump(PLOT_JUMP[card["chapter"]])])

                if card["arms"]:
                    vbox:
                        spacing 6
                        xsize 700
                        for arm_name, arm_text, arm_on in card["arms"]:
                            text arm_name + "  " + arm_text:
                                xmaximum 680
                                size 16
                                color ("#5C4EA8" if arm_on else "#8A84A0")
                                font gui.interface_text_font
    else:
        text "点章节头像或旁边的分支。" xpos 480 ypos 868 size 22 color "#6E6790" font gui.interface_text_font

screen people_gallery():
    tag menu

    use game_menu("人物图鉴"):
        text ("见过 " + str(len(met_people)) + " 人") size 22 color "#E8D6BC" font gui.interface_text_font

        vpgrid:
            cols 5
            spacing 12
            xsize 1280
            ysize 680
            mousewheel "vertical"
            draggable True
            scrollbars "vertical"

            for name, face, line in people_book:
                frame:
                    xsize 236
                    ysize 210
                    background Solid("#241C28")

                    if name in met_people:
                        vbox:
                            spacing 6
                            xalign 0.5
                            ypos 12
                            add face:
                                xalign 0.5
                                xysize (96, 96)
                            text name:
                                xalign 0.5
                                size 22
                                color "#FFE08A"
                                font gui.interface_text_font
                            text line:
                                xalign 0.5
                                text_align 0.5
                                size 15
                                color "#E8D6BC"
                                font gui.interface_text_font
                                xmaximum 210
                    else:
                        text "尚未遇见":
                            xalign 0.5
                            yalign 0.5
                            size 20
                            color "#8A7A70"
                            font gui.interface_text_font


screen endings_gallery():
    tag menu

    use game_menu("结局图鉴"):
        grid 3 3:
            xalign 0.5
            yalign 0.5
            spacing 16

            for code, title, kind in ending_catalog:
                frame:
                    style "ending_slot"

                    vbox:
                        spacing 4
                        text code style "ending_code"

                        if code in persistent.endings:
                            text title style "ending_title"
                            text kind style "ending_kind"
                        else:
                            text "未解锁" style "ending_locked"


screen about():
    tag menu

    use game_menu("制作名单"):
        vbox:
            spacing 12

            text "《红卫的春天》" style "about_title"
            text gui.about style "about_text"
            text "画面：农村、绿皮车、市场、作坊、国贸用的是改革开放前后的纪实风格照片。邓小平同志的照片是真实照片。春声仍是故事里的收音机牌子。" style "about_small"


screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    add "gui/overlay/confirm.png"

    frame:
        style "confirm_frame"

        vbox:
            spacing 24
            text message style "confirm_text"

            hbox:
                spacing 20
                xalign 0.5
                textbutton "确定" action yes_action
                textbutton "取消" action no_action

    use quick_menu


screen notify(message):
    zorder 160

    frame:
        at notify_appear
        background Frame("gui/notify.png", 20, 10)
        padding (30, 14, 30, 14)
        xalign 0.98
        yalign 0.04

        text message style "notify_text"


screen chapter_card(chapter, title, place):
    zorder 200

    add Solid("#1E2428E6") xysize (1920, 1080)
    add "gui/seal.png" xalign 0.5 ypos 142 xysize (110, 110)

    vbox:
        at chapter_appear
        xalign 0.5
        yalign 0.48
        spacing 14

        text chapter style "chapter_kicker"
        text title style "chapter_title"
        text place style "chapter_time"

    use play_hud


screen ending_card(code, title, subtitle):
    zorder 200

    add Solid("#0E1114CC") xysize (1920, 1080)
    add "gui/seal.png" xalign 0.5 ypos 136 xysize (100, 100)

    vbox:
        at chapter_appear
        xalign 0.5
        yalign 0.50
        spacing 14

        text code style "ending_card_code"
        text title style "ending_card_title"
        text subtitle style "ending_card_subtitle"

    text "点击返回标题" style "ending_hint" xalign 0.5 yalign 0.92

    use play_hud


screen skip_indicator():
    zorder 100

    frame:
        background Solid("#1E2428AA")
        padding (18, 6, 18, 6)
        xalign 0.5
        yalign 0.02

        text "快进中…" style "indicator_text"


screen auto_indicator():
    zorder 100

    frame:
        background Solid("#1E2428AA")
        padding (18, 6, 18, 6)
        xalign 0.5
        yalign 0.02

        text "自动播放中…" style "indicator_text"


## Styles ######################################################################

style default:
    font gui.text_font
    size gui.text_size
    color gui.text_color
    line_spacing 8
    outlines []

style button:
    padding (12, 6, 12, 6)

style button_text:
    font gui.interface_text_font
    size gui.interface_text_size
    color gui.button_text_idle_color
    hover_color gui.button_text_hover_color
    selected_color gui.button_text_selected_color
    insensitive_color gui.button_text_insensitive_color
    xalign gui.button_text_xalign

style window:
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 330
    background Image("gui/textbox.png")

style namebox:
    xpos 270
    ypos 8
    xanchor 0.0
    xsize None
    yminimum 84
    background Frame("gui/namebox.png", 20, 10)
    padding (22, 8, 28, 8)

style name_mark:
    font gui.name_text_font
    size 58
    color "#FFE08A"
    outlines [(4, "#3A100C", 0, 0), (1, "#FFF6D8", 0, 0)]
    yalign 0.5

style say_label:
    font gui.name_text_font
    size gui.name_text_size
    color "#FFF6DE"
    xalign 0.0
    yalign 0.5

style say_dialogue:
    xpos 320
    ypos 158
    xsize 1280
    color "#2B2420"
    size 32
    line_spacing 10
    adjust_spacing False

style choice_vbox:
    xalign 0.5
    yalign 0.52
    spacing 16

style choice_button:
    xsize 1400
    background Frame("gui/button/choice_idle_background.png", 40, 20)
    hover_background Frame("gui/button/choice_hover_background.png", 40, 20)
    padding (56, 22, 56, 22)
    activate_sound "audio/click.wav"

style choice_button_text:
    font gui.choice_button_text_font
    size gui.choice_button_text_size
    color gui.choice_button_text_idle_color
    hover_color gui.choice_button_text_hover_color
    insensitive_color "#8A7A6A"
    xalign 0.0
    text_align 0.0
    line_spacing 6

style quick_button:
    background Solid("#3A241CE6")
    hover_background Solid("#8A3A22")
    selected_background Solid("#6A3018")
    padding (12, 6)
    yminimum 40

style quick_button_text:
    font gui.interface_text_font
    size 22
    color "#FFE08A"
    hover_color "#FFFFFF"
    selected_color "#FFFFFF"
    xalign 0.5

style main_menu_button:
    xsize 360
    padding (0, 3, 0, 3)
    background None

style main_menu_button_text:
    font gui.interface_text_font
    size 30
    color "#D9C9B8"
    hover_color "#D99A4E"
    selected_color "#A33327"
    xalign 0.0

style main_menu_tagline:
    font gui.interface_text_font
    size 24
    color "#D9C9B8"

style main_menu_version:
    font gui.interface_text_font
    size 18
    color "#D9C9B8AA"

style nav_button:
    padding (0, 4, 0, 4)
    background None

style nav_button_text:
    font gui.interface_text_font
    size 28
    color "#D9C9B8"
    hover_color "#D99A4E"
    selected_color "#A33327"
    xalign 0.0

style game_menu_frame:
    background Frame("gui/frame.png", 40, 30)
    padding (52, 38, 52, 38)

style game_menu_title:
    font gui.interface_text_font
    size 46
    color "#A33327"
    bold True
    xalign 0.0

style pref_header:
    font gui.interface_text_font
    size 30
    color "#7A2E2E"
    bold True

style pref_label:
    font gui.interface_text_font
    size 25
    color "#3A2A20"

style pref_bgm:
    font gui.interface_text_font
    size 21
    color "#4A3A2C"
    line_spacing 4

style pref_slider:
    xsize 620
    ysize 12
    left_bar Solid("#A33327")
    right_bar Solid("#E8DCC8")
    thumb Solid("#8B5E3C", xsize=18, ysize=18)

style stats_title:
    font gui.interface_text_font
    size 34
    color "#A33327"
    bold True

style stat_label:
    font gui.interface_text_font
    size 32
    color "#3A2A20"
    xsize 110
    text_align 1.0

style stat_bar:
    xsize 720
    ysize 28
    left_bar Solid("#D64532")
    right_bar Solid("#F3E0C4")

style stat_value:
    font gui.interface_text_font
    size 34
    color "#7A2E2E"
    bold True

style route_text:
    font gui.interface_text_font
    size 24
    color "#3A2A20"

style stat_conflict:
    font gui.interface_text_font
    size 24
    color "#E07A72"

style thought_text:
    font gui.text_font
    size 24
    color "#5A4A3A"
    italic True

style history_who:
    font gui.interface_text_font
    size 26
    color "#A33327"
    bold True

style history_text:
    font gui.text_font
    size 25
    color "#2B2420"
    line_spacing 6

style slot_button:
    xsize 380
    ysize 170
    background Frame("gui/button/slot_idle_background.png", 20, 20)
    hover_background Frame("gui/button/slot_hover_background.png", 20, 20)
    padding (24, 18, 24, 18)

style slot_number:
    font gui.interface_text_font
    size 26
    color "#7A2E2E"
    bold True

style slot_time:
    font gui.interface_text_font
    size 19
    color "#6B5B4B"

style slot_name:
    font gui.text_font
    size 19
    color "#2B2420"

style ending_slot:
    xsize 380
    ysize 190
    background Frame("gui/button/slot_idle_background.png", 20, 20)
    padding (22, 16, 22, 16)

style ending_code:
    font gui.interface_text_font
    size 18
    color "#8A7A6A"

style ending_title:
    font gui.interface_text_font
    size 28
    color "#A33327"
    bold True

style ending_kind:
    font gui.interface_text_font
    size 18
    color "#5A4A3A"

style ending_locked:
    font gui.interface_text_font
    size 24
    color "#8A7A6A"

style confirm_frame:
    xsize 820
    ysize 320
    xalign 0.5
    yalign 0.5
    background Frame("gui/frame.png", 40, 30)
    padding (52, 44, 52, 44)

style confirm_text:
    font gui.text_font
    size 30
    color "#2B2420"
    text_align 0.5
    xalign 0.5

style notify_text:
    font gui.interface_text_font
    size 23
    color "#2B2420"

style chapter_kicker:
    font gui.interface_text_font
    size 26
    color "#D99A4E"
    bold True
    xalign 0.5

style chapter_title:
    font gui.interface_text_font
    size 74
    color "#F3E7D3"
    bold True
    xalign 0.5

style chapter_time:
    font gui.interface_text_font
    size 26
    color "#D9C9B8"
    xalign 0.5

style ending_card_code:
    font gui.interface_text_font
    size 24
    color "#D99A4E"
    xalign 0.5

style ending_card_title:
    font gui.interface_text_font
    size 64
    color "#F3E7D3"
    bold True
    xalign 0.5

style ending_card_subtitle:
    font gui.interface_text_font
    size 28
    color "#D9C9B8"
    xalign 0.5
    text_align 0.5

style ending_hint:
    font gui.interface_text_font
    size 20
    color "#D9C9B8AA"

style indicator_text:
    font gui.interface_text_font
    size 22
    color "#F3E7D3"

style about_title:
    font gui.interface_text_font
    size 42
    color "#A33327"
    bold True

style about_text:
    font gui.text_font
    size 24
    color "#2B2420"
    line_spacing 8

style about_small:
    font gui.text_font
    size 20
    color "#6B5B4B"
    italic True

style vscrollbar:
    xsize 12
    base_bar Solid("#E8DCC8")
    thumb Solid("#A33327")
    unscrollable "hide"
