#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
导入相关库
"""
import sys
import tty, termios
import rospy 
from geometry_msgs.msg import Twist   

cmd = Twist() #速度相关的消息
pub = rospy.Publisher("cmd_vel", Twist, queue_size=1) #创建速度相关的话题发布者对象
def keyboardLoop(): #键盘监听的函数
    rospy.init_node("teleop_robot")
    rate = rospy.Rate(rospy.get_param("~hz",10)) #初始化监听键盘按钮时间间隔 
    #速度变量
    # 慢速
    walk_vel_ = rospy.get_param('walk_vel', 0.2)
    yaw_rate_ = rospy.get_param('yaw_rate', 1.0)
    # 快速
    run_vel_ = rospy.get_param('run_vel', 1.0)
    yaw_rate_run_ = rospy.get_param('yaw_rate_run', 1.5)
    # walk_vel_前后速度
    max_tv = walk_vel_
    # yaw_rate_旋转速度
    max_rv = yaw_rate_
    # 参数初始化
    speed = 0
    turn = 0
    #提示信息
    print ("使用[WASD]控制机器人") 
    print ("按[Q]退出" )  
    #读取按键循环
    while not rospy.is_shutdown():
        # linux下读取键盘按键
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
		#不产生回显效果
        old_settings[3] = old_settings[3] & ~termios.ICANON & ~termios.ECHO
        try :
            tty.setraw( fd )
            ch = sys.stdin.read( 1 )
        finally :
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # ch代表获取的键盘按键
        if ch == 'w':
            max_tv = walk_vel_     #慢速前进
            speed = 1
            turn = 0
        elif ch == 's':
            max_tv = walk_vel_     #慢速后退
            speed = -1
            turn = 0
        elif ch == 'a':
            max_rv = yaw_rate_     #慢速左转
            speed = 0
            turn = 1
        elif ch == 'd':
            max_rv = yaw_rate_     #慢速右转
            speed = 0
            turn = -1
        elif ch == 'W':            #快速前进
            max_tv = run_vel_
            speed = 1
            turn = 0
        elif ch == 'S':           #快速后退
            max_tv = run_vel_
            speed = -1
            turn = 0
        elif ch == 'A':           #快速左转
            max_rv = yaw_rate_run_
            speed = 0
            turn = 1
        elif ch == 'D':           #快速右转
            max_rv = yaw_rate_run_
            speed = 0
            turn = -1
        elif ch == 'q':           #退出
            exit()
        else:
            max_tv = walk_vel_
            max_rv = yaw_rate_
            speed = 0
            turn = 0
        #发送消息
        cmd.linear.x = speed * max_tv
        cmd.angular.z = turn * max_rv
        pub.publish(cmd)
        rate.sleep()

def stop_robot():
    cmd.linear.x = 0.0
    cmd.angular.z = 0.0
    pub.publish(cmd)
 
if __name__ == '__main__':
    try:
        keyboardLoop()
    except rospy.ROSInterruptException:
        pass  
    
    

