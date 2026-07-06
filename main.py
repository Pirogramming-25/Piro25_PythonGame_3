# 전체 게임 흐름 제어 (입력, 대결 상대 설정, 메인 턴 루프, 상태 업데이트)
# [개인이 임의로 수정하지 말 것!]
import random

def print_intro():
    print("~" * 80)
    print("🍺 PIRO Alcohol Game 🍺")
    print("~" * 80)
    print("안주 먹을🍗 시간이⏰ 없어요❌ 마시면서 배우는 술게임 🍻🍺")
    print("~" * 80)

    answer = input("게임을 진행할까요? (y/n): ")

    if answer.lower() != "y":
        print("게임을 종료합니다.")
        return False

    return True

def get_player_name():
    name = input("\n오늘 거하게 취해볼 당신의 이름은?: ")

    while name.strip() == "":
        print("이름은 비워둘 수 없습니다.")
        name = input("이름을 다시 입력해주세요: ")

    return name

def choose_alcohol_limit():
    print("\n" + "~" * 22 + " 🍺 소주 기준 당신의 주량은? 🍺 " + "~" * 22)
    print(" " * 24 + "🍺 1. 소주 반병 (2잔)")
    print(" " * 24 + "🍺 2. 소주 반병에서 한병 (4잔)")
    print(" " * 24 + "🍺 3. 소주 한병에서 한병 반 (6잔)")
    print(" " * 24 + "🍺 4. 소주 한병 반에서 두병 (8잔)")
    print(" " * 24 + "🍺 5. 소주 두병 이상 (10잔)")
    print("~" * 80)

    alcohol_options = {
        "1": 2,
        "2": 4,
        "3": 6,
        "4": 8,
        "5": 10
    }

    while True:
        choice = input("당신의 치사량(주량)은 얼마만큼인가요? (1~5을 선택해주세요): ")

        if choice in alcohol_options:
            return alcohol_options[choice]

        print("잘못된 입력입니다. 1~5 중에서 선택해주세요.")

def invite_friends():
    list_candidate_names = ["은서", "하연", "연서", "예진", "헌도"]

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    while True:
        try:
            num_invite = int(input("함께 취할 친구들은 얼마나 필요하신가요?(최대 3명까지 초대할 수 있어요!) : "))
            if 1 <= num_invite <= 3:
                break
            else:
                print("❌ 최대 3명까지만 초대할 수 있습니다.")
        except ValueError:
            print("❌ 숫자로 입력해주세요.")

    selected_bots = random.sample(list_candidate_names, num_invite)
    
    # { "이름": [현재 마신 잔(0), 랜덤 치사량] }
    dic_bots_info = {}
    for bot in selected_bots:
        bot_limit = random.randint(2, 10)
        dic_bots_info[bot] = [0, bot_limit]
        print(f"오늘 함께 취할 친구는 {bot}입니다! (치사량 : {bot_limit})")

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # 사용자 제외 나머지 플레이어의 정보만 담겨있음 주의!
    return dic_bots_info

def print_games():
    print("~~~~~~~~~~~~~~~~~~~~ 🍺 오늘의 Alcohol GAME 🍺 ~~~~~~~~~~~~~~~~~~~~~~")
    print("                     🍺 1. 더 게임 오브 데스\n                     🍺 2. 쥐를 잡자 게임\n                     🍺 3. 아파트 게임\n                     🍺 4. 지하철 게임\n                     🍺 5. 베스킨라빈스 31\n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   
def main():
    if not print_intro():
        return

    player_name = get_player_name()
    alcohol_limit = choose_alcohol_limit()

    print("\n" + "~" * 80)
    print(f"{player_name}님 환영합니다!")
    print(f"{player_name}님의 치사량은 {alcohol_limit}잔입니다.")
    print("~" * 80)

