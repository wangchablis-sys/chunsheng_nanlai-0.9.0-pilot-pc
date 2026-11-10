## 红卫的春天 — fixed bonuses, ending router and ending scenes

label apply_fixed_bonuses:
    if flag_ten and flag_su_return and flag_debt:
        $ change_stats(money=30, rep=10, tech=10, thought=10, family=5, silent=True)
        n "有些账，是在人看不见的地方慢慢结清的。"

    if flag_fengyang and flag_father_reconcile:
        $ change_stats(money=20, rep=10, tech=5, family=10, thought=10, silent=True)

    if flag_legacy:
        $ change_stats(thought=5, silent=True)

    return


label ending_router:
    $ mark_stage("ending")
    if not flag_bonus_applied:
        $ flag_bonus_applied = True
        call apply_fixed_bonuses from _call_apply_fixed_bonuses

    ## 1. 警示优先：隐瞒 / 灰色
    if flag_hide:
        jump ending_fail

    if flag_gray:
        if money >= 55 and rep >= 45:
            jump ending_divided
        jump ending_fail

    ## 2. 回避南巡、拒绝重启
    if thought <= 30 and flag_tour == 0 and not flag_restart:
        jump ending_stuck

    ## 3. 隐藏升华
    if (rep >= 85 and tech >= 85 and family >= 85 and thought >= 85 and money >= 50
            and flag_wu and flag_recall and flag_tour == 1 and flag_restart
            and flag_ten and flag_su_return and flag_debt and flag_fengyang
            and flag_father_reconcile and flag_legacy):
        jump ending_hidden

    ## 4. 正向：春声归乡
    if (rep >= 75 and tech >= 75 and thought >= 75 and family >= 75 and money >= 40
            and flag_wu and flag_recall and flag_tour >= 1 and flag_fengyang
            and flag_su_return):
        jump ending_home

    ## 5. 正向：质造立身
    if (rep >= 75 and tech >= 75 and thought >= 60 and money >= 50
            and flag_recall and flag_ten and flag_su_return):
        jump ending_quality

    ## 6. 正向：薪火基层
    if (family >= 75 and rep >= 60 and tech >= 60 and thought >= 50
            and flag_fengyang and flag_father_reconcile and flag_ten):
        jump ending_skills

    ## 7. 中性：道分两路
    if (money >= 60 and 40 <= rep <= 69 and flag_profit
            and not flag_hide and not flag_gray and not flag_su_break):
        jump ending_divided

    ## 8. 中性：安稳立足
    if (40 <= money <= 70 and 40 <= rep <= 70 and 40 <= tech <= 70
            and 40 <= family <= 70 and 40 <= thought <= 70
            and not flag_hide and not flag_gray and not flag_su_break):
        jump ending_stable

    ## 9. 兜底
    jump ending_common


label show_ending(code, title, subtitle):
    show screen ending_card(code, title, subtitle)
    with Dissolve(0.8)
    pause
    hide screen ending_card
    with Dissolve(0.6)
    return


label ending_hidden:
    $ unlock_ending("E8")
    scene bg_end_e8 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_good.ogg" fadein 2.0 loop

    n "2008年，改革开放三十周年。"
    n "凤阳大包干纪念馆里，多了一只干裂的印泥盒。"
    scene bg_g02_thumb at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "捐赠人一栏，写着“孙红卫”。"

    n "年轻的讲解员问他，为什么要把这么旧的东西捐出来。"
    l "因为当年按下这个手印的人，没想过自己会走进历史。"
    scene bg_end_e8 at slow_push  # auto-bg
    with dissolve  # auto-bg
    l "他们只是想让家里人，吃上一顿白面馒头。"

    n "展厅外，春风从南边来。"
    scene bg_g02_thumb_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "吹过深圳的高楼，也吹过凤阳的田野。"
    n "一只红手印，一点电烙铁的微光，终于接上了。"
    call show_ending("E8", "潮头回声，精神传承", "一个人的红手印，最终按进了一个时代的记忆。") from _call_show_ending
    return


label ending_home:
    $ unlock_ending("E1")
    scene bg_end_e1 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_good.ogg" fadein 2.0 loop

    n "1995年，凤阳小岗村。"
    n "春声电器的总部，从深圳迁了回来。"
    n "一百多号工人，七成来自周边村镇。"

    scene bg_g32_factory at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "父亲孙守成每天绕着车间走一圈，还是不肯进门。"
    n "直到厂里第一个女工拿着工资，给生病的母亲抓了药。"
    scene bg_end_e1 at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "那天下午，他第一次走进车间，帮着整理零件。"

    n "新一代收音机下线，红卫把第一台带回老屋。"
    n "父亲坐在门槛上，摩挲着那只印泥盒。"
    scene bg_g32_factory_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    l "外头叫孙总，深圳的老朋友叫彪子。"
    l "您和我妈，还是叫我红卫。"

    scene bg_g32_factory_z at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "父亲把印泥盒递还给他：“这回收好，别再乱按了。”"
    n "村口，班车停下，年轻的工人说笑着下车。"
    n "他们眼里的光，和当年揣着二十元钱南下的他，一模一样。"
    call show_ending("E1", "春声归乡，共同富裕", "把根扎回乡土，才听得见春天真正的回声。") from _call_show_ending_1
    return


label ending_quality:
    $ unlock_ending("E2")
    scene bg_end_e2 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_good.ogg" fadein 2.0 loop

    n "春声没有急着做大。"
    n "它先做十台，再做一百台，再做一千台。"
    n "每一批产品都要抽检，每一台机器都贴着工人编号。"

    scene bg_g30_shanghai at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "苏文静把“先做十台”四个字，刻成一块小木牌，挂在车间门口。"
    s "不是不想快。"
    scene bg_end_e2 at slow_push  # auto-bg
    with dissolve  # auto-bg
    s "是知道慢在哪里，才敢快。"

    n "很多年后，春声成了正规的电子品牌。"
    n "有人问孙红卫，企业最重要的资产是什么。"
    scene bg_g30_shanghai_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    l "不是厂房，不是渠道。"
    l "是那些年，我们没敢省掉的那几道工序。"

    scene bg_g30_shanghai_z at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "窗外，深圳的楼更高了。"
    n "车间里，电烙铁的热气还在往上走。"
    call show_ending("E2", "质造立身，实业报国", "把每一台机器做好，就是那个时代最朴素的报国。") from _call_show_ending_2
    return


label ending_skills:
    $ unlock_ending("E3")
    scene bg_end_e3 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_good.ogg" fadein 2.0 loop

    n "春声在凤阳办了免费的技能培训班。"
    n "只要是农村户口、愿意学技术的青年，都能来。"
    n "学电路维修，学组装质检，学看图纸。"

    scene bg_g11_stall at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "合格的人，可以留厂上班，也可以回家开维修铺。"
    n "短短两年，凤阳周边多了二十多家家电维修铺。"
    scene bg_end_e3 at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "掌柜的，全是春声培训班出来的学员。"

    n "苏文静从上海寄来一箱旧教材，扉页上写着一行字："
    s "技术留在人手里，才叫技术。"

    scene bg_g11_stall_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "梁师傅在黑板前画电路图，粉笔灰落了一身。"
    n "他教得慢，年轻人记得牢。"
    scene bg_g11_stall_z at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "窗外的田野，正在返青。"
    call show_ending("E3", "薪火基层，技能兴乡", "技术留在家乡，才真正长成了根。") from _call_show_ending_3
    return


label ending_divided:
    $ unlock_ending("E5")
    scene bg_end_e5 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_neutral.ogg" fadein 2.0 loop

    n "很多年后，深圳的一条街上，开着两家店。"
    n "街这头，是孙红卫的维修铺。"
    n "街那头，是陈海生的大卖场。"

    scene bg_g14_bus at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "陈海生的生意做得很大，广告牌换了一块又一块。"
    n "孙红卫的铺子很小，招牌旧了也没换。"
    scene bg_end_e5 at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "但街坊的收音机坏了，还是愿意多走两步，送到他这里。"

    n "两个人偶尔在街口遇见，点个头，各自走开。"
    n "没有人能说清，哪条路才是对的。"
    scene bg_g14_bus_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "时代容得下不同的答案，也记得住不同的代价。"
    call show_ending("E5", "道分两路，各自求索", "同一个时代，容得下不同的答案。") from _call_show_ending_4
    return


label ending_stable:
    $ unlock_ending("E4")
    scene bg_end_e4 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_neutral.ogg" fadein 2.0 loop

    n "债，一笔一笔还清了。"
    n "孙红卫没有再把生意做大。"
    scene bg_g04_repair at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "他在深圳的街角，守着一间小小的维修铺。"

    n "每天早上开门，先把招牌擦一遍。"
    n "然后把电烙铁插上，等它慢慢热起来。"
    scene bg_end_e4 at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "收音机里的声音，从早到晚，没有停过。"

    n "有人替他可惜，说当年要是再闯一闯，说不定又是另一个孙老板。"
    scene bg_g04_repair_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "他只是笑笑，把修好的收音机递过去。"
    l "能守住一间铺子，也不容易。"

    n "窗外的春天，每年都来。"
    scene bg_g04_repair_z at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "不是每个人都要成为传奇。"
    n "守住一盏灯，也是。"
    call show_ending("E4", "安稳立足，平凡坚守", "不是每个人都要成为传奇，守住一盏灯也是。") from _call_show_ending_5
    return


label ending_fail:
    $ unlock_ending("E6")
    scene bg_end_e6 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_bad.ogg" fadein 2.0 loop

    if flag_hide:
        n "那批货，终究没能瞒过去。"
        n "更多地区爆发故障，工商部门介入调查。"
        scene bg_g23_smoke at slow_push  # auto-bg
        with dissolve  # auto-bg
        n "春声作坊被查封，门口贴上了封条。"
    else:
        n "灰色链条断得比想象中更快。"
        n "钱没有填上窟窿，反而把窟窿撕得更大。"
        scene bg_end_e6 at slow_push  # auto-bg
        with dissolve  # auto-bg
        n "案件牵连进来，春声作坊彻底散了。"

    n "债主堵在门口，工人等着工资，经销商不接电话。"
    scene bg_g23_smoke_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "孙红卫卖了摩托车，卖了手表，还是不够。"
    n "父亲摔断腿的电报，压在抽屉最底下，他一直没敢回。"

    n "离开深圳那天，他提着一只旧包。"
    scene bg_g23_smoke_z at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "路过当年摆摊的街口，他停了停，没有抬头。"
    n "春天还在，可他已经听不见回声。"
    call show_ending("E6", "失信落败，黯然离场", "底线一旦破了，时代不会再给你第二次信任。") from _call_show_ending_6
    return


label ending_stuck:
    $ unlock_ending("E7")
    scene bg_end_e7 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_bad.ogg" fadein 2.0 loop

    n "1992年的那场谈话，孙红卫没有去听。"
    n "后来，报纸上的字慢慢泛黄。"
    scene bg_g16_watches at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "他把报纸压在维修摊的玻璃板底下，再没有翻开过。"

    n "债还得很慢，日子过得更慢。"
    n "当年的闯劲，像电烙铁上的一缕烟，散了就散了。"
    scene bg_end_e7 at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "有人劝他再试一试，他摆摆手：“现在这样，也挺好。”"

    n "街上的店换了一茬又一茬。"
    scene bg_g16_watches_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "只有他的旧招牌，一直挂在那里。"
    n "风吹过来，招牌晃两下，又安静了。"

    n "时代从不等站在原地的人。"
    scene bg_g16_watches_z at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "它只是从你身边走过去，连头也不回。"
    call show_ending("E7", "故步自封，困守一隅", "时代从不等站在原地的人。") from _call_show_ending_7
    return


label ending_common:
    $ unlock_ending("E0")
    scene bg_end_e0 at slow_push
    with fade
    stop music fadeout 2.0
    play music "audio/ending_neutral.ogg" fadein 2.0 loop volume 0.55

    n "后来的日子，没有大富大贵，也没有一败涂地。"
    n "孙红卫还在修收音机。"
    scene bg_g03_harvest at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "春声的牌子，有时候还挂在店里。"

    n "有人记得他当年的风光，也有人记得他摔过的跟头。"
    n "他自己很少提。"
    scene bg_end_e0 at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "只是每年春天，都会把那只印泥盒拿出来，擦一擦。"

    n "春风从南边来，吹过深圳的高楼，也吹过凤阳的田野。"
    scene bg_g03_harvest_c at slow_push  # auto-bg
    with dissolve  # auto-bg
    n "日子还在往前走。"
    n "春天，每年都会来。"
    call show_ending("E0", "红卫的春天", "日子还在往前走，春天每年都会来。") from _call_show_ending_8
    return
