codeit
======


Tools for building debugging and maintaining code.

label
-----
    
    a breakpointable inline print decorator will label data items before using the data. 
        
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
    
    inline print decorator same as label (minus the label) will peek at a value before using it

view
----

    inline print decorator will view a block of data with conditional suppression and breakpoint ability

sample
------
    
    grab a sample of a big dataset (works on list like or dict type data).

tabulate
-------- 

    decorator for tabulate 
    