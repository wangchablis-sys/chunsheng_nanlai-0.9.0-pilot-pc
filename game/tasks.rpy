## 任务界面。鼠标和键盘都要用到。放弃会回到剧情，不算卡死。

default task_msg = ""
default task_step = 0
default task_miss = 0
default task_hits = 0
default task_done = ""
default task_pick = None
default task_battery_in = False
default task_lit = False
default task_error = 9
default task_bad = 1
default task_dead = 4
default task_found = False
default task_place_time = 0.0
default task_caps = []


init python:
    def task_begin_common():
        store.task_msg = ""
        store.task_step = 0
        store.task_miss = 0
        store.task_hits = 0
        store.task_done = ""
        store.task_pick = None

    def task_begin_torch():
        task_begin_common()
        store.task_battery_in = False
        store.task_lit = False
        store.task_msg = "把电池拖进尾盖，或点推进去。然后点筒身上的开关。"

    def task_torch_moved(drags, drop):
        if drop is not None and getattr(drop, "drag_name", None) == "tube":
            store.task_battery_in = True
            store.task_msg = "电池到位。点筒身上的开关，或按空格。"
            renpy.restart_interaction()
            return True
        store.task_msg = "没对准尾盖。再拖一次，或点推进去。"
        renpy.restart_interaction()
        return None

    def task_torch_insert():
        store.task_battery_in = True
        store.task_msg = "电池到位。点筒身上的开关，或按空格。"

    def task_torch_switch():
        if not store.task_battery_in:
            store.task_msg = "先把电池推进尾盖。"
            return
        store.task_lit = True
        store.task_done = "ok"

    def task_begin_circuit():
        task_begin_common()
        store.task_msg = "按键盘 1 2 3 4，顺着电源、电阻、电容、喇叭。"

    def task_circuit_key(k):
        if store.task_step >= 4:
            return
        need = ["1", "2", "3", "4"][store.task_step]
        if k == need:
            store.task_step += 1
            store.task_msg = "对上了。" if store.task_step < 4 else "顺序走完了。用鼠标点喇叭。"
        else:
            store.task_step = 0
            store.task_msg = "顺序断了，从 1 重新来。"

    def task_circuit_speaker():
        if store.task_done:
            return
        if store.task_step < 4:
            store.task_msg = "先把 1 2 3 4 按完。"
            return
        renpy.music.set_volume(0.25, delay=0.05, channel="music")
        renpy.music.play("audio/horn.wav", channel="horn", relative_volume=1.0)
        store.task_msg = "喇叭响了。"
        store.task_done = "ok"

    def task_begin_crown():
        task_begin_common()
        store.task_error = 9
        store.task_msg = "方向键或 A D 把误差调到 0，再按回车。"

    def task_crown_nudge(delta):
        if store.task_done:
            return
        store.task_error = max(-20, min(20, store.task_error + delta))
        if store.task_error > 0:
            store.task_msg = "还是快了 " + str(store.task_error) + " 秒。"
        elif store.task_error < 0:
            store.task_msg = "还是慢了 " + str(-store.task_error) + " 秒。"
        else:
            store.task_msg = "准了。按回车，或用鼠标点合盖。"

    def task_crown_close():
        if store.task_error == 0:
            store.task_done = "ok"
            return
        store.task_miss += 1
        store.task_msg = "还没对准就合盖，表针又偏了。"
        if store.task_miss >= 3:
            store.task_done = "fail"

    def task_begin_listen():
        task_begin_common()
        store.task_bad = renpy.random.randint(0, 2)
        store.task_msg = "用鼠标点那台发闷的，再按回车确认。"

    def task_listen_pick(i):
        if store.task_done:
            return None
        if store.task_pick == i:
            return task_listen_confirm()
        store.task_pick = i
        store.task_msg = "选了第 " + str(i + 1) + " 台。按回车确认。"
        return None

    def task_listen_timeout():
        if not store.task_done:
            store.task_done = "fail"
            store.task_msg = "时间到了。三台还是分不清。"

    def task_listen_confirm():
        if store.task_done:
            return None
        if store.task_pick is None:
            store.task_msg = "先用鼠标点一台。"
            return None
        if store.task_pick == store.task_bad:
            store.task_done = "ok"
            store.task_msg = "就是这台。"
            return "ok"
        store.task_miss += 1
        store.task_pick = None
        store.task_msg = "这台声音是正常的。"
        if store.task_miss >= 2:
            store.task_done = "fail"
        return None

    def task_begin_wire():
        task_begin_common()
        store.task_dead = 4
        store.task_found = False
        store.task_msg = "用鼠标点那盏不亮的灯。"

    def task_wire_pick(i):
        if store.task_done:
            return
        if i == store.task_dead:
            store.task_found = True
            store.task_step = 0
            store.task_msg = "就是这盏。按键盘 ↑ ← ↓ 把线接回去。"
            return
        store.task_msg = "这盏是亮的。"

    def task_wire_key(k):
        if store.task_done:
            return
        if not store.task_found:
            store.task_msg = "先用鼠标点那盏不亮的。"
            return
        need = ["up", "left", "down"][store.task_step]
        if k == need:
            store.task_step += 1
            store.task_msg = "接上了一截。"
        else:
            store.task_step = 0
            store.task_msg = "线接岔了，从 ↑ 重新来。"
        if store.task_step >= 3:
            store.task_done = "ok"
            store.task_msg = "这排灯亮了。"

    def task_begin_paper():
        task_begin_common()
        store.task_msg = "用鼠标点中下一句，再按空格把它圈上。从上到下。"

    def task_paper_click(i):
        if store.task_done:
            return
        store.task_pick = i
        store.task_msg = "点中了。按空格圈下来。"

    def task_paper_stamp():
        if store.task_done:
            return
        if store.task_pick is None:
            store.task_msg = "先用鼠标点一句。"
            return
        if store.task_pick != store.task_step:
            store.task_miss += 1
            store.task_msg = "先圈还没圈的那一句，从上往下。"
            if store.task_miss >= 3:
                store.task_done = "fail"
            return
        store.task_step += 1
        store.task_pick = None
        store.task_msg = "圈上了。"
        if store.task_step >= 3:
            store.task_done = "ok"

    def task_heat_now():
        t = renpy.display.core.get_time() % 1.6
        if t < 0.8:
            return int(t / 0.8 * 100)
        return int((1.6 - t) / 0.8 * 100)

    def task_iron_down():
        return (renpy.display.core.get_time() - store.task_place_time) < 1.4

    def task_begin_solder():
        task_begin_common()
        store.task_place_time = 0.0
        store.task_msg = "鼠标点焊盘，趁金区按空格。要四个焊点。"

    def task_solder_place():
        if store.task_done:
            return
        store.task_place_time = renpy.display.core.get_time()
        store.task_msg = "烙铁贴上去了。金区里按空格。"

    def task_solder_stamp():
        if store.task_done:
            return
        heat = task_heat_now()
        if not task_iron_down():
            store.task_miss += 1
            store.task_msg = "烙铁没贴在焊盘上。先用鼠标点那块铜皮。"
        elif 40 <= heat <= 62:
            store.task_hits += 1
            store.task_place_time = 0.0
            store.task_msg = "焊点亮了。" + str(store.task_hits) + "/4"
        else:
            store.task_miss += 1
            store.task_msg = "锡没化开，或者烫糊了。"
        if store.task_hits >= 4:
            store.task_done = "ok"
        elif store.task_miss >= 4:
            store.task_done = "fail"

    def task_pump():
        if not store.task_done:
            renpy.restart_interaction()

    def task_begin_sort():
        task_begin_common()
        store.task_caps = [["good", False], ["bad", False], ["good", False], ["bad", False]]
        store.task_msg = "鼠标点一颗，再按 Q 放进装机，按 E 退回。"

    def task_sort_pick(i):
        if store.task_done:
            return
        if store.task_caps[i][1]:
            store.task_msg = "这颗已经分过了。"
            return
        store.task_pick = i
        store.task_msg = "选中了。按 Q 装机，或按 E 退回。"

    def task_sort_bin(bin_name):
        if store.task_done:
            return
        i = store.task_pick
        if i is None:
            store.task_msg = "先用鼠标点一颗电容。"
            return
        kind = store.task_caps[i][0]
        right = (bin_name == "good" and kind == "good") or (bin_name == "bad" and kind == "bad")
        if right:
            store.task_caps[i][1] = True
            store.task_msg = "放对了。"
        else:
            store.task_miss += 1
            store.task_msg = "这颗放错了，拿回来。"
        store.task_pick = None
        if all(cap[1] for cap in store.task_caps):
            store.task_done = "ok"
        elif store.task_miss >= 3:
            store.task_done = "fail"


screen task_chrome(title, hint):
    add Solid("#100C14F6")

    text title xpos 270 ypos 28 size 40 color "#FFE08A" font gui.interface_text_font xmaximum 880
    text hint xpos 270 ypos 84 size 24 color "#E8D6BC" font gui.interface_text_font xmaximum 880

    text task_msg xpos 270 ypos 132 size 26 color "#FFF6DE" font gui.interface_text_font xmaximum 880

    transclude

    textbutton "放弃任务":
        xpos 270
        ypos 990
        action Return("giveup")
        text_size 24
        text_color "#E8D6BC"
        text_hover_color "#FFE08A"
        background Solid("#2A2430")
        hover_background Solid("#6A3018")
        padding (22, 10)

    if task_done != "":
        timer 0.45 action Return(task_done)

    use play_hud


screen task_torch():
    modal True
    zorder 220

    key "K_SPACE" action Function(task_torch_switch)

    use task_chrome("任务 王婶的手电", "把电池拖进右边尾盖，或点推进去。然后点筒身上的开关，或按空格。"):
        add ("gui/torch_on.png" if task_lit else "gui/torch_off.png") xpos 300 ypos 390

        if not task_battery_in:
            draggroup:
                drag:
                    drag_name "cell"
                    xpos 70
                    ypos 500
                    draggable True
                    droppable False
                    mouse_drop True
                    dragged task_torch_moved
                    add "gui/torch_cell.png"

                drag:
                    drag_name "tube"
                    xpos 1230
                    ypos 450
                    draggable False
                    droppable True
                    frame:
                        xsize 230
                        ysize 270
                        background Solid("#FFE08A33")
                        text "尾盖" xalign 0.5 ypos 16 size 26 color "#FFE08A" font gui.interface_text_font

            text "拖到尾盖" xpos 78 ypos 740 size 22 color "#E8D6BC" font gui.interface_text_font
            textbutton "推进去":
                xpos 70
                ypos 780
                action Function(task_torch_insert)
                text_size 26
                text_color "#2B2420"
                background Solid("#E7C98A")
                hover_background Solid("#FFF1B8")
                padding (28, 10)
        else:
            add "gui/torch_cell.png" xpos 1320 ypos 500 xysize (90, 160)

        textbutton "开关":
            xpos 820
            ypos 404
            xysize (270, 96)
            action Function(task_torch_switch)
            text_size 32
            text_color "#2B2420"
            background Solid("#F0D48A")
            hover_background Solid("#FFF6C8")
            text_xalign 0.5
            text_yalign 0.5


screen task_circuit():
    modal True
    zorder 220

    key "1" action Function(task_circuit_key, "1")
    key "K_KP1" action Function(task_circuit_key, "1")
    key "2" action Function(task_circuit_key, "2")
    key "K_KP2" action Function(task_circuit_key, "2")
    key "3" action Function(task_circuit_key, "3")
    key "K_KP3" action Function(task_circuit_key, "3")
    key "4" action Function(task_circuit_key, "4")
    key "K_KP4" action Function(task_circuit_key, "4")

    use task_chrome("任务 报纸上的电路", "键盘按 1 2 3 4。走完以后，用鼠标点喇叭。"):
        hbox:
            xpos 160
            ypos 280
            spacing 36
            for i, name in enumerate(("1 电源", "2 电阻", "3 电容", "4 喇叭")):
                frame:
                    xsize 280
                    ysize 120
                    background Solid("#6A3018" if task_step > i else "#2A2430")
                    text name xalign 0.5 yalign 0.5 size 32 color "#FFE08A" font gui.interface_text_font

        textbutton "喇叭":
            xpos 800
            ypos 520
            sensitive (task_step >= 4)
            action Function(task_circuit_speaker)
            text_size 36
            text_color "#2B2420"
            background Solid("#E7C98A" if task_step >= 4 else "#5A5048")
            padding (48, 18)


screen task_crown():
    modal True
    zorder 220

    key "K_LEFT" action Function(task_crown_nudge, -1)
    key "K_RIGHT" action Function(task_crown_nudge, 1)
    key "a" action Function(task_crown_nudge, -1)
    key "d" action Function(task_crown_nudge, 1)
    key "K_RETURN" action Function(task_crown_close)
    key "K_KP_ENTER" action Function(task_crown_close)

    use task_chrome("任务 校一只电子表", "键盘 ← → 或 A D 微调。鼠标点两边的钮也行。调到 0 再按回车。"):
        text ("快 " + str(task_error) + " 秒" if task_error > 0 else ("慢 " + str(-task_error) + " 秒" if task_error < 0 else "准")):
            xalign 0.5
            ypos 300
            size 72
            color ("#7DFFB2" if task_error == 0 else "#FFE08A")
            font gui.interface_text_font

        textbutton "－":
            xpos 620
            ypos 460
            action Function(task_crown_nudge, -1)
            text_size 48
            text_color "#FFE08A"
            background Solid("#2A2430")
            padding (36, 8)

        textbutton "＋":
            xpos 1180
            ypos 460
            action Function(task_crown_nudge, 1)
            text_size 48
            text_color "#FFE08A"
            background Solid("#2A2430")
            padding (36, 8)

        textbutton "合盖":
            xalign 0.5
            ypos 640
            action Function(task_crown_close)
            text_size 32
            text_color "#2B2420"
            background Solid("#E7C98A")
            padding (40, 14)


screen task_listen():
    modal True
    zorder 220

    key "K_RETURN" action Function(task_listen_confirm)
    key "K_KP_ENTER" action Function(task_listen_confirm)
    timer 18.0 action Function(task_listen_timeout)

    use task_chrome("任务 听出那台发闷的", "三台样机。鼠标点一台，再按回车。选对了马上结束。点错还能再听一次。十八秒内没定下来就算失败。"):
        hbox:
            xpos 180
            ypos 300
            spacing 48
            for i in range(3):
                textbutton ("第 " + str(i + 1) + " 台\n" + ("嗡——" if i == task_bad else "沙沙")):
                    action Function(task_listen_pick, i)
                    xsize 420
                    text_size 32
                    text_color "#FFE08A"
                    text_align 0.5
                    xalign 0.5
                    background Solid("#6A3018" if task_pick == i else "#2A2430")
                    hover_background Solid("#8A3A22")
                    padding (24, 36)


screen task_wire():
    modal True
    zorder 220

    key "K_UP" action Function(task_wire_key, "up")
    key "K_LEFT" action Function(task_wire_key, "left")
    key "K_DOWN" action Function(task_wire_key, "down")

    use task_chrome("任务 国贸这排灯", "鼠标点不亮的那盏。然后按键盘 ↑ ← ↓。"):
        hbox:
            xpos 120
            ypos 320
            spacing 24
            for i in range(6):
                textbutton ("不亮" if i == task_dead else "亮"):
                    action Function(task_wire_pick, i)
                    xsize 250
                    ysize 180
                    text_size 32
                    text_color ("#E07A72" if i == task_dead else "#7DFFB2")
                    background Solid("#1A1024" if i == task_dead else "#243028")
                    hover_background Solid("#6A3018")

        text "接线进度 " + str(task_step) + " / 3" xalign 0.5 ypos 620 size 28 color "#E8D6BC" font gui.interface_text_font


screen task_paper():
    modal True
    zorder 220

    key "K_SPACE" action Function(task_paper_stamp)

    use task_chrome("任务 把三句话圈下来", "鼠标按从上到下的顺序点中一句，再按空格圈上。"):
        vbox:
            xpos 220
            ypos 250
            spacing 22
            for i, line in enumerate((
                "改革开放胆子要大一些，敢于试验。",
                "看准了的，就大胆地试，大胆地闯。",
                "发展才是硬道理。",
            )):
                textbutton line:
                    action Function(task_paper_click, i)
                    xsize 1480
                    text_size 30
                    text_align 0.0
                    text_color "#2B2420"
                    background Solid("#E7C98A" if task_step > i else ("#FFF6DE" if task_pick == i else "#D9C9B8"))
                    hover_background Solid("#FFE08A")
                    padding (28, 16)


screen task_solder():
    modal True
    zorder 220

    key "K_SPACE" action Function(task_solder_stamp)
    timer 0.05 repeat True action Function(task_pump)

    use task_chrome("任务 四个焊点", "鼠标点焊盘，让烙铁贴上去。红色的条走进金色区域时，按空格。"):
        $ heat = task_heat_now()

        frame:
            xpos 360
            ypos 250
            xsize 1200
            ysize 36
            background Solid("#2A2430")

            frame:
                xpos 480
                ypos 0
                xsize 264
                ysize 36
                background Solid("#6A5430")

            frame:
                xpos 0
                ypos 0
                xsize max(8, int(1200 * heat / 100.0))
                ysize 36
                background Solid("#E25B4A")

        text "金区在中间。焊点 " + str(task_hits) + "/4    失误 " + str(task_miss) + "/4":
            xalign 0.5
            ypos 310
            size 26
            color "#E8D6BC"
            font gui.interface_text_font

        textbutton "焊盘":
            xalign 0.5
            ypos 430
            action Function(task_solder_place)
            xsize 360
            text_size 36
            text_color "#2B2420"
            background Solid("#E7C98A" if task_iron_down() else "#C4A35A")
            padding (40, 28)

        text ("烙铁贴着" if task_iron_down() else "先点焊盘") xalign 0.5 ypos 620 size 26 color "#FFE08A" font gui.interface_text_font


screen task_sort():
    modal True
    zorder 220

    key "q" action Function(task_sort_bin, "good")
    key "e" action Function(task_sort_bin, "bad")

    use task_chrome("任务 把电容分开", "鼠标点一颗。好的按 Q，受潮发暗的按 E。"):
        hbox:
            xpos 180
            ypos 280
            spacing 36
            for i in range(4):
                $ kind = task_caps[i][0] if len(task_caps) > i else "good"
                $ placed = task_caps[i][1] if len(task_caps) > i else False
                textbutton ("已分出" if placed else ("金亮" if kind == "good" else "发暗")):
                    action Function(task_sort_pick, i)
                    xsize 340
                    ysize 200
                    text_size 36
                    text_color ("#8A7A6A" if placed else "#2B2420")
                    background Solid("#3A342C" if placed else ("#6A3018" if task_pick == i else ("#E7C98A" if kind == "good" else "#8A5A48")))
                    padding (20, 48)

        hbox:
            xpos 520
            ypos 560
            spacing 80
            frame:
                xsize 360
                ysize 120
                background Solid("#243028")
                text "Q  装机" xalign 0.5 yalign 0.5 size 32 color "#7DFFB2" font gui.interface_text_font
            frame:
                xsize 360
                ysize 120
                background Solid("#3A2420")
                text "E  退回" xalign 0.5 yalign 0.5 size 32 color "#E07A72" font gui.interface_text_font
