#!/usr/bin/python
'''
Created on Oct 22, 2011
Converted to cross platform July, 2013.

@author: Rod Hinman

Assists easy counting of white blood cells under a microscope.
Written for Python 2 or 3.

Version 0.01 2011.11.17: Basic functionality, works on XP, but not Win7.
Version 0.02 2013-07-30: Cross platform for Win, Mac, and Linux
  (though beep doesn't work on Ubuntu Linux)

Things to add:
Put results in place instead of scrolling (msvcrt equiv. of curses?)
'''
from __future__ import print_function # So we can print('') rather than print '' in Python 2. 
#import msvcrt
import sys
import time
try:
    import winsound
    def beeper():
        winsound.Beep(440,500)
except:
    import curses
    def beeper():
        curses.beep()



class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys, termios # import termios now or else you'll get the Unix version on the Mac

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        if sys.version_info < (3, 0):
            return msvcrt.getch()
        else:
            return msvcrt.getwch() # Python 3, strings are Unicode, so we need to get a wide character.

def cell_counter(stdscr): # Need a variable for curses.wrapper() to pass standard screen.
    if sys.platform.startswith('win32'):
        ret = ''
    else:
        ret = '\r'
        curses.nocbreak()
        stdscr.refresh() # Need to do this beforehand, for some reason.
#        curses.nl() # I don't know why curses.nl() doesn't seem to work,
                     # but unless we add carriage return explicitly, we get stairstep.
    answer = 'n'
    inkey = _Getch()
    while answer != 'P':
        # Must kill the window or hit P to quit.
        # Initialize counter variables.
        seg = 0
        band = 0
        lymph = 0
        eos = 0
        mono = 0
        total = 0
        # Print instructions.
        print('Cell Counter version 0.02' + ret)
        print('Hit "a" for segs.' + ret)
        print('Hit "s" for bands.' + ret)
        print('Hit "d" for lymphs.' + ret)
        print('Hit "f" for eos.' + ret)
        print('Hit spacebar for mono.' + ret)
        print('Hit "q" to quit counting before total = 100.' + ret)
        # Loop until 100 items have been counted.
        while total < 100:
            if sys.platform.startswith('win32'):
                pass
            else:
                stdscr.refresh() # Refresh after printing and before asking for input.
            c = inkey()
            if c == 'a' or c == 'A':
                seg += 1
            elif c == 's' or c == 'S':
                band += 1
            elif c == 'd' or c == 'D':
                lymph += 1
            elif c == 'f' or c == 'F':
                eos += 1
            elif c == ' ':
                mono += 1
            elif c == 'q' or c == 'Q':
                break
            else:
                continue # Ignore every other key.
            total += 1
            if total == 50:
                beeper()
            print('\nInterim results:' + ret)
            print('(a) cell type seg:   %3d counts, %3d%% %s' % (seg, (100*seg)/total, ret))
            print('(s) cell type band:  %3d counts, %3d%% %s' % (band, (100*band)/total, ret))
            print('(d) cell type lymph: %3d counts, %3d%% %s' % (lymph, (100*lymph)/total, ret))
            print('(f) cell type eos:   %3d counts, %3d%% %s' % (eos, (100*eos)/total, ret))
            print('( ) cell type mono:  %3d counts, %3d%% %s' % (mono, (100*mono)/total, ret))
            print('Total counts: %3d %s' % (total, ret))
        # Print results.
        print('\n\n----------------' + ret)
        print('----------------' + ret)
        if total != 0:
            # Prevent divide by zero error if user hits 'q' before entering any cells.
            if total == 100:
                print('    Final results.' + ret)
                beeper()
                time.sleep(0.1)
                beeper()
            else:
                print('    Results based on partial sample:' + ret)
            print('    cell type seg:   %3d counts, %3d%% %s' % (seg, (100*seg)/total, ret))
            print('    cell type band:  %3d counts, %3d%% %s' % (band, (100*band)/total, ret))
            print('    cell type lymph: %3d counts, %3d%% %s' % (lymph, (100*lymph)/total, ret))
            print('    cell type eos:   %3d counts, %3d%% %s' % (eos, (100*eos)/total, ret))
            print('    cell type mono:  %3d counts, %3d%% %s' % (mono, (100*mono)/total, ret))
            print('    Total cells counted: %3d %s' % (total, ret))
        # A little delay to allow fingers to come off the keyboard.
        time.sleep(0.5)
        # Wait for input so user can record the results.
        print('\nHit any key to go again, P to exit program.' + ret)
        if sys.platform.startswith('win32'):
            pass
        else:
            stdscr.refresh()	
        answer = inkey()
        print('\n\n\n', ret)
        time.sleep(0.5)



if __name__ == '__main__':
    if sys.platform.startswith('win32'):
        cell_counter(None)
    else:
        curses.wrapper(cell_counter)

