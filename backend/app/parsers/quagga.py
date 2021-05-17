# Warning: this file uses regex strings from an Apache 2.0 Licensed project
# from https://github.com/CiscoTestAutomation/genieparser/blob/master/src/genie/libs/parser/iosxe/show_bgp.py
# License: https://github.com/CiscoTestAutomation/genieparser/blob/master/LICENSE
import re

class QuaggaParser():
  def get_routes(self, fh):

    APACHE_REGEX_3_2 = re.compile(r'^\s*(?P<status_codes>(s|x|S|d|h|\*|\>|m|r|\s)+)?'
                              r'(?P<path_type>(i|e|c|l|a|r|I))?\s{10,20}'
                              r'(?P<next_hop>[a-zA-Z0-9\.\:]+)'
                              r' +(?P<metric>(?:\d+(?=[ \d]{13}\d ))?) +(?P<weight>\d+)'
                              r'(?P<path>[0-9 \S\{\}]+)$')

    APACHE_REGEX_P4 = re.compile(r'^\s*(?P<status_codes>(?:s|x|S|d|h|m|r|\*|\>|\s)+)?'
                            r'(?P<path_type>(?:i|e|c|l|a|r|I))? *'
                            r'(?P<prefix>[a-zA-Z0-9\.\:\/\-\[\]]+) +'
                            r'(?P<next_hop>[a-zA-Z0-9\.\:]+) +'
                            r'(?P<metric>(?:\d+(?=[ \d]{13}\d ))?) +'
#                           r'(?P<local_prf>(?:\d+(?=[ \d]{6}\d ))?) +'
                            r'(?P<weight>\d+)(?P<path>[0-9 \S\{\}]+)$')


    route_count = 0
    routes = []
    active_route = None
    for line in fh:
     parsed_line = APACHE_REGEX_P4.match(line.strip())
     if parsed_line:
       if parsed_line.group('next_hop') == '0':
         parsed_line = APACHE_REGEX_3_2.match(line.strip())
         if parsed_line is None:
           continue
       else:
         active_route = parsed_line.group('prefix')
         if "/" not in active_route:
           active_route += "/24"
         route_count += 1
       routes.append(active_route + ";" + self.filter_path(parsed_line.group('path').strip()))
    return routes, route_count

  def filter_path(self, as_path):
    asn_list = as_path.split()
    new_path = ""
    for asn in asn_list:
      if not self.hasNumbers(asn):
         continue
      new_path += asn + " "
    return new_path.strip()


  def hasNumbers(self, inputString):
    return any(char.isdigit() for char in inputString)

