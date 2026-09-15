import time
from neuromeka import IndyDCP3

# ==========================================
# 1. 기본 설정 및 파라미터 정의
# ==========================================
ROBOT_IP = "192.168.3.5"
indy = IndyDCP3(ROBOT_IP)

# 속도 및 가속도 비율 (%)
MOVE_VEL = 50
MOVE_ACC = 30
APPROACH_VEL = 50
APPROACH_ACC = 30

# Digital I/O 주소 맵핑
VACUUM_DO = 2
DI_TRIGGER_1_A = 3    # Pattern 1 트리거 A
DI_TRIGGER_1_B = 8    # Pattern 1 트리거 B
DI_TRIGGER_2 = 9      # Pattern 2 트리거 (언로딩)
DI_TRIGGER_HOME = 10  # Home 이동 트리거

# [경유점 관절 각도] Home <-> 작업 영역 이동 시 거치는 안전 관절 각도 (deg)
# ※ JSON 파일의 홈 및 작업 중간자세 기준: [-40.0, -15.0, -80.0, 0.0, -85.0, -40.0]
# 현장 로봇 자세에 맞춰 각도값을 수정하여 사용하세요.
VIA_JOINT = [-40.0, -15.0, -80.0, 0.0, -85.0, -40.0]

# [고정 위치 1] 피킹 타겟 (PICK_POS)
PICK_POS = [312.82, -384.7, 334.92, -0.78, -162.23, 0.03]
PICK_OFFSET_Z = 150.0  # approach/retract 150mm

# [고정 위치 2] 배출 타겟 (DISCHARGE_POS)
DISCHARGE_POS = [-1.91, -388.36, 473.71, 178.93, -0.42, 179.94]
DISCHARGE_OFFSET_Z = 100.0  # approach/retract 100mm

# [팔레트 1 (test1)] 좌표 리스트 & Approach 높이
PALLET_TEST1 = [
    [177.43, -591.16, 404.55, 179.80, -0.19, 179.83],
    [173.34, -554.99, 407.53, 179.71, -0.24, 179.83],
    [132.07, -559.29, 406.21, 179.41, -0.39, 179.82],
    [136.15, -595.46, 403.22, 179.51, -0.33, 179.82],
]
PALLET_TEST1_OFFSET_Z = 80.0

# [팔레트 2 (test2)] 좌표 리스트 & Approach 높이
PALLET_TEST2 = [
    [175.34, -594.25, 431.73, 179.44, -0.37, 179.82],
    [175.44, -556.02, 424.56, 179.39, -0.40, 179.83],
    [139.36, -557.98, 424.46, 179.24, -0.48, 179.82],
    [139.26, -596.21, 431.63, 179.30, -0.44, 179.81],
]
PALLET_TEST2_OFFSET_Z = 150.0


# ==========================================
# 2. 로봇 제어 유틸리티 함수
# ==========================================
def check_result(result, command_name):
    if isinstance(result, dict):
        code = result.get("code")
        if code not in (0, "0", None):
            raise RuntimeError(f"{command_name} 실패: {result}")


def wait_move():
    indy.wait_for_motion_state("is_target_reached")


def move_joint(target_joint, vel=MOVE_VEL, acc=MOVE_ACC):
    """관절 각도 기준 이동 (MoveJ)"""
    result = indy.movej(
        jtarget=target_joint,
        blending_type=0,
        blending_radius=0.0,
        vel_ratio=vel,
        acc_ratio=acc,
    )
    check_result(result, "MoveJ")
    wait_move()


def move_linear(target_pose, vel=MOVE_VEL, acc=MOVE_ACC):
    """Base 좌표계 기준 절대 좌표 선형 이동 (MoveL)"""
    result = indy.movel(
        target_pose,
        blending_type=0,
        base_type=0,
        blending_radius=0.0,
        vel_ratio=vel,
        acc_ratio=acc,
    )
    check_result(result, "MoveL(Base)")
    wait_move()


def move_tool_relative(dz, vel=APPROACH_VEL, acc=APPROACH_ACC):
    """Tool 좌표계 기준 상대 직선 이동 (Z축 진입/복귀)"""
    target = [0.0, 0.0, dz, 0.0, 0.0, 0.0]
    result = indy.movel(
        target,
        blending_type=0,
        base_type=1,  # Tool 기준 상대 이동
        blending_radius=0.0,
        vel_ratio=vel,
        acc_ratio=acc,
    )
    check_result(result, "MoveL(Tool)")
    wait_move()


def move_via_point():
    """안전 경유점으로 관절 이동 (MoveJ)"""
    print(f"\n[안전 이동] 경유점으로 MoveJ 이동 중... -> {VIA_JOINT}")
    move_joint(VIA_JOINT)


def vacuum_on():
    """scup_on2: 흡착 ON"""
    result = indy.set_do([(VACUUM_DO, True)])
    check_result(result, "Vacuum ON")
    time.sleep(0.3)


def vacuum_off():
    """scup_off2: 흡착 OFF"""
    result = indy.set_do([(VACUUM_DO, False)])
    check_result(result, "Vacuum OFF")
    time.sleep(0.3)


def read_di(address):
    """DI 신호 상태 읽기"""
    try:
        res = indy.get_di()
        if isinstance(res, dict) and "signals" in res:
            signals = res["signals"]
            if len(signals) > address and signals[address].get("address") == address:
                return signals[address].get("state") == 1
            for item in signals:
                if item.get("address") == address:
                    return item.get("state") == 1
    except Exception:
        pass
    return False


# ==========================================
# 3. 작업 시퀀스 단위 함수
# ==========================================
def pick_from_pose(pose, approach_dist):
    """목표 지점으로 이동 후 진입 -> 흡착 -> 복귀"""
    move_linear(pose)
    move_tool_relative(approach_dist)
    vacuum_on()
    move_tool_relative(-approach_dist)


def place_to_pose(pose, approach_dist):
    """목표 지점으로 이동 후 진입 -> 분사/해제 -> 복귀"""
    move_linear(pose)
    move_tool_relative(approach_dist)
    vacuum_off()
    move_tool_relative(-approach_dist)


def run_pattern_palletize():
    """패턴 1: 픽업대에서 물건을 가져와 test1, test2에 적재"""
    print("\n>>> [동작] 팔레타이징 시퀀스 시작 (DI 3 & DI 8)")
    
    # 0. 시작 전 안전 경유점 MoveJ 이동
    move_via_point()

    # 1. test1 팔레트에 4개 적재
    print("--- [1/2] Pallet test1 적재 시작 ---")
    for idx, place_pos in enumerate(PALLET_TEST1, start=1):
        print(f"test1 [{idx}/4] Pick & Place")
        pick_from_pose(PICK_POS, PICK_OFFSET_Z)
        place_to_pose(place_pos, PALLET_TEST1_OFFSET_Z)

    # 2. test2 팔레트에 4개 적재
    print("--- [2/2] Pallet test2 적재 시작 ---")
    for idx, place_pos in enumerate(PALLET_TEST2, start=1):
        print(f"test2 [{idx}/4] Pick & Place")
        pick_from_pose(PICK_POS, PICK_OFFSET_Z)
        place_to_pose(place_pos, PALLET_TEST2_OFFSET_Z)

    # 작업 완료 후 경유점을 거쳐 복귀
    move_via_point()
    print(">>> [완료] 팔레타이징 시퀀스 완료\n")


def run_pattern_depalletize():
    """패턴 2: test2, test1에서 물건을 가져와 배출 위치로 이동"""
    print("\n>>> [동작] 디팔레타이징 시퀀스 시작 (DI 9)")

    # 0. 시작 전 안전 경유점 MoveJ 이동
    move_via_point()

    # 1. test2 팔레트에서 4개 언로딩
    print("--- [1/2] Pallet test2 픽업 -> 배출 ---")
    for idx, pick_pos in enumerate(PALLET_TEST2, start=1):
        print(f"test2 [{idx}/4] De-palletize")
        pick_from_pose(pick_pos, PALLET_TEST2_OFFSET_Z)
        place_to_pose(DISCHARGE_POS, DISCHARGE_OFFSET_Z)

    # 2. test1 팔레트에서 4개 언로딩
    print("--- [2/2] Pallet test1 픽업 -> 배출 ---")
    for idx, pick_pos in enumerate(PALLET_TEST1, start=1):
        print(f"test1 [{idx}/4] De-palletize")
        pick_from_pose(pick_pos, PALLET_TEST1_OFFSET_Z)
        place_to_pose(DISCHARGE_POS, DISCHARGE_OFFSET_Z)

    # 작업 완료 후 경유점을 거쳐 복귀
    move_via_point()
    print(">>> [완료] 디팔레타이징 시퀀스 완료\n")


# ==========================================
# 4. 메인 루프 (Conty 3.3 대응)
# ==========================================
def main():
    print(f"IndyDCP3 연결 시도: {ROBOT_IP}...")
    vacuum_off()
    print("대기 상태: DI 신호 입력을 기다립니다. (종료: Ctrl + C)")

    while True:
        di3 = read_di(DI_TRIGGER_1_A)
        di8 = read_di(DI_TRIGGER_1_B)
        di9 = read_di(DI_TRIGGER_2)
        di10 = read_di(DI_TRIGGER_HOME)

        # 조건 1: DI 3 ON & DI 8 ON
        if di3 and di8:
            run_pattern_palletize()

        # 조건 2: DI 9 ON
        elif di9:
            run_pattern_depalletize()

        # 조건 3: DI 10 ON
        elif di10:
            print("\n>>> [동작] 경유점(MoveJ)을 거쳐 HOME 위치로 이동 (DI 10)")
            move_via_point()
            indy.move_home()
            wait_move()
            print(">>> [완료] HOME 도착\n")

        time.sleep(0.05)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자에 의해 프로그램을 중단합니다.")
        vacuum_off()
        indy.stop_motion()
    except Exception as e:
        print(f"\n[오류 발생]: {e}")
        vacuum_off()
        indy.stop_motion()
    finally:
        print("프로그램 종료")