# inspiration: https://pypi.python.org/pypi/python-librsync/0.1-5
# librsync in c: http://rproxy.samba.org/doxygen/librsync/refman.pdf
# notes: https://docs.python.org/2/library/ctypes.html

import os,sys
import ctypes
import ctypes.util
import hashlib
import traceback

global _librsync

if os.name == 'posix':
    path = ctypes.util.find_library('rsync')
    if path is None:
        raise ImportError('Could not find librsync, make sure it is installed')
    try:
        _librsync = ctypes.cdll.LoadLibrary(path)
    except OSError:
        raise ImportError('Could not load librsync at "%s"' % path)
elif os.name == 'nt':
    try:
        _librsync = ctypes.cdll.librsync
    except:
        raise ImportError('Could not load librsync, make sure it is installed')
else:
    raise NotImplementedError('Librsync is not supported on your platform')



def rsync_sig(fname):
	# example of (blocking) sig call
	# ---------------------------------
	_librsync.rs_sig_file.restype = ctypes.c_long
	_librsync.rs_sig_file.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_void_p]

	if os.path.isfile(fname):

		try:

			hash_object = hashlib.md5(fname)
			internal_name = hash_object.hexdigest()
			sig_f_name = internal_name+'.sig'

			orig=_librsync.fopen(fname, 'rb')
			sig=_librsync.fopen(sig_f_name, 'wb')

			if (_librsync.rs_sig_file(orig, sig, 2048, 8, None) != 0 ):
				raise Exception("librsync call failed")

			_librsync.fclose(orig)
			_librsync.fclose(sig)

			return True, sig_f_name

		except:
			traceback.print_exc(file=sys.stdout)
			return False, None

	else:
		print "file not found"
		return False, None



def rsync_delta(sig_file, new_file):
	# example of (blocking) delta call
	# ---------------------------------
	# rs result rs delta file (rs signature t * , FILE * new file, FILE * delta file, rs stats t * )
	_librsync.rs_delta_file.restype = ctypes.c_long
	_librsync.rs_delta_file.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]

	if os.path.isfile(sig_file):

		try:
			delta_f_name = os.path.split(sig_file)[1].split('.')[0] + ".delta"

			sig=_librsync.fopen(sig_file, 'rb')
			delta = _librsync.fopen(delta_f_name, 'wb')
			newF = _librsync.fopen(new_file, 'rb')


			if (_librsync.rs_delta_file(sig, newF, delta, None) != 0 ):
				raise Exception("librsync call failed")

			_librsync.fclose(delta)
			_librsync.fclose(sig)
			_librsync.fclose(newF)

			return True, delta_f_name

		except:
			traceback.print_exc(file=sys.stdout)
			return False, None

	else:
		print "file not found"
		return False, None

	
def rsync_patch(delta_file, basis_file, new_file):
	# example of (blocking) patch call
	# ---------------------------------
	# rs result rs patch file (FILE * basis file, FILE * delta file, FILE * new file, rs stats t * )

	_librsync.rs_patch_file.restype = ctypes.c_long
        _librsync.rs_patch_file.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]

	if os.path.isfile(delta_file):
		try:
			basis=_librsync.fopen(basis_file, 'rb')
			delta=_librsync.fopen(delta_file, 'rb')
			newF=_librsync.fopen(new_file, 'wb')

			
			if ( _librsync.rs_patch_file(basis, delta, newF, None) != 0 ):
				raise Exception("librsync call failed")

			_librsync.fclose(delta)
			_librsync.fclose(basis)
			_librsync.fclose(newF)

			return True, None

		except:
			traceback.print_exc(file=sys.stdout)
			return False, None

	else:
		print "file not found"
		return False, None

