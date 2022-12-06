"""
<<Main>>

This Module is coded for extracting data from XML file related to ..., ..., ....
The output Data Structure is :....

"""

# /Users/pouyafirouzmakan/Desktop/VANET/small_data_Richmondhill/sumoTrace_geo.xml

import random
import xml.dom.minidom

import Hash
from Zone import ZoneID

__author__ = "Adrian (Pouya) Firouzmakan"
__all__ = ["mac_address"]

sumoTrace_address = input("Please Input sumoTrace.xml file's address: ")
# osmPoly_address = input("Please Input osm.poly.xml file's address: ")

# this file is the sumoTrace.xml file extracted from SUMO
sumo_trace = xml.dom.minidom.parse(sumoTrace_address)
fcd = sumo_trace.documentElement  # Floating Car Data (FCD) from sumoTrace.xml
times = fcd.getElementsByTagName('timestep')  # includes data for all seconds

# Min and Max Latitude and Longitude of the area to define zones
area = dict(min_lat=43.586568,
            min_long=-79.540771,
            max_lat=44.012923,
            max_long=-79.238069)
area_zones = ZoneID(area)  # This is a hash table including all zones and their max and min lat and longs
area_zones.zones()
number_of_cars = 1000


def mac_address():
    mac = [152, 237, 92,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


class DataTable:
    # This class is determined for defining the hash_table, updating data, routing messages,
    # and defining IP addresses by using trace (which is sumo_trace)

    def __init__(self, trace, n_cars, zones):
        """

        :param trace: sumo_trace file from SUMO
        :param n_cars: number of cars
        :param zones: all the zones of the area
        """

        self.bus_table = Hash.HashTable(n_cars * 100)
        self.veh_table = Hash.HashTable(n_cars * 100)

        self.zone_vehicles = {}
        self.zone_buses = {}
        for veh in trace.documentElement.getElementsByTagName('timestep')[0].childNodes[1::2]:
            if 'bus' in veh.getAttribute('id'):
                self.bus_table.set_item(veh.getAttribute('id'),
                                        dict(long=veh.getAttribute('x'),
                                             lat=veh.getAttribute('y'),
                                             angle=veh.getAttribute('angle'),
                                             speed=veh.getAttribute('speed'),
                                             pos=veh.getAttribute('pos'),
                                             lane=veh.getAttribute('lane'),
                                             zone=zones.det_zone(float(veh.getAttribute('y')),
                                                                 float(veh.getAttribute('x'))
                                                                 ),
                                             prev_zone=None,
                                             message_dest={},
                                             message_source={},
                                             MAC=mac_address(),
                                             IP=None,
                                             cluster_IPs={},
                                             cluster_MACs={},
                                             in_area=True,
                                             trans_range=500
                                             )
                                        )
            else:
                self.veh_table.set_item(veh.getAttribute('id'),
                                        dict(long=veh.getAttribute('x'),
                                             lat=veh.getAttribute('y'),
                                             angle=veh.getAttribute('angle'),
                                             speed=veh.getAttribute('speed'),
                                             pos=veh.getAttribute('pos'),
                                             lane=veh.getAttribute('lane'),
                                             zone=zones.det_zone(float(veh.getAttribute('y')),
                                                                 float(veh.getAttribute('x'))
                                                                 ),
                                             caluster_head={},
                                             IP=None,
                                             MAC=mac_address(),  # The mac address of each car is determined
                                             # using mac_address method
                                             in_area=True,
                                             trans_range=200
                                             )
                                        )

            if 'bus' in veh.getAttribute('id'):
                self.zone_buses[self.bus_table.values(veh.getAttribute('id'))['zone']] = \
                    veh.getAttribute('id')
            else:
                self.zone_vehicles[self.veh_table.values(veh.getAttribute('id'))['zone']] = \
                    veh.getAttribute('id')

    def neighbor_zones(self,zone_id):
        num = int(zone_id[4:])
        prev = num - 1
        next = num + 1
        return []







    def print_table(self):
        self.bus_table.print_hash_table()
        self.veh_table.print_hash_table()

    # def cluster(self):


a = DataTable(sumo_trace, 8000, area_zones)
a.print_table()
