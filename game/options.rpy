define config.screen_width = 1920
define config.screen_height = 1080

## 红卫的春天 — project options
define config.name = _("红卫的春天")
define gui.show_name = True
define config.version = "0.9.0-pilot"
define build.name = "chunsheng_nanlai"
define build.version = "0.9.0-pilot"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = "audio/prologue.ogg"
define config.splashscreen_suppress_overlay = False

define config.enter_transition = Dissolve(0.35)
define config.exit_transition = Dissolve(0.35)
define config.intra_transition = Dissolve(0.20)
define config.after_load_transition = Dissolve(0.35)
define config.end_game_transition = Fade(0.4, 0.2, 0.4)
define config.window_show_transition = Dissolve(0.15)
define config.window_hide_transition = Dissolve(0.15)

define config.save_directory = "chunsheng_nanlai-1"
define config.window_icon = "gui/window_icon.png"
define config.default_fullscreen = False
define config.rollback_enabled = True
define config.developer = True

define config.window = "auto"
define config.quit_action = Quit(confirm=True)

## Force 1:1 virtual pixels on 150%/200% Windows displays.
define config.de_minimus_dpi_scale = 3.0
