"""A library of useful utilities."""

import pickle
import hashlib
import dis
import io

from streamlit.local.util import streamlit_read, streamlit_write

def memoize(func):
	"""A function decorator which enables the function to cache its
	input/output behavior to disk."""

	CACHE_PATH = '.streamlit'

	# def hash(obj):
	# 	"""Returns the md5 hash of any object."""
	#

	# 	hasher.update((obj, pickle.HIGHEST_PROTOCOL))
	# 	return hasher.hexdigest()

	def wrapped_func(*argc, **argv):
		"""This function wrapper will only call the underlying function in
		the case of a cache miss. Cached objects are stored in the cache/
		directory."""

		# Calculate the filename hash.
		hasher = hashlib.new('md5')
		print('hexdigest 0', hasher.hexdigest())
		hasher.update(pickle.dumps((
			argc, argv, list(dis.get_instructions(func))),
			pickle.HIGHEST_PROTOCOL))
		print('hexdigest 1', hasher.hexdigest())
		path = f'cache/f{hasher.hexdigest()}.pickle'
		print('cached filename', path)
		# # hasher.update(pickle.dumps(argv, pickle.HIGHEST_PROTOCOL))
		# # print('hexdigest 2', hasher.hexdigest())
		# # stream = io.StringIO()
		# #
		# # print('hexdigest 3', hasher.hexdigest())
		# import sys
		# sys.exit(-1)
		# hash_args = (func.__name__, func.__doc__, argc, argv)
		# hash_key = hash(hash_args)

		# Load the file (hit) or compute the function (miss)
		try:
			with streamlit_read(path, binary=True) as input:
				rv = pickle.load(input)
				print('%s (HIT)' % path)
		except FileNotFoundError:
			rv = func(*argc, **argv)
			with streamlit_write(path, binary=True) as output:
				pickle.dump(rv, output, pickle.HIGHEST_PROTOCOL)
			print('%s (MISS)' % path)
		return rv

	# make this a well-behaved decorator by preserving important function attributes
	try:
		wrapped_func.__name__ = func.__name__
		wrapped_func.__doc__ = func.__doc__
		wrapped_func.__dict__.update(func.__dict__)
	except AttributeError:
		pass

	# return the funciton which wraps our function
	return wrapped_func

# def readable_time(seconds):
# 	"""Converts a number of seconds into a human readable amount."""
# 	seconds = int(seconds)
# 	minutes, seconds = seconds / 60, seconds % 60
# 	hours  , minutes = minutes / 60, minutes % 60
# 	days   , hours   = hours   / 24, hours   % 24
#
# 	if days != 0:
# 		return '%id %ih %im %is' % (days, hours, minutes, seconds)
# 	elif hours != 0:
# 		return '%ih %im %is' % (hours, minutes, seconds)
# 	elif minutes != 0:
# 		return '%im %is' % (minutes, seconds)
# 	else:
# 		return '%is' % (seconds)
#
# def timed_iter(iterator, length=None, interval=60.0):
# 	"""Takes an iterator and returns an iterator which prints out
# 	estimated time remaining each interval seconds.
#
# 	iterator - the iterable object (or an int for xrange behavior)
# 	length   - the length of iterator, if len(iterator) doesn't work
# 	interval - the interval to display information
# 	"""
# 	import time
#
# 	# figure out how many iterations are required
# 	if type(iterator) == int:
# 		length = iterator
# 		iterator = range(iterator)
# 	elif length == None:
# 		length = len(iterator)
#
# 	# iterate estimating runtime
# 	start_time = time.time()
# 	prev_time = start_time
# 	for ii, xx in enumerate(iterator):
# 		curr_time = time.time()
# 		if curr_time - prev_time > interval:
# 			elapsed = curr_time - start_time
# 			complete = ii / float(length)
# 			estimated = elapsed * (1.0 - complete) / complete
# 			print('%.2i%% - % 7s (elapsed) - % 7s (remain) - % 7s (total)' % \
# 				(int(complete * 100),
# 				readable_time(elapsed),
# 				readable_time(estimated),
# 				readable_time(elapsed + estimated)))
# 			prev_time = curr_time
# 		yield xx
#
# def timed_function(func):
# 	"""A function decorator which simply measures the amount of time it
# 	takes a function to execute."""
# 	import time
#
# 	def wrapped_func(*argc, **argv):
# 		# call the function, measuring the elapsed time
# 		start_time = time.time()
# 		rv = func(*argc, **argv)
# 		delta = time.time() - start_time
#
# 		# write the elapsed time
# 		print('%s() : %s (%s)' % (func.__name__, readable_time(delta), delta))
#
# 		# all done
# 		return rv
#
# 	# make this a well-behaved decorator by preserving important function attributes
# 	try:
# 		wrapped_func.__name__ = func.__name__
# 		wrapped_func.__doc__ = func.__doc__
# 		wrapped_func.__dict__.update(func.__dict__)
# 	except AttributeError:
# 		pass
#
# 	# return the funciton which wraps our function
# 	return wrapped_func
#
# @timed_function
# def example(xx):
# 	the_list = []
# 	for ii in timed_iter(list(range(xx)), interval=1):
# 		the_list.append(ii)
#
# def unit_test():
# 	print(example(int(1e8)))
#
# if __name__ == '__main__':
# 	unit_test()
