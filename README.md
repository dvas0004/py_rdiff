PY_RDIFF
--------

A python module providing a (thin) [ctypes](https://docs.python.org/2/library/ctypes.html) wrapper around [librsync](https://github.com/librsync/librsync). Inspiration for this module comes primarily from [python-librsync](https://pypi.python.org/pypi/python-librsync/0.1-5). Librsync API was researched from: [http://rproxy.samba.org/doxygen/librsync/refman.pdf](http://rproxy.samba.org/doxygen/librsync/refman.pdf)

Like python-librsync, py_rdiff provides identical functionality to the linux command *rdiff* (http://linux.die.net/man/1/rdiff)[http://linux.die.net/man/1/rdiff], in that the main actions that can be performed are:

* creating a file signature (py_rdiff.rysnc_sig)
* creating a file delta (py_rdiff.rsync_delta)
* patching the original file to become identical to the destination file (py_rdiff.rsync_patch)


There are some differences between py_rdiff and python-librsync. You will notice that there is a lot less code in this module. The main reason is that python-librsync makes use of librsync asyncronous / non-blocking capabilities (referred to as "jobs" in librsync terminology). However, the author still wraps the jobs in while loops, waiting for the call to complete before exiting. Py_rdiff makes use of the native librsync \*\_file family of library calls to achieve the same result but in less code.

Example of usage:
-----------------

```bash
$ python
```
```python
>>> import py_rdiff
>>> completed, sig_file = py_rdiff.rsync_sig('test.txt')

>>> completed
True

>>> sig_file
'dd18bf3a8e0a2a3e53e2661c7fb53534.sig

>>> if completed:
...     completed, delta_file = py_rdiff.rsync_delta(sig_file, 'test2.txt')
 

>>> completed
True

>>> delta_file
'dd18bf3a8e0a2a3e53e2661c7fb53534.delta'

>>> if completed:
...     completed = py_rdiff.rsync_patch(delta_file,'test.txt', 'patched_test.txt')

>>> completed
(True, None)
```
```bash
$ cat test.txt 
asdqwezxcrfv

$ cat test2.txt 
qwerty qwerty qwerty

$ cat patched_test.txt 
qwerty qwerty qwerty

```
