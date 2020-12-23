codeit
======


Use codeit to aid code writing by using inline watch functions to colorize and visualize data. There is a helper to make shell commands easier and table creation 

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

Inline print decorator will view a block of data with conditional suppression and breakpoint ability

sample
------
    
Grab a sample of a big dataset (works on list like or dict type data).

tabulate
-------- 

Extended functionality for tabulate to pick columns to display in the table as well as line number location and labeling. 
    
    
shell
-----

humanize
--------



Takes  
    