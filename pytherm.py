#! /usr/bin/env python

__author__ = "Benny Carbajal"
__copyright__ = "Copyright 2019, Kerneloid"
__credits__ = [ "Benny Carbajal", "Dexter Scott Belmont" ]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = [ "Benny Carbajal", "Dexter Scott Belmont" ]
__email__ = [ "benny.carbajalb@gmail.com", "xedret@gmail.com" ]
__status__ = "Beta"

import clr, json, platform, os

#List for hardware types and sensor types that our DLL can open
OHM_hwtypes = [ 'Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD' ]
OHM_sensortypes = [
 'Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData'
]


def init_OHM() :
 clr.AddReference( os.path.abspath( os.path.dirname( __file__ ) ) + R'\OpenHardwareMonitorLib.dll' )
 from OpenHardwareMonitor import Hardware
 hw = Hardware.Computer()
 hw.MainboardEnabled, hw.CPUEnabled, hw.RAMEnabled, hw.GPUEnabled, hw.HDDEnabled = True, True, True, True, True
 hw.Open()
 return hw


def fetch_data( handle ) :
 out = []
 for i in handle.Hardware :
  i.Update()
  for sensor in i.Sensors : 
   thing = parse_sensor( sensor )
   if thing is not None :
    out.append( thing )
  for j in i.SubHardware :
   j.Update()
   for subsensor in j.Sensors :
    thing = parse_sensor( subsensor )
    out.append( thing )
 return out


def parse_sensor( snsr ) :
 if snsr.Value is not None :
  if snsr.SensorType == OHM_sensortypes.index( 'Temperature' ) :
   HwType = OHM_hwtypes[ snsr.Hardware.HardwareType ]
   return { "Type" : HwType, "Name" : snsr.Hardware.Name, "Sensor" : snsr.Name, "Reading" : u'%s\xb0C' % snsr.Value }


def main() :
 return json.dumps( { platform.node(): fetch_data( init_OHM() ) }, indent=1, sort_keys=True, ensure_ascii=False )


if __name__ == "__main__" :
 print('Hardware Monitor:')
 print(main())

