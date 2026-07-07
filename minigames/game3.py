# 담당 부원 : 이지아
# 기본 함수 구조는 README.md 참고해주세요.

""" 아파트 게임 (이지아)

규칙
-사람들이 손을 쌓아 아파트를 만든 뒤 층수를 외침
-맨 아래 손부터 하나씩 위로 올리면서 외친 숫자를 시작으로 역카운트
-마지막으로 외친 층수에서 맨 위에 놓이는 손의 주인이 패배
"""

import random
import time


def play_apt(players):


    print("=== A P T 게임 시작!===")
    print("==규칙==" \
    """
    -사람들이 손을 쌓아 아파트를 만든 뒤 사람 손 이하의 층수를 외친다
    -맨 아래 손부터 하나씩 위로 올리면서 외친 숫자를 시작으로 역카운트한다.
    -마지막으로 외친 층수에서 맨 위에 놓이는 손의 주인이 패배!
    """)
    hands = []
    for name in players:
        hands.append(name)
        hands.append(name)

    random.shuffle(hands)

    total_floors = len(hands)
    print(f"\n{total_floors}층짜리 아파트가 완성되었습니다.")
    print(f"참가자: {' · '.join(players)}")

    print("\n층수를 외쳐주세요.")
    time.sleep(0.3)

    while True:
        user_input = input(
            f"   '아파트 몇 층!' (1 ~ {total_floors}) : "
        ).strip()

        if not user_input.isdigit():
            print("숫자만 입력하세요")
            continue

        floor = int(user_input)

        if not (1 <= floor <= total_floors):
            print(f"1 ~ {total_floors} 사이의 숫자를 입력해주세요.")
            continue

        break

    print(f"\n\"아파트 {floor} 층!!\"")

    print("\n손을 아래에서부터 하나씩 위로 올립니다.")
    for i in range(floor):
        time.sleep(0.35)
        print(f"{i + 1}층  -> {hands[i]}(의) 손")


    loser = hands[floor - 1]

    print("\n" + "-" * 60)
    print(f" {floor}층 도착! 맨 위 손의 주인은 [{loser}] !")
    print(f" [{loser}] (이)가 술을 마십니다.")
    print("-" * 60)
    time.sleep(0.5)

    return loser