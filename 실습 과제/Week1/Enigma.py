# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by
# Wehrmacht and Luftwaffe, Nazi Germany.
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

import copy
from ctypes import ArgumentError

# Enigma Components
# UKW <- 3 WHEELS <- ETW
# turn -> 0 ~ 25
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16  # 0 ~ 16 -> 16은 Q (Turnover)
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4  # 0 ~ 4 -> 4는 E (Turnover)
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21  # 0 ~ 21 -> 21은 V (Turnover)
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}


def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)


# Enigma Logics Start

# Plugboard
# ex) input = AB일 때 문자 A가 들어오면 B 값을 뱉어냄
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input


# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]


# 과제 부분 - 201702074 조성훈
# Wheels ( reverse = True or reverse = False)
def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    # reverse가 True일 경우는 UKW -> ETW, False 경우는 UKW <- ETW
    # 입력받은 input(알파벳 하나)이 휠을 통과하면서 바뀌는 알파벳 값을 저장
    # SETTINGS["WHEELS"]에 원소가 삽입된 순서대로 방향 구현

    # 참고자료에서 주어진 에니그마 에뮬레이터의 구조를 보고 구현(RING 세팅X)
    # https://piotte13.github.io/enigma-cipher/

    # 로터 1과 2, 2와 3의 포지션 차이 -> 이걸 이용해 포지션마다 알파벳 바뀌는 것을 고려해줌
    wheel_position1 = SETTINGS["WHEEL_POS"][1] - SETTINGS["WHEEL_POS"][0]
    wheel_position2 = SETTINGS["WHEEL_POS"][2] - SETTINGS["WHEEL_POS"][1]

    # 로터 1, 로터 2, 로터 3 안에서의 신호 통과 과정 구현(입력받은 포지션과 로터를 이용)
    # reverse가 True
    if reverse:
        wheel_I = SETTINGS["ETW"][(ord(input) - ord('A') + SETTINGS["WHEEL_POS"][2]) % 26]
        wheel_I = SETTINGS["ETW"][SETTINGS["WHEELS"][2]['wire'].index(wheel_I)]

        wheel_II = SETTINGS["ETW"][(ord(wheel_I) - ord('A') - wheel_position2) % 26]
        wheel_II = SETTINGS["ETW"][SETTINGS["WHEELS"][1]['wire'].index(wheel_II)]

        wheel_III = SETTINGS["ETW"][(ord(wheel_II) - ord('A') - wheel_position1) % 26]
        wheel_III = SETTINGS["ETW"][SETTINGS["WHEELS"][0]['wire'].index(wheel_III)]

        wheel_III = SETTINGS["ETW"][(ord(wheel_III) - ord('A') - SETTINGS["WHEEL_POS"][0]) % 26]

    # reverse가 False
    else:
        wheel_I = SETTINGS["WHEELS"][0]['wire'][((ord(input) - ord('A') + SETTINGS["WHEEL_POS"][0]) % 26)]

        wheel_II = SETTINGS["WHEELS"][1]['wire'][(ord(wheel_I) - ord('A') + wheel_position1) % 26]

        wheel_III = SETTINGS["WHEELS"][2]['wire'][(ord(wheel_II) - ord('A') + wheel_position2) % 26]
        wheel_III = SETTINGS["ETW"][(ord(wheel_III) - ord('A') - SETTINGS["WHEEL_POS"][2]) % 26]

    return wheel_III


# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]


# 과제 부분 - 201702074 조성훈
# Wheel Rotation
# 알파벳 하나씩 입력될 때마다 제일 먼저 입력된 로터가 인덱스 하나씩 움직임
# 그러다 해당 로터의 turn 값과 같아진 후 글자가 입력되면 그 다음 로터의 인덱스 하나씩 움직임(홈에 걸려서 돌아가는 느낌)
def rotate_wheels():
    # Implement Wheel Rotation Logics
    # 첫 번째 로터의 인덱스가 첫 번째 로터의 turn 값보다 같거나 작을 경우에는 인덱스 하나씩 증가
    # turn 값일 경우 노치에 걸려서 다음 번째 로터가 1씩 증가

    if SETTINGS["WHEEL_POS"][0] == SETTINGS["WHEELS"][0]['turn']:
        # ex) 포지션에 Q E _(16 4 _) 입력 -> turn 값이 두 개나 걸리는 조건
        if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]['turn']:
            SETTINGS["WHEEL_POS"][1] += 1
            SETTINGS["WHEEL_POS"][2] += 1
        else:
            SETTINGS["WHEEL_POS"][1] += 1

    if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]['turn']:
        SETTINGS["WHEEL_POS"][2] += 1

    SETTINGS["WHEEL_POS"][0] += 1


    pass

# Enigma Exec Start
# 평문, 반사판, 휠 선택, 플러그 보드 설정 입력
# L -> R, 입력한 순서대로 신호가 들어가게끔 구현했음
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

# 입력받은 설정 적용하는 함수 실행
apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

# Enigma 작동 과정
for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
