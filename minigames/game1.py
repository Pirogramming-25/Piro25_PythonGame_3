import random
import time

def play_game_of_death(players,user_name):
    print("\n" + "="*40)
    print("신난다~ 재미난다~ 더 게임 오브 데스! ")
    print("="*40)
    time.sleep(1)

    print("\n[게임 규칙 설명]")
    print("  1. 주도자가 '숫자(최소 3 이상'를 외칩니다.")
    print("  2. 모든 플레이어는 동시에 서로를 손가락으로 지목합니다.")
    print("  3. 주도자부터 시작해 지목한 손가락을 따라 숫자를 세어나갑니다.")
    print("  4. 주도자가 외친 숫자에 딱 걸린 사람이 당첨(벌주)됩니다!")
    print("-" * 60)
    
    time.sleep(2.5)

    leader = random.choice(players)
    print(f"이번 판의 주도자는 [{leader}]입니다!")
    
    target_count = 0
    if leader == user_name:
        while True:
            try:
                target_count = int(input("몇 번 만에 끝내시겠습니까? (최소 3 이상 입력): "))
                if target_count >= 3:
                    break
                print("게임의 재미를 위해 3 이상의 숫자를 입력해주세요.")
            except ValueError:
                print("올바른 숫자를 입력해주세요.")
    else:
        target_count = random.randint(3, 15)
        print(f"주도자 [{leader}]가 숫자를 고르고 있습니다...")
        time.sleep(1.5)
        print(f"[{leader}]가 외친 숫자: {target_count}")

    print("\n" + "-"*40)
    print("모두 지목할 대상을 고르고 있습니다...")
    print("-"*40)
    time.sleep(1.5)

    pointing_dict = {}

    for player in players:
        if player == user_name:
            choices = [p for p in players if p != user_name]
            print(f"현재 참여자: {choices}")
            while True:
                choice = input("누구를 지목하시겠습니까? (이름 정확히 입력): ").strip()
                if choice in choices:
                    pointing_dict[user_name] = choice
                    break
                print("올바른 참가자의 이름을 입력해주세요.")
        else:
            choices = [p for p in players if p != player]
            pointing_dict[player] = random.choice(choices)

    print("\n[지목 결과 발표!]")
    for pointer, pointee in pointing_dict.items():
        print(f"  [{pointer}] -> [{pointee}]")
    print("-"*40)
    time.sleep(2)

    print("\n신호가 시작됩니다! 3! 2! 1! ...")
    current_person = leader
    
    for i in range(1, target_count + 1):
        next_person = pointing_dict[current_person]
        print(f" [{i}번] {current_person} -> {next_person}")
        current_person = next_person
        time.sleep(0.8)

    loser = current_person
    print("\n" + "="*40)
    print(f"최종 패패자는 [{loser}] 입니다!")
    print("="*40 + "\n")
    
    return loser



