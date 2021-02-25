import subprocess, os
from inspect import currentframe
import time


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
    
    from https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

    '''
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class in_dir:
    '''
    in_dir changes directory context while doing system commands. Example ::

        with in_dir('/tmp'):
            open('tmpfile', 'w').write('test\n')
    '''
    def __init__(self, new_dir):
        self.new_dir = new_dir
        self.old_dir = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *a):
        os.chdir(self.old_dir)


def shell(cmd, warn=True, capture=True, success_codes=[0], **kwargs):
    '''
    easy to use subprocess wrapper returning an executed system command.
    async safe but not thread safe.
        
    :param cmd:      Shell command to run.
    :param warn:     Don't bail on command failure if this is True
    :param capture:  buffer stderr and stdout to property value.
    
    :param success_codes: most unix processes return 0 when they succeed, but some (cmp, diff, etc) have non zero return values. success_codes is a list of codes that are considered as non failure. This affects shell(<cmd>).success  and shell(<cmd>).faulure states
        
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
        succeeded    just the inverse of failed
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
    '''
    if capture:
        p = subprocess.run(cmd, shell=True, encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    else:
        p = subprocess.run(cmd, shell=True, encoding='utf8')
    setattr(p, "failed", p.returncode not in success_codes) 
    setattr(p, "succeeded", not p.failed) 
    setattr(p, "return_code", p.returncode)
    setattr(p, "out", p.stdout) 
    setattr(p, "err", p.stderr)
    setattr(p, "text", f"-cmd({cmd})\nexit({p.returncode}) success is {not p.failed}\n:out:\n-----\n{p.stdout}\n:err:\n-----\n{p.stderr}" )
    
    if p.failed and warn == False:
        raise RuntimeError(f"Failed:{cmd} exit {p.return_code}\nout:\n{p.out}err:\n{p.err}\n")
    return p
    
    
    
class NoRef:
    pass 
    
def ref(obj=NoRef):
    if obj is NoRef:
       return ref.obj
    ref.obj = obj
    return obj
ref.obj = None


def humanize(val, scale='U', precision=2):
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
        fmt=f'.{precision}f'
    else:
        fmt='f'
    
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
    
def timeit(method):
    def timed(*args, **kw):
        begin = time.time()
        result = method(*args, **kw)
        if kw.get('logtime', None):
            kw.get('logtime')(f"{((currentframe().f_back).f_lineno)} {method.__name__} took {(time.time() - begin) * 1000:.2f} ms")
        else:
            print( red((currentframe().f_back).f_lineno),  yellow(f'{method.__name__}'),  f'took {(time.time() - begin) * 1000:.2f} ms')
        return result
    return timed
    
    
def hold(*a):
    if len(a) == 0: return hold.data
    hold.data = a
    if len(a) > 1:
        return hold.data
    else:
        return hold.data[0]
hold.data = None 
    
if __name__ == "__main__":
    
    from display import label, view
    from pathlib import Path
    
    k12 = 1024 * 12
    k12_2 = 1024 * 12 + 200
    label('12k in decimal', k12)
    for v in [k12, k12_2]:
        label(f'{v} B', humanize(v, 'B'))
        label(f'{v} K', humanize(v, 'K'))
        label(f'{v} U', humanize(v, 'U'))
        label(f'{v} Tho', humanize(v, 'Tho'))
        label(f'{v} Mil', humanize(v, 'Mil'))
    
    
    me = Path(__file__)
    with indir(me.parent):
        view("ls -l ." , shell(f'ls -l | grep {me.name}').text)
        
        
def prompt(question, choice=['y','n'], success=['y']):
    while True:
        ans = (input(question)).lower()
        if not valid or a in valid:
            break
        print("please choose")
 
    return ans in success
        