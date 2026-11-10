## 红卫的春天 — main script
## A playable pilot adapted from the optimized novella and the branch/stat document.

label splashscreen:
    show screen quick_menu
    play music "audio/prologue.ogg" fadein 1.5 loop
    scene black
    with fade

    show text "{size=64}{color=#FFF6DE}一九七八年{/color}{/size}" at splash_title
    with Dissolve(0.6)
    $ renpy.pause(1.5, hard=False)

    scene hist_garden at splash_drift
    with Dissolve(1.0)
    show text "{size=46}{color=#FFF6DE}包产到户{/color}{/size}" at splash_caption
    $ renpy.pause(2.2, hard=False)

    scene hist_street at splash_drift
    with Dissolve(1.0)
    show text "{size=46}{color=#FFF6DE}出门{/color}{/size}" at splash_caption
    $ renpy.pause(2.0, hard=False)

    scene hist_luohu at splash_drift
    with Dissolve(1.0)
    show text "{size=46}{color=#FFF6DE}南下{/color}{/size}" at splash_caption
    $ renpy.pause(2.0, hard=False)

    scene hist_border at splash_drift
    with Dissolve(1.0)
    show text "{size=46}{color=#FFF6DE}深圳{/color}{/size}" at splash_caption
    $ renpy.pause(2.0, hard=False)

    scene hist_guomao at splash_drift
    with Dissolve(1.0)
    show text "{size=46}{color=#FFF6DE}一九九二年{/color}{/size}" at splash_caption
    $ renpy.pause(2.2, hard=False)

    scene hist_cover
    with Dissolve(1.2)
    show text "{size=92}{color=#FFF6DE}红卫的春天{/color}{/size}" at splash_title
    $ renpy.pause(2.4, hard=False)

    $ quick_menu = True
    hide screen quick_menu
    return


label start:
    $ reset_game()
    $ quick_menu = True
    jump prologue


label chapter_card(chapter, title, place):
    show screen chapter_card(chapter, title, place)
    with Dissolve(0.5)
    pause 2.2
    hide screen chapter_card
    with Dissolve(0.5)
    return


label speech_takeaway:
    if thought >= 60:
        n "他忽然懂了。自己以前只想着“敢闯”，却没看清该往哪儿闯。"
        n "只想着快点赚钱，却忘了当初靠什么站住的脚。"
    elif thought < 45:
        n "他只记住了“大胆地闯”。"
        n "“看清往哪儿闯”那半句，从耳边滑过去了。"
    else:
        n "他听见了，也记住了。可哪一句该先照做，他还说不清。"
    return


## ===========================================================================
## 序章：红手印
## ===========================================================================

label prologue:
    $ mark_stage("south")
    scene hist_garden at slow_push
    with fade
    play music "audio/prologue.ogg" if_changed loop
    play sound "audio/chapter.wav"

    play music "audio/mus_c1_a.wav" fadeout 0.8 fadein 0.8 loop
    call chapter_card("第一章", "从小岗到深圳", "1978—1985，凤阳到深圳") from _call_chapter_card

    $ mark_beat("seal")
    n "一九七八年冬，小岗村堂屋里，大人们偷偷按手印，包产到户。父亲孙守成成分不好，把手缩了回去。"
    n "人散后，十二岁的孙红卫把小拇指按进印泥，在旧报纸上盖了个歪斜的红印。大伯孙守义折回来，看见了。"

    menu:
        "承认。那是我按的。":
            $ change_stats(rep=2, family=5, thought=5)
            $ flag_seal_active = True

            l "……是我按的。"
            n "大伯看了他很久，没有发火。他把那只印泥盒塞进红卫手里。"
            u "留着。拿不定主意的时候，想想今天。总得有人先走一步。"

        "低下头，不承认。":
            $ change_stats(family=-2, thought=-2)
            $ flag_seal_active = False

            l "不是我。"
            n "大伯看了看他沾红的拇指，没有拆穿，只把印泥盒收进柜子。"
            u "不认，也行。可有些事，不是不认，就没发生过。"

    scene hist_garden at slow_push
    with dissolve
    n "第二年真丰收了。白面馒头到了桌上，母亲掰给弟弟妹妹。红卫把印泥盒带在身上。村里的收音机、手电筒坏了，都来找他。"

    $ mark_beat("torch")
    n "王婶把一只不亮的手电放在桌上。筒是铁的，电池滚到了边沿。"
    menu:
        "今晚就把这只手电修好。":
            $ task_begin_torch()
            call screen task_torch
            if _return == "ok":
                $ flag_torch = 1
                $ change_stats(rep=4, tech=4, thought=2)
                n "光柱打在土墙上。王婶笑出声，塞给他两个鸡蛋。"
            else:
                $ flag_torch = 2
                $ change_stats(tech=1)
                n "电池没卡紧，光闪了两下又灭了。他说明天再来。"

        "先睡。手电放着，明天再说。":
            $ flag_torch = 3
            $ change_stats(thought=-1)
            n "手电在桌上躺了一夜。第二天王婶自己拿去镇上了。"

    scene hist_street at slow_push
    with fade

    n "一九八四年，同乡张长喜从广东回来，手腕上亮着电子表。红卫瞒着家里卖了猪凑路费。父亲第一次打了他。"
    f "你以为外面的钱，是从地上捡的？"
    l "在家熬着，一辈子都熬不出头。"
    n "母亲把二十元缝进棉袄夹层。父亲送到院门口，没再往前。"

    $ mark_beat("father")
    menu:
        "回去，叫一声爹。":
            $ change_stats(family=5, thought=2)
            $ flag_call_father = True

            n "红卫放下行李，跑了回去。"
            l "爹。"
            if family >= 48:
                n "父亲侧过身。声音比那天的巴掌软。"
                f "外边冷，把棉袄穿好。"
                n "红卫走了。他没看见，父亲抬手抹了一把脸。"
            else:
                n "父亲没有回头。"
                f "去吧。"
                n "背后没有第二句话。"

        "沉默着离开。":
            $ change_stats(family=-3)
            $ flag_call_father = False

            n "红卫把话咽回去，头也不回地走了。身后没有人叫他的名字。"

    scene hist_luohu at slow_push
    with fade

    scene hist_carriage at slow_push
    with dissolve
    n "绿皮火车上，他认识了三个人。陈海生满脑子生意。苏文静是上海电子学校的技术员。吴国强是安徽老乡，介绍费被人骗光了。"
    s "修东西不能只靠试。看懂了线路，就知道毛病出在哪。"
    n "她在报纸边角画了张收音机电路图。红卫折好，塞进棉袄最里面。"

    $ mark_beat("circuit")
    menu:
        "跟着她的图，把顺序走一遍。":
            $ task_begin_circuit()
            call screen task_circuit
            $ renpy.music.set_volume(1.0, delay=0.4, channel="music")
            if _return == "ok":
                $ flag_circuit = 1
                $ change_stats(tech=6, thought=3)
                n "电源、电阻、电容、喇叭。他用手指点过喇叭的位置，图在脑子里亮了一下。"
                s "记住顺序。手比眼睛老实。"
            else:
                $ flag_circuit = 2
                $ change_stats(tech=1)
                n "顺序断在半路。他把报纸折好，先把这趟车坐完。"

        "先收好，下车再说。":
            $ flag_circuit = 3
            n "图在棉袄最里面。车上人多，他没有摊开。"

label wu_menu:
    $ mark_beat("wu")
    if money < 20:
        n "他摸到口袋底。五元凑不齐，可也不能当没看见。"

    menu:
        "拿出五元，直接塞给他。" if money >= 20:
            $ change_stats(money=-5, rep=5, thought=5)
            $ flag_wu = True
            $ flag_wu_decided = True

            n "红卫摸出五元，塞进吴国强手里。路费少了四分之一。"
            w "兄弟，这份情我记下了。以后回凤阳，一定来找我。"

        "五元不够，把零钱和干粮塞给他。" if money < 20:
            $ change_stats(money=-2, rep=4, thought=4)
            $ flag_wu = True
            $ flag_wu_decided = True

            n "五元拿不出来。他把零钱和剩下的半块馒头塞过去。"
            w "兄弟，这份情我记下了。以后回凤阳，一定来找我。"

        "先把地址记下，到了深圳再补给他。":
            $ change_stats(rep=3, thought=3)
            $ flag_wu = True
            $ flag_wu_decided = True

            n "红卫没有把整张票子掏出来。他写下名字，说车费到了深圳再补。"
            w "行。人到了就好。"

        "自顾不暇，不资助。":
            $ change_stats(rep=-5, thought=-3)
            $ flag_wu = False
            $ flag_wu_decided = True

            n "红卫攥了攥口袋，最终没有伸手。吴国强在下一站下了车。"

    scene hist_border at slow_push
    with fade

    n "张长喜留的地址是空的。红卫第一晚睡在货运站屋檐下。白天搬砖，晚上给工友修收音机。深圳没有黄金。"
    n "工地扩音器坏了，他用铁丝临时接上。苏文静找来，递给他一套半旧的电工工具。"
    s "你手挺稳，别一直拿去搬砖。"

    $ mark_beat("tools")
    menu:
        "接过工具。":
            $ change_stats(rep=2, tech=5, thought=2)
            $ flag_su_tools = True

            n "红卫接过工具，手指在旧螺丝刀上停了一下。"
            s "别谢我。工具是死的，人是活的。"

        "拒绝，怕欠人情。":
            $ change_stats(tech=-5, thought=-2)
            $ flag_su_tools = False

            l "不用了。我这样，也挺好。"
            s "那你就继续用铁丝吧。"

    scene hist_abacus at slow_push
    with dissolve
    n "他在路口挂起招牌：彪子电器维修，修不好不要钱。苏文静每周两个晚上来教：先测电源，换件查参数，修好通电半小时。"

    scene hist_factory at slow_push
    with dissolve

    n "老工人抱来一台坏了几年的收音机，说是儿子留下的。红卫装错电阻，烧了线圈。苏文静陪他在垃圾堆里翻出同型号的零件。"

    $ mark_beat("radio")
    menu:
        "继续修，修到响为止。":
            $ change_stats(money=-3, rep=5, tech=10, thought=5)
            $ flag_old_radio = True

            n "天快亮时，收音机里传出断断续续的广播。他修的不只是机器，还有别人心里的念想。"
            s "修坏了不可怕。怕的是不认，也不改。"

        "赔一台新的，省事。":
            $ change_stats(money=-10, rep=2, tech=-5, thought=-3)
            $ flag_old_radio = False

            n "红卫买了台新的送过去。老人说了谢谢，却再也没来。有些东西，新的替不了旧的。"

    $ finish_stage("south")
    jump spring


label spring:
    $ mark_stage("spring")
    scene hist_market at slow_push
    with fade
    play music "audio/chapter2.ogg" fadein 2.0 loop
    play sound "audio/chapter.wav"

    call chapter_card("第二章", "春声作坊", "1985—1986，招牌挂上") from _call_chapter_card_spring

    n "陈海生拉他合伙：自己跑货，红卫验货维修。一趟下来，比搬砖一个月还多。"
    scene hist_garden at slow_push
    with dissolve
    n "第一次回凤阳，他提着录音机。父亲拿起来翻看。"
    f "有发票吗？坏了的东西，你也卖吗？"
    n "红卫把三百元拍在桌上。父亲没碰，进了屋。"

    $ mark_beat("invoice")
    menu:
        "追进去，解释清楚。":
            $ change_stats(family=5, thought=3)
            $ flag_invoice = True

            n "红卫把进货单、发票摊在炕上。"
            l "爹，坏了的，我修好再卖。"
            f "挣钱可以。别挣那种，半夜睡不着觉的钱。"

        "赌气离开。":
            $ change_stats(family=-5, thought=-2)
            $ flag_invoice = False

            n "红卫把钱收回口袋，转身出了门。那顿饭，谁也没吃好。"

    $ mark_beat("date")
    n "回深圳后，陈海生塞来一张进货单。日期比到货早了一天。"
    c "改前一天，税就好算。就一个字的事。"
    menu:
        "不改。日期是哪天，就写哪天。":
            $ flag_date = 1
            $ change_stats(rep=4, thought=4)
            n "红卫把单子推回去。陈海生啧了一声，没再劝。"
            if flag_invoice:
                n "他想起父亲那句：别挣半夜睡不着的钱。"

        "把日期改了。":
            $ flag_date = 2
            $ change_stats(money=4, rep=-6, thought=-4)
            $ flag_profit = True
            n "字改得很轻。那张单子，他一直没敢给父亲看。"

    scene bg_watch at slow_push
    with dissolve

    n "陈海生低价收了一批电子表。一测，近三分之一走时不准，问题在晶振和廉价电容。"

    if tech < 40:
        s "逐台校准，你现在还悬。可以先把一摆就停的挑出来。"

label watch_menu:
    $ mark_beat("watch")
    menu:
        "直接售卖，回笼资金。":
            $ change_stats(money=10, rep=-10, thought=-8)
            $ flag_watch = 0
            $ flag_watch_decided = True
            $ flag_profit = True

            n "残次表批给了外地商贩。钱来得快。江西的商人上过一次当，再也没回头。"

        "降价，并告诉买主差在哪。":
            $ change_stats(money=3, rep=5, tech=2, thought=3)
            $ flag_watch = 1
            $ flag_watch_decided = True

            n "摊前贴了张纸：走时不准，降价处理。利润薄了，几个觉得他实在的商贩成了回头客。"

        "先挑出停走的，其余降价说清楚。" if tech < 40:
            $ change_stats(money=1, rep=6, tech=4, thought=5)
            $ flag_watch = 1
            $ flag_watch_decided = True

            n "他做不到逐台校准。一摆就停的挑出来，摊前写明问题在晶振。"
            s "先认毛病，再谈手艺。"

        "暂停出货，逐台校准。" if tech >= 40:
            $ change_stats(money=-8, rep=10, tech=10, thought=8)
            $ flag_watch = 2
            $ flag_watch_decided = True

            n "货全部扣下。他和苏文静连着熬了几个通宵，逐个校准晶振。"
            s "拿劣质元件当好的卖，早晚砸自己招牌。"

    if flag_watch == 2:
        n "几个月后，那位江西商人找了来。就数他们家的电子表返修率最低。"
        j "先签一年。货可以慢，但不能砸。"
    elif flag_watch == 1:
        n "几个回头客带来了新订单。不多，够把摊子撑下去。"
    else:
        n "钱是赚到了。有些商贩再见到他，眼神变了。"

    $ mark_beat("crown")
    n "桌上还剩一只走得飞快的表。旋钮很紧。"
    menu:
        "现在就把它校到准。":
            $ task_begin_crown()
            call screen task_crown
            if _return == "ok":
                $ flag_crown = 1
                $ change_stats(tech=5, rep=3, thought=2)
                n "误差归零，他才合上后盖。这只表他没卖，留给了自己。"
            else:
                $ flag_crown = 2
                $ change_stats(tech=1)
                n "盖合早了。表还是快，进了次品箱。"

        "别费这个功夫，塞进次品箱。":
            $ flag_crown = 3
            n "他没动旋钮。那只表和停走的堆在一起。"

    scene hist_factory at slow_push
    with fade

    n "倒卖的利润薄了。三个人租了漏雨的平房，挂上“春声电器作坊”。红卫管采购，苏文静管电路和质量，陈海生跑销售，梁师傅带工人。"

    $ mark_beat("sign")
    n "招牌是梁师傅连夜刷的。红漆还没干，雨点就打上来。房东站在门口，等这个月的钱。"
    menu:
        "租金先交三个月，把这间屋守住。":
            $ flag_sign = 1
            $ change_stats(money=-6, thought=3, rep=2)
            n "他把卖表剩下的钱拍在房东手里。三个月。屋是漏的，门锁是自己的。"
            liang "有门，就有地方把线摊开。"

        "先交一个月，剩下的钱拿去进货。":
            $ flag_sign = 2
            $ change_stats(money=4, thought=-2)
            $ flag_profit = True
            n "房东把钥匙扔在桌上。下个月再来，不一定还是这把锁。"
            c "货比房子好周转。房子又不会跑。"

    n "夜里四个人围着一张缺腿的桌子。陈海生摊开地图，从深圳画到江西。铅笔印子有的地方已经断了。"
    s "先把这一间屋的灯接亮。别的，等有订单再说。"

    $ finish_stage("spring")
    jump chapter3


label downfall_route:
    scene bg_collapse at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 1.0 loop

    if flag_hide:
        n "那批货终究没瞒过去。工商介入，春声作坊被查封。红卫背上一身债务和骂名。"
    else:
        n "灰色链条断得比想象中更快。钱没填上窟窿，案件牵了进来。春声作坊散了。"

    n "门上贴了封条。春声两个字被雨冲得只剩半边。工具箱被梁师傅连夜拎走，说先替他保管。"
    n "父亲摔断腿的电报，压在抽屉最底下。他一直没敢回。"

    $ finish_stage("chapter4")
    jump ending_router



## ===========================================================================
## 第五章：一九九二年的冬天
## ===========================================================================

label chapter6:
    $ mark_stage("chapter6")
    scene bg_stall at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop
    play sound "audio/chapter.wav"

    call chapter_card("第五章", "一九九二年的冬天", "1992年1月，深圳国贸大厦") from _call_chapter_card_6

    $ mark_beat("stall")
    n "红卫靠着维修摊慢慢还债。日子过得紧巴巴，却也踏实。临近年关的一天，梁师傅找到他。"
    scene hist_guomao at slow_push
    with dissolve  # auto-bg
    liang "国贸大厦那边，临时需要人手检查扩音设备和线路。工钱给得高。"

    $ mark_beat("wage")
    liang "这趟要是你去，工钱可以对半。我带你认门。"
    menu:
        "留下他的一份。":
            $ flag_wage = 1
            $ change_stats(rep=3, thought=2)
            n "红卫点头。钱少了一半，梁师傅把电笔递了过来。"

        "这趟我一个人拿。":
            $ flag_wage = 2
            $ change_stats(money=4, rep=-3, thought=-2)
            $ flag_profit = True
            n "工钱进了自己口袋。梁师傅把地址写下，没再说什么。"

    scene bg_g28_lobby_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "那天，正好是债主约他谈还款的日子。"

    $ mark_beat("tour")
    menu:
        "推掉债主会面，去国贸接活。":
            $ change_stats(money=5, tech=2, thought=10)
            $ flag_tour = 1
            $ flag_tour_decided = True

            n "红卫没多想，拎起工具箱就去了。他需要这笔钱。也说不清为什么，心里还有一点别的东西在动。"

        "先见债主，再去抢修。":
            $ change_stats(money=3, rep=3, tech=2, thought=5)
            $ flag_tour = 2
            $ flag_tour_decided = True

            n "红卫先和债主谈好了分期还款。刚松口气，就接到梁师傅的电话。设备突然出故障，只有他熟这种老线路。"
            n "他匆匆赶过去，站在了人群边缘。"

        "让梁师傅代班，专心协商还款。":
            $ change_stats(rep=2, thought=-10)
            $ flag_tour = 0
            $ flag_tour_decided = True

            scene bg_g28_lobby at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫安心谈妥了还款计划。他没有去现场。那几句话，他是几天后从报纸和电视里看到的。"

    # speech-hold-begin
    $ mark_beat("speech")
    scene bg_g28_lobby at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.5 loop

    if flag_tour > 0:
        n "国贸大厦的大厅里，已经站满了人。红卫钻在音控台后面，拧着接头。"

        $ mark_beat("wire")
        liang "左边那排灯，有一盏不亮。你上，还是我上？"
        menu:
            "电笔给我，我来查。":
                $ task_begin_wire()
                call screen task_wire
                if _return == "ok":
                    $ flag_wire = 1
                    $ change_stats(money=3, tech=4, rep=2)
                    n "灯一排亮起来。梁师傅吹了声口哨，说这半天的工钱给你加一截。"
                else:
                    $ flag_wire = 2
                    n "线没接住。梁师傅后头补了一截，灯才亮。"

            "你先接着，我去看前面。":
                $ flag_wire = 3
                n "梁师傅自己接上了。红卫往人群那边看。"

        scene bg_g28_lobby_z at slow_push
        with dissolve
        n "外面忽然传来一阵脚步声。工作人员示意所有人停下手里的活。有人低声说：“小平同志来了。”"

        scene bg_deng_speech at slow_push
        with dissolve
        play music "audio/fuguang.ogg" fadein 2.5 loop
        n "人群往两边让开。一位老人站在大厅中间，深色大衣，头发花白。旁边有人拿着本子，一笔一笔地记。"

        scene bg_deng_gap at slow_push
        with dissolve
        n "人群挡住了视线。红卫站在最后排，手上还沾着线路上的黑油。他只能从肩膀的缝隙里，看见那位老人。"

        scene bg_deng_speech_near at slow_push
        with dissolve
        n "谈话不是慷慨激昂的演讲。更像和身边人的闲聊。他离得远，听不全，只断断续续接住几句。"

        scene bg_deng_speech at slow_push
        with dissolve
        $ renpy.music.set_volume(0.4, delay=0.5, channel="music")
        play talk "audio/nanfang.ogg" volume 4.0
        n "“改革开放胆子要大一些，敢于试验。”"

        scene bg_deng_speech_near at slow_push
        with dissolve
        n "“看准了的，就大胆地试，大胆地闯。”"

        scene bg_deng_speech at slow_push
        with dissolve
        n "“发展才是硬道理。”"

        if thought >= 60:
            l "敢闯不够。得看清，往哪儿闯。"

        scene bg_deng_speech_near at slow_push
        with dissolve
        n "周围的人往前挤、鼓掌。他却站着没动。三个声音，在他脑子里来回响。"

        u "总得有人先走一步。"
        s "错了敢认，也得有本事改。"
        f "坏了的东西，你也卖吗？"

        stop talk fadeout 0.4
        $ renpy.music.set_volume(1.0, delay=0.4, channel="music")
        play music "audio/mus_c1_a.wav" fadein 2.0 loop
        scene bg_stall at slow_push
        with dissolve
        n "后来他才知道，那天老人还说了很多。他把报纸上的话剪下来，贴在维修摊的挡板上。"

        call speech_takeaway

        n "人群散去后，梁师傅催他收工具。却看见他盯着修好的扩音器发呆。"
        liang "想什么呢？"
        l "我以前只顾着闯，没看清往哪儿闯。"
        liang "那就重新看。"
        n "梁师傅把螺丝刀递回他手里。"
    else:
        scene bg_stall at slow_push
        with fade
        show deng_inset at inset_card
        play music "audio/fuguang.ogg" fadein 2.0 loop
        n "几天后，红卫在维修摊前，一字一句读完了那篇谈话。报纸上的话印得清清楚楚，他却读得很慢。像在跟每一个字较劲。"

        $ mark_beat("paper")
        menu:
            "把那三句，自己圈出来。":
                $ task_begin_paper()
                call screen task_paper
                if _return == "ok":
                    $ flag_paper = 1
                    $ change_stats(thought=6, tech=1)
                    n "三句都圈在了报边上。红笔还没干。"
                else:
                    $ flag_paper = 2
                    $ change_stats(thought=1)
                    n "红笔点错了行。他把报纸折起来，又摊开。"

            "只看标题。":
                $ flag_paper = 3
                $ change_stats(thought=-2)
                n "标题看过了。正文他折进抽屉。"

        $ renpy.music.set_volume(0.4, delay=0.5, channel="music")
        play talk "audio/nanfang.ogg" volume 4.0
        n "“改革开放胆子要大一些，敢于试验。”"
        n "“看准了的，就大胆地试，大胆地闯。”"
        n "“发展才是硬道理。”"

        if thought >= 60:
            l "敢闯不够。得看清，往哪儿闯。"

        n "三个声音，在他脑子里来回响。"
        u "总得有人先走一步。"
        s "错了敢认，也得有本事改。"
        f "坏了的东西，你也卖吗？"

        hide deng_inset
        stop talk fadeout 0.4
        $ renpy.music.set_volume(1.0, delay=0.4, channel="music")
        play music "audio/mus_c1_a.wav" fadein 2.0 loop
        call speech_takeaway

        n "收工后，梁师傅打来电话，说国贸的活干完了，工钱一分不少。"
        n "红卫道了谢，挂了电话，在摊前坐了很久。"
    # speech-hold-end

    $ mark_beat("board")
    n "三句话还在耳朵里。维修摊的挡板上，有一块空。"
    menu:
        "把三句抄在挡板上。":
            $ flag_board = 1
            $ change_stats(thought=4, rep=2)
            n "字不大。来修收音机的人，排队的时候会看见。"

        "只记在心里。":
            $ flag_board = 2
            n "挡板还是空的。那三句他来回念，没有写下来。"

    scene bg_warehouse at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop

    n "那天夜里，红卫没有去找人喝酒。也没有等来什么贵人。他独自回到停工半年的旧仓库。"
    n "借着门口的路灯，撬开一只落满灰尘的木箱。"

    n "里面全是被退回来的春声收音机。他拿出一台故障最严重的，拉过板凳坐下，插上电烙铁。"

    n "电烙铁的顶端慢慢热起来，泛出一点暗红。像极了当年煤油灯下，那枚鲜红的手印。收音机先发出一阵刺耳的杂音。"
    n "随后，清晰的广播声，慢慢流淌出来。"

    menu:
        "留下来，把退货一台台拆开。":
            $ change_stats(tech=5, thought=10)
            $ flag_restart = True

            scene bg_g29_solder_c at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫把木箱拖到灯下。一台，两台，三台。他拆到天亮，手指上全是机油。"
            n "他知道，自己得从第一台开始，重新来。"

        "去酒馆，先喝一顿再说。":
            $ change_stats(money=-3, thought=-10)
            $ flag_restart = False

            n "红卫把电烙铁拔了，转身去了街口的酒馆。他喝到半夜，想了很多，又好像什么都没想。第二天醒来，仓库里的木箱还开着。"
            scene bg_g29_solder at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "收音机没有响。"

    $ finish_stage("chapter6")
    jump chapter7


## ===========================================================================
## 第六章：卷土重来
## ===========================================================================

label chapter7:
    $ mark_stage("chapter7")
    scene bg_warehouse at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop
    play sound "audio/chapter.wav"

    call chapter_card("第六章", "卷土重来", "1992—1995年，深圳与凤阳") from _call_chapter_card_7

    $ mark_beat("restart")
    n "南巡的讲话，没有立刻送来订单。却给红卫拨正了方向。真正的振作，是从一件件小事开始的。"

    if flag_restart:
        scene bg_g29_solder_c at slow_push  # auto-bg
        with dissolve  # auto-bg
        n "他把所有退货的机器，一台台拆开。凭着苏文静教给他的技术，很快定位了所有问题。一是劣质电容耐压不足。"
        n "二是当初为了省成本，保护电路被简化了。"
    else:
        n "他在仓库里坐了很久，才重新拿起螺丝刀。拆第一台机器的时候，他的手有点生。"
        n "可拆到第三台，那些熟悉的线路，又回来了。他对着当年苏文静留下的图纸，一点点补上保护电路。"
    n "反复测试参数，直到样机连续开机七十二小时都不出问题。那些当年他没听进去的话、没放在心上的设计，摔过跟头后，全都刻进了骨子里。"

    $ mark_beat("note")
    n "退货的木箱还开着。箱盖内侧是空白的。"
    menu:
        "把失败的原因写在箱盖上。":
            $ flag_note = 1
            $ change_stats(thought=5, tech=3, rep=2)
            n "他用铅笔写了两行：劣质电容，保护电路被省掉。写给后来打开这只箱子的人。"

        "只记合格的数，别的不写。":
            $ flag_note = 2
            $ change_stats(thought=-2)
            n "箱盖还是空白。失败留在他嘴里，没留在木头上。"

    scene bg_shanghai at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "复产前，陈海生已经走了。红卫手里，只剩下一笔小得可怜的钱。"

    $ mark_beat("ten")
    menu:
        "先做十台，没问题再扩。":
            $ change_stats(money=-5, rep=10, tech=10, thought=5)
            $ flag_ten = True

            scene bg_g30_shanghai at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫买了十套最好的元件。十台机器，每一台都亲手调试。他知道，这次不能再赌。"

        "直接做一百台，抢回市场。":
            $ change_stats(money=10, rep=-5, tech=-5, thought=-5)
            $ flag_ten = False
            $ flag_profit = True

            scene bg_1995 at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫把所有的钱都压了上去。一百台机器，流水一样下线。他告诉自己，这次一定能把失去的抢回来。"

    $ mark_beat("weld")
    n "去上海之前，他在自己桌上插上电烙铁。锡丝搁在手边。"
    menu:
        "先把四个焊点焊完。":
            $ task_begin_solder()
            call screen task_solder
            if _return == "ok":
                $ flag_solder_task = 1
                $ change_stats(tech=6, thought=3)
                n "四个焊点都亮着。他这才敢把样机装箱。"
            else:
                $ flag_solder_task = 2
                $ change_stats(tech=1)
                n "锡点发黑。他擦掉，告诉自己路上再补。"

        "样机已经响了，不必再练。":
            $ flag_solder_task = 3
            n "他把烙铁搁下。样机在箱子里，还是热的。"

    scene bg_shanghai at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop

    n "红卫带着改好的样机，去了上海。苏文静没有立刻答应。她拆开机器，仔细检查了半天。"
    scene bg_g30_shanghai_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    s "这参数，是按我当年跟你讲的算的？"
    l "当年没听进去。摔了一跤，反倒记牢了。"
    s "这一次，准备做多少台？"
    l "先做十台。十台都没问题，再做一百台。"

    $ mark_beat("su")
    menu:
        "全部接受苏文静的三个条件。":
            $ change_stats(rep=5, tech=10, thought=5)
            $ flag_su_return = True
            $ flag_su_break = False

            s "第一，每批产品必须抽检。第二，不合格的，绝对不能出厂。第三，技术人员有权直接叫停生产。"
            l "我答应。"
            scene bg_g30_shanghai_c at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "苏文静看了他很久，终于点了点头。"

        "部分接受，生产权不能全交出去。":
            $ change_stats(tech=3, thought=-2)
            $ flag_su_return = False
            $ flag_su_break = False

            n "红卫答应了抽检，却不肯把叫停生产的权力交出去。"
            scene bg_g30_shanghai_z at slow_push  # auto-bg
            with dissolve  # auto-bg
            s "你还是没明白。"
            n "苏文静没有回来。但她把一套新的图纸，留在了桌上。"

        "拒绝。厂子只能有一个人说了算。":
            $ change_stats(rep=-5, tech=-10, thought=-5)
            $ flag_su_return = False
            $ flag_su_break = True

            scene bg_shanghai at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫把图纸推了回去。"
            l "厂子只能有一个人说了算。"
            scene bg_g30_shanghai at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "苏文静没有再劝。她收起图纸，转身走了。那扇门关上以后，红卫在桌前坐了很久。"

    scene bg_longbus at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop

    n "红卫找到那位江西经销商。没提要新订单，只递上一份还款计划和改进后的样机。对方让他走。"
    scene bg_g14_bus_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "他就把机器放在桌上。"
    l "你试试。不好用，我再拿回去。"

    $ mark_beat("debt")
    menu:
        "如实还款，哪怕慢一点。":
            $ change_stats(rep=10, tech=2, thought=5)
            $ flag_debt = True

            n "几天后，对方打来电话。"
            j "先要五十台。卖不出去，你自己拉回来。"
            n "红卫握着电话，半天没说出话。"

        "先拖一拖，等资金缓过来。":
            $ change_stats(rep=-10, thought=-5)
            $ flag_debt = False
            $ flag_profit = True

            scene bg_g14_bus at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫把还款计划收了回去。他告诉自己，再等等，等资金缓过来。可对方再也没有打来电话。"

    scene bg_reopen at slow_push
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop

    n "红卫找到以前的工人。没承诺高工资，只说："
    l "欠你们的，我一笔一笔还。愿意回来的，咱们从五十台开始干。"

    n "最初，只有梁师傅和两个年轻工人回来。重新开工那天，门上还留着当年停工时的封条。红卫没让人刮掉。"
    l "留着。提醒自己，以后别再犯浑。"

    n "生意慢慢有了起色。红卫萌生了回凤阳建组装车间的想法。"

    $ mark_beat("home")
    menu:
        "回凤阳，把根扎回乡土。":
            $ change_stats(money=-10, rep=5, family=10, thought=10)
            $ flag_fengyang = True
            $ flag_end_decided = True

            n "他本以为要费很多功夫。没想到消息传回小岗村，大伯孙守义主动找上了门。身后跟着十几个村里的年轻人。"
            n "村里把闲置的旧仓库腾出来，免租金给他当厂房。条件只有一个：优先招村里困难家庭的青年。"

            n "几户受过红卫帮助的农户，主动拉着板车来打扫仓库、修理门窗。"
            n "还有人家拿出积蓄，说算小额入股，赔了也认。就信他的人品。"

            if flag_wu:
                n "吴国强也赶了过来，主动管起后勤和本地采购。"
                scene bg_factory at slow_push  # auto-bg
                with dissolve  # auto-bg
                w "当年你帮我一把，现在我帮你搭个手。咱们凤阳人，要干就一起干出个样子。"
            else:
                n "吴国强没有出现。红卫托人带话，想把当年的同乡情分续上。"
                n "对方只回了一句：“路是你自己选的，我不怪你。只是这回，我帮不上。”"
                scene bg_g32_factory_c at slow_push  # auto-bg
                with dissolve  # auto-bg
                n "红卫在村口站了半天，把这句话咽了下去。后来厂里招工，他特意给吴国强家留了一个名额。人没来，名额一直空着。"

        "留在深圳，继续扩产。":
            $ change_stats(money=10, family=-5, thought=-5)
            $ flag_fengyang = False
            $ flag_end_decided = True
            $ flag_profit = True

            scene bg_g32_factory_z at slow_push  # auto-bg
            with dissolve  # auto-bg
            n "红卫把回凤阳的念头压了下去。深圳的订单更多，离客户更近。他告诉自己，等再大一点，再回去。"
            n "可“再大一点”这句话，一说就是很多年。"

    if flag_fengyang:
        scene bg_factory at slow_push
        with fade
        play music "audio/mus_c1_a.wav" fadein 2.0 loop

        n "开工第一天，红卫把那只干裂的印泥盒，从贴身口袋里掏出来。摆在车间最显眼的桌上。"
        u "当年按手印，是为了吃饱饭。今天开厂子，是为了过好日子。"
        u "道理都一样——大家拧成一股绳，就没有过不去的坎。"
    else:
        scene bg_1995 at slow_push
        with fade
        play music "audio/mus_c1_a.wav" fadein 2.0 loop

        n "深圳的车间越扩越大。红卫把那只印泥盒，放在办公室的窗台上。每天上班，他都能看见。"
        n "只是回凤阳的次数，越来越少。"

    n "父亲孙守成起初还坚持种地。每天绕着车间走一圈，也不进门。"

    $ mark_beat("sort")
    n "桌上好电容和受潮的混在一起。父亲就站在门口。"
    menu:
        "先把电容分开，再请他看。":
            $ task_begin_sort()
            call screen task_sort
            if _return == "ok":
                $ flag_sort = 1
                $ change_stats(tech=4, family=3, thought=2)
                n "金亮的进了装机盒，发暗的退到一边。父亲的目光在两只盒子上停了一下。"
            else:
                $ flag_sort = 2
                $ change_stats(tech=1)
                n "好的坏的又混回一堆。他把手收回来。"

        "先别忙活，跟他说句话。":
            $ flag_sort = 3
            n "零件还堆着。红卫先转过身。"

    menu:
        "主动请父亲进车间，帮你看物料。":
            $ change_stats(family=10, thought=5)
            $ flag_father_reconcile = True

            n "红卫把父亲请到车间。"
            scene hist_factory at slow_push
            with dissolve  # auto-bg
            l "爹，你帮我看看物料。你眼睛毒，谁也别想糊弄你。"
            n "父亲板着脸，没说好，也没说不好。第二天，他却比谁都早到。"

        "等他自己愿意。":
            $ flag_father_reconcile = False

            n "红卫没有开口。父亲也没有进去。两个人隔着一道门槛，谁都没有先迈过去。"

    if flag_fengyang:
        scene bg_threshold at slow_push
        with fade
        play music "audio/mus_c1_a.wav" fadein 2.0 loop

        n "新一代收音机下线那天，红卫把第一台带回了老屋。父亲坐在门槛上。红卫把印泥盒放在他手边。"
        scene bg_g34_threshold_c at slow_push  # auto-bg
        with dissolve  # auto-bg
        n "父亲拿起来，慢慢摩挲着。收音机里播着新闻，屋外传来车间换班的铃声。"
        scene bg_g34_threshold_z at slow_push  # auto-bg
        with dissolve  # auto-bg
        f "现在外头，都叫你孙总了？"
        l "外头叫孙总。深圳的老朋友，叫彪子。您和我妈，还是叫我红卫。"
    else:
        scene bg_1995 at slow_push
        with fade
        play music "audio/mus_c1_a.wav" fadein 2.0 loop

        n "那年冬天，父亲第一次来了深圳。他站在车间门口，看了很久，才迈进去。红卫把印泥盒放在他手边。"
        n "父亲拿起来，慢慢摩挲着。"

        f "现在外头，都叫你孙总了？"
        scene bg_1995 at slow_push  # auto-bg
        with dissolve  # auto-bg
        l "外头叫孙总。深圳的老朋友，叫彪子。您和我妈，还是叫我红卫。"

    n "父亲把印泥盒递还给他，语气平静。"
    f "这回收好。别再乱按了。"

    menu:
        "把印泥盒和车票、电路图收在一起。":
            $ change_stats(family=3, thought=5)
            $ flag_legacy = True

            n "红卫没说话。他把印泥盒放进收音机的包装箱里。和当年那张皱巴巴的南下车票、苏文静画在报纸上的第一张电路图，收在了一起。"

        "把印泥盒收进抽屉。":
            $ change_stats(thought=-3)
            $ flag_legacy = False

            n "红卫把印泥盒收进抽屉。抽屉里还有很多别的东西。他关上抽屉，听见“咔哒”一声。"

    if flag_fengyang:
        scene bg_bus at slow_push
        with fade
        play music "audio/mus_c1_a.wav" fadein 2.0 loop

        n "窗外，曾经等着救济粮的村口，如今停着接送工人的班车。年轻的姑娘小伙说笑着从车上下来。"
        scene bg_g35_busstop_c at slow_push  # auto-bg
        with dissolve  # auto-bg
        n "眼里的光，和当年揣着二十元钱南下的他，一模一样。"

    scene bg_spring at drift_left
    with fade
    play music "audio/mus_c1_a.wav" fadein 2.0 loop

    n "春风从南边来。吹过深圳的高楼，也吹过凤阳的田野。十七年过去。"
    scene bg_warehouse at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "红手印的勇气、电烙铁的微光，终于在这片土地上，长出了实实在在的好日子。"

    $ finish_stage("chapter7")
    jump ending_router
