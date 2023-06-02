init:
    $ config.keymap['button_select'].append('K_F5')
screen input(prompt,nvl=False):
    if nvl:
        default input_d = MultipleLineInput(id='input', max_lines=10, # сколько максимум можем быть строк
        **renpy.get_displayable_properties('input')
        )
        key 'K_F5' action Return(input_d.content)
        style_prefix "input"
        window:
            style "nvl_window"
            has vbox:
                style "nvl_vbox"
                xalign gui.dialogue_text_xalign
                xpos gui.dialogue_xpos
                xsize gui.dialogue_width
                ypos gui.dialogue_ypos
            text prompt style "input_prompt"
            
            add input_d
             

        use quick_menu
    else:
        style_prefix "input"

        window:
            vbox:
                xalign gui.dialogue_text_xalign
                xpos gui.dialogue_xpos
                xsize gui.dialogue_width
                ypos gui.dialogue_ypos

                text prompt style "input_prompt"
                input id "input"
                

style input_prompt is default

style input_prompt:
    color "#fff"
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    color "#fff"
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width
