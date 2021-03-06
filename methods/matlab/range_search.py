'''
  @file range_search.py
  @author Marcus Edel

  Class to benchmark the matlab Range Search method.
'''

import os
import sys
import inspect

# Import the util path, this method even works if the path contains symlinks to
# modules.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
  os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../util")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from log import *
from profiler import *

import shlex
import subprocess
import re
import collections

'''
This class implements the Range Search benchmark.
'''
class RANGESEARCH(object):

  '''
  Create the Range Search benchmark instance.

  @param dataset - Input dataset to perform Range Search on.
  @param timeout - The time until the timeout. Default no timeout.
  @param path - Path to the matlab binary.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, timeout=0, path=os.environ["MATLAB_BIN"],
      verbose=True):
    self.verbose = verbose
    self.dataset = dataset
    self.path = path
    self.timeout = timeout

  '''
  Perform Range Search. If the method has been successfully completed return the
  elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or a negative value if the method was not
  successful.
  '''
  def RunMetrics(self, options):
    Log.Info("Perform Range Search.", self.verbose)

    # Parse options into string.
    optionsStr = ""
    if "max" in options:
      optionsStr = "-M " + str(options.pop("max"))
    else:
      Log.Fatal("Parameter 'max' is required!")
      raise Exception("missing parameter")

    if "leaf_size" in options:
      optionsStr = optionsStr + " -l " + str(options.pop("leaf_size"))
    if "naive_mode" in options:
      optionsStr = optionsStr + " -N"
      options.pop("naive_mode")

    if len(options) > 0:
      Log.Fatal("Unknown parameters: " + str(options))
      raise Exception("unknown parameters")

    # If the dataset contains two files then the second file is the query file.
    # In this case we add this to the command line.
    if len(self.dataset) == 2:
      inputCmd = "-r " + self.dataset[0] + " -q " + self.dataset[1] + " " \
          + optionsStr
    else:
      inputCmd = "-r " + self.dataset + " " + optionsStr

    # Split the command using shell-like syntax.
    cmd = shlex.split(self.path + "matlab -nodisplay -nosplash -r \"try, " +
        "RANGESEARCH('"  + inputCmd + "'), catch, exit(1), end, exit(0)\"")

    # Run command with the nessecary arguments and return its output as a byte
    # string. We have untrusted input so we disable all shell based features.
    try:
      s = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False,
          timeout=self.timeout)
    except subprocess.TimeoutExpired as e:
      Log.Warn(str(e))
      return -2
    except Exception as e:
      Log.Fatal("Could not execute command: " + str(cmd))
      return -1

    # Datastructure to store the results.
    metrics = {}

    # Parse data: runtime.
    timer = self.parseTimer(s)

    if timer != -1:
      metrics['Runtime'] = timer.total_time

      Log.Info(("total time: %fs" % (metrics['Runtime'])), self.verbose)

    return metrics

  '''
  Parse the timer data form a given string.

  @param data - String to parse timer data from.
  @return - Namedtuple that contains the timer data or -1 in case of an error.
  '''
  def parseTimer(self, data):
    # Compile the regular expression pattern into a regular expression object to
    # parse the timer data.
    pattern = re.compile(br"""
        .*?total_time: (?P<total_time>.*?)s.*?
        """, re.VERBOSE|re.MULTILINE|re.DOTALL)

    match = pattern.match(data)
    if not match:
      Log.Fatal("Can't parse the data: wrong format")
      return -1
    else:
      # Create a namedtuple and return the timer data.
      timer = collections.namedtuple("timer", ["total_time"])

      return timer(float(match.group("total_time")))
