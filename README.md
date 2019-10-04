All Autocomplete Sublime Text
===========================================================

Extends the default autocomplete to find matches in all open files.

By default Sublime only considers words found in the current file.

## Installation

### By Package Control

1. Download & Install **`Sublime Text 3`** (https://www.sublimetext.com/3)
1. Go to the menu **`Tools -> Install Package Control`**, then,
   wait few seconds until the installation finishes up
1. Now,
   Go to the menu **`Preferences -> Package Control`**
1. Type **`Add Channel`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
   input the following address and press <kbd>Enter</kbd>
   ```
   https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json
   ```
1. Go to the menu **`Tools -> Command Palette...
   (Ctrl+Shift+P)`**
1. Type **`Preferences:
   Package Control Settings – User`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
   find the following setting on your **`Package Control.sublime-settings`** file:
   ```js
       "channels":
       [
           "https://packagecontrol.io/channel_v3.json",
           "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json",
       ],
   ```
1. And,
   change it to the following, i.e.,
   put the **`https://raw.githubusercontent...`** line as first:
   ```js
       "channels":
       [
           "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/channel.json",
           "https://packagecontrol.io/channel_v3.json",
       ],
   ```
   * The **`https://raw.githubusercontent...`** line must to be added before the **`https://packagecontrol.io...`** one, otherwise,
     you will not install this forked version of the package,
     but the original available on the Package Control default channel **`https://packagecontrol.io...`**
1. Now,
   go to the menu **`Preferences -> Package Control`**
1. Type **`Install Package`** on the opened quick panel and press <kbd>Enter</kbd>
1. Then,
search for **`AllAutocomplete`** and press <kbd>Enter</kbd>

See also:
1. [ITE - Integrated Toolset Environment](https://github.com/evandrocoan/ITE)
1. [Package control docs](https://packagecontrol.io/docs/usage) for details.


Settings
--------

You can disable the additional autocompletion provided by this package for specific source files and even select syntax within files. In the Sublime menu go to Preferences > Package Settings > All Autocomplete > Settings – User.

Example: the following Setting would disable All Autocomplete for CSS and JavaScript code:

```
"exclude_from_completion": [
	"css",
	"js"
]
```

The names provided in this list are matched against the so-called "syntax scope" of the currently autocompleted input. For example, in a CSS file, when you start typing a new CSS class name, the syntax scope is "source.css meta.selector.css". The names you provide in the config above are partially matched against this scope. This means, you can completely disable All Autocomplete for all CSS code by specifying "css" – or you can disable it only for specific parts, for example, CSS selectors by specifying "selector.css". Or to disable completion in comments, include "comment" in the list.

Note, if you want to disable it in C source, but not in CSS, add "source.c" in the list (since "c" alone would also match css).

You can find the syntax scope of code at the current cursor position with Control+Shift+P.


LICENSE
-------

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
Version 2, December 2004

Copyright (C) 2013 Adrian Lienhard <adrian.lienhard@gmail.com>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO.
