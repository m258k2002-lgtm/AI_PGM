
from neuromeka import IndyDCP3
from time import sleep
ROBOT_IP = "192.168.3.2"
MOVE_VEL = 10
MOVE_ACC = 10
VACUUM_DO = 2
GRID_SIZE = 5
CELL_PITCH = 40.0
APPROACH_HEIGHT = 50.0
CENTER_X = 
CENTER_Y = 
TARGET_Z = 
RX = 
RY = 
RZ = 
indy = IndyDCP3(ROBOT_IP)
def motion_done_check():
    indy.wait_for_motion_state("is_target_reached")
def move_linear(target_position):
    indy.movel( ttarget=target_position,vel_ratio=MOVE_VEL,acc_ratio=MOVE_ACC )
    motion_done_check()
def vacuum_on():
    indy.set_do([{"address": VACUUM_DO, "state": True } ])
    sleep(1)
def vacuum_off():
    indy.set_do([{ "address": VACUUM_DO, "state": False } ])
    sleep(1)
# Pick 동작
# 접근 → 타겟 → 흡착 → 리트랙트
def pick(cell_index):
    move_linear(pos[cell_index][0])
    move_linear(pos[cell_index][1])
    vacuum_on()
    move_linear(pos[cell_index][2])
# Place 동작
# 접근 → 타겟 → 흡착 해제 → 리트랙트
def place(cell_index):
    move_linear(pos[cell_index][0])
    move_linear(pos[cell_index][1])
    vacuum_off()
    move_linear(pos[cell_index][2])
def create_grid_positions():
    position_list = []
    for row_index in range(GRID_SIZE):
        for column_index in range(GRID_SIZE):
            x = CENTER_X + (row_index - 2) * CELL_PITCH
            y = CENTER_Y + (column_index - 2) * CELL_PITCH
            approach_position = [x, y, TARGET_Z + APPROACH_HEIGHT,
                RX,  RY,  RZ  ]
            target_position = [ x,y, TARGET_Z, RX, RY, RZ ]
            retract_position = [x,y,TARGET_Z + APPROACH_HEIGHT, RX, RY, RZ ]
            position_list.append([approach_position,target_position,
                retract_position ])
    return position_list
pos = create_grid_positions()
print(pos)
indy.move_home()
motion_done_check()
# 1번 → 2번, 2번 → 3번, ... , 24번 → 25번
# 총 24회의 Pick & Place 수행
for cell_index in range(len(pos) - 1):
    pick(cell_index)
    current_position = indy.get_control_state()["p"]
    print("Pick 완료 위치:", current_position)
    place(cell_index + 1)
    current_position = indy.get_control_state()["p"]
    print("Place 완료 위치:", current_position)
move_linear(pos[12][0])
motion_done_check()
indy.movel(ttarget=pos[12][1]) 

