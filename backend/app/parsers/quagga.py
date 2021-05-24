"""

BGP table version is 0, local router ID is 74.80.100.4
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, R Removed
Origin codes: i - IGP, e - EGP, ? - incomplete

   Network          Next Hop            Metric LocPrf Weight Path
*> 1.0.0.0/24       198.32.243.60            0             0 13335 i
*> 1.0.4.0/22       198.32.242.176           0             0 6939 4826 38803 i
*  1.0.4.0/24       198.32.124.227           0             0 6461 6461 6461 6461 4637 4637 4637 4637 1221 38803 38803 38803 i
*>                  198.32.242.176           0             0 6939 4826 38803 i

Total number of prefixes 3
"""


class QuaggaParser:
    # Constants
    BEST_ROUTE_MARK = ">"
    VALID_ROUTE_MARK = "*"
    INACTIVE_ROUTE_MARK = " "

    def __init__(self, store_inactive_routes=False):
        self.store_inactive_routes = store_inactive_routes

    # with open('route-collector.mia.pch.net-ipv4_bgp_routes.2021.02.09') as fh:
    def get_routes(self, fh):
        parseRoutes = False
        active_route = ""
        for line in fh:
            line = line.rstrip()
            if (
                "   Network          Next Hop            Metric LocPrf Weight Path"
                in line
            ):
                parseRoutes = True
                continue
            if parseRoutes and len(line) != 0 and line[0] in "RSs* ":
                # https://github.com/Quagga/quagga/blob/master/bgpd/bgp_route.c#L5918
                route_status = line[0]  # [RSs* ]
                line = line[1:]
                original_line = line[:]

                # Ignore invalid routes
                if route_status != self.VALID_ROUTE_MARK:
                    continue

                # https://github.com/Quagga/quagga/blob/master/bgpd/bgp_route.c#L5933
                route_status2 = line[0]  # [hd> ]
                line = line[1:]

                # Accept only inactive and best paths
                if route_status2 not in [
                    self.BEST_ROUTE_MARK,
                    self.INACTIVE_ROUTE_MARK,
                ]:
                    continue

                # https://github.com/Quagga/quagga/blob/master/bgpd/bgp_route.c#L5945
                internal_route = line[0]  # [i ]
                line = line[1:]

                # check different path for same route
                # https://github.com/lagopus/quagga/blob/2a71e9ce89c6f76c099dea67dddbe8da454d9de7/bgpd/bgp_route.c#L5628
                # print(line)
                if " " * 17 == line[0:17]:
                    # new path, same prefix than previous route
                    line = line[17:]
                elif len(line) > 16 and line[16] == " ":
                    # 17 chars padded ip block
                    active_route = line[0:17].strip()
                    line = line[17:]
                elif len(line[0:17].strip()) == 17:
                    # https://github.com/Quagga/quagga/blob/master/bgpd/bgp_route.c#L5904
                    # Multi-line route
                    active_route = line.split(" ")[0]
                    line = fh.readline().rstrip()
                    line = line[20:]
                else:
                    print("Ignored line: '%s'" % (original_line))

                if "/" not in active_route:
                    if ".0.0.0" in active_route[-6]:
                        active_route += "/8"
                    elif ".0.0" in active_route[-4:]:
                        active_route += "/16"
                    elif ".0" in active_route[-2:]:
                        active_route += "/24"

                nexthop = line[0:16].strip()
                line = line[16:]

                med = line[0:10].strip()
                line = line[10:]

                localpref = line[0:7].strip()
                line = line[7:]

                weight = line[0:7].strip()

                # https://github.com/lagopus/quagga/blob/2a71e9ce89c6f76c099dea67dddbe8da454d9de7/bgpd/bgp_route.c#L5669
                line = line[8:]  # extra space after weight
                origin = line[-1]
                aspath = line[:-1].strip()

                # Available data per path: route_status, route_status2, internal_route, nexthop, med, localpref, weight, origin, aspath
                if self.store_inactive_routes:
                    yield "%s;%s" % (active_route, aspath)
                else:
                    if route_status2 == self.BEST_ROUTE_MARK:
                        yield "%s;%s" % (active_route, aspath)
