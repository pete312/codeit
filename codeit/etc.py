import subprocess, os
from copy import deepcopy


class AttrDict(dict):
    '''
    Converts a dictionary into a an object that can be referenced with the dot :code:`.` operator. ::
    
    >>> obj = AttrDict({'a':1, 'b':2})
    >>> obj.a
    1
    >>> obj
    {'a': 1, 'b': 2}
    >>> obj.c = 3
    >>> obj
    {'a': 1, 'b': 2, 'c': 3}

    '''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class indir:
    '''
    indir switches context within a directory using the with statement ::

        with indir('/tmp'):
            open('tmpfile', 'w').write('test\n')
    '''
    def __init__(self, new_dir):
        self.new_dir = new_dir
        self.old_dir = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *a):
        os.chdir(self.old_dir)


def shell(cmd, warn=True, pipe=None, success_codes=[0]):
    '''
    ergonomic system call wrapper returning an executed system command.
        
    :param cmd:   Shell command to run.
    :param warn:  do not bail if this is True
    :param pipe:  if True buffer stderr and stdout
    
    :param success_codes:  list of codes that are non failures (cmp, diff, etc)
            
        :ref:  http://www.tldp.org/LDP/abs/html/exitcodes.html
            
         * 1       - Catchall for general errors
         * 2       - Misuse of shell builtins (according to Bash documentation)
         * 126     - Command invoked cannot execute
         * 127     - “command not found”
         * 128     - Invalid argument to exit
         * 128+n   - Fatal error signal “n”  -- kill -9 $PPID returns 137 (128 + 9) 
         * 130     - Script terminated by Control-C
         * 255\*   - Exit status out of range
                        
    :return: an instance of subprocess.CompletedProcess with extra attributes
       
        failed       True if failed test of success_codes
        return_code  copy of returncode
        out          copy of stdout
        err          copy of stderr
     
    Example prints to stdout and throws if garbage is not present ::
     
        shell('rm -r /tmp/garbage')
        
    Example pipe output and does not trow on error::
    
        if shell('rm -r /tmp/garbage', warn=True, pipe=True).failed:
            print ("garbage not found")
            
    Example define multiple success conditions. Bails if return codes are not part of a success list ::
    
        if shell('cmp file1 file2', success_codes=[0,1]).return_code == 0:
            print('same content')
        else:
            print('files differ')
    '''
    if pipe:
        p = subprocess.run(cmd, shell=True, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.run(cmd, shell=True, encoding='utf8')
    setattr(p, "failed", p.returncode not in success_codes) 
    setattr(p, "return_code", p.returncode)
    setattr(p, "out", p.stdout) 
    setattr(p, "err", p.stderr)
    setattr(p, "text", f"-cmd({cmd})\nexit({p.returncode}) success is {not p.failed}\n:out:\n-----\n{p.stdout}\n:err:\n-----\n{p.stderr}" )
    
    if p.failed and warn == False:
        raise RuntimeError(f"Failed:{cmd} exit {p.return_code}\nout:\n{p.out}err:\n{p.err}\n")
    return p
    
    
def humanize(val, scale='U', prec=2):
    """
    Convert a value to a string value ... eg 12.4 M or 12.4 Mil 
    val  : numeric value to be converted to human readable string value 
    scale: initial scale shows what the val is in.  The output will be multiples of this.
           B = Bytes, K = Kilobytes, 
           U = Units, Tho, Mil, Trl 
           >>> humanize(192000000)
           '192 Mil'

    """
    set1 = 'BKkMGT'
    set2 = 'Tho Mil Bil Trl U'.split()
    
    if precision:
        fmt=f{f'.{prec}f'}
    else:
        fmt=f{f'f'}
    
    if scale in set1:
        _scale = {'':1,'B':1,'K':1000,'M':1000 ** 2,'G':1000 ** 3,'T':1000 ** 4}
        val = val * _scale[scale]
        human_readable_val = val 
        if val / _scale['K'] >= 1.0:
            human_readable_val = f"{val/_scale['K']:{fmt}}K"
            human_readable_val = human_readable_val.replace('.00K', 'K')
        if val / _scale['M'] >= 1.0:
            human_readable_val = f"{val/_scale['M']:{fmt}}M"
            human_readable_val = human_readable_val.replace('.00M', 'M')
        if val / _scale['G'] >= 1.0:
            human_readable_val = f"{val/_scale['G']:{fmt}}G"
            human_readable_val = human_readable_val.replace('.00G', 'G')
        if val / _scale['T'] >= 1.0:
            human_readable_val = f"{val/_scale['T']:{fmt}}T"
            human_readable_val = human_readable_val.replace('.00T', 'T')
    elif scale in set2:
        _scale = {'':1,'U':1,'Tho':1000,'Mil':1000000,'Bil': 1000000000,'Trl':1000000000000}
        val = val * _scale[scale]
        human_readable_val = val 
        if val / _scale['Tho'] >= 1.0:
            human_readable_val = f"{val/_scale['Tho']:{fmt}} Tho"
            human_readable_val = human_readable_val.replace('.00 Tho', ' Tho')
        if val / _scale['Mil'] >= 1.0:
            human_readable_val = f"{val/_scale['Mil']:{fmt}} Mil"
            human_readable_val = human_readable_val.replace('.00 Mil', ' Mil')
        if val / _scale['Bil'] >= 1.0:
            human_readable_val = f"{val/_scale['Bil']:{fmt}} Bil"
            human_readable_val = human_readable_val.replace('.00 Bil', ' Bil')
        if val / _scale['Trl'] >= 1.0:
            human_readable_val = f"{val/_scale['Trl']:{fmt}} Trl"
            human_readable_val = human_readable_val.replace('.00 Trl', ' Trl')
    

    return human_readable_val
    
    
    
import math
millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n,fmt=''):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
    
    
    
if __name__ == "__main__":
    
    from display import *
    
    k12 = 1024 * 12
    k12_2 = 1024 * 12 + 200
    for v in [k12, k12_2]:
        label(f'{v} B', humanize(v, 'B'))
        label(f'{v} K', humanize(v, 'K'))
        label(f'{v} U', humanize(v, 'U'))
        label(f'{v} Tho', humanize(v, 'Tho'))
        label(f'{v} Mil', humanize(v, 'Mil'))
    