## 红卫的春天 — characters, stats, flags, transforms

define n = Character(None, what_color="#2B2420")
define l = Character("孙红卫", who_color="#F3E7D3")
define f = Character("孙守成", who_color="#F3E7D3")
define u = Character("孙守义", who_color="#F3E7D3")
define m = Character("周桂兰", who_color="#F3E7D3")
define s = Character("苏文静", who_color="#F3E7D3")
define c = Character("陈海生", who_color="#F3E7D3")
define w = Character("吴国强", who_color="#F3E7D3")
define liang = Character("梁师傅", who_color="#F3E7D3")
define z = Character("赵万金", who_color="#F3E7D3")
define j = Character("江西经销商", who_color="#F3E7D3")
define old = Character("老工人", who_color="#F3E7D3")
define zhang = Character("张长喜", who_color="#F3E7D3")
define nv = Character("年轻女工", who_color="#F3E7D3")

define portrait_map = {
    "孙红卫": "portrait_lin",
    "孙守成": "portrait_father",
    "孙守义": "portrait_uncle",
    "周桂兰": "portrait_mother",
    "苏文静": "portrait_su",
    "陈海生": "portrait_chen",
    "吴国强": "portrait_wu",
    "梁师傅": "portrait_liang",
    "赵万金": "portrait_zhao",
    "江西经销商": "portrait_dealer",
    "老工人": "portrait_old",
    "张长喜": "portrait_zhang",
    "年轻女工": "portrait_nv",
}

define people_book = (
    ("孙红卫", "portrait_lin", "小岗村出来的学徒，后来把春声撑起来。"),
    ("孙守成", "portrait_father", "红卫的父亲，人在外面干活。"),
    ("孙守义", "portrait_uncle", "红卫的叔叔，守着村里的手艺。"),
    ("周桂兰", "portrait_mother", "红卫的母亲，家里的事都从她嘴里过。"),
    ("苏文静", "portrait_su", "和红卫一起摆弄收音机的姑娘。"),
    ("陈海生", "portrait_chen", "市场里算账算得很快的人。"),
    ("吴国强", "portrait_wu", "手里有路子，也开得出条件。"),
    ("梁师傅", "portrait_liang", "作坊里带过红卫的老师傅。"),
    ("赵万金", "portrait_zhao", "城里做买卖的，眼睛盯着货。"),
    ("江西经销商", "portrait_dealer", "从江西过来收货的人。"),
    ("老工人", "portrait_old", "厂里干了多年的老师傅。"),
    ("张长喜", "portrait_zhang", "村里管章子的干部。"),
    ("年轻女工", "portrait_nv", "车间里的年轻女工。"),
)

define ending_catalog = [
    ("E1", "春声归乡", "正向，共同富裕"),
    ("E2", "质造立身", "正向，实业报国"),
    ("E3", "薪火基层", "正向，技能兴乡"),
    ("E4", "安稳立足", "中性，平凡坚守"),
    ("E5", "道分两路", "中性，各自求索"),
    ("E6", "失信落败", "警示，黯然离场"),
    ("E7", "故步自封", "警示，困守一隅"),
    ("E8", "潮头回声", "隐藏，精神传承"),
    ("E0", "红卫的春天", "普通结局"),
]

default money = 50
default rep = 50
default tech = 30
default family = 40
default thought = 30
default stat_pulse = {"money": 0, "rep": 0, "tech": 0, "family": 0, "thought": 0}

default flag_seal_active = False
default flag_wu = False
default flag_call_father = False
default flag_su_tools = False
default flag_old_radio = False
default flag_watch = 0          # 0 直接售卖 / 1 降价说明 / 2 逐台维修
default flag_invoice = False
default flag_steal_power = False
default flag_qc = False
default flag_bad_cap = False
default flag_recall = False
default flag_hide = False
default flag_gray = False
default flag_downfall = False
default flag_father_home = False
default flag_tour = 0           # 0 回避 / 1 完整 / 2 边缘
default flag_restart = False
default flag_ten = False
default flag_su_return = False
default flag_su_break = False
default flag_debt = False
default flag_fengyang = False
default flag_father_reconcile = False
default flag_legacy = False
default flag_profit = False
default flag_wu_decided = False
default flag_watch_decided = False
default flag_accident_decided = False
default flag_tour_decided = False
default flag_end_decided = False
default flag_bonus_applied = False
default flag_torch = 0
default flag_circuit = 0
default flag_date = 0
default flag_crown = 0
default flag_listen = 0
default flag_wage = 0
default flag_wire = 0
default flag_paper = 0
default flag_board = 0
default flag_solder_task = 0
default flag_sort = 0
default flag_note = 0
default flag_sign = 0
default flag_rain = 0
default flag_credit = 0
default flag_apprentice = 0
default flag_books = 0
default flag_noodle = 0
default flag_oem = 0
default flag_payday = 0
default flag_license = 0
default flag_bike = 0
default flag_refurb = 0
default story_mark = ""
default seen_stages = []
default done_stages = []
default seen_beats = []
default story_beat = ""
default met_people = []


init python:
    import math

    if persistent.endings is None:
        persistent.endings = []

    renpy.music.register_channel("talk", mixer="music", loop=False)
    renpy.music.register_channel("horn", mixer="music", loop=False)

    if "stat_strip" not in config.always_shown_screens:
        config.always_shown_screens.append("stat_strip")

    def remember_person(event, who_name, interact=True, **kwargs):
        if event != "begin" or not who_name:
            return
        if who_name not in store.met_people:
            store.met_people.append(who_name)

    def _bind_memory(who_name):
        def _cb(event, interact=True, **kwargs):
            remember_person(event, who_name, interact=interact, **kwargs)
        return _cb

    for _speaker in (l, f, u, m, s, c, w, liang, z, j, old, zhang, nv):
        if _speaker.name:
            _speaker.callback = _bind_memory(_speaker.name)

    def clamp(v):
        return max(0, min(100, int(v)))

    def reset_game():
        store.money = 50
        store.rep = 50
        store.tech = 30
        store.family = 40
        store.thought = 30
        for name in [
            "flag_seal_active", "flag_wu", "flag_call_father", "flag_su_tools",
            "flag_old_radio", "flag_invoice", "flag_steal_power", "flag_qc",
            "flag_bad_cap", "flag_recall", "flag_hide", "flag_gray", "flag_downfall",
            "flag_father_home", "flag_restart", "flag_ten", "flag_su_return",
            "flag_su_break", "flag_debt", "flag_fengyang", "flag_father_reconcile",
            "flag_legacy", "flag_profit", "flag_wu_decided", "flag_watch_decided",
            "flag_accident_decided", "flag_tour_decided", "flag_end_decided",
            "flag_bonus_applied",
        ]:
            setattr(store, name, False)
        store.flag_watch = 0
        store.flag_tour = 0
        for name in (
            "flag_torch", "flag_circuit", "flag_date", "flag_crown", "flag_listen",
            "flag_wage", "flag_wire", "flag_paper", "flag_board", "flag_solder_task",
            "flag_sort", "flag_note", "flag_sign", "flag_rain", "flag_credit",
            "flag_apprentice", "flag_books", "flag_noodle", "flag_oem", "flag_payday",
            "flag_license", "flag_bike", "flag_refurb",
        ):
            setattr(store, name, 0)
        store.story_mark = ""
        store.seen_stages = []
        store.done_stages = []
        store.seen_beats = []
        store.story_beat = ""
        store.met_people = []
        store.stat_pulse = {"money": 0, "rep": 0, "tech": 0, "family": 0, "thought": 0}

    def clear_stat_pulse():
        store.stat_pulse = {"money": 0, "rep": 0, "tech": 0, "family": 0, "thought": 0}

    def money_blurb():
        if store.money < 35:
            return "路费经不起再送出去。"
        if store.money >= 70:
            return "手头松了一些。"
        return "钱刚够周转。"

    def rep_blurb():
        if store.rep < 40:
            return "有人见了你会绕开。"
        if store.rep >= 75:
            return "别人愿意把货交给你。"
        return "名声还谈不上好坏。"

    def tech_blurb():
        if store.tech < 40:
            return "不少毛病，还是在碰运气。"
        if store.tech >= 70:
            return "线路看得懂了。"
        return "开始知道毛病出在哪。"

    def family_blurb():
        if store.family < 40:
            return "家里的信越来越短。"
        if store.family >= 70:
            return "家里那头，还愿意等他。"
        return "亲情绷着，没有断。"

    def thought_blurb():
        if store.thought >= 60:
            return "你知道自己为什么出发，也知道要守住什么。"
        if store.thought >= 45:
            return "你开始看清方向，但偶尔还会被快钱晃眼。"
        return "你还在往前闯，却不太敢停下来问为什么。"

    def stat_conflict():
        return store.money >= 60 and store.rep <= 42

    PLOT_NODES = [
        ("south", "第一章", "从小岗到深圳", "1978—1985"),
        ("spring", "第二章", "春声作坊", "1985—1986"),
        ("chapter3", "第三章", "深圳没有黄金", "1986—1987"),
        ("chapter4", "第四章", "挫挫又折折", "1987—1991"),
        ("chapter6", "第五章", "一九九二年的冬天", "1992，国贸"),
        ("chapter7", "第六章", "卷土重来", "1992—1995"),
        ("ending", "终局", "按现在的选择结算", "看到结局"),
    ]

    PLOT_JUMP = {
        "south": "prologue",
        "spring": "spring",
        "chapter3": "chapter3",
        "chapter4": "chapter4",
        "chapter6": "chapter6",
        "chapter7": "chapter7",
        "ending": "ending_router",
    }

    PLOT_CLEAR = {
        "south": ["flag_seal_active", "flag_call_father", "flag_wu", "flag_wu_decided", "flag_su_tools", "flag_old_radio", "flag_torch", "flag_circuit"],
        "spring": ["flag_invoice", "flag_watch_decided", "flag_date", "flag_crown", "flag_sign"],
        "chapter3": ["flag_rain", "flag_credit", "flag_apprentice", "flag_books", "flag_noodle"],
        "chapter4": ["flag_oem", "flag_steal_power", "flag_payday", "flag_qc", "flag_listen", "flag_license", "flag_bike", "flag_bad_cap", "flag_recall", "flag_hide", "flag_gray", "flag_downfall", "flag_father_home", "flag_accident_decided", "flag_refurb"],
        "chapter6": ["flag_tour_decided", "flag_restart", "flag_wage", "flag_wire", "flag_paper", "flag_board"],
        "chapter7": ["flag_ten", "flag_su_return", "flag_su_break", "flag_debt", "flag_fengyang", "flag_father_reconcile", "flag_legacy", "flag_end_decided", "flag_solder_task", "flag_sort", "flag_note"],
        "ending": [],
    }

    def plot_ids():
        return [node[0] for node in PLOT_NODES]

    def stage_index(nid):
        if nid == "chapter5":
            nid = "chapter4"
        ids = plot_ids()
        if nid in ids:
            return ids.index(nid)
        return 0

    def plot_here():
        mark = store.story_mark
        if mark == "chapter5":
            mark = "chapter4"
        if mark in plot_ids():
            return mark
        if store.flag_end_decided or store.flag_ten or store.flag_debt or store.flag_su_return or store.flag_su_break:
            return "chapter7"
        if store.flag_tour_decided or store.flag_restart:
            return "chapter6"
        if (store.flag_accident_decided or store.flag_father_home or store.flag_bad_cap
                or store.flag_downfall or store.flag_bike or store.flag_refurb):
            return "chapter4"
        if (store.flag_steal_power or store.flag_qc or store.flag_oem or store.flag_payday
                or store.flag_license or store.flag_listen):
            return "chapter4"
        if (store.flag_rain or store.flag_credit or store.flag_apprentice
                or store.flag_books or store.flag_noodle):
            return "chapter3"
        if (store.flag_watch_decided or store.flag_invoice or store.flag_sign
                or store.flag_date or store.flag_crown):
            return "spring"
        if store.flag_wu_decided or store.flag_call_father or store.flag_su_tools or store.flag_old_radio:
            return "south"
        return "south"

    def mark_stage(nid):
        store.story_mark = nid
        if nid not in store.seen_stages:
            store.seen_stages = list(store.seen_stages) + [nid]

    def finish_stage(nid):
        if nid not in store.done_stages:
            store.done_stages = list(store.done_stages) + [nid]

    CHAPTER_BEATS = (
        ("south", "seal", "堂屋红手印"),
        ("south", "torch", "王婶的手电"),
        ("south", "father", "村口，叫不叫爹"),
        ("south", "circuit", "报纸上的电路"),
        ("south", "wu", "吴国强的路费"),
        ("south", "tools", "接不接那套工具"),
        ("south", "radio", "老收音机"),
        ("spring", "invoice", "给父亲的收音机"),
        ("spring", "date", "日期不对的进货单"),
        ("spring", "watch", "电子表"),
        ("spring", "crown", "校一只表"),
        ("spring", "sign", "租金交几个月"),
        ("chapter3", "rain", "淋雨的纸箱"),
        ("chapter3", "credit", "供销社的赊账"),
        ("chapter3", "apprentice", "烫穿线路板的学徒"),
        ("chapter3", "books", "挂历背面的账"),
        ("chapter3", "noodle", "第一声孙老板"),
        ("chapter4", "oem", "拨盘上的名字"),
        ("chapter4", "power", "停电那一夜"),
        ("chapter4", "payday", "周五的工钱"),
        ("chapter4", "qc", "要不要质检"),
        ("chapter4", "listen", "听出那台发闷的"),
        ("chapter4", "license", "个体户登记"),
        ("chapter4", "bike", "摩托车还是屋顶"),
        ("chapter4", "caps", "电容，抽不抽检"),
        ("chapter4", "accident", "事故怎么收场"),
        ("chapter4", "leg", "父亲的腿"),
        ("chapter4", "refurb", "旧壳当不当新的"),
        ("chapter6", "stall", "维修摊还债"),
        ("chapter6", "wage", "国贸的工钱"),
        ("chapter6", "tour", "去不去国贸"),
        ("chapter6", "wire", "国贸这排灯"),
        ("chapter6", "paper", "报纸上圈三句"),
        ("chapter6", "speech", "南方谈话"),
        ("chapter6", "board", "抄不抄在挡板上"),
        ("chapter7", "restart", "卷土重来"),
        ("chapter7", "note", "箱盖上的字"),
        ("chapter7", "ten", "先做十台，还是一百台"),
        ("chapter7", "weld", "四个焊点"),
        ("chapter7", "su", "苏文静的条件"),
        ("chapter7", "debt", "债怎么还"),
        ("chapter7", "home", "回凤阳，还是留深圳"),
        ("chapter7", "sort", "把电容分开"),
    )

    def mark_beat(bid):
        store.story_beat = bid
        if bid not in store.seen_beats:
            store.seen_beats = list(store.seen_beats) + [bid]

    def beats_of(nid):
        return [(bid, title) for stage, bid, title in CHAPTER_BEATS if stage == nid]

    def beat_stage(bid):
        for stage, name, _title in CHAPTER_BEATS:
            if name == bid:
                return stage
        return "south"

    FORKS = {
        "south": [
            ("seal", "堂屋红手印", "一九七八年冬，小岗村偷偷按手印。红卫盖了个红印，大伯折回来看见了。", (
                ("admit", "承认", "大伯把印泥盒交给他：总得有人先走一步。"),
                ("deny", "不承认", "大伯没拆穿。不认，事情也发生过。"),
            )),
            ("torch", "王婶的手电", "村里的手电坏了。王婶把那只不亮的放在桌上。", (
                ("ok", "今晚修好", "电池推进去，开关一按，光打在土墙上。"),
                ("fail", "没装上", "光闪了两下又灭。他说明天再来。"),
                ("skip", "明天再说", "手电在桌上躺了一夜。"),
            )),
            ("father", "村口", "卖猪凑了路费。父亲打了他，却只送到院门口。", (
                ("call", "回去叫一声爹", "亲情够的话，父亲让他把棉袄穿好。"),
                ("quiet", "沉默着离开", "身后没有人再叫他。"),
            )),
            ("circuit", "报纸上的电路", "苏文静在报纸边角画了张收音机电路。", (
                ("ok", "把顺序走完", "电源、电阻、电容、喇叭。他点了喇叭，图活了。"),
                ("fail", "没走完", "顺序断了。他把报纸折好，先下车。"),
                ("skip", "先收着", "图塞进棉袄最里面，车上没看。"),
            )),
            ("wu", "吴国强的路费", "火车上，老乡的介绍费被骗光，连车票都不够。", (
                ("help", "资助", "五元、零钱，或记到深圳再补。他记下了这份情。"),
                ("none", "不资助", "吴国强下一站下了车。"),
            )),
            ("tools", "一套工具", "深圳没有黄金。他用铁丝接上扩音器，苏文静递来工具。", (
                ("take", "接过", "有了第一套自己的电工工具。"),
                ("refuse", "怕欠人情", "她把工具收回去：那你就继续用铁丝。"),
            )),
            ("radio", "老收音机", "老工人的收音机是儿子留下的。他装错电阻，烧了线圈。", (
                ("fix", "修到响", "天亮时广播响了。修的是机器，也是念想。"),
                ("new", "赔一台新的", "老人收了，再没来过。新的替不了旧的。"),
            )),
        ],
        "spring": [
            ("invoice", "父亲的收音机", "第一次回凤阳。父亲问：有发票吗？坏了的，你也卖吗？", (
                ("explain", "追进去解释", "挣钱可以。别挣半夜睡不着的钱。"),
                ("leave", "赌气离开", "那顿饭，谁也没吃好。"),
            )),
            ("date", "日期不对的进货单", "陈海生塞来一张日期早了一天的单子，说税好算。", (
                ("keep", "不改", "日期是哪天，就写哪天。"),
                ("forge", "改前一天", "字改了。那张单子，他没敢给父亲看。"),
            )),
            ("watch", "电子表", "低价收来的表，近三分之一走时不准。", (
                ("sell", "直接卖", "钱来得快。江西商人上过当，再不回头。"),
                ("tell", "降价说清楚", "手艺不够就先挑出停走的。守住了没把坏的当好的卖。"),
                ("cal", "逐台校准", "返修率最低。江西签下一年的货。"),
            )),
            ("crown", "校一只表", "桌上还剩一只走得飞快的。", (
                ("ok", "调到准", "误差归零，他才合盖。这只留给了自己。"),
                ("fail", "没对准", "合早了。表还是快，进了次品箱。"),
                ("skip", "塞进次品箱", "没动旋钮。"),
            )),
            ("sign", "租金", "招牌还没干。房东等这个月的钱。", (
                ("hold", "先交三个月", "屋是漏的，门锁是自己的。"),
                ("stock", "先拿去进货", "下个月不一定还是这把锁。"),
            )),
        ],
        "chapter3": [
            ("rain", "淋雨的纸箱", "车过韶关，篷布被风掀开。", (
                ("dry", "擦干并说明", "只退了受潮的三台。买主下回还肯见。"),
                ("shut", "钉死当没淋", "三天后有一台开不了机。"),
            )),
            ("credit", "供销社赊账", "四十台。钱等秋收以后再结。", (
                ("half", "先收一半", "另一半写在复写纸的第二联。"),
                ("credit", "全赊", "名字送进了县里。钱还在别人抽屉里。"),
                ("no", "不赊", "这笔不做。陈海生骂了一路。"),
            )),
            ("apprentice", "烫穿的板子", "学徒阿国第一周烫穿了一块线路板。", (
                ("keep", "留下重绕", "废板钉在门口。下回对着它吃饭。"),
                ("send", "送回老家", "人走了。教训要是也走了，下回还会烫穿。"),
            )),
            ("books", "挂历背面的账", "路费那一栏是空的。陈海生说请客不好写。", (
                ("open", "念给四个人听", "请客写成推销。账在桌上，人还坐一张桌。"),
                ("hide", "销售账不公开", "梁师傅问结余，没有人接。"),
            )),
            ("noodle", "孙老板", "第一笔货款到了。夜市有人这么喊他。", (
                ("treat", "请大家吃面", "四碗阳春面。称呼先请得起一碗面。"),
                ("save", "票子进铁盒", "没有人再喊一声孙老板。"),
            )),
        ],
        "chapter4": [
            ("oem", "拨盘上的名字", "百货公司要二百台，条件是不能有春声。", (
                ("cover", "贴纸盖住", "箱子是他们的。机器里他还认得。"),
                ("keep", "必须是春声", "二百台没了。名字还在。"),
                ("card", "里面留保修卡", "坏了，人还是会找到这条街。"),
            )),
            ("power", "停电", "作坊刚把货排上桌就停电。国营厂的灯还亮着。", (
                ("steal", "偷偷接电", "货赶出来了。苏文静说：今天偷电，明天就敢偷工减料。"),
                ("lamp", "煤油灯查线路", "来电后再逐台通电。"),
            )),
            ("payday", "周五的工钱", "铁盒比上周轻。学徒在门口等。", (
                ("full", "工钱发足", "焊锡可以欠。工钱欠了，人明天不来。"),
                ("half", "先发一半", "像一句没说完的话。"),
                ("tin", "先结焊锡", "学徒家里等着米。"),
            )),
            ("qc", "质检", "第一批出厂。苏文静要编号，陈海生要先出货。", (
                ("check", "编号质检", "慢了三天，返修率压下去了。"),
                ("rush", "先出货", "钱回来得快，退货也跟着回来。"),
            )),
            ("listen", "听出那台发闷的", "出货前夜里，三台样机并排响着。", (
                ("ok", "扣下那台", "发闷的没混进货里。"),
                ("fail", "听岔了", "坏的跟着好的走了。退货里有它。"),
                ("skip", "三台一起装箱", "他没停下来听。"),
            )),
            ("license", "个体户登记", "街道会计夹着一本登记说明上门。", (
                ("real", "按真实地址登记", "那张纸压在玻璃板下面。"),
                ("borrow", "借亲戚的执照", "出了事要先解释这是谁的摊。"),
                ("skip", "先不登记", "铁盒又数了一遍。"),
            )),
            ("bike", "摩托车还是屋顶", "二手摩托停在店里。家里来信，屋顶该翻了。", (
                ("ride", "买下车", "油门一拧，巷子里的人都回头。"),
                ("roof", "钱寄回凤阳", "汇款单上四个字：先把屋补上。"),
            )),
            ("caps", "电容", "赵万金的货便宜得不正常。江西的大单又催着。", (
                ("sample", "先抽检", "果然有问题，货退了。赵万金记了恨。"),
                ("bad", "先装机", "他以为这次又赌赢了。"),
            )),
            ("accident", "事故", "收音机过热，供销社仓库冒烟。电容是假货，单上是他的名字。", (
                ("hide", "隐瞒，推给仓储", "局面稳住一阵。雷埋得更深，后来被查封。"),
                ("gray", "找赵万金填窟窿", "快钱补上了。脚踩进了泥里，作坊散了。"),
                ("recall", "全面召回", "该赔的赔。资金断了，信誉还留着一点。"),
            )),
            ("leg", "父亲的腿", "春声倒了。电报说父亲干活摔断了腿。", (
                ("go", "回凤阳治腿", "父亲第一句问：厂子呢？"),
                ("stay", "留在深圳挣钱", "他把电报折好。有些伤等不了。"),
            )),
            ("refurb", "旧壳", "有人把旧机壳打磨一新，问能不能当新货。", (
                ("no", "不当新的卖", "学校的喇叭免费修了。旧壳让人拉走。"),
                ("yes", "先把债顶上", "半个月后，其中一台又回到摊上。他认得自己的焊点。"),
            )),
        ],
        "chapter6": [
            ("stall", "维修摊", "他还着债。梁师傅说，国贸要人查线路，工钱给得高。同一天，债主也来了。", ()),
            ("wage", "国贸的工钱", "梁师傅说，这趟工钱可以对半。", (
                ("share", "留下他的一份", "钱少了一半。梁师傅把电笔递了过来。"),
                ("take", "这趟我一个人拿", "工钱进了自己口袋。梁师傅没再说什么。"),
            )),
            ("tour", "去不去国贸", "债和国贸撞在同一天。", (
                ("go", "推掉债主，去现场", "他拎着工具箱去了。后来在大厅里看见了那位老人。"),
                ("edge", "先见债主，再抢修", "谈好分期，又被叫去。他站在人群边缘。"),
                ("skip", "让梁师傅代班", "他没去。那几句话，是后来在报纸上读到的。"),
            )),
            ("wire", "国贸这排灯", "大厅有一排灯不亮。只有去了现场才会遇上。", (
                ("ok", "自己接亮", "点中那盏，再按上、左、下把线接回去。"),
                ("fail", "没接上", "灯还是暗的。梁师傅后头补了一截。"),
                ("skip", "让梁师傅接", "他往人群那边看。"),
            )),
            ("paper", "报纸上圈三句", "没去现场的人，后来在摊上读报。", (
                ("ok", "三句都圈上", "胆子、大胆地试、硬道理。圈在了报边上。"),
                ("fail", "圈乱了", "红笔点错了行。他把报纸折起来。"),
                ("skip", "只看标题", "正文没往下读。"),
            )),
            ("speech", "南方谈话", "三句被他记住：胆子要大一些；大胆地试，大胆地闯；发展才是硬道理。", (
                ("live", "在现场听见", "人多，他听不全，只断断续续接住这几句。"),
                ("paper", "在报纸上读到", "字印得清楚。他读得很慢，像在跟每一个字较劲。"),
            )),
            ("board", "抄不抄在挡板上", "三句话还在耳朵里。挡板上有一块空。", (
                ("copy", "抄上去", "字贴在维修摊上，天天看得见。"),
                ("keep", "只记在心里", "挡板还是空的。"),
            )),
        ],
        "chapter7": [
            ("restart", "旧仓库", "夜里打开退货的木箱。电烙铁热起来，收音机响了。", (
                ("stay", "一台台拆开", "拆到天亮。他知道得从第一台重新来。"),
                ("drink", "先去酒馆", "喝到半夜。第二天木箱还开着，收音机没有响。"),
            )),
            ("note", "箱盖上的字", "退货的原因，要不要写在箱盖内侧。", (
                ("write", "写给后来的人看", "劣质电容、保护电路。字刻在木头上。"),
                ("hide", "只记合格", "失败留在嘴里，没留在箱子上。"),
            )),
            ("ten", "做多少台", "样机稳住了。手里只剩一点钱。", (
                ("ten", "先做十台", "十套好元件，每台亲手调。这次不能再赌。"),
                ("hundred", "直接做一百台", "钱全压上去。他想把失去的一次抢回来。"),
            )),
            ("weld", "四个焊点", "去上海之前，他在自己桌上练手。", (
                ("ok", "四个都亮了", "金区里按下烙铁。手热了，才敢装箱。"),
                ("fail", "焊糊了", "锡点发黑。他擦掉，改日再练。"),
                ("skip", "不必再练", "样机已经响了。他把烙铁搁下。"),
            )),
            ("su", "苏文静的条件", "她拆开样机：抽检，不合格不出厂，技术可以叫停生产。", (
                ("yes", "三个都答应", "她点了头，回来了。"),
                ("part", "生产权不交", "她留下图纸，人没有回来。"),
                ("no", "一个人说了算", "话谈到这里，断了。"),
            )),
            ("debt", "怎么还债", "还款计划和样机放在江西经销商桌上。对方让他走。", (
                ("pay", "如实还，哪怕慢", "几天后电话来了：先要五十台。"),
                ("delay", "先拖一拖", "他把计划收回去。对方再也没打来。"),
            )),
            ("home", "回不回凤阳", "生意有了起色。他想回凤阳建组装车间。", (
                ("feng", "把根扎回去", "大伯带着村里的年轻人，腾出旧仓库。"),
                ("sz", "留在深圳扩产", "“再大一点再回去”，一说就是很多年。"),
            )),
            ("dad", "父亲进不进门", "父亲绕着车间走，不进门。", (
                ("ask", "请他看物料", "他没说好。第二天却比谁都早到。"),
                ("wait", "等他自己愿意", "两个人隔着门槛，谁都没先迈。"),
            )),
            ("sort", "把电容分开", "桌上好的和受潮的混在一起。父亲站在门口。", (
                ("ok", "先分好", "金亮的进装机，发暗的退回。他看见了两只盒子。"),
                ("fail", "分乱了", "好的坏的又混回一堆。"),
                ("skip", "先说话", "零件还堆着。他先开口。"),
            )),
            ("box", "印泥盒", "父亲把印泥盒递还给他：这回收好，别再乱按了。", (
                ("keep", "和车票、电路图放一起", "三样东西留在手头。"),
                ("drawer", "收进抽屉", "盒子关上了。"),
            )),
        ],
    }

    def plot_forks(nid):
        return FORKS.get(nid, [])

    def fork_pick(bid):
        seen = bid in store.seen_beats
        if bid == "seal":
            return ("admit" if store.flag_seal_active else "deny") if seen else ""
        if bid == "father":
            return ("call" if store.flag_call_father else "quiet") if seen else ""
        if bid == "wu":
            if not store.flag_wu_decided:
                return ""
            return "help" if store.flag_wu else "none"
        if bid == "tools":
            return ("take" if store.flag_su_tools else "refuse") if seen else ""
        if bid == "radio":
            return ("fix" if store.flag_old_radio else "new") if seen else ""
        if bid == "invoice":
            return ("explain" if store.flag_invoice else "leave") if seen else ""
        if bid == "watch":
            if not store.flag_watch_decided:
                return ""
            if store.flag_watch == 2:
                return "cal"
            if store.flag_watch == 1:
                return "tell"
            return "sell"
        if bid == "power":
            return ("steal" if store.flag_steal_power else "lamp") if seen else ""
        if bid == "qc":
            return ("check" if store.flag_qc else "rush") if seen else ""
        if bid == "caps":
            return ("bad" if store.flag_bad_cap else "sample") if seen else ""
        if bid == "accident":
            if not store.flag_accident_decided:
                return ""
            if store.flag_hide:
                return "hide"
            if store.flag_gray:
                return "gray"
            if store.flag_recall:
                return "recall"
            return ""
        if bid == "leg":
            return ("go" if store.flag_father_home else "stay") if seen else ""
        if bid == "tour":
            if not store.flag_tour_decided:
                return ""
            if store.flag_tour == 1:
                return "go"
            if store.flag_tour == 2:
                return "edge"
            return "skip"
        if bid == "speech":
            return ("live" if store.flag_tour > 0 else "paper") if seen else ""
        if bid == "restart":
            return ("stay" if store.flag_restart else "drink") if seen else ""
        if bid == "ten":
            return ("ten" if store.flag_ten else "hundred") if seen else ""
        if bid == "su":
            if not seen:
                return ""
            if store.flag_su_break:
                return "no"
            if store.flag_su_return:
                return "yes"
            return "part"
        if bid == "debt":
            return ("pay" if store.flag_debt else "delay") if seen else ""
        if bid == "home":
            if not store.flag_end_decided:
                return ""
            return "feng" if store.flag_fengyang else "sz"
        if bid == "dad":
            if store.flag_father_reconcile:
                return "ask"
            if "chapter7" in store.done_stages:
                return "wait"
            return ""
        if bid == "box":
            if store.flag_legacy:
                return "keep"
            if "chapter7" in store.done_stages:
                return "drawer"
            return ""
        simple = {
            "sign": (store.flag_sign, ("hold", "stock")),
            "rain": (store.flag_rain, ("dry", "shut")),
            "credit": (store.flag_credit, ("half", "credit", "no")),
            "apprentice": (store.flag_apprentice, ("keep", "send")),
            "books": (store.flag_books, ("open", "hide")),
            "noodle": (store.flag_noodle, ("treat", "save")),
            "oem": (store.flag_oem, ("cover", "keep", "card")),
            "payday": (store.flag_payday, ("full", "half", "tin")),
            "license": (store.flag_license, ("real", "borrow", "skip")),
            "bike": (store.flag_bike, ("ride", "roof")),
            "refurb": (store.flag_refurb, ("no", "yes")),
        }
        if bid in simple:
            if not seen:
                return ""
            val, arms = simple[bid]
            if 1 <= val <= len(arms):
                return arms[val - 1]
            return ""
        if bid in ("torch", "circuit", "crown", "listen", "wire", "paper", "weld", "sort"):
            if not seen:
                return ""
            flag = {
                "torch": store.flag_torch,
                "circuit": store.flag_circuit,
                "crown": store.flag_crown,
                "listen": store.flag_listen,
                "wire": store.flag_wire,
                "paper": store.flag_paper,
                "weld": store.flag_solder_task,
                "sort": store.flag_sort,
            }[bid]
            if flag == 1:
                return "ok"
            if flag == 2:
                return "fail"
            if flag == 3:
                return "skip"
            return ""
        if bid == "date":
            if not seen:
                return ""
            if store.flag_date == 1:
                return "keep"
            if store.flag_date == 2:
                return "forge"
            return ""
        if bid == "wage":
            if not seen:
                return ""
            if store.flag_wage == 1:
                return "share"
            if store.flag_wage == 2:
                return "take"
            return ""
        if bid == "board":
            if not seen:
                return ""
            if store.flag_board == 1:
                return "copy"
            if store.flag_board == 2:
                return "keep"
            return ""
        if bid == "note":
            if not seen:
                return ""
            if store.flag_note == 1:
                return "write"
            if store.flag_note == 2:
                return "hide"
            return ""
        return ""

    def beat_state(nid, bid):
        if store.story_beat == bid:
            return "now"
        if bid in store.seen_beats:
            return "done"
        if stage_index(nid) > stage_index(plot_here()):
            return "far"
        if plot_skipped(nid):
            return "skip"
        return "wait"

    def plot_node(nid):
        for node in PLOT_NODES:
            if node[0] == nid:
                return node
        return PLOT_NODES[0]

    def plot_skipped(nid):
        if not store.seen_stages and not store.story_mark:
            return False
        return stage_index(nid) < stage_index(plot_here()) and nid not in store.seen_stages

    def plot_left_early(nid):
        return (
            nid in store.seen_stages
            and nid not in store.done_stages
            and nid != plot_here()
            and stage_index(nid) < stage_index(plot_here())
        )

    def plot_branch(nid):
        here = plot_here()
        if stage_index(nid) > stage_index(here):
            return "还没走到"
        if plot_skipped(nid):
            return "这一段被跳过了"
        if plot_left_early(nid):
            return "没走完就离开了"
        if nid == here:
            return "你在这里"
        if nid == "south":
            seal = "按了手印" if store.flag_seal_active else "没按手印"
            if not store.flag_wu_decided:
                return seal
            wu = "资助了吴国强" if store.flag_wu else "没有资助吴国强"
            return seal + "，" + wu
        if nid == "spring":
            if store.flag_sign == 1:
                return "租金交了三个月"
            if store.flag_sign == 2:
                return "钱先拿去进货"
            if store.flag_watch_decided:
                return "电子表的事定了"
            return "春声的招牌还没干"
        if nid == "chapter3":
            if store.flag_credit == 1:
                return "供销社先收了一半"
            if store.flag_credit == 2:
                return "四十台全赊了"
            if store.flag_credit == 3:
                return "这笔赊账没做"
            return "货在长途车上"
        if nid == "chapter4":
            if store.flag_downfall:
                return "招牌倒了，人离开了这条路"
            if store.flag_recall:
                return "召回之后，回到了街口"
            if store.flag_refurb == 1:
                return "旧壳没有当新的卖"
            if store.flag_refurb == 2:
                return "翻新顶过一个月的债"
            if store.flag_bike or store.flag_bad_cap:
                return "窟窿还在"
            if store.flag_oem == 2:
                return "拨盘上还是春声"
            if store.flag_oem == 1:
                return "名字被贴纸盖住"
            if store.flag_license == 1:
                return "按真实地址登了记"
            return "作坊的灯还亮着"
        if nid == "chapter6":
            if not store.flag_tour_decided:
                return "南巡，还没选"
            if store.flag_tour == 1:
                tour = "去了现场"
            elif store.flag_tour == 2:
                tour = "站在边缘"
            else:
                tour = "没有去"
            restart = "决定重开" if store.flag_restart else "没有重开"
            return tour + "，" + restart
        if nid == "chapter7":
            if not store.flag_end_decided:
                return "终局的去向，还没选"
            where = "回凤阳建厂" if store.flag_fengyang else "留在深圳"
            return where
        return "按当前选择结算结局"

    def plot_detail(nid):
        node = plot_node(nid)
        if stage_index(nid) > stage_index(plot_here()):
            return "还没玩到这里。跳过去的话，中间没经历的选择都当作没发生。已经改过的数值留着。"
        if plot_skipped(nid):
            return "这一段是跳过来的，里面的选择没有发生。"
        if plot_left_early(nid):
            return "进过这一段，没走完就离开了。里面没做完的选择，当作没发生。"
        if nid == plot_here():
            return "正在这一段。" + node[3] + "。"
        return plot_branch(nid) + "。"

    def prepare_plot_jump(nid):
        renpy.music.set_volume(1.0, delay=0, channel="music")
        renpy.music.stop(channel="talk", fadeout=0)
        renpy.context()._menu = False
        store._menu = False
        store.main_menu = False
        store.suppress_overlay = False
        if nid == "south":
            reset_game()
            store.story_mark = "south"
            return
        idx = stage_index(nid)
        store.seen_stages = [s for s in store.seen_stages if stage_index(s) < idx]
        store.done_stages = [s for s in store.done_stages if stage_index(s) < idx]
        store.seen_beats = [b for b in store.seen_beats if stage_index(beat_stage(b)) < idx]
        store.story_beat = ""
        for later in plot_ids()[idx:]:
            for name in PLOT_CLEAR[later]:
                setattr(store, name, False)
        if idx <= stage_index("spring"):
            store.flag_watch = 0
            store.flag_profit = False
        if idx <= stage_index("chapter6"):
            store.flag_tour = 0
        store.story_mark = nid

    def plot_confirm(nid):
        node = plot_node(nid)
        title = node[1] + " " + node[2]
        if nid == "south":
            return "从头再走「" + title + "」？数值和全部选择都会清空。"
        if stage_index(nid) > stage_index(plot_here()):
            return "跳到「" + title + "」？中间的阶段会跳过，那些选择当作没发生。已经改过的数值留着。"
        return "回到「" + title + "」重走？这一段和后面的选择会清掉，前面做过的留下。数值不退回。"

    def change_stats(money=0, rep=0, tech=0, family=0, thought=0, silent=False):
        before = (store.money, store.rep, store.tech, store.family, store.thought)
        store.money = clamp(store.money + money)
        store.rep = clamp(store.rep + rep)
        store.tech = clamp(store.tech + tech)
        store.family = clamp(store.family + family)
        store.thought = clamp(store.thought + thought)
        after = (store.money, store.rep, store.tech, store.family, store.thought)
        keys = ("money", "rep", "tech", "family", "thought")
        store.stat_pulse = {key: b - a for key, a, b in zip(keys, before, after)}
        if not silent:
            labels = ("资金", "信誉", "技术", "亲情", "思想")
            parts = []
            for label, a, b in zip(labels, before, after):
                if a != b:
                    parts.append("%s %+d" % (label, b - a))
            if parts:
                renpy.notify("　".join(parts))

    def unlock_ending(code):
        endings = list(persistent.endings or [])
        if code not in endings:
            endings.append(code)
        persistent.endings = endings

    def plot_progress():
        ids = [fork[0] for nid in plot_ids() if nid != "ending" for fork in plot_forks(nid)]
        done = sum(1 for bid in ids if bid in store.seen_beats)
        total = max(len(ids), 1)
        return done, total

    def plot_curve(x1, y1, x2, y2, bend):
        dist = math.hypot(x2 - x1, y2 - y1) or 1.0
        px = -(y2 - y1) / dist * bend
        py = (x2 - x1) / dist * bend
        cx = (x1 + x2) / 2.0 + px
        cy = (y1 + y2) / 2.0 + py
        steps = 8
        pts = []
        for i in range(steps + 1):
            t = i / float(steps)
            u = 1.0 - t
            pts.append((u * u * x1 + 2 * u * t * cx + t * t * x2, u * u * y1 + 2 * u * t * cy + t * t * y2))
        segs = []
        for i in range(steps):
            ax, ay = pts[i]
            bx, by = pts[i + 1]
            segs.append((ax, ay, bx, by))
        return segs

    def plot_segment(x1, y1, x2, y2, color):
        dist = math.hypot(x2 - x1, y2 - y1)
        return {
            "x": (x1 + x2) / 2.0,
            "y": (y1 + y2) / 2.0,
            "w": max(int(dist), 1),
            "angle": math.degrees(math.atan2(y2 - y1, x2 - x1)),
            "color": color,
        }

    def plot_geometry():
        faces = {
            "south": "portrait_lin",
            "spring": "portrait_chen",
            "chapter3": "portrait_chen",
            "chapter4": "portrait_liang",
            "chapter6": "deng_inset",
            "chapter7": "portrait_father",
            "ending": "gui/seal.png",
        }
        bands_c = ("#D9E4FB", "#E4DDF8", "#F6E3EE", "#E3F0E6", "#F4EBD9")
        gap = 1720
        cy = 390
        here = plot_here()
        nodes = []
        lines = []
        bands = []
        chapters = plot_ids()
        for i, nid in enumerate(chapters):
            cx = 260 + i * gap
            node = plot_node(nid)
            future = stage_index(nid) > stage_index(here)
            if nid == "ending":
                future = "chapter7" not in store.done_stages and store.story_mark != "ending"
            bands.append({"x": cx - 180, "w": gap, "color": bands_c[i % len(bands_c)]})
            nodes.append({
                "id": "c:" + nid,
                "kind": "chapter",
                "x": cx,
                "y": cy,
                "title": node[1],
                "sub": node[2],
                "face": faces.get(nid, "portrait_lin"),
                "locked": future,
                "here": nid == here,
                "nid": nid,
            })
            if i < len(chapters) - 1:
                for ax, ay, bx, by in plot_curve(cx + 78, cy, cx + gap - 78, cy, 0):
                    lines.append(plot_segment(ax, ay, bx, by, "#7C6AE0"))
            forks = [] if nid == "ending" else plot_forks(nid)
            above = [fork for n, fork in enumerate(forks) if n % 2 == 0]
            below = [fork for n, fork in enumerate(forks) if n % 2 == 1]

            def place(group, y0, y1, bend):
                count = len(group)
                if count == 0:
                    return
                span = gap - 460
                for j, fork in enumerate(group):
                    t = 0.5 if count == 1 else j / float(count - 1)
                    fx = cx + 210 + span * t
                    fy = y0 if count == 1 else y0 + (y1 - y0) * t
                    picked = fork_pick(fork[0])
                    seen = fork[0] in store.seen_beats
                    nodes.append({
                        "id": "f:" + fork[0],
                        "kind": "fork",
                        "x": fx,
                        "y": fy,
                        "title": fork[1],
                        "locked": future or (not seen and stage_index(nid) > stage_index(here)),
                        "seen": seen,
                        "picked": bool(picked),
                        "nid": nid,
                    })
                    color = "#7C6AE0" if seen else "#C9C3E4"
                    for ax, ay, bx, by in plot_curve(cx, cy, fx, fy, bend):
                        lines.append(plot_segment(ax, ay, bx, by, color))

            place(above, 36, 250, -36)
            place(below, 530, 730, 36)
        width = 260 + len(chapters) * gap
        return {"width": width, "lines": lines, "nodes": nodes, "bands": bands}

    def plot_card(focus):
        if not focus or ":" not in focus:
            return None
        kind, ident = focus.split(":", 1)
        if kind == "c":
            node = plot_node(ident)
            return {
                "title": node[1] + " " + node[2],
                "body": plot_detail(ident),
                "chapter": ident,
                "arms": [],
                "locked": stage_index(ident) > stage_index(plot_here()) and ident != "ending",
            }
        for nid in plot_ids():
            for fork in plot_forks(nid):
                if fork[0] != ident:
                    continue
                locked = stage_index(nid) > stage_index(plot_here())
                chosen = "" if locked else fork_pick(ident)
                arms = []
                if not locked:
                    for arm in fork[3]:
                        arms.append((arm[1], arm[2], arm[0] == chosen and chosen != ""))
                return {
                    "title": fork[1],
                    "body": "还没走到这里。" if locked else fork[2],
                    "chapter": nid,
                    "arms": arms,
                    "locked": locked,
                }
        return None


transform slow_push:
    xalign 0.5
    yalign 0.5
    zoom 1.0
    linear 16.0 zoom 1.06

transform inset_card:
    xalign 0.97
    yalign 0.14

transform drift_left:
    xalign 0.5
    yalign 0.5
    linear 18.0 xalign 0.455

transform splash_drift:
    xalign 0.5
    yalign 0.5
    zoom 1.12
    linear 8.0 zoom 1.0

transform splash_title:
    xalign 0.5
    yalign 0.42

transform splash_caption:
    xalign 0.5
    yalign 0.84

transform chapter_appear:
    alpha 0.0
    yoffset 24
    linear 0.7 alpha 1.0 yoffset 0

transform notify_appear:
    alpha 0.0
    yoffset -12
    linear 0.25 alpha 1.0 yoffset 0
