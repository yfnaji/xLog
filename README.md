# xLog
xLog allows you to output logs in your console or terminal with a little _zing_.
This package provides an easy-to-use interface to color, _italicize_, **bolden**, underline (and much more!) your python logs by simply setting exactly what you need with an `xLog` class.

This documentation will highlight how you can do this in the sections below - but if you are too excited to wait, you can clone the package now and run `python3 xlog.py --help` which will provide a helpful interactive interface which allows you to navigate to any configuration you wish to try out.

<h1>Contents</h1>

1. [fg (foreground)](#fg)
    * [Escape Codes](#fg-escape)
    * [RGB](#fg-rgb)
    * [8-bit Colors](#fg-8bit)
2. [bg (background)](#bg)
    * [Escape Codes](#bg-escape)
    * [RGB](#bg-rgb)
    * [8-bit Colors](#bg-8bit)
3. [styles](#styles)
4. [func](#func)
    * [Output](#output)
    * [Errors](#errors)
5. [Return a string](#return-str)
6. [Additional Notes](#additional-notes)


<h1 id="fg">fg (foreground)</h1>

The fg parameter allows you to set the color of the text. There are several ways to do this elaborated below:

<h2 id="fg-escape">Escape Codes</h2>

Here is the table of escape codes available:


<img width="395" alt="Screenshot 2022-12-19 at 01 04 32" src="https://user-images.githubusercontent.com/59436765/208329531-3b56cde3-62a5-49f3-b732-2676c46af92f.png">


To implement any of these colors in your prompt, you can set `fg` to the name of the color (on the left) **_or_** the escape code (on the right).

For example:

```
from xlog import xLog

prompt = xLog(fg="red") # Or you can set `fg=31`
prompt("I am in red!")
```

<img width="93" alt="fg_red" src="https://user-images.githubusercontent.com/59436765/208327076-70f6490c-6689-4138-a977-30c29f3f225d.png">


<h2 id="fg-rgb">RGB</h2>

To use the RGB color scheme, you can pass a tuple of length 3 with the RGB values.

```
from xlog import xLog

prompt = xLog(fg=(31, 165, 161)) # A kind of teal color
prompt("I was made by using RGB colors!")
```

<img width="229" alt="Screenshot 2022-12-19 at 00 19 40" src="https://user-images.githubusercontent.com/59436765/208327642-bf95d711-1a93-4071-9869-2a108d872156.png">


<h2 id="fg-8bit">8-bit Colors</h2>
Finally, we can use 8-bit colors, defined in a range from 0 to 255:

<img width="594" alt="8bit" src="https://user-images.githubusercontent.com/59436765/208327378-f67e1c05-696f-4d8f-8d48-b4bcebf52d4c.png">


**_NOTE_**: When using an 8-bit color for the foreground, you must use the `fg_255` parameter (as opposed to `fg`). If you set `fg` at the same time, `fg_255` will be used instead. 

Example with 8-bit coloring:

```
from xlog import xLog

prompt = xLog(fg_255=214)
prompt("I would call this color pumpkin!")
```

<img width="221" alt="Screenshot 2022-12-19 at 00 20 43" src="https://user-images.githubusercontent.com/59436765/208327402-390a9b49-a2ed-4896-9381-5f55264c80f0.png">


<h1 id="bg">bg (background)</h1>

The bg parameter will set the background color of the string you pass to the `xLog` object.

<h2 id="bg-escape">Background Escape Codes</h2>

Your background color escape code options are:

<img width="395" alt="Screenshot 2022-12-19 at 01 05 01" src="https://user-images.githubusercontent.com/59436765/208329566-ff36391c-e00a-449f-b2f8-1b892588c1a5.png">

Implementing background escape code colors is almost identical to setting the foreground colors - you just use the `bg` parameter instead to set the background color:

```
from xlog import xLog

prompt = xLog(bg="red_hi") # can equally do `bg=101`
prompt("I am red, red is me")
```

<img width="141" alt="Screenshot 2022-12-19 at 00 21 20" src="https://user-images.githubusercontent.com/59436765/208327451-e9a889f9-d060-4f65-ba12-e9c7e1f6e562.png">


<h2 id="bg-rgb">RGB</h2>

Similar to setting the foreground color with RGB values, you can pass a tuple of length 3 to `bg` to set the background color:

```
from xlog import xLog

prompt = xLog(bg=(135,0,255))
prompt("A cool background color!")
```

<img width="182" alt="Screenshot 2022-12-19 at 00 21 41" src="https://user-images.githubusercontent.com/59436765/208327469-f4321534-e5b1-41f8-b0b1-490a448f6f05.png">


<h2 id="bg-8bit">8-bit Colors</h2>

Again, using the 8-bit color scheme for the background color is very similar to that of the foreground except that you must use the `bg_255` parameter:

```
from xlog import xLog

prompt = xLog(bg_255=33)
prompt("I'm blue da ba dee da ba dye!")
```

<img width="211" alt="Screenshot 2022-12-19 at 00 38 48" src="https://user-images.githubusercontent.com/59436765/208328133-c8a234ad-61ef-43d3-80a2-68c4392fae93.png">


<h1 id="styles">styles</h1>

The style parameter allows you to print various font styles such as **bold**, *italic* etc.

Your escape code style options are:

![styles_table](https://user-images.githubusercontent.com/59436765/208328766-0f4f58bd-1b03-4318-b15b-7875aaf5dde3.gif)


_Note: this table may be expanded if necessary or upon request_

We can set one particular style in the following way:

```
from xlog import xLog

prompt_1 = xLog(style=1) # you can also set style="bold"
prompt_1("Look, i'm bold!")
```


<img width="123" alt="Screenshot 2022-12-19 at 00 22 09" src="https://user-images.githubusercontent.com/59436765/208327540-709a6b94-9001-4c97-a8c1-d6aee82106a5.png">

You can also employ several different styles by setting the `styles` parameter to a set, list or tuple containing the styles name or escape codes:

```
from xlog import xLog

prompt = xLog(style=[1, "italic", 4]) # Yes, you can mix and match using int and strings!
prompt("I'm bold, italic and underlined!")
```

<img width="230" alt="Screenshot 2022-12-19 at 00 22 32" src="https://user-images.githubusercontent.com/59436765/208327552-802155cf-ef33-406f-ba73-8d64e31d4613.png">


<h1 id="func">func</h1>

<h2 id="output">Output</h2>

You can specify which function you want to use to output your prompts using the `func` parameter. The built-in `print` function is used by default.

For example, if we want to use `logging.warning`:

```
from xlog import xLog
import logging

prompt = xLog(fg="green", func=logging.warning)
prompt("I am the Grinch!")
```

<img width="224" alt="Screenshot 2022-12-19 at 00 22 48" src="https://user-images.githubusercontent.com/59436765/208327583-fbfff654-72cf-4348-b97e-ba5132a7b6e9.png">


<h2 id="errors">Raising Errors</h2>

You can also use `xLog` to raise errors by setting `func` to an exception class:

```
from xlog import xLog

class CustomError(Exception):
    pass

err_prompt = xLog(bg=101, func=CustomError)
err_prompt("This custom error has been raised!")
```

<img width="400" alt="Screenshot 2022-12-19 at 00 23 05" src="https://user-images.githubusercontent.com/59436765/208327597-5b5d5724-3d22-498c-bcaf-c7b6e2b5f379.png">

_Note: for this to work, the custom error **must** inherit from the `Exception` class_

<h2 id="return-str">Returning a string</h2>

If you do not feel like printing your (cooler looking) logs just yet, you have the option to save the string (along with the set colors and styles) to be printed later if you wish.

You can do this with the `return_str` method in the following way:

```
from xlog import xLog

prompt = xLog(fg="red_hi", bg=44, styles = [1, "italic"])
xlog_str = prompt.return_str("I will be printed later, and it will be great!")

# Do whatever you like in-between

print(xlog_str)
```

<img width="303" alt="Screenshot 2022-12-19 at 00 23 27" src="https://user-images.githubusercontent.com/59436765/208327613-f8bbf929-27a1-4888-855b-8261d5d0cd02.png">


<h1 id="additional-notes">Additional Notes</h1>

Thank you for making it this far!

I am open to amendments and suggestions, so feel free to drop a message or write a comment and I will get around to addressing whatever you have raised.