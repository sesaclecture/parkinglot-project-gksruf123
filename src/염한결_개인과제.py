# 염한결 - 주차 타워 관리 시스템 개인 과제입니다!

#모듈
import datetime

#변수
cur_parking_lot = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

registered_car = {
    1995 : 30
}

user_info = {}

parking_lot_info_flag = True

parking_fee = 1000

#진입점
run = True

while run:
    user_request = int(input("what ya gonna do? [1 - check the current parking lot / 2 - parking a car / 3 - get out a car / 4 - check a membership information / 5 - register our membership / 6 - deregister our membership / 0 - exit this program]"))
    match user_request:
        case 1: #주차장 현황 확인
            for row in cur_parking_lot:
                print(row)
        case 2: #입차
            is_full = sum(sum(row) for row in cur_parking_lot)
            if is_full == 100:
                print("there's no parking zone")
                break
            else:
                if parking_lot_info_flag:    
                    for row in cur_parking_lot:
                        print(row)
                    parking_lot_info_flag = False
                while True:
                    car_num = int(input("type your car number. if you wanna back, press 0."))  
                    if car_num == 0:
                        break
                    elif car_num in user_info:
                        print("you've already parked.")
                        continue
                    elif car_num in registered_car:
                        print("welcome my homie!")
                        break
                    else:
                        break
                if car_num == 0:
                    continue
                if car_num not in user_info:
                    user_info[car_num] = {}
                while True:
                    try:
                        selected_floor = int(input("plz select your preferred parking floor. (ex: 1~10) if you wanna back, press 0."))
                        if selected_floor == 0:
                            break
                        elif selected_floor > 0 and selected_floor <= 10:
                            if sum(cur_parking_lot[10-selected_floor]) == 10:
                                print("there's no place to park on that floor. choose other floor.")
                                continue
                            else:
                                print("the floor is selected!")
                                break                
                        else:
                            print("c'mon dude. that's invalid number.")
                            continue
                    except:
                        print("Bro... that ain't even a number:(")
                        continue
                if selected_floor == 0:
                    continue
                while True:
                    try:
                        selected_spot = int(input("plz select your preferred parking spot. (ex: 1~10) if you wanna back, press 0."))
                        if selected_spot == 0:
                            break
                        elif selected_spot > 0 or selected_spot <= 10:
                            if cur_parking_lot[10-selected_floor][selected_spot-1] == 1:
                                # 이것도 최종적으로 선택된 자리.
                                print("there's no place to park on that spot. choose other spot.")
                            else:
                                print("the spot is selected!")
                                break
                        else:
                            print("c'mon dude. that's invalid number.")
                            continue
                    except:
                        print("Bro... that ain't even a number:(")                    
                        continue
                if selected_spot == 0:
                    continue
                enter_time = datetime.datetime.now()
                chosen_spot = {
                    "floor" : 10-selected_floor,
                    "spot" : selected_spot-1
                } #chosen_spot 이게 최종적으로 선택된 자리.
                user_info[car_num]["chosen_spot"] = chosen_spot
                user_info[car_num]["enter_time"] = enter_time
                print(user_info)
                cur_parking_lot[10-selected_floor][selected_spot-1] = 1
                parking_lot_info_flag = True
                print("you successfully parked your car!")
        case 3: #출차
            while True:
                car_num = int(input("what's your car number? if you wanna quit, press 0."))
                if car_num in user_info:
                    parked_time = datetime.datetime.now() - user_info[car_num]["enter_time"]
                    parked_sec = parked_time.total_seconds()
                    basic_fee = int(parked_sec) * parking_fee
                    print(f"your basic fee is {basic_fee}")
                    if car_num in registered_car:
                        total_fee = basic_fee * (100 - registered_car[car_num]) / 100
                        print(f"hello! you are my guy! so, you got a {registered_car[car_num]}% discount!")
                    else:
                        total_fee = basic_fee
                    print(cur_parking_lot)
                    print(f"your total fee is '{total_fee}'won!")
                    print("thank you for using our service! byebye!")
                    user_info.pop(car_num)
                    break
                elif car_num == 0:
                    break
                else:
                    print("check the number!!!")
                    continue
        case 4: #정기 등록 차량 정보 확인
            print(registered_car)
        case 5: #정기 등록하기
            while True:
                car_num = int(input("what's your car number? if you wanna quit, press 0."))
                if car_num in registered_car:
                    print("you're already our member! thank you!")
                    break
                elif car_num == 0:
                    break
                else:
                    discount_rate = int(input("how much discount rate do you want?"))
                    print(f"from now you're our member! your discount rate is {discount_rate}%!")
                    registered_car[car_num] = discount_rate
                    break
        case 6: #정기 등록 해제하기
            while True:
                car_num = int(input("okay.. so, what's your car number? if you wanna quit, press 0."))
                if car_num in registered_car:
                    registered_car.pop(car_num)
                    print(registered_car)
                    print("deregistering is succeeded.")
                    print("someday, we'll meet again.")
                    break
                elif car_num == 0:
                    break
                else:
                    print("check the number.")
                    continue
        case 0:
            run = False
        case _:
            continue