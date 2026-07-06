# 담당 부원 : 정지민
# 기본 함수 구조는 README.md 참고해주세요.
import random
import time

def play_game5(players):
    """
    베스킨라빈스 31 게임
    :param players: 현재 게임에 참여 중인 플레이어들의 이름 리스트
    :return: 31을 말한 패배자 이름(str)
    """

    print("\n" + "=" * 45)
    print("🍦 베스킨라빈스 31 게임 🍦")
    print("=" * 45)
    print("규칙: 한 번에 1~3개의 숫자를 말할 수 있습니다.")
    print("31을 말하는 사람이 패배합니다.")
    print("패배자는 술을 마십니다! 🍺")
    print("=" * 45)

    current_number = 0
    turn_index = 0

    while current_number < 31:
        current_player = players[turn_index]

        print(f"\n현재 숫자: {current_number}")
        print(f"👉 {current_player}님의 차례입니다.")

        if turn_index == 0:
            count = get_user_count(current_number)
        else:
            count = get_computer_count(current_number)
            print(f"{current_player}님은 {count}개의 숫자를 말합니다.")
            time.sleep(0.5)

        print(f"\n{current_player}님이 말한 숫자:")
        for _ in range(count):
            current_number += 1
            print(current_number)
            time.sleep(0.2)

            if current_number == 31:
                print("\n" + "💥" * 10)
                print(f"{current_player}님이 31을 말했습니다!")
                print(f"패배자는 {current_player}님입니다. 🍺")
                print("💥" * 10)
                return current_player

        turn_index = (turn_index + 1) % len(players)

def get_user_count(current_number):
    while True:
        try:
            count = int(input("몇 개의 숫자를 말할까요? (1~3): "))

            if count < 1 or count > 3:
                print("1, 2, 3 중에서 입력해주세요.")
                continue

            if current_number + count > 31:
                print("31을 넘길 수 없습니다.")
                continue

            return count

        except ValueError:
            print("숫자만 입력해주세요.")

def get_computer_count(current_number):
    remaining = 31 - current_number

    if remaining <= 3:
        return remaining

    return random.randint(1, 3)

