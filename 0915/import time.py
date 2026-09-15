import time
from neuromeka import IndyDCP3

indy = IndyDCP3("192.168.3.5")

# 1초마다 DI 원본 데이터 출력
while True:
    di_raw = indy.get_di()
    print("수신된 get_di() 원본:", di_raw, " | Type:", type(di_raw))
    time.sleep(1)