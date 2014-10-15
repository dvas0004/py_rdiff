$ python

>>> completed, sig_file = py_rdiff.rsync_sig('test.txt')

>>> completed
True

>>> sig_file
'dd18bf3a8e0a2a3e53e2661c7fb53534.sig

>>> if completed:
...     completed, delta_file = py_rdiff.rsync_delta(sig_file, 'test2.txt')
... 

>>> completed
True

>>> delta_file
'dd18bf3a8e0a2a3e53e2661c7fb53534.delta'

>>> if completed:
...     completed = py_rdiff.rsync_patch(delta_file,'test.txt', 'patched_test.txt')

>>> completed
(True, None)

$ cat test.txt 
asdqwezxcrfv

$ cat test2.txt 
qwerty qwerty qwerty

$ cat patched_test.txt 
qwerty qwerty qwerty


