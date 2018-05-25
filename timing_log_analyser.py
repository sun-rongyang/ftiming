#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-05-25 22:46
#  
#  Description: ftiming project. Timing log analyser.
# 


import sys
import re
from collections import namedtuple
split_weight = 96


class RoutTimColl(object):

  """Routine timing collection. """

  def __init__(self, routine, times, tot, max, min):
    self.routine = routine
    self.times = times
    self.tot = tot
    self.max = max
    self.min = min

  def get_avg_time(self):
    self.avg = self.tot / self.times


def print_sample_analy_header(log_file):
  """Print sample analysis header

  :log_file: TODO
  :returns: TODO

  """
  print('\n\n\n' + '*' * split_weight +'\n'+ '*' * split_weight)
  print(log_file.rstrip())
  print('\n'.rstrip())
  print('{0:25} {1:5} {2:>15} {3:>15} {4:>15} {5:>15}'.format('routine', 'times', 'tot time', 'avg time', 'max time', 'min time'))
  print('*' * split_weight)
  

def clean_log_data(file_lines):
  """Get timing log from original log file.

  :file_lines: TODO
  :returns: TODO

  """
  start_marker = 'START TIMING'
  for idx in range(len(file_lines)):
    if start_marker in file_lines[idx]:
      break
  timing_log_orig = file_lines[idx+1:]

  pattern = r'^\[timing\]\s+(\S+)\s+(\S+)\s+$'
  regex = re.compile(pattern)
  mo_list = list(regex.search(line) for line in timing_log_orig)
  mo_list = list(mo for mo in mo_list if mo is not None)
  data_filtered = list(
        list(str_.strip() for str_ in mo.groups()) for mo in mo_list)

  return list([timing_log_item[0], float(timing_log_item[1])] for
            timing_log_item in data_filtered)


def timing_profile_analyser(timing_log):
  """Analysis timing log.

  :timing_log: TODO
  :returns: TODO

  """
  routines = []
  routtimcolls = {}
  for item in timing_log:
    routine = item[0]
    elag_time = item[1]
    if routine in routines:
      routtimcoll = routtimcolls[routine]
      routtimcoll.times += 1
      routtimcoll.tot += elag_time
      routtimcoll.max = max(routtimcoll.max, elag_time)
      routtimcoll.min = min(routtimcoll.min, elag_time)
    else:
      routines.append(routine)
      routtimcolls.update({routine: RoutTimColl(routine, 1,
                                                elag_time,
                                                elag_time,
                                                elag_time)})
  for _, routtimcoll in routtimcolls.items():
    routtimcoll.get_avg_time()
    print('{0:25} {1:5d} {2:15.3f} {3:15.3f} {4:15.3f} {5:15.3f}'.format(
                                                           routtimcoll.routine,
                                                           routtimcoll.times,
                                                           routtimcoll.tot,
                                                           routtimcoll.avg,
                                                           routtimcoll.max,
                                                           routtimcoll.min))

  
def print_sample_analy_tailer():
  """Print sample analysis tailer
  :returns: TODO

  """
  print('*' * split_weight)
  

if __name__ == '__main__':
  log_file_path = sys.argv[1]
  log_file_name = log_file_path.split('/')[-1]
  split_weight = max(split_weight, len(log_file_name)+1)
  print_sample_analy_header(log_file_name)
  with open(log_file_path, 'r') as file_obj:
    timing_log = clean_log_data(file_obj.readlines())
  timing_profile_analyser(timing_log)
  print_sample_analy_tailer()
