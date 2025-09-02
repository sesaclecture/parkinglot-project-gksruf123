import datetime
import json

MAX_FLOOR = 10
FEE_PARK = 1

def print_park_info():
    print(f"{"=" * 20} parking lot information {"=" * 20}")
    for i in range(MAX_FLOOR):
        print(f"{MAX_FLOOR - i}층:\t", end="")
        for j in range(10):
            print("[ ]" if parking_lot_info[i][j] == 0 else "[X]", end = "\n" if j == 9 else " ")
    print()

def print_registered_vehicle_info():
    print(f"{"=" * 20} registered vehicle information {"=" * 20}")
    print(json.dumps(registered_vehicle_info, indent=4), end="\n\n")

def get_parking_position():
    for i in range(MAX_FLOOR - 1, -1, -1):
        for j in range(10):
            if parking_lot_info[i][j] == 0:
                return (i, j)
    
    return (None, None)

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

parked_vehicle_info = dict()

registered_vehicle_info = {
    "1234": 20,
    "4567": 30,
    "3682": 40,
    "4482": 50
}

ticket_codes = {
    "ABC": 10,
    "DEF": 20
}

parking_lot_flag = True
registered_vehicle_flag = True

while True:
    if parking_lot_flag:
        parking_lot_flag = False
        print_park_info()

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

            if car_num in parked_vehicle_info:
                print(f"Error: {car_num} is already parked. Manager called.")
                continue
            enter_time = datetime.datetime.now()

            parking_floor, parking_num = get_parking_position()

            if parking_floor is None or parking_num is None:
                print("Parking tower full!")
                continue

            print(f"{MAX_FLOOR -parking_floor} floor - {parking_num + 1} is empty. I'll park your vehicle \"{MAX_FLOOR -parking_floor} floor - {parking_num + 1}\"")

            parking_lot_info[parking_floor][parking_num] = 1
            
            car_type = input("Enter car type (electric, gasoline): ")

            parked_vehicle_info[car_num] = {"entertime": enter_time, "floor": parking_floor, "num": parking_num, "cartype": car_type, "parkingticket": False}

            parking_lot_flag = True
        # 2는 차량 나감
        case "2":
            car_num = input("Enter your car number: ")

            cur_vehicle_info = parked_vehicle_info.pop(car_num)

            parking_lot_info[cur_vehicle_info["floor"]][cur_vehicle_info["num"]] = 0

            parking_time = datetime.datetime.now() - cur_vehicle_info["entertime"]

            print(f"Parked time: {parking_time.total_seconds():.1f} seconds")

            if cur_vehicle_info["parkingticket"]:
                print(f"Parking ticket applied, discount: {cur_vehicle_info["parkingticket"]} seconds")
                if parking_time.total_seconds() > cur_vehicle_info["parkingticket"]:
                    parking_senconds = parking_time.total_seconds() - cur_vehicle_info["parkingticket"]
                else:
                    parking_senconds = 0
            else:
                parking_senconds = parking_time.total_seconds()
                if parking_senconds < 5:
                    print(f"Parked time is less than 5 seconds, free parking applied!")
                    parking_senconds = 0
            
            total_fee = parking_senconds * FEE_PARK

            if parking_senconds and car_num in registered_vehicle_info:
                print(f"Registered number, {registered_vehicle_info[car_num]}% discount applied!")
                total_fee = total_fee * (100 - registered_vehicle_info[car_num]) / 100

            if parking_senconds and cur_vehicle_info["cartype"] == "electric":
                print("Electric car, 20% discount applied!")
                total_fee = total_fee * 80 / 100

            print()
            print(f"{car_num} | total fee: {total_fee:.0f}")

            parking_lot_flag = True
        # 3은 정기 차량 등록
        case "3":
            car_num = input("Enter your car number: ")
            discount_rate = int(input("Enter discount rate(%): "))

            registered_vehicle_info[car_num] = discount_rate

            registered_vehicle_flag = True
        # 4는 정기 차량 삭제
        case "4":
            car_num = input("Enter your car number: ")

            registered_vehicle_info.pop(car_num)

            registered_vehicle_flag = True
        # 5는 들어온 차량 정보 출력
        case "5":
            print(f"parked vehicle info: {parked_vehicle_info}", end="\n\n")
        # 6은 주차권 등록
        case "6":
            car_num = input("Enter your car number: ")
            code = input("Enter ticket code: ")
            if code in ticket_codes:
                parked_vehicle_info[car_num]["parkingticket"] = ticket_codes[code]
            else:
                print("Invalid code!")
