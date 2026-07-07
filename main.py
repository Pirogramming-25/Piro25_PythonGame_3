# 전체 게임 흐름 제어 (입력, 대결 상대 설정, 메인 턴 루프, 상태 업데이트)
# [개인이 임의로 수정하지 말 것!]
import random
from minigames import game1, game2, game3, game4, game5
import time

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


AVAILABLE_GAMES = [
    {"name": "더 게임 오브 데스", "func": game1.play_game_of_death, "needs_user_name": True},
    {"name": "쥐를 잡자", "func": game2.play_catch_mouse, "needs_user_name": True},
    {"name": "아파트 게임", "func": game3.play_apt, "needs_user_name": False},
    {"name": "지하철 게임", "func": game4.play_subway, "needs_user_name": False, "chooser_first": True},
    {"name": "베스킨라빈스 31 게임", "func": game5.play_game5, "needs_user_name": True}
]

def choose_and_play_game(current_turn_player, player_status, user_name):
    """
    현재 턴인 플레이어가 게임을 선택하고 실행합니다.
    'exit' 입력 시 프로그램 종료 신호(None)를 반환합니다.
    """
    players_list = list(player_status.keys())
    selected_game = None

    print(f"\n(현재 턴: {current_turn_player})")

    # 1. 사용자(나)의 턴인 경우
    if current_turn_player == user_name: 
        print_games()
        while True:
            user_input = input("원하는 게임의 번호나 'exit'를 입력하세요: ").strip()
            
            if user_input.lower() == 'exit':
                return "EXIT_SIGNAL"
            
            if user_input.isdigit() and 1 <= int(user_input) <= len(AVAILABLE_GAMES):
                selected_game = AVAILABLE_GAMES[int(user_input) - 1]
                break
            else:
                print(" 올바른 번호나 'exit'를 입력해주세요.\n")
    
    # 2. 컴퓨터 NPC의 턴인 경우 (랜덤 선택)
    else:
        print_games()
        print(f" {current_turn_player}(이)가 게임을 신중하게 고르고 있습니다...")
        time.sleep(1.5)
        selected_game = random.choice(AVAILABLE_GAMES)
        print(f"{current_turn_player}(이)가 '{selected_game['name']}'을(를) 선택했습니다!")

        input(" 진행하려면 [Enter] 키를 누르세요...") 

    # 3. 선택된 게임 실행 
    print(f"\n{selected_game['name']} 시작합니다!")

    if selected_game.get("chooser_first"):
        start = players_list.index(current_turn_player)
        players_list = players_list[start:] + players_list[:start]
    
    if selected_game["needs_user_name"]:
        loser = selected_game["func"](players_list, user_name)
    else:
        loser = selected_game["func"](players_list)
    
    return loser



def print_player_table(player_status):
    """참가자들의 실시간 상태 테이블만 출력하는 함수"""
    print(f"{'이름':<10} | {'마신 잔 수 / 치사량':<15} | {'상태':<15}")
    print("-" * 45)
    
    for name, cups in player_status.items():
        current_cups, max_cups = cups[0], cups[1]
        left_cups = max(0, max_cups - current_cups)
        
        gauge = "■" * current_cups + "□" * left_cups if (left_cups > 0) else "■" * max_cups
        if current_cups >= max_cups:
            status_text = "💀기절 직전!"
        else:
            status_text = f"정상 ({left_cups}잔 남음)"
            
        print(f"{name:<10} | {current_cups} /{max_cups} 잔 {gauge:<15} | {status_text}")
    print("="*40 + "\n")


def update_and_print_status(loser, player_status):
    if loser not in player_status:
        print(f"오류: {loser}는 참가자 명단에 없습니다.")
        return

    # 1. 패배자 잔 수 업데이트
    player_status[loser][0] += 1
    
    # 2. 상단 알림 출력
    print("\n" + "="*40)
    print(f"🍺 [게임 결과] {loser}(이)가 패배하여 술을 마십니다! (+1잔)")
    print("="*40)
    
    # 3. 분리한 테이블 출력 함수 호출
    print_player_table(player_status)



def check_game_over(player_status):
    """
    치사량에 달한 플레이어가 있는지 검사합니다.
    치사량 도달 시 True와 전사자 이름을 반환하고, 아니면 False, None을 반환합니다.
    """
    for name, cups in player_status.items():
        current_cups, max_cups = cups[0], cups[1]
        
        # 현재 마신 잔이 치사량(최대 주량) 이상인 경우 게임 오버
        if current_cups >= max_cups:
            print("\n" + "=" * 65)
            print("=" * 65)
            print(r"""
                    ____    _    __  __ _____    ___  _   _ _____ ____  _ 
                    / ___|  / \  |  \/  | ____|  / _ \| | | | ____|  _ \| |
                    | |  _  / _ \ | |\/| |  _|   | | | | | | |  _| | |_) | |
                    | |_| |/ ___ \| |  | | |___  | |_| | |_| | |___|  _ < |_|
                    \____/_/   \_\_|  |_|_____|  \___/ \___/|_____|_| \_(_)
                """)
            print("=" * 65)
            print("=" * 65)
            print(f"\n 💀 기절 완료: [{name}](이)가 치사량({max_cups}잔)에 도달했습니다!")
            print("    인사불성이 되어 더 이상 게임을 진행할 수 없습니다.")
            print("    술자리를 종료합니다. 모두 고생하셨습니다!\n")
            print("=" * 65 + "\n")  
            return True
            
    return False


def main():
    if not print_intro():
        return

    player_name = get_player_name()
    alcohol_limit = choose_alcohol_limit()

    print("\n" + "~" * 80)
    print(f"{player_name}님 환영합니다!")
    print(f"{player_name}님의 치사량은 {alcohol_limit}잔입니다.")
    print("~" * 80)

    # 1. 초대된 친구들(봇) 정보 가져오기
    player_status = invite_friends()

    # 2. 사용자의 정보를 player_status 딕셔너리에 추가하기
    player_status[player_name] = [0, alcohol_limit]

    # 플레이어 명단 생성 및 첫 번째 턴 플레이어 설정
    players_list = list(player_status.keys())
    current_turn_idx = players_list.index(player_name)

    game_round = 0
    total_players = len(players_list)
    
    print_player_table(player_status)

    print("\n멤버 세팅 완료! 잠시 후 술게임을 시작합니다...")
    time.sleep(1.5)  

    while True:
        if game_round < total_players:
            current_turn_player = players_list[current_turn_idx]
            print(f"\n [첫 라운드] 순서대로 게임을 선택합니다. ({game_round + 1}/{total_players}번째 순서)")
            current_turn_idx = (current_turn_idx + 1) % len(players_list)
        else:
            current_turn_player = random.choice(players_list)
            print("\n[랜덤 라운드] 이제부터 게임 선택자가 랜덤으로 결정됩니다!")

        # 게임 선택 및 진행 
        loser = choose_and_play_game(current_turn_player, player_status, player_name)

        # 사용자가 'exit'를 입력해 게임을 종료한 경우
        if loser == "EXIT_SIGNAL":
            print("\n👋 게임을 중단하고 술자리를 나갑니다. 안녕히 가세요!")
            break

        # 미니게임 종료 후 결과 정산 전 딜레이
        print("\n📊 게임이 끝났습니다! 결과를 집계 중입니다...")
        time.sleep(1.5)

        # 패배자 상태 업데이트 및 전광판 출력
        update_and_print_status(loser, player_status)

        # 치사량 도달 여부 검사 (게임 오버 조건)
        if check_game_over(player_status):
            break

        time.sleep(1)
        print("-" * 60)
        answer = input(
            "다음 게임을 진행할까요? (종료하려면 n 입력 / 계속하려면 아무 키나 누르세요): "
        )
        print("-" * 60)

        if answer.strip().lower() == "n":
            print(
                "\n 'n'을 입력하셨으므로 게임을 중단합니다. 즐거웠습니다! 안녕히 가세요."
            )
            break


        print("\n다음 턴을 준비하고 있습니다...")
        time.sleep(1)

        game_round += 1


if __name__ == "__main__":
    main()