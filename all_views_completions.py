# Extends Sublime Text autocompletion to find matches in all open
# files. By default, Sublime only considers words from the current file.

import sublime_plugin
import sublime
import re
import time
import datetime
import os
from os.path import basename

# limits to prevent bogging down the system
MIN_WORD_SIZE = 3
MAX_WORD_SIZE = 50

MAX_VIEWS = 20
MAX_WORDS_PER_VIEW = 100
MAX_FIX_TIME_SECS_PER_VIEW = 0.01


# Debugging
startTime = datetime.datetime.now()
print_debug_lastTime = startTime.microsecond

# Enable editor debug messages: (bitwise)
#
# 0  - Disabled debugging.
# 1  - Errors messages.
# 2  - Outputs when it starts a file parsing.
# 4  - General messages.
# 8  - Analyzer parser.
# 15 - All debugging levels at the same time.
g_debug_level = 0

g_word_autocomplete = False
g_is_amxmodx_enabled = False
g_use_all_autocomplete = False


def plugin_loaded():

    on_settings_modified();

    userSettings = sublime.load_settings("Preferences.sublime-settings")
    amxxSettings = sublime.load_settings("amxx.sublime-settings")

    amxxSettings.add_on_change('amxx', on_settings_modified)
    userSettings.add_on_change('Preferences', on_settings_modified)

def is_amxmodx_file(view) :
    return view.match_selector(0, 'source.sma')

def is_package_enabled( userSettings, package_name ):

    print_debug(1, "is_package_enabled = " + sublime.packages_path()
            + "/All Autocomplete/ is dir? " \
            + str( os.path.isdir( sublime.packages_path() + "/" + package_name ) ))

    print_debug(1, "is_package_enabled = " + sublime.installed_packages_path()
            + "/All Autocomplete.sublime-package is file? " \
            + str( os.path.isfile( sublime.installed_packages_path() + "/" + package_name + ".sublime-package" ) ))

    ignoredPackages = userSettings.get('ignored_packages')

    if ignoredPackages is not None:

        return ( os.path.isdir( sublime.packages_path() + "/" + package_name ) \
                or os.path.isfile( sublime.installed_packages_path() + "/" + package_name + ".sublime-package" ) ) \
                and not package_name in ignoredPackages

    return os.path.isdir( sublime.packages_path() + "/" + package_name ) \
            or os.path.isfile( sublime.installed_packages_path() + "/" + package_name + ".sublime-package" )

def on_settings_modified():
#{
    print_debug( 1, "on_settings_modified" )

    global g_word_autocomplete
    global g_is_amxmodx_enabled
    global g_use_all_autocomplete

    userSettings = sublime.load_settings("Preferences.sublime-settings")
    amxxSettings = sublime.load_settings("amxx.sublime-settings")

    # When the `g_use_all_autocomplete` is set to true on the package `amxmodx`, we use this package
    # to handle all the completions on the current view file.
    g_use_all_autocomplete = amxxSettings.get('use_all_autocomplete', False)

    g_word_autocomplete  = amxxSettings.get('word_autocomplete', False)
    g_is_amxmodx_enabled = is_package_enabled( userSettings, "amxmodx" )


class AllAutocomplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):

        if not g_word_autocomplete:
            return None

        words = []

        # Limit number of views but always include the active view. This
        # view goes first to prioritize matches close to cursor position.
        other_views = [v for v in sublime.active_window().views() if v.id != view.id]
        views = [view] + other_views
        views = views[0:MAX_VIEWS]

        is_the_current_view = False
        not_always_use_autocomplete = g_is_amxmodx_enabled and not g_use_all_autocomplete

        for v in views:

            is_the_current_view = v.id == view.id

            # Avoid duplicated entries for the current view, if it is an AMXX file
            if not_always_use_autocomplete \
                    and is_the_current_view \
                    and is_amxmodx_file( v ):
                continue

            if len(locations) > 0 and is_the_current_view:
                view_words = v.extract_completions(prefix, locations[0])
            else:
                view_words = v.extract_completions(prefix)
            view_words = filter_words(view_words)
            view_words = fix_truncation(v, view_words)
            words += [(w, v) for w in view_words]

        words = without_duplicates(words)
        matches = []
        for w, v in words:
            trigger = w
            contents = w.replace('$', '\\$')
            if v.id != view.id and v.file_name():
                trigger += '\t(%s)' % basename(v.file_name())
            matches.append((trigger, contents))
        return matches


def filter_words(words):
    words = words[0:MAX_WORDS_PER_VIEW]
    return [w for w in words if MIN_WORD_SIZE <= len(w) <= MAX_WORD_SIZE]


# keeps first instance of every word and retains the original order
# (n^2 but should not be a problem as len(words) <= MAX_VIEWS*MAX_WORDS_PER_VIEW)
def without_duplicates(words):
    result = []
    used_words = []
    for w, v in words:
        if w not in used_words:
            used_words.append(w)
            result.append((w, v))
    return result


# Ugly workaround for truncation bug in Sublime when using view.extract_completions()
# in some types of files.
def fix_truncation(view, words):
    fixed_words = []
    start_time = time.time()

    for i, w in enumerate(words):
        #The word is truncated if and only if it cannot be found with a word boundary before and after

        # this fails to match strings with trailing non-alpha chars, like
        # 'foo?' or 'bar!', which are common for instance in Ruby.
        match = view.find(r'\b' + re.escape(w) + r'\b', 0)
        truncated = is_empty_match(match)
        if truncated:
            #Truncation is always by a single character, so we extend the word by one word character before a word boundary
            extended_words = []
            view.find_all(r'\b' + re.escape(w) + r'\w\b', 0, "$0", extended_words)
            if len(extended_words) > 0:
                fixed_words += extended_words
            else:
                # to compensate for the missing match problem mentioned above, just
                # use the old word if we didn't find any extended matches
                fixed_words.append(w)
        else:
            #Pass through non-truncated words
            fixed_words.append(w)

        # if too much time is spent in here, bail out,
        # and don't bother fixing the remaining words
        if time.time() - start_time > MAX_FIX_TIME_SECS_PER_VIEW:
            return fixed_words + words[i+1:]

    return fixed_words


if sublime.version() >= '3000':
    def is_empty_match(match):
        return match.empty()
else:
    def is_empty_match(match):
        return match is None


def print_debug(level, msg) :
#{
    global print_debug_lastTime
    currentTime = datetime.datetime.now().microsecond

    # You can access global variables without the global keyword.
    if g_debug_level & level != 0:

        print( "[AMXX-Editor] " \
                + str( datetime.datetime.now().hour ) + ":" \
                + str( datetime.datetime.now().minute ) + ":" \
                + str( datetime.datetime.now().second ) + ":" \
                + str( currentTime ) \
                + "%7s " % str( currentTime - print_debug_lastTime ) \
                + msg )

        print_debug_lastTime = currentTime


