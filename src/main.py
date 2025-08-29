import datetime
import json

MAX_FLOOR = 10
FEE_PARK = 1

# 주차장 주차 현황 출력
def print_park_info():
    print(f"{"=" * 20} parking lot information {"=" * 20}")
    for i in range(MAX_FLOOR):
        print(f"{MAX_FLOOR - i}층:\t", end="")
        for j in range(10):
            if j == 9:
                print("[ ]" if parking_lot_info[i][j] == 0 else "[X]")
            else:
                print("[ ]" if parking_lot_info[i][j] == 0 else "[X]", end=" ")
    print()

# 정기 등록 차량 출력
def print_registered_vehicle_info():
    print(f"{"=" * 20} registered vehicle information {"=" * 20}")
    print(json.dumps(registered_vehicle_info, indent=4), end="\n\n")

# 빈 주차장 자리 찾기
def get_parking_position():
    flag = False

    for i in range(MAX_FLOOR - 1, -1, -1):
        for j in range(10):
            if parking_lot_info[i][j] == 0:
                flag = True
                break
        if flag:
            break
    
    return (i, j)

# 주차장 정보 (0: 빔, 1: 참)
parking_lot_info = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 1]
]

# 주차장에 들어온 차량 정보
parked_vehicle_info = dict()

# 정기 등록 차량 정보
registered_vehicle_info = {
    "1234": 20,
    "4567": 30,
    "3682": 40,
    "4482": 50
}

# 처음 시작 주차장 정보, 정기 등록 차량 출력을 위한 작업
parking_lot_flag = True
registered_vehicle_flag = True

while True:
    # 처음 시작이거나 주차장 정보가 변경 됐을 때만 출력
    if parking_lot_flag:
        parking_lot_flag = False
        print_park_info()

    # 처음 시작이거나 정기 등록 차량 정보가 변경 됐을 때만 출력
    if registered_vehicle_flag:
        registered_vehicle_flag = False
        print_registered_vehicle_info()

    command = input("Enter command (\"exit\": exit | \"1\": vehicle in | \"2\": vehicle out | \"3\": add registered vehicle | \"4\": delete registered vehicle) | \"5\": read parked vehicle info | \"6\": add parking ticket: ")

    match command:
        # exit은 exit
        case "exit":
            break
        # 1은 차량 들어감
        case "1":
            car_num = input("Enter your car number: ")
            # 들어온 시간 | datetime.datetime.now()는 현재 시각 (년,월,일,시간,분,초)
            enter_time = datetime.datetime.now()
            # get_parking_position 1층부터 1번 자리부터 찾아서 빈 자리를 가져오는 함수
            parking_floor, parking_num = get_parking_position()

            print(f"{MAX_FLOOR -parking_floor} floor - {parking_num + 1} is empty. I'll park your vehicle \"{MAX_FLOOR -parking_floor} floor - {parking_num + 1}\"")

            # 주차장 자리에 자리 참 표시
            parking_lot_info[parking_floor][parking_num] = 1
            
            car_type = input("Enter car type (electric, gasoline): ")

            # 지금 들어온 차량의 정보를 주차된 차량 정보에 저장
            parked_vehicle_info[car_num] = {"entertime": enter_time, "floor": parking_floor, "num": parking_num, "cartype": car_type, "parkingticket": False}

            # 주차장 정보가 변경 됐기 때문에 출력을 위한 flag
            parking_lot_flag = True
        # 2는 차량 나감
        case "2":
            car_num = input("Enter your car number: ")

            # cur_vehicle_info는 현재 나가는 차량의 정보
            # 주차된 차량의 정보를 저장하는 dict에서 차량 번호를 가지고 정보를 가져와서 cur_vehicle_info에 저장
            cur_vehicle_info = parked_vehicle_info.pop(car_num)

            # 주차장에서 나가는 차량의 자리 자리 빔으로 변경
            parking_lot_info[cur_vehicle_info["floor"]][cur_vehicle_info["num"]] = 0

            # 현재 시간 - 지금 나가는 차량의 들어온 시간 (현재시간: datetime.datetime.now())
            parking_time = datetime.datetime.now() - cur_vehicle_info["entertime"]

            # 지금 나가는 차량이 주차권을 받았으면
            if cur_vehicle_info["parkingticket"]:
                # 20초 할인인데 들어온지 20초가 안됐으면 주차 시간이 음수가 됨 그래서 20초 이상이면 주차 시간에서 20초 뺌
                if parking_time.total_seconds() > 20:
                    parking_senconds = parking_time.total_seconds() - 20
                # 20초 이하면 그냥 주차시간 0으로 바꿈
                else:
                    parking_senconds = 0
            # 주차권을 받지 않았으면
            else:
                # 그냥 나간 시간 - 들어온 시간이 주차 시간
                parking_senconds = parking_time.total_seconds()
                # 주차 시간이 5초 이하면 회차로 주차시간 0으로 변경
                if parking_senconds < 5:
                    parking_senconds = 0
            
            # 주차료는 1초에 1원
            total_fee = parking_senconds * FEE_PARK

            # 지금 나가는 차량이 정기 등록 차량이면
            if car_num in registered_vehicle_info:
                # 그 차량의 할인율 만큼 할인
                total_fee = total_fee * (100 - registered_vehicle_info[car_num]) / 100

            # 지금 나가는 차량이 전기차면
            if cur_vehicle_info["cartype"] == "electric":
                # 20% 할인
                total_fee = total_fee * 80 / 100

            print(f"{car_num} | total fee: {total_fee}")

            # 주차장 정보가 변경 됐기 때문에 출력을 위한 flag
            parking_lot_flag = True
        # 3은 정기 차량 등록
        case "3":
            car_num = input("Enter your car number: ")
            discount_rate = int(input("Enter discount rate(%): "))

            # 정기 등록 차량을 차량번호를 key, 할인률을 value로 저장
            registered_vehicle_info[car_num] = discount_rate

            # 정기 등록 차량 정보가 변경 됐기 때문에 출력을 위한 flag
            registered_vehicle_flag = True
        # 4는 정기 차량 삭제
        case "4":
            car_num = input("Enter your car number: ")

            # 정기 등록 차량 정보에서 입력 받은 차 제거
            registered_vehicle_info.pop(car_num)

            # 정기 등록 차량 정보가 변경 됐기 때문에 출력을 위한 flag
            registered_vehicle_flag = True
        # 5는 들어온 차량 정보 출력
        case "5":
            print(f"parked vehicle info: {parked_vehicle_info}", end="\n\n")
        # 6은 주차권 등록
        case "6":
            car_num = input("Enter your car number: ")
            # 해당 차량 번호의 주차권은 True
            parked_vehicle_info[car_num]["parkingticket"] = True
