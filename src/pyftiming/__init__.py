# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-25 14:53
#  
#  Description: ftiming project. `pyftiming` package.
# 
import re


class RoutTimColl(object):

  """Routine timing collection. """

  def __init__(self, routine, times, tot, max, min):
    """Initialize  a RoutTimColl obj.

    :routine: str
        Name of the routine.
    :times: int
        Times of routine called.
    :tot: float
        Total time used.
    :max: float
        Maximal time used.
    :min: float
        Minimal time used.

    """
    self.routine = routine
    self.times = times
    self.tot = tot
    self.max = max
    self.min = min
    
  def get_avg_time(self):
    """Get average time for the routine. """
    self.avg = float(self.tot) / self.times


class TimCase(object):

  """Contain timing data and properties for a case. """

  def __init__(self, data=None, props=None):
    """Initialise a timing test case.

    :data: dict
        Key is the name of the routine,
        value is a RoutTimColl obj.
    :props: dict

    """
    if data is None:
      self.data = {}
    else:
      self.data = dict(data)
    if props is None:
      self.props = {}
    else:
      self.props = dict(props)


def load_timing_log(log):
  """Load timing log file.

  :log: str
      Path string for log file.
  :returns: TimCase
      Contain data in this timing case.

  """
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
  return TimCase(data=routtimcolls)


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
