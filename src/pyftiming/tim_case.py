# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-25 20:45
#  
#  Description: ftiming project. Module for data structures.
# 
import json
from os.path import basename, splitext


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
    self.avg = None
    
  def get_avg_time(self):
    """Get average time for the routine. """
    self.avg = float(self.tot) / self.times


class TimCase(object):

  """Contain timing data and properties for a case. """

  @classmethod
  def load(cls, log):
    """Load TimCase instance from json file.

    :log: str
        Path string for log file.
    :returns: TimCase
        Contain data in this timing case.

    """
    js_file = _get_js_file(log)
    with open(js_file) as fp:
      jss = fp.read()
    return json.loads(jss, cls=TimCaseJSONDecoder)

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

  def dump(self, log):
    """Dump TimCase instance to json file.

    :log: str
        Path string for log file.
    :returns: 0

    """
    js_file = _get_js_file(log)
    with open(js_file, 'w') as fp:
      fp.write(json.dumps(self, cls=TimCaseJSONEncoder, indent=2))
    return 0


def _get_js_file(log):
  file_name = basename(log)
  path = log.replace(file_name, '')
  basename_ = splitext(file_name)[0]
  return path + basename_ + '.json'


class TimCaseJSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, TimCase):
      tim_case = {}
      tim_case['props'] = obj.props
      tim_case_data = {}
      for key, val in obj.data.items():
        tim_case_data[key] = {'routine': val.routine,
                              'times': val.times,
                              'tot': val.tot,
                              'max': val.max,
                              'min': val.min,
                              'avg': val.avg}
      tim_case['data'] = tim_case_data
      return tim_case
    else:
      return super().default(self, obj)


class TimCaseJSONDecoder(json.JSONDecoder):
  def __init__(self, *args, **kwargs):
    # create object_hook method to decode DataSet object.
    json.JSONDecoder.__init__(self,
                              object_hook = self.object_hook,
                              *args,
                              **kwargs)

  def object_hook(self, obj):
    try:
      props = obj['props']
      data_dict = obj['data']
      data = {}
      for key, val in data_dict.items():
        routtimcoll = RoutTimColl(val['routine'],
                                  val['times'],
                                  val['tot'],
                                  val['max'],
                                  val['min'])
        routtimcoll.avg = val['avg']
        data[key] = routtimcoll
      return TimCase(data=data, props=props)
    except:
      return obj
