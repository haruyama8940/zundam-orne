#! /usr/bin/env python3
from numpy import diff
import rospy
from std_msgs.msg import String
import time
import simpleaudio
import roslib
from std_srvs.srv import SetBool, SetBoolResponse, SetBoolRequest
roslib.load_manifest('zundam_orne')
from waypoint_manager_msgs.msg import Waypoint

class speakNode():
    def __init__(self):
        self.sub = rospy.Subscriber('waypoint', Waypoint, self.waypoint_callback)
        self.srv = rospy.Service('test_speak', SetBool, self.callback_srv) 
        self.goal_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne')+'/voice/goal.wav')
        self.white_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne') +'/voice/white.wav')
        self.akete_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne') +'/voice/akete.wav')
        self.auto_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne')+'/voice/auto.wav')
 
        self.waypoint_id = 1
        self.old_waypoint_id = 0
        self.id_diff=0     
#        self.waypoint_key

        # self.pub = rospy.Publisher('topic name', String, queue_size=1)

    def waypoint_callback(self, data):
        self.waypoint_id = data.identity
        self.waypoint_key =data.properties

    def callback_srv(self,data):
        resp = SetBoolResponse()
        if data.data == True:
            play_sound = self.auto_sound.play()
            play_sound.wait_done()

    def spaeck_function(self):
        if self.waypoint_key == "white":
            play_sound = self.white_sound.play()
            play_sound.wait_done()

        if self.old_waypoint_id != self.waypoint_id:
            play_sound = self.auto_sound.play()
            play_sound.wait_done()
            self.old_waypoint_id = self.waypoint_id

        if self.waypoint_key =="end":
            play_sound =self.goal_sound.play()
            play_sound.wait_done()

if __name__ == '__main__':
    rospy.init_node('test_node')

    time.sleep(1.0)
    speak_node = speakNode()
    print("ready")
    while not rospy.is_shutdown():
        speak_node.spaeck_function()       
        rospy.sleep(1.0)
