from neuromeka import IndyDCP3 
import time

ROBOT_IP = "192.168.3.5"
indy = IndyDCP3(ROBOT_IP)



WAYPOINT1 = [0,0,-90,0,-90,0]
WAYPOINT2 = [-30,20,-70,30,-80,-50]
WAYPOINT3 = [30,10,-60,-20,-70,40]
def wait_move_done():
    print("이동 완료 대기 중...")
    while True:
        motion_data = indy.get_motion_data()
        movedone = motion_data['is_target_reached']
        print("movedone=",movedone)
        q = indy.get_robot_data()['q']
        print(q)
        if movedone == True:
            break
        time.sleep(0.1)
    print("이동 완료!")

print("Home 이동")
indy.move_home()
wait_move_done()

print("Waypoint1 이동")
indy.movej(jtarget=WAYPOINT1, vel_ratio=20, acc_ratio=20)
wait_move_done()

print("Waypoint2 이동")
indy.movej(jtarget=WAYPOINT2, vel_ratio=20, acc_ratio=20)
wait_move_done()

print("Waypoint3 이동")
indy.movej(jtarget=WAYPOINT3, vel_ratio=20, acc_ratio=20)
wait_move_done()

print("Home 복귀")
indy.move_home()

print("전체 동작 완료")