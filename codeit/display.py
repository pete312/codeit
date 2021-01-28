from inspect import currentframe
from pprint import pformat
import sys
from tabulate import tabulate as _tabulate


WHITE_BLACK = [231,188,145,102,59,16]
WHITE_RED_BLACK     = [231,224,217,210,203,196,160,124,88,52,16]
WHITE_YELLOW_BLACK = [231,230,229,228,227,226,184,142,100,58,16]
WHITE_GREEN_BLACK   = [231,194,157,120,83,46,40,34,28,22,16]
WHITE_CYAN_BLACK    = [231,195,159,123,87,51,44,37,30,23,16]
WHITE_BLUE_BLACK    = [231,189,147,105,63,21,20,19,18,17,16]
WHITE_MAGENTA_BLACK = [231,225,219,213,207,201,164,127,90,53,16]
GREYS = [231,255,254,253,252,251,250,249,248,247,246,245,244,243,242,241,240,239,238,237,236,235,234,233,232,16]
GRAYS = GREYS

RESET = "\x1b[0m"

COLOR = {
    "REDS" : WHITE_RED_BLACK,
    "YELLOWS" : WHITE_YELLOW_BLACK,
    "GREENS" : WHITE_GREEN_BLACK,
    "CYANS" : WHITE_CYAN_BLACK,
    "BLUES" : WHITE_BLUE_BLACK,
    "MAGENTAS" : WHITE_MAGENTA_BLACK,
    "GREYS" : GREYS,
    "GRAYS" : GREYS
}

plus_minus=chr(0x00B1)

def red(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in red color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = WHITE_RED_BLACK
    assert -5 <= tone <= 5  , f"tone can be {plus_minus} 5 but was {tone}"
    tone = 5 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"

def blue(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in red color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = WHITE_BLUE_BLACK
    assert -5 <= tone <= 5  , f"tone can be {plus_minus} 5"
    tone = 5 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"
    
def green(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in green color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = WHITE_GREEN_BLACK
    assert -5 <= tone <= 5  , f"tone can be {plus_minus} 5"
    tone = 5 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"
    
def yellow(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in yellow color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = WHITE_YELLOW_BLACK
    assert -5 <= tone <= 5  , f"tone can be {plus_minus} 5"
    tone = 5 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"
    
def magenta(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in magenta color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = WHITE_MAGENTA_BLACK
    assert -5 <= tone <= 5  , f"tone can be {plus_minus} 5"
    tone = 5 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"

def cyan(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in cyan color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = WHITE_CYAN_BLACK
    assert -5 <= tone <= 5  , f"tone can be {plus_minus} 5"
    tone = 5 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"
    
def grey(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in grey color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = GREYS
    assert -12 <= tone <= 13 , "tones limited between -12 and 13"
    tone = 13 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"
    
def gray(s, tone=0, reverse=False, reset=RESET):
    ''' decorate text in gray color
        s : str(text) 
        tone : color tone -5 to 5 default( 0 )
        reverse : reverse text color. default ( False )
        reset :  color code to reset text to. default( default terminal color ). 
    '''
    COL = GREYS
    assert -12 <= tone <= 13 , "tones limited between -12 and 13"
    tone = 13 - tone
    return f"\x1b[38;5;{COL[tone]}m{s}{reset}"
    
    
def white(s, reset=RESET):
    return f"\x1b[38;5;{WHITE_BLACK[0]}m{s}{reset}"
    
def black(s, reset=RESET):
    return f"\x1b[38;5;{WHITE_BLACK[-1]}m{s}{reset}"

def fg(n):
    assert -1 < n < 256, f"{n} value outside (0,255)"
    return f"\x1b[38;5;{n}m"

def bg(n):
    assert -1 < n < 256, f"{n} value outside (0,255)"
    return f"\x1b[48;5;{n}m"
    

def exit(value=0):
    '''
    provides a line numbered exit statement to show which exit() function caused termination. Overrides built in function exit()
    '''
    last_line = getframeinfo(currentframe().f_back).lineno
    print( red(last_line), yellow('exit %s' % value))
    sys.exit(value)


def view(caption, content, color=None, file=sys.stdout, formatter=str):
    '''
    data visualizer that performs a view before use action on any variable. 
    Handy in list or dict comprensions or anywhere you need to inspect data values without a debugger.
    
    example shows inline inspection of the key and val of each filtered item
        
    data = {'key1':['val1','val2'], 'key2':['val3','val4']}
    filtered_values = {key:view(f'value of {key}', val) for key,val in data.items() if key == 'key1'}
    
    line numbered output:
    2 value of key1 ...
        val1
        val2
    ...

    '''
    
    if getattr(view, 'suppress', None) == None:
        view.suppress = []
        
    if getattr(view, 'disable', False):
        return content
        
    if caption in view.suppress:
        return content
        
    last_line = (currentframe().f_back).f_lineno

    caption_color = yellow
    if color == yellow:
        caption_color == red
    print(red(last_line), caption_color(caption),caption_color('...'), file=file)
    content_size = 0
    if isinstance(content, list) or isinstance(content, tuple):
        for i in content:
            content_size += len(str(i))
            if color:
                print(',,  ',color(i), file=file)
            else:
                print('  ',i, file=file)
    elif isinstance(content, dict):
        scontent = pformat(content)
        content_size = len(scontent)
        if color:
            print("  ", color(scontent), file=file)
        else:
            print("  ", scontent, file=file)
    elif isinstance(content, str) and len(content) < 300:
        # just do a single line entry 
        if color:
            print(color(content), file=file)
        else:
            print(content, file=file)
        return content
    else:
        content_size = len(str(content))
        if color:
            print(color(content), file=file)
        else:
            print(content, file=file)
    if content_size > 2000:
        print(caption_color('...'), red(last_line), caption_color(caption), "\n", file=file)
    else:
        print(caption_color('...'), file=file)
        
    if last_line in view.bp:
        input(f'bp line {last_line}')
    
    return content
    
    
def peek(d, color=None, formatter=str):
    '''
    decorator function that displays a value returning its contents. Will label the output with the line number. 
    color text color formatter function default None.
    formatter text formater function, default str
    '''
    last_line = (currentframe().f_back).f_lineno
    _label = f'{last_line:<-4d}:'
    if color:
        print(grey(_label), color(formatter(d)))
    else:
        print(grey(_label), formatter(d))
    if last_line in peek.bp:
        input(f'bp line {last_line}')
    return d
    
peek.bp = []


def label(caption, d, color=str, format=False):
    '''
    print a label with the value and its line number.
    returns origional content unless format option is True.
    color: colorizer function eg( red, blue etc.) defaults to no color 
    format <True|False> will return formatted text
    
    if label.bp contains a number that matches the line number of 
    the label function a breakpoint like stop will occur 
    requiring <Enter> key to be pressed to continue. 
    
    '''
    if isinstance(caption,str) and caption[-1] == '\n':
        caption = yellow(f'{caption[:-1]} ..\n' )
    else:
        caption = yellow(f'{caption} ..')
    last_line = (currentframe().f_back).f_lineno 
    _label = f'{last_line:<-4d}: {caption}'
    if isinstance(d, str):
        if format:
            return grey(_label) + " " + color(d)
        else:
            print(grey(_label), color(d))
    else:
        if format:
            return grey(_label) + " " + color(pformat(d))
        else:
            print(grey(_label), color(pformat(d)))
    if last_line in label.bp:
        input(f'bp line {last_line}')
    return d
    
label.bp = []

def tabulate(grid, *args, pick=[], headers=[], label='', verbose=False, tablefmt='psql', disable_numparse=True, **kwargs):
    '''
    Tabulate presentation wrapper extends tabulate to be able to pick column numbers to view and supports table label and line number location.
    
    '''
    width = 0 if not grid else len(grid[0])
    
    if verbose or label:
        print((currentframe().f_back).f_lineno , " :", label)
    if pick and headers and (len(pick) > len(headers)):
        raise ValueError(f"number of cols in pick {len(pick)} exceeds headers {len(headers)}")
    if pick:
        _s = sorted(pick)
        _min,_max = _s[0], _s[-1]
        if (1 + _max > width) or (_min < -width ):
            raise ValueError(f"column pick exceeds the width of grid. Value must be between {-width} and {width - 1}")
         
        _grid = [[row[i] for i in pick] for row in grid]
        return _tabulate(_grid, *args, tablefmt=tablefmt, headers=headers, disable_numparse=disable_numparse, **kwargs)
    if headers and width != len(headers):
        raise ValueError("headers do not match the the width of grid. Did you forget to set a pick range?")
        
    return _tabulate(grid, *args, tablefmt=tablefmt, headers=headers, disable_numparse=disable_numparse, **kwargs)


def sample(obj, maxdepth=2, formatter=pformat):
    '''
    returns a sample of the data of a list or dictionary
    '''
    if isinstance(obj, list):
        samp = []
        for i, val in enumerate(obj,1):
            if i > maxdepth:
                break
            samp.append(deepcopy(val))
    else:
        samp = {}
        for i, key in enumerate(obj,1):
            if i > maxdepth:
                break
            samp[key] = deepcopy( obj[key] )
    return samp

    
if __name__ == "__main__":
    color_func = red, yellow, green, magenta, cyan, blue, grey
    color_names = 'reds yellows greens magentas cyans blues'.split()
    
    colors = zip(color_names, color_func)
    
    print("test colors")
    
    for name, color in colors:
        for i in range(-5,6): 
            print(f"{i:3d}",color(f"{name} No.{i:3d}", i))
            
    for i in range(-12,14):
        print(f"{i:3d}", grey(f"greys No.{i:3d}", i))
        
    
    grid = [color_names, color_names, color_names]
    
    print(tabulate(grid, label="tabulate test", headers=color_names))
    
    print(tabulate(grid, label="print columns 2 and 4", headers=color_names, pick=[2,4]))
    
    grid = []
    for i in range(-5,6): 
        row = [f"{i:3d}"]        
        for name, color in zip(color_names, color_func):
            row.append(color(f"{name}", i))
        grid.append(row)
    
    print(tabulate(grid, label=f'color table demo.. e.g print(red("red")) = {red("red")}, print(red("light red", 3)) = {red("light red ", 3)}', headers=['tone'] +color_names))
        
    
    
    