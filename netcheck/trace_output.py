"""
Steven Portzer
Start Date: 08/13/2012

Purpose: To log the output generated by modeling a set of traces.

"""

import trace_ordering
from ip_matching import format_addr
from ip_matching import addr_dont_care
from ip_matching import is_addr_match



###### Output Level Configuration ######

# Print system calls that raise warnings even if SHOW_SYSCALLS  is False
SHOW_WARNINGS = True

# Print system calls that raise notices even if SHOW_SYSCALLS is False
SHOW_NOTICES = False

# Print all system calls except possibly those that raise don't care
SHOW_SYSCALLS = False

# If SHOW_SYSCALLS is True, still don't print system calls we don't care about
SUPPRESS_DONTCARE = False

# If SHOW_SYSCALLS is True, still don't print failed attempts of system
# calls (calls that cause the model to raise an error and must be
# reattempted later)
SUPPRESS_ATTEMPTS = False


# If not None, only print this many characters of string arguments
MAX_STRING_LEN = 32

######################################



def log_intialize():
  """
  Starts logging ordering information.
  """

  print "-" * 80
  print "Verifying Traces"
  print "-" * 80



def log_syscall(trace_id, syscall, err=None):
  """
  Logs the result of a system call.
  """

  name, args, ret = syscall

  if err is None:
    if SHOW_SYSCALLS:
      print "trace", str(trace_id) + ":", shorten_syscall(syscall)

  elif isinstance(err, trace_ordering.SyscallDontCare):

    if SHOW_SYSCALLS and not SUPPRESS_DONTCARE:
      print "[Don't Care] trace", str(trace_id) + ":", shorten_syscall(syscall)

  elif isinstance(err, trace_ordering.SyscallNotice):
    if SHOW_SYSCALLS or SHOW_NOTICES:
      print "[Notice] trace", str(trace_id) + ":", shorten_syscall(syscall)
      print "   => %s: %s" % err.args[1:]

  elif isinstance(err, trace_ordering.SyscallWarning):
    if SHOW_SYSCALLS or SHOW_WARNINGS:
      print "[Warning] trace", str(trace_id) + ":", shorten_syscall(syscall)
      print "   => %s: %s" % err.args[1:]

  elif isinstance(err, model.SyscallError):
    print "[Error] trace", str(trace_id) + ":", shorten_syscall(syscall)
    print "   => %s: %s" % err.args[1:]



def log_syscall_attempt(trace_id, syscall, err):
  """
  Logs a failed attempt to execute a system call.
  """

  if SUPPRESS_ATTEMPTS or not SHOW_SYSCALLS:
    return

  name, args, ret = syscall

  print "[Failed to Execute] trace", str(trace_id) + ":", shorten_syscall(syscall)
  print "   => %s: %s" % err.args[1:]



def log_execution_blocked(syscall_list):
  """
  Logs failure of system call ordering.
  """

  print
  print "No valid action:"
  for trace_id, syscall, err in syscall_list:
    print "[Error] trace", str(trace_id) + ":", shorten_syscall(syscall)
    print "   => %s: %s" % err.args[1:]



def log_done():
  """
  Logs successful completion of system call ordering.
  """

  print
  print "Done"



def shorten_syscall(syscall):
  """
  Returns the system call with strings abridged if neccessary.
  """

  name, args, ret = syscall
  args = tuple(map(shorten_string, args))
  
  return name, args, ret



def shorten_string(obj):
  """
  Returns the object, abridged if neccessary.
  """

  if isinstance(obj, str) and MAX_STRING_LEN and len(obj) > MAX_STRING_LEN:
    return obj[:MAX_STRING_LEN] + "..."
  else:
    return obj

