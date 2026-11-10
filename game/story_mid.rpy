## 第三章，以及合并后的第四章。跑货，然后挫挫又折折。

label chapter3:
    $ mark_stage("chapter3")
    scene hist_carriage at slow_push
    with fade
    play music "audio/chapter3_daylight.ogg" fadein 2.0 loop
    play sound "audio/chapter.wav"

    call chapter_card("第三章", "深圳没有黄金", "1986—1987，长途车和供销社") from _call_chapter_card_3

    n "招牌挂上以后，订单没有自己走进门。陈海生买了两张长途汽车票，纸箱用麻绳捆在车顶。"
    n "红卫坐在过道的箱子上。箱子里是第一批打着春声牌子的收音机，外壳还带着车间的机油味。"
    c "江西那边的供销社认货，不认人。到了就拆给他看。"

    scene hist_street at slow_push
    with dissolve
    n "车过韶关的时候下了暴雨。篷布被风掀起一角，纸箱的牛皮纸湿了一片。"

    $ mark_beat("rain")
    menu:
        "停车擦干，到了跟买主说清楚。":
            $ flag_rain = 1
            $ change_stats(rep=4, thought=3, money=-2)
            n "他们在路边茶棚把受潮的三台挑出来，用干布擦喇叭网。买主听完，只退了那三台。"
            c "少赚一点。可他下回还肯见我们。"

        "把篷布钉死，当没淋过。":
            $ flag_rain = 2
            $ change_stats(money=3, rep=-4, thought=-3)
            $ flag_profit = True
            n "箱子原样卸下来。三天后有一台开不了机。买主的信比货到得还快。"
            s "潮气进了线圈。这种事，瞒得过秤，瞒不过开机。"

    scene hist_market at slow_push
    with fade
    n "县城供销社的院子里堆着化肥。主任用搪瓷缸敲了敲桌沿，缸底还沾着茶叶。"
    n "他要四十台。钱等秋收以后，粮站把款拨下来再结。"
    c "四十台。我们垫得起零件，垫不起三个月的伙食。"

    $ mark_beat("credit")
    menu:
        "先收一半订金，剩下的秋后再结。":
            $ flag_credit = 1
            $ change_stats(money=4, rep=3, thought=2)
            n "主任算了半天，还是把一半款子点给了他。另一半写在复写纸的第二联上。"
            l "没有订金，这批货我不敢开工。"

        "全赊。先把春声的名字送进这个县。":
            $ flag_credit = 2
            $ change_stats(rep=5, money=-6, thought=1)
            n "四十台拉进了库房。红卫回家的路上一直在算，秋天要是收成不好，这批货就压在别人的账上。"
            s "名字送进去了。钱还在别人抽屉里。"

        "不赊。宁可不做这笔。":
            $ flag_credit = 3
            $ change_stats(money=2, rep=-2, thought=2)
            n "主任把缸子放下，没送他们出门。陈海生在车上骂了一路，又说骂完还是觉得他做得对。"

    scene hist_factory at slow_push
    with fade
    n "活多起来以后，梁师傅从老乡里找了两个学徒。一个手稳。另一个叫阿国，第一周就把一块线路板烫穿了。"
    liang "板子不贵。人要是赶回去，这口锅就没人刷了。"
    s "烫穿一次不可怕。怕的是他下次还觉得自己会了。"

    $ mark_beat("apprentice")
    menu:
        "留下。让他当着大家把线圈重绕十遍。":
            $ flag_apprentice = 1
            $ change_stats(tech=4, rep=2, thought=2)
            n "阿国绕到第七遍，手指起了泡。第八遍，匝数终于对上。梁师傅把那块废板钉在门口。"
            liang "看着。谁再烫穿，就对着这块板吃饭。"

        "送回老家。作坊养不起第二次。":
            $ flag_apprentice = 2
            $ change_stats(money=2, rep=-3, thought=-2)
            n "阿国把铺盖卷走的时候没回头。门口那块烫穿的板子，后来也被人垫了桌腿。"
            s "人走了，教训要是也走了，下回还是会烫穿。"

    scene hist_abacus at slow_push
    with dissolve
    n "月底，苏文静把一张旧挂历翻过来。正面是年画，背面是这个月的账：零件、焊锡、房租、陈海生的路费。"
    n "路费那一栏是空的。陈海生说，请客的钱不好写。"
    c "不请客，货出不去。写上去，像我贪了。"

    $ mark_beat("books")
    menu:
        "把数字念出来，四个人一起听。":
            $ flag_books = 1
            $ change_stats(rep=4, thought=4, family=1)
            n "红卫念得很慢。请客写上了，写成“推销”。陈海生耳朵红了，没辩。"
            s "账在桌上，人就还坐在一张桌上。"

        "销售的账先不公开。":
            $ flag_books = 2
            $ change_stats(money=2, rep=-3, thought=-2)
            n "挂历只给苏文静和红卫看。梁师傅问了一句这个月结余，没有人接。"
            liang "不知道剩多少，我不好跟学徒说下个月还有没有工。"

    scene hist_street at slow_push
    with fade
    n "第一笔货款到的那天，夜市的灯都亮了。有人喊他孙老板。红卫在口袋里捏着那叠还没暖热的票子。"

    $ mark_beat("noodle")
    menu:
        "请大家吃面。老板这个称呼，得先请得起一碗面。":
            $ flag_noodle = 1
            $ change_stats(money=-2, rep=3, family=2, thought=1)
            n "四碗阳春面。阿国要是还在，就是五碗。陈海生吸溜着面条说，这比请客烟便宜，也比请客烟干净。"

        "票子进铁盒。面明天再说。":
            $ flag_noodle = 2
            $ change_stats(money=3, thought=2)
            n "铁盒锁上的时候，夜市的汤味还飘进窗缝。没有人抱怨。也没有人再喊一声孙老板。"

    n "一九八七年开春，挂历背面已经写满了。订单从江西又伸到了邻县。屋顶还是漏，接水的盆换了一只更大的。"

    $ finish_stage("chapter3")
    jump chapter4


label chapter4:
    $ mark_stage("chapter4")
    scene hist_factory at slow_push
    with fade
    play music "audio/chapter4_ocean.ogg" fadein 2.0 loop
    play sound "audio/chapter.wav"

    call chapter_card("第四章", "挫挫又折折", "1987—1991，从牌子到街口") from _call_chapter_card_4

    n "百货公司的采购员把样品翻来覆去，手指在商标上停住。"
    n "他要二百台。条件是拨盘上不能有春声，改贴他们商场的牌子。箱子也换。"
    c "二百台。够我们干两个月。名字又不能当饭。"
    s "名字要是能揭掉，下回谁还记得是谁修的。"

    $ mark_beat("oem")
    menu:
        "接。先活下来，名字以后再说。":
            $ flag_oem = 1
            $ change_stats(money=8, rep=-4, thought=-3)
            $ flag_profit = True
            n "贴纸盖住了春声两个字。红卫贴到最后一台，手指上全是胶水。"
            l "箱子上是他们的。机器里，我还是知道是我们的。"

        "不接。拨盘上必须是春声。":
            $ flag_oem = 2
            $ change_stats(rep=6, thought=4, money=-3)
            n "采购员把样品放下，说再看看别家。门关上以后，作坊里安静了很久。"
            s "二百台没了。名字还在。"

        "箱子用他们的，机器里面留一张春声的保修卡。":
            $ flag_oem = 3
            $ change_stats(money=4, rep=3, thought=3)
            n "采购员想了想，答应了。保修卡比邮票大一圈。坏了，人还是会找到这条街。"
            liang "找得到人，就还有下一次。"

    $ mark_beat("power")
    n "刚把这批货排上桌，电就停了。对门国营厂的灯还亮着。红卫想托关系，私接一根线。"

    menu:
        "偷偷接电，先把货赶出来。":
            $ change_stats(money=5, rep=-10, tech=-5, thought=-10)
            $ flag_steal_power = True
            $ flag_profit = True

            n "线接上了，货赶出来了。苏文静站在门口看了他很久。"
            s "你今天敢偷电，明天就敢偷工减料。"

        "听苏文静的，点煤油灯查线路。":
            $ change_stats(rep=5, tech=5, thought=5)
            $ flag_steal_power = False

            n "全作坊就着煤油灯，把每台机器的线路重新捋了一遍。来电后再逐台通电。"

    n "发工资的周五，铁盒比上周轻。焊锡的账还欠着，学徒已经在门口等。"

    $ mark_beat("payday")
    menu:
        "先把工钱发足。焊锡的账下周再说。":
            $ flag_payday = 1
            $ change_stats(rep=5, family=2, money=-4, thought=2)
            n "票子一张张数到每个人手里。焊锡店的人下午来过，红卫让他坐，倒了杯茶，没给钱。"
            liang "茶可以欠。工钱欠了，人明天就不来了。"

        "先发一半，周一补齐。":
            $ flag_payday = 2
            $ change_stats(money=-1, rep=-1, thought=-1)
            n "一半工钱在手里，像一句还没说完的话。周一的钱后来是补上了，可那三天谁都没怎么说话。"

        "先结焊锡。工钱等这批货的款。":
            $ flag_payday = 3
            $ change_stats(money=2, rep=-5, thought=-3)
            $ flag_profit = True
            n "焊锡店的人走的时候笑了。学徒把工具放下，说家里等着米。红卫答应了，自己先去夜市修了两台别人的收音机。"

    $ mark_beat("qc")
    n "第一批出厂前，苏文静要编号质检。陈海生要先出货。"

    menu:
        "执行编号质检。":
            $ change_stats(money=-3, rep=5, tech=5, thought=3)
            $ flag_qc = True

            n "每台贴编号，逐台测试。出货慢了三天，返修率低得让陈海生闭了嘴。"

        "先赶工出货，边卖边修。":
            $ change_stats(money=5, rep=-3, tech=-3, thought=-3)
            $ flag_qc = False
            $ flag_profit = True

            n "货先发出去。钱回来得快，退货也跟着回来。"

    $ mark_beat("listen")
    n "出货前的夜里，三台样机并排响着。苏文静说，有一台声音发闷。"
    menu:
        "坐下来，把那台听出来。":
            $ task_begin_listen()
            call screen task_listen
            if _return == "ok":
                $ flag_listen = 1
                $ change_stats(rep=4, tech=4, thought=2)
                n "发闷的那台被他扣下，没混进货里。苏文静看了他一眼，没说话。"
            else:
                $ flag_listen = 2
                $ change_stats(rep=-2, tech=1)
                n "他听岔了。坏的跟着好的走了，退货里后来有它。"

        "三台一起装箱。":
            $ flag_listen = 3
            $ change_stats(thought=-2)
            n "他没停下来听。箱子合上的时候，三台还在响。"

    scene hist_abacus at slow_push
    with dissolve
    n "街道的会计找上门，怀里夹着一本个体户登记的说明。登记要费用，要房租证明，还要把春声两个字写进公章旁边。"
    n "不登记也能做。查到了，就是另一笔钱。"

    $ mark_beat("license")
    menu:
        "按真实地址登记。费用从铁盒里出。":
            $ flag_license = 1
            $ change_stats(money=-4, rep=5, thought=4)
            n "公章盖下去的时候，墨有点淡。会计说淡一点也算数。红卫把那张纸压在玻璃板下面。"
            s "有这张纸，退货的人至少知道该找谁。"

        "先借亲戚的摊位执照顶着。":
            $ flag_license = 2
            $ change_stats(money=-1, rep=-2, thought=-2)
            n "亲戚的名字写在前面。春声还是他们的，出了事情却要先解释半天这是谁的摊。"

        "先不登记。等做大了再说。":
            $ flag_license = 3
            $ change_stats(money=2, thought=-3, rep=-3)
            $ flag_profit = True
            n "会计把说明收回去，说门随时开着。红卫送他到巷口，回来把铁盒又数了一遍。"

    n "这年秋天，邻县的广播站用他们的机器放天气预报。声音大，有一点噪。红卫站在别人的屋檐下听完了全程。"
    l "是我们的。噪点在第三档，我听得出来。"

    scene hist_factory at slow_push
    with fade

    n "一九八八年，作坊第一次觉得自己站稳了。门口停着别人的自行车，红卫看上了一辆二手摩托车，说跑县里不用再求货车。"
    n "同一周，家里来信。小岗的屋顶该翻了。信纸很短，短得像不好意思开口。"

    $ mark_beat("bike")
    menu:
        "买下车。货要自己送，才不用看别人的脸色。":
            $ flag_bike = 1
            $ change_stats(money=-6, tech=1, thought=-1)
            n "油门一拧，巷子里的人都回头。梁师傅说，架子有了，别让架子先于货。"
            l "我不是摆架子。我是不想再把纸箱放在别人的车顶上淋雨。"

        "钱寄回凤阳。屋顶比摩托车急。":
            $ flag_bike = 2
            $ change_stats(money=-5, family=6, thought=4)
            n "汇款单上他只写了四个字：先把屋补上。摩托车还在店里。第二天他照旧去挤长途车。"
            f "钱收到了。屋补了。你自己呢。"

    scene bg_crisis at slow_push
    with fade
    n "订单多了，“孙老板”的称呼也多了。赵万金请他吃饭，圆桌上的酒瓶排成一圈。"
    z "都是自己人。电容我有一批，价格你出去问，问不到这么低。"
    n "苏文静没入席。她在作坊里等，等他回来把样品放下。"
    s "便宜到这个地步，要么是他亏，要么是货亏。他不会亏。"

    n "为了再压一点价，也为了江西那张大单，红卫把样品带了回来。"

    $ mark_beat("caps")
    menu:
        "先抽检，再装机。":
            $ change_stats(money=-3, rep=5, tech=5, thought=5)
            $ flag_bad_cap = False

            n "一抽，果然有问题。货退了回去，躲过一场大祸。赵万金从此记恨上他。"

        "先装机，赶订单。":
            $ change_stats(money=5, rep=-5, tech=-10, thought=-5)
            $ flag_bad_cap = True
            $ flag_profit = True

            n "工人直接装机。货发出去的时候，红卫以为这次又赌赢了。"

    n "货发出去不久，收音机过热。一台在供销社仓库冒烟。火扑灭了，人没伤。整批退回，货款停付，工资要发不出。"
    n "苏文静拆开故障机：电容是假货。进货单上签着红卫的名字。"

    if flag_qc:
        n "每台都贴了工人编号，他们很快查清了问题批次。"
    else:
        n "没有编号，连问题出在哪一批都说不清。作坊里一片死寂。"

    $ mark_beat("accident")
    menu:
        "隐瞒出货，把责任推给仓储。":
            $ change_stats(money=5, rep=-20, tech=-5, thought=-15)
            $ flag_hide = True
            $ flag_accident_decided = True
            $ flag_downfall = True
            $ flag_profit = True

            n "他调货继续发，把责任推给仓储。局面稳住了一阵。雷埋得更深了。"

        "找赵万金做灰色生意，用快钱填窟窿。":
            $ change_stats(money=15, rep=-25, tech=-5, thought=-20)
            $ flag_gray = True
            $ flag_accident_decided = True
            $ flag_downfall = True
            $ flag_profit = True

            n "灰色生意来钱快，窟窿暂时补上了。他的脚也踩进了泥里。"

        "全面召回，承担赔偿。":
            $ change_stats(money=-20, rep=20, tech=5, thought=15)
            $ flag_recall = True
            $ flag_accident_decided = True

            n "该赔的赔，该退的退。资金链断了，作坊撑不下去。信誉还留着最后一点。"
            j "你这人，还不算烂透。"

    if flag_downfall:
        jump downfall_route

    n "春声作坊还是倒了。陈海生抽走最后一点货款。苏文静父亲病重，回上海前把图纸留下。梁师傅另谋生路。"

    if flag_bike == 1:
        n "电报来了：父亲干活摔断了腿。红卫卖了摩托车和手表，连债务的零头都不够。"
    else:
        n "电报来了：父亲干活摔断了腿。红卫卖了手表和最后一箱零件，连债务的零头都不够。"

    $ mark_beat("leg")
    menu:
        "回凤阳，先给父亲治腿。":
            $ change_stats(money=-5, family=15, thought=5)
            $ flag_father_home = True

            n "红卫连夜赶回。父亲躺在炕上，第一句话是："
            f "厂子呢？"
            n "红卫没说话，把药费放在炕头。"

        "留在深圳，先挣钱。":
            $ change_stats(money=5, family=-15, thought=-5)
            $ flag_father_home = False

            n "他把电报折好，塞进口袋。有些腿伤，等不了。"

    if flag_wu:
        n "邮局送来汇款单和一包挂面、布鞋。附言写着：小岗村老少爷们凑的，先给叔治病。"
        n "是吴国强回村后，把火车上的事说了个遍。红卫一直以为自己一个人在闯。身后站着整个小岗村。"
    else:
        n "汇款单没有来。梁师傅塞来一个信封，大伯托人捎来卖猪的钱：先给你爹治腿。他欠的，不只是钱。"

    scene bg_stall at slow_push
    with fade

    n "他回到最初那个街口，挂上“彪子电器维修”。再也没人叫他孙老板。"
    n "一九九零年，日子变成一台一台的收音机。学校的广播坏了，老师把喇叭抱到摊上，说升旗要响。"
    n "也有人把旧机壳打磨一新，问他能不能当新货出手。差价够他半个月的债。"

    $ mark_beat("refurb")
    menu:
        "学校的喇叭免费修。旧机壳不当新的卖。":
            $ flag_refurb = 1
            $ change_stats(rep=5, thought=4, money=-2)
            n "升旗的早上他去听了。喇叭有一点破音，国歌还是完整的。那箱打磨过的旧壳，他让人拉走了。"
            liang "债可以慢。这行的名，慢不得。"

        "旧壳翻新，先把这个月的债顶上。":
            $ flag_refurb = 2
            $ change_stats(money=5, rep=-4, thought=-3)
            $ flag_profit = True
            n "壳是新的，里面还是旧线圈。买的人高兴了一阵。半个月后，其中一台又回到了这个摊上。"
            n "红卫没说话，只把后盖打开。他认得自己当年的焊点。"

    n "一九九一年冬天，债本比去年薄了一点。薄得不多。梁师傅有时晚上还来坐，两个人看一阵过路的车，就不说话。"
    n "红卫把春声的保修卡压在玻璃板最底下。字已经淡了。他还是没扔。"

    $ finish_stage("chapter4")
    jump chapter6
