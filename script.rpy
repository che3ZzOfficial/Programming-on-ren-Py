init python:
    import builtins
    config.keymap['input_next_line'] = ['shift_K_RETURN','K_RETURN']
    def my_input(prompt=''):
        return renpy.input(prompt)
  
    def my_print(*what):
        def convert(obj):
            return str(obj).replace('[', '[[').replace('{', '{{')
        converted_what = map(convert, what)
        text = ' '.join(converted_what)
        user_prints = []
        user_prints = [text]
        renpy.say(None, text)
    class MultipleLineInput(Input):
        def __init__(self, *args, **kwargs):
            self.max_lines = kwargs.pop('max_lines', 0)
            super(MultipleLineInput, self).__init__(*args, **kwargs)

        def update_text(self, new_content, *args, **kwargs):
            max_lines = self.max_lines
            if max_lines > 0:
                lines = new_content.split('\n') # на каждое обновление текста, мы делим его на линии, что в теории, может сказаться на производительности
                if len(lines) > max_lines:
                    lines = lines[:max_lines]
                    new_content = '\n'.join(lines)
                    self.caret_pos = len(new_content)
            
            return super(MultipleLineInput, self).update_text(new_content, *args, **kwargs)

        def event(self, ev, x, y, st):
            if not self.editable:
                return None
                
            elif renpy.map_event (ev , 'K_TAB'):
                self.st = st
                self.old_caret_pos = self.caret_pos

                indent = '    '
                new_content = self.content[:self.caret_pos]
                new_content += indent
                new_content += self.content[self.caret_pos:]
                self.caret_pos += len(indent)
                self.update_text(new_content, self.editable)
                renpy.redraw(self, 0)
                raise renpy.IgnoreEvent()

            if renpy.map_event(ev, 'input_next_line'):
                self.st = st
                self.old_caret_pos = self.caret_pos
                content = self.content[:self.caret_pos] + '\n' + self.content[self.caret_pos:]
                self.caret_pos += 1
                self.update_text(content, self.editable)

                renpy.redraw(self, 0)
                raise renpy.IgnoreEvent()
            return super(MultipleLineInput, self).event(ev, x, y, st)
            
def code_s():
        while True:
            code = renpy.input('Введите код: ', '' , show_nvl=True)
            exec_locals = {}
            exec_globals = {
                'print': my_print,
                'input': my_input
            }
            try:
                builtins.exec(code, exec_globals, exec_locals)
            except TypeError:
                renpy.say(None, "Ошибка в типах данных.")
                renpy.say(None, "Попробуйте снова.")
                continue
            except SyntaxError:
                renpy.say(None, "Ошибка в синтаксисе.")
                renpy.say(None, "Попробуйте снова.")
                continue
            except NameError:
                renpy.say(None, "Ошибка в переменных.")
                renpy.say(None, "Попробуйте снова.")
                continue
            except ValueError:
                renpy.say(None, "Не правильное значение переменной.")
                renpy.say(None, "Попробуйте снова.")
            except OSError:
                renpy.say(None, "Системная ошибка.")
                renpy.say(None, "Попробуйте снова.")
            except Exception:
                renpy.say(None, "Неизвестная ошибка.")
                renpy.say(None, "Попробуйте снова.")
            else:
                return
# start label (начало игры)
$ renpy.input('Normal input')
$ renpy.input('NVL input', show_nvl=True)

label start:
$ renpy.notify("Чтобы запустить код, нажмите F5.")
$ code_s()
