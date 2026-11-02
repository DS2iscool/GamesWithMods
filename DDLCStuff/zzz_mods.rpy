# ============================================================
# zzz_mods.rpy  —  unofficial QoL / cheat mod for DDLC 1.1.1
#
# HOW TO INSTALL:
#   Drop this file directly into your game's "game/" folder,
#   next to script.rpyc etc:
#     DDLC-1.1.1-pc/game/zzz_mods.rpy
#   Ren'Py auto-compiles loose .rpy files on next launch and
#   prefers them over the packed .rpyc of the same name — but
#   since this is a NEW filename, it just loads alongside
#   everything else. No repacking of scripts.rpa needed.
#
#   The "zzz_" prefix just makes sure it's compiled/loaded
#   after the base game's own files (alphabetical load order).
#
# WHAT THIS DOES NOT DO (on purpose):
#   - Does not touch persistent.yuri_kill or any of the
#     in_yuri_kill / seen_eyes flags. Those specifically gate
#     the game's graphic self-harm CG sequence (cgs.rpyc ties
#     images/cg/y_kill/*.png to yuri_kill thresholds). I'm
#     leaving that content-gate alone rather than building a
#     one-click unlock for it.
#   - Does not include any actual music files. See the MUSIC
#     section below — I built the swap mechanism, but you
#     supply audio you actually have rights to use.
# ============================================================

init 999 python:

    # ---- Cheat menu hotkey: press Shift+M in-game ----
    config.keymap['ddlc_mod_menu'] = ['shift_M']

    def ddlc_mod_max_affection():
        """Maxes out each character's poem-appeal / general appeal
        trackers. These are read at chapter transitions to decide
        which route you end up on."""
        store.n_appeal = 100
        store.s_appeal = 100
        store.y_appeal = 100
        store.m_appeal = 100
        store.n_poemappeal = 100
        store.s_poemappeal = 100
        store.y_poemappeal = 100
        store.m_poemappeal = 100
        renpy.notify("Affection maxed for Natsuki / Sayori / Yuri / Monika")

    def ddlc_mod_complete_poems():
        """Marks every poem as read/delivered so poem-dependent
        checks don't block progress. Does not touch the special
        end-game 'clearall' CG variant or the self-harm gate."""
        store.n_readpoem = True
        store.s_readpoem = True
        store.y_readpoem = True
        store.m_readpoem = True
        store.n_read3 = True
        store.y_read3 = True
        store.poemsread = 20
        renpy.notify("All poems marked as read")

    def ddlc_mod_toggle_anticheat():
        persistent.anticheat = not getattr(persistent, "anticheat", False)
        renpy.notify("anticheat flag = %r" % persistent.anticheat)

    def ddlc_mod_list_labels():
        """Prints every label in the loaded script to the console
        (open dev console with Shift+O) so you can renpy.jump()
        anywhere by name without guessing."""
        names = sorted(k for k in renpy.game.script.namemap.keys() if isinstance(k, str))
        for n in names:
            print(n)
        renpy.notify("Label list printed to console/log — open with Shift+O")

    # ---- MUSIC SWAP ----
    # Original tracks are tagged like "<loop 22.073>bgm/1.ogg" via
    # defines t1, t2, t3 ... m1, mend, ghostmenu, g1, g2, hb (see
    # definitions.rpyc). This wraps each one: if you drop a file
    # with a matching name into game/bgm_custom/, it's used instead
    # of the original — original loop timing is dropped since your
    # replacement track has its own length, so it'll just loop
    # start-to-end.
    #
    # Put your own licensed/owned audio at, e.g.:
    #   game/bgm_custom/t1.ogg
    #   game/bgm_custom/t6.ogg
    #   game/bgm_custom/m1.ogg
    # (must be .ogg — Ren'Py's default supported format)

    import os

    _ddlc_mod_custom_dir = os.path.join(config.gamedir, "bgm_custom")

    def ddlc_mod_track(key, original):
        custom_path = os.path.join(_ddlc_mod_custom_dir, key + ".ogg")
        if os.path.isfile(custom_path):
            return "bgm_custom/%s.ogg" % key
        return original

    # Re-point each music define through the swap function.
    # (Safe even if bgm_custom/ doesn't exist — falls back silently.)
    for _key in ["t1","t2","t2g","t2g2","t2g3","t3","t3g","t3g2","t3g3","t3m",
                 "t4","t4g","t5","t5b","t5c","t6","t6g","t6r","t6s","t7","t7a",
                 "t7g","t8","t9","t9g","t10","t10y","td","m1","mend",
                 "ghostmenu","g1","g2","hb"]:
        if _key in globals():
            globals()[_key] = ddlc_mod_track(_key, globals()[_key])

    # Force the built-in Ren'Py dev console + shift+D dev menu on,
    # regardless of the game's shipped "developer" define.
    config.developer = True
    config.console = True


screen ddlc_mod_menu():
    zorder 999
    frame:
        xalign 1.0
        yalign 0.0
        padding (15, 15)
        background "#000000cc"
        vbox:
            spacing 6
            text "DDLC Mods" size 22 color "#ffffff" bold True
            textbutton "Max Affection" action Function(ddlc_mod_max_affection)
            textbutton "Complete All Poems" action Function(ddlc_mod_complete_poems)
            textbutton "Toggle Anticheat Flag" action Function(ddlc_mod_toggle_anticheat)
            textbutton "Print All Labels to Console" action Function(ddlc_mod_list_labels)
            text "Shift+O = dev console" size 14 color "#aaaaaa"
            text "Shift+D = dev menu" size 14 color "#aaaaaa"
            textbutton "Close" action Hide("ddlc_mod_menu")

# Bind Shift+M to open the menu from anywhere
init python:
    def _ddlc_mod_show_menu():
        if not renpy.get_screen("ddlc_mod_menu"):
            renpy.show_screen("ddlc_mod_menu")
        else:
            renpy.hide_screen("ddlc_mod_menu")

    config.underlay.append(
        renpy.Keymap(shift_M=_ddlc_mod_show_menu)
    )
