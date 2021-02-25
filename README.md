codeit
======


Use codeit to aid code writing by using inline data watch functions to colorize and visualize data with optional breakpoints. There is a helper to make shell commands easier and table creation. 

view, label and peek perform a passthough print that outputs the line number of the data.

label
-----
    
A breakpointable inline print decorator will label data items before using the data. 
        
        mylist = [label('mod 2', i) for i in range(12) if i % 2]
        
        output: 
        1   : mod 2:   1
        1   : mod 2:   3
        1   : mod 2:   5
        1   : mod 2:   7
        1   : mod 2:   9
        1   : mod 2:   11
        
peek
----
    
Inline print decorator same as label (minus the label) will peek at a value before using it

view
----

view acts the same as label but it output format is different 

sample
------
    
Grab a sample of a big dataset (works on list like or dict type data).

tabulate
-------- 

Extended functionality for tabulate to pick columns to display in the table as well as line number location and labeling. 
    
    
shell
-----
    
    ergonomic system call wrapper returning an executed system command.
        
    :param cmd:      Shell command to run.
    :param warn:     Don't bail if this is True
    :param capture:  buffer stderr and stdout
    
    :param success_codes: numeric exit codes that mean success. Works with commands that deliver non zero exit codes (cmp, diff, etc)
        
        Some standard exit codes.     
            
         * 1       - Catchall for general errors
         * 2       - Misuse of shell builtins (according to Bash documentation)
         * 126     - Command invoked cannot execute
         * 127     - “command not found”
         * 128     - Invalid argument to exit
         * 128+n   - Fatal error signal “n”  -- kill -9 $PPID returns 137 (128 + 9) 
         * 130     - Script terminated by Control-C
         * 255\*   - Exit status out of range
         
        :ref:  http://www.tldp.org/LDP/abs/html/exitcodes.html
                        
    :returns: an instance of subprocess.CompletedProcess with extra attributes added.
       
        failed       True retrun code does not meet success_codes condtions
        return_code  copy of returncode
        out          copy of stdout
        err          copy of stderr
        text         a formatted summary of the command output. 
     
    Example: prints to stdout and throws if the file garbage is not present ::
     
        shell('rm -r /tmp/garbage', capture=False)
        
    Example: captures output and does not trow on error::
    
        if shell('rm -r /tmp/garbage', warn=True).failed:
            print ("garbage not found")
            
    Example define multiple success conditions. Bails if return codes are not part of a success list ::
    
        if shell('cmp file1 file2', success_codes=[0,1]).return_code == 0:
            print('same content')
        else:
            print('files differ')

humanize
--------


AttrDict
--------

A dictionary that also has attribute accessors ::

    >>> fruit = etc.AttrDict()
    >>> print(fruit)
    {}
    
    >>> fruit.apple = 'green'
    >>> print(fruit)
    {'apple': 'green'}
    
    >>> fruit['grape'] = 'black'
    >>> print(fruit)
    {'apple': 'green', 'grape': 'black'}
    
    >>> for name, color in fruit.items(): print(name, color)
    ...
    grape black
    apple green

    
    >>> del fruit.apple
    >>> print(fruit)
    {'grape': 'black'}


from https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
 

    