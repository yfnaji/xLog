import sys
from enum import Enum


class EscapeCodes(Enum):
    reset = 0
    # Text styles
    bold = 1
    dim = 2
    italic = 3
    underline = 4
    blinking = 5
    strikethrough = 9
    # Text Colours
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    purple = 35
    cyan = 36
    white = 37
    # Background Colours
    black_bg = 40
    red_bg = 41
    green_bg = 42
    yellow_bg = 43
    blue_bg = 44
    purple_bg = 45
    cyan_bg = 46
    white_bg = 47
    # High Intensity Text Colours
    black_hi = 90
    red_hi = 91
    green_hi = 92
    yellow_hi = 93
    blue_hi = 94
    purple_hi = 95
    cyan_hi = 96
    white_hi = 97
    # High Intensity Background Colours
    black_hi_bg = 100
    red_hi_bg = 101
    green_hi_bg = 102
    yellow_hi_bg = 103
    blue_hi_bg = 104
    purple_hi_bg = 105
    cyan_hi_bg = 106
    white_hi_bg = 107


class xLogError(Exception):
    __module__ = "builtins"


class xLog:
    def __init__(
        self, bg=None, fg=None, style=[], func=print, fg_255=None, bg_255=None
    ):
        self.func = func
        self.config = []

        if not any((fg, bg, style, fg_255, bg_255)):
            print(
                "xLog: No configurations specified - "
                "will just use terminal default (unless specified elsewhere)"
            )
            self.config = ""
            return

        def _rgb_validator(rgb):
            assert len(rgb) == 3 and all(
                (
                    -1 < int(rgb[0]) < 256, 
                    -1 < int(rgb[1]) < 256, 
                    -1 < int(rgb[2]) < 256
                )
            )

        def _is_int_or_int_str(code):
            return type(code) is int or (type(code) is str and code.isdigit())

        def _str_to_escape_code(code, context="fg"):

            code = code.lower()
            hi = 0
            bg = ""

            if code[-2:] == "hi":
                hi = 60
                code = code[:-3]
            if context == "bg":
                bg = "_bg"

            return EscapeCodes[code + bg].value + hi

        def _escape_code_validator(code, context):
            fg = 29 < code < 38 or 89 < code < 98
            bg = 39 < code < 48 or 98 < code < 108

            if context == "fg":
                assert fg
            elif context == "bg":
                assert bg
            elif context == "style":
                assert not fg and not bg

        def _set_color(var, var_255, _fg=False):
            context = "fg" if _fg else "bg"
            try:
                if _fg:
                    esc_code = "38"
                else:
                    esc_code = "48"

                if var_255:
                    var = None
                    assert -1 < var_255 < 256
                    var = ";".join([esc_code, "5", str(var_255)])
                elif _is_int_or_int_str(var):
                    _escape_code_validator(int(var), context)
                elif type(var) is str:
                    var = _str_to_escape_code(var, context)
                    _escape_code_validator(var, context)
                elif type(var) is tuple:
                    _rgb_validator(var)
                    var = ";".join(
                            [
                            esc_code,
                            "2",
                            str(var[0]),
                            str(var[1]),
                            str(var[2]),
                        ]
                    )
                else:
                    err = f"{var if var else var_255} "
                    err += "is using an incompatible datatype for "
                    err += f"{context}\n"
                    err += f"{context} must be either int, str or tuple\n"
                    err += "Refer to xLog().help() "
                    err += "if you need further guidance"
                    raise xLogError(err)
                
                self.config.append(str(var))
                
            except AssertionError:
                if var_255:
                    err = f"{var_255} is not a valid code for {context}_255\n"
                    err += "Use int between (inclusive) 0 and 255"
                else:
                    err = f"{var} is not a valid code for {context}\n"
                    err += "Refer to xLog().help() "
                    err += "if you need further guidance"
                raise xLogError(err)
            except TypeError:
                if var_255:
                    err = f"Incorrect datatype used for {context}_255\n"
                    err += "Use int between (inclusive) 0 and 255"
                else:
                    err = f"{var} is not a valid code for {context}\n"
                    err += "Refer to xLog().help() "
                    err += "if you need further guidance"
                raise xLogError(err)
            except KeyError:
                if _is_int_or_int_str(var):
                    err = f"Unkown Escape code {var}"
                elif type(var) is str:
                    err = f"Unknown Escape code string value <{var}>\n"
                err += "Refer to xLog().help() "
                err += "if you need further guidance"
                raise xLogError(err)

        colors = [
            (var, var_255, _fg)
            for var, var_255, _fg in [(fg, fg_255, True), (bg, bg_255, False)]
            if any((var, var_255))
        ]

        for color, color_255, _fg in colors:
            _set_color(color, color_255, _fg)

        if type(style) in (str, int):
            style = [style]
        elif type(style) not in (list, set, tuple):
            err = f"Datatype {type(style)} for style is incompatible\n"
            err += "Must be one of string, int or sting/int items in "
            err += "list, set or tuple"
            raise xLogError(err)

        for st in style:
            try:
                if _is_int_or_int_str(st):
                    st = EscapeCodes(int(st)).value
                else:
                    st = _str_to_escape_code(st)

                _escape_code_validator(st, "style")
                self.config.append(str(st))
            except KeyError:
                if _is_int_or_int_str(st):
                    err = f"Unkown code input <{st}>"
                else:
                    err = f"Unknown string input <{st}>"
                raise xLogError(f"{err}")
            except AssertionError:
                name = EscapeCodes(st).name
                name = name.replace('_hi', '').replace('_bg', '')
                err = f"Cannot set style to {st} ({name})\n"
                err += f"{st} is reserved for the "
                if 29 < int(st) < 38 or 89 < int(st) < 98:
                    err += "fg parameter"
                else:
                    err += "bg parameter"
                raise xLogError(err)

        self.config = ";".join(self.config)

    def __call__(self, text):
        text = f"\x1b[{self.config}m{text}\x1b[0m"
        if type(self.func) is type and issubclass(self.func, Exception):
            raise self.func(text)
        self.func(text)

    def return_str(self, text):
        return f"\x1b[{self.config}m{text}\x1b[0m"

    @staticmethod
    def help():

        base_config = "\x1b[1;3;40;97"
        border = "~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~\n\n"
        intro = f"{base_config};4mHello and thank you for using xLog!\n\x1b[0m"

        print(intro)

        def color_prompt(context):
            bg_shift = 0

            colors = [
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "purple",
                "cyan",
                "white",
            ]

            colors = (color for color in colors)

            if context == "bg":
                bg_shift = 10

            msg = ""
            msg_hi = ""
            for code in range(30 + bg_shift, 38 + bg_shift):
                color = next(colors)
                if code == 30:
                    msg += f" {base_config};{code};{107}m{color}: {code}\x1b[0m{base_config}m\n"
                    msg_hi += f" {base_config};{code+60};{107}m{color}_hi: {code+60}\x1b[0m{base_config}m\n"
                elif code == 47:
                    msg += f" {base_config};{code};{90}m{color}: {code}\x1b[0m{base_config}m\n"
                    msg_hi += f" {base_config};{code+60};{90}m{color}_hi: {code+60}\x1b[0m{base_config}m\n"
                else:
                    msg += (
                        f" {base_config};{code}m{color}: {code}\x1b[0m{base_config}m\n"
                    )
                    msg_hi += f" {base_config};{code+60}m{color}_hi: {code+60}\x1b[0m{base_config}m\n"

            hi = 'You also have a choice of "High Intensity" (hi) colors:\n'

            return msg + "\n\n" + hi + msg_hi + "\n"

        option = f"{base_config}mChoose one of the following options for details on options and implementation:\n\n"
        option += "-" + f"{'foreground (fg)': >20}\n"
        option += "-" + f"{'background (bg)': >20}\n"
        option += "-" + f"{'style (st)': >20}\n"
        option += "-" + f"{'rgb (rgb)': >20}\n"
        option += "-" + f"{'255-color (255)': >20}\n"
        option += "-" + f"{'func (f)': >20}\n\n"
        option += "** NOTE: Some style and functionalities may not work on certain terminals! **"
        option += "\n\nor alternatively, you can quit (q)\n\n"

        while True:
            go_back = False

            choice = input(option)
            choice = choice.lower()

            if choice in ("fg", "foreground"):
                msg = "\n\n" + border
                msg += "Here are the foreground color options:\n"
                msg += color_prompt("fg")
                msg += "You can set the foreground color setting the fg parameter in the following ways:\n\n"
                msg += 'prompt = xLog(fg="red") ~OR~ prompt = xLog(fg=31)\n\n'
                msg += 'prompt("Hello World!")\n'
                msg += f"> {base_config};31mHello World!{base_config}m\n"
                msg += 'You can do the same with "high intensity" (hi) colors like this:\n\n'
                msg += (
                    'prompt = xLog(fg="red_hi") # append color name with _hi\n'
                )
                msg += 'prompt("Hello World!")\n'
                msg += f"> {base_config};91mHello World!{base_config}m\n\n"
                msg += border
                print(msg)

            elif choice in ("bg", "background"):
                msg = "\n\n" + border
                msg += "Here are the background color options:\n"
                msg += color_prompt("bg")
                msg += "You can set the foreground color setting the bg parameter in the following ways:\n\n"
                msg += (
                    'prompt = xLog(bg="red") ~OR~ prompt = xLog(bg=41)\n'
                )
                msg += 'prompt("Hello World!")\n'
                msg += f"> {base_config};41mHello World!{base_config}m\n\n"
                msg += 'You can do the same with "high intensity" (hi) colors like this:\n\n'
                msg += (
                    'prompt = xLog(fg="red_hi") # append color name with _hi\n'
                )
                msg += 'prompt("Hello World!")\n'
                msg += f"> {base_config};101mHello World!{base_config}m\n\n"
                msg += border
                print(msg)

            elif choice in ("st", "style", "styles"):
                msg = "\n\n" + border
                msg += "Here are your style options:\n\n"
                msg += f" \x1b[40;97;1mbold: 1\x1b[0m\n"
                msg += f" \x1b[40;2mdim: 2\x1b[0m\n"
                msg += f" \x1b[40;97;3mitalic: 3\x1b[0m\n"
                msg += f" \x1b[40;97;4munderline: 4\x1b[0m\n"
                msg += f" \x1b[40;97;5mblinking: 5\x1b[0m\n"
                msg += f" \x1b[40;97;9mstrikethrough: 9\x1b[0\n\n"

                msg += "You can one choose particular font style by setting the style parameter in the following ways\n\n"
                msg += 'prompt = xLog(style="underline") ~OR~ prompt = xLog(style=4)\n'
                msg += 'prompt("Hello World!")\n'
                msg += f"> {base_config};4mHello World!\x1b[0m{base_config}m\n\n"
                msg += "But you can also pass in several style fonts by using a list (or any iterable):\n\n"
                msg += 'prompt(style=["underline", "strikethrough"]) ~OR~ prompt(style=[4, 9]) ~OR EVEN~ prompt(style=[4, "strikethrough"])\n'
                msg += f"> {base_config};4;9mHello World!\x1b[0m{base_config}m\n\n"
                msg += border
                print(msg)

            elif choice == "rgb":
                msg = "\n\n" + border
                msg += "You can use RGB values setting the fg and bg parameters to tuples of the form (r, g, b) \n"
                msg += "where r, g and b are the rgb values between 0 and 255 (inclusive)\n\n"
                msg += "prompt = xLog(fg=(255,0,0), bg=(0,0,255))\n"
                msg += 'prompt("Hello World!")\n'
                msg += (
                    f"> \x1b[38;2;255;0;0;48;2;0;0;255mHello World!{base_config}m\n\n"
                )
                msg += border
                print(msg)

            elif choice == "255":
                msg = "\n\n" + border
                msg += "You need to use the fg_255 (foreground) and bg_255 (background) parameters for 255-color palette\n\n"
                msg += "prompt = xLog(fg_255=196, bg_255=21)\n"
                msg += 'prompt("Hello World!")\n'
                msg += f"> \x1b[38;5;196;48;5;21mHello World!{base_config}m\n\n"
                msg += border
                print(msg)
            elif choice in ("f", "func"):
                msg = "\n\n" + border
                msg += "You can set your own console logging function by using the func parameter\n\n"
                msg += "import logging\n"
                msg += 'prompt = xLog(fg="red", func=logging.warning)\n'
                msg += 'prompt("Oh no, something is not quite right!")\n'
                msg += f"> WARNING:root:{base_config};31mOh no, something is not quite right!\x1b[0m{base_config}m\n\n"

                msg += "You can also raise errors using func!\n\n"
                msg += "class CustomError(Exception): # You must inherit from Exception for this to work\n"
                msg += "    pass\n\n"
                msg += 'prompt = xLog(fg="red", func=CustomError)\n'
                msg += 'prompt("This is a custom error!")\n'
                msg += "... (traceback)\n"
                msg += f"> __main__.CustomError: {base_config};31mThis is a custom error!\x1b[0m{base_config}m\n\n"
                msg += border
                print(msg)
            elif choice in ("q", "quit"):
                break
            else:
                go_back = True
                print("\nSorry, I didn't quite get that\n\n")

            if not go_back:
                choice = input(
                    'Press enter to continue or "quit" (q) and enter to exit\n\n'
                )

            if choice in choice in ("q", "quit"):
                break

        print("Goodbye and good luck!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("help", "--help"):
        xLog().help()
