# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-25 14:53
#  
#  Description: ftiming project. `pyftiming` package.
# 
from .tim_case import *

import re


def load_timing_log(log):
  """Load timing log file.

  :log: str
      Path string for log file.
  :returns: TimCase
      Contain data in this timing case.

  """
  try:
    return TimCase.load(log)
  except:
    timing_log = _clean_log_data(log)
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
        routtimcolls.update({routine: RoutTimColl(routine,
                                                  1,
                                                  elag_time,
                                                  elag_time,
                                                  elag_time)})
    for rtc in routtimcolls.values(): rtc.get_avg_time()
    timing_case = TimCase(data=routtimcolls)
    timing_case.dump(log)
    return timing_case


def _clean_log_data(log):
  with open(log, 'r') as fp:
    log_lines = fp.readlines()
  start_marker = 'START TIMING'
  for idx in range(len(log_lines)):
    if start_marker in log_lines[idx]: break
  timing_log_orig = log_lines[idx+1:]
  pattern = r'^\[timing\]\s+(\S+)\s+(\S+)\s+$'
  regex = re.compile(pattern)
  mo_list = list(regex.search(line) for line in timing_log_orig)
  mo_list = list(mo for mo in mo_list if mo is not None)
  data_filtered = list(
        list(str_.strip() for str_ in mo.groups()) for mo in mo_list)

  return list([timing_log_item[0], float(timing_log_item[1])] for
            timing_log_item in data_filtered)
