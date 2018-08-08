#!/usr/bin/python -u

# Ping1DMavlinkDriver.py
# Request distance measurements from a Blue Robotics Ping1D device over udp (PingProxy)
# Send results to autopilot via mavproxy over udp for use as mavlink rangefinder
# Don't request if we are already getting data from device (ex. there is another client
# (pingviewer gui) making requests to the proxy)

import time
import argparse
from Ping import PingMessage
import socket, errno
from pymavlink import mavutil

parser = argparse.ArgumentParser(description="Ping1D to mavlink bridge.")
parser.add_argument('--ping', action="store", type=str, default="0.0.0.0:9090", help="Ping device udp address and port. ex \"0.0.0.0:9090\"")
parser.add_argument('--mavlink', action="store", type=str, default="0.0.0.0:9000", help="Mavlink udp address and port. ex \"0.0.0.0:9000\"")
parser.add_argument('--min-confidence', action="store", type=int, default=50, help="Minimum acceptable confidence percentage for depth measurements.\"")
args = parser.parse_args()

## The time that this script was started
tboot = time.time()

## Parser to decode incoming PingMessage
ping_parser = PingMessage.PingParser()

## Messages that have the current distance measurement in the payload
distance_messages = [PingMessage.PING1D_DISTANCE, PingMessage.PING1D_DISTANCE_SIMPLE, PingMessage.PING1D_PROFILE]

## The minimum interval time for distance updates to the autopilot
ping_interval_ms = 0.1

## The last time a distance measurement was received
last_distance_measurement_time = 0

## The last time a distance measurement was requested
last_ping_request_time = 0

pingargs = args.ping.split(':')
pingserver = (pingargs[0], int(pingargs[1]))

autopilot_io = mavutil.mavlink_connection("udpout:" + args.mavlink, source_system=1, source_component=192)

ping1D_io = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ping1D_io.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ping1D_io.setblocking(False)

## Send a request for distance_simple message to ping device
def sendPing1DRequest():
  data = PingMessage.PingMessage()
  data.request_id = PingMessage.PING1D_DISTANCE_SIMPLE
  data.src_device_id = 0
  data.packMsgData()
  ping1D_io.sendto(data.msgData, pingserver)

# some extra information for the DISTANCE_SENSOR mavlink message fields
min_distance = 20
max_distance = 5000
type = 2
orientation = 25
covarience = 0

## Send distance_sensor message to autopilot
def sendDistanceData(distance, deviceid, confidence):
  print("sending distance %d confidence %d" % (distance, confidence))
  if confidence < args.min_confidence:
    distance = 0

  autopilot_io.mav.distance_sensor_send(
    (time.time() - tboot) * 1000, # time_boot_ms
    min_distance, # min_distance
    max_distance, # max_distance
    distance/10, # distance
    type, # type
    deviceid, # device id
    orientation,
    covarience)

while True:
  time.sleep(0.001)
  tnow = time.time()
  
  # request data from ping device
  if(tnow > last_distance_measurement_time + ping_interval_ms):
    if(tnow > last_ping_request_time + ping_interval_ms):
      last_ping_request_time = time.time()
      sendPing1DRequest()

  # read data in from ping device
  try:
    data, address = ping1D_io.recvfrom(4096)
  except Exception as e:
            if e.errno == errno.EAGAIN:
              pass # waiting for data
            else:
              raise e
            continue # back to top of loop

  # decode data from ping device, forward to autopilot
  for byte in data:
    if ping_parser.parseByte(byte) == PingMessage.PingParser.NEW_MESSAGE:
      if ping_parser.rxMsg.message_id in distance_messages:
        last_distance_measurement_time = time.time()
        distance = ping_parser.rxMsg.distance
        deviceid = ping_parser.rxMsg.src_device_id
        confidence = ping_parser.rxMsg.confidence
        sendDistanceData(distance, deviceid, confidence)
