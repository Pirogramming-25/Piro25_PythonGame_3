# 전체 게임 흐름 제어 (입력, 대결 상대 설정, 메인 턴 루프, 상태 업데이트)
# [개인이 임의로 수정하지 말 것!]
import random
from minigames import game1, game2, game3, game4, game5

AVAILABLE_GAMES = [
    {"name": "더 게임 오브 데스", "func": game1.play_game_of_death, "needs_user_name": True},
    {"name": "훈민정음", "func": game2.play_initial, "needs_user_name": True},
    {"name": "아파트 게임", "func": game3.play_apt, "needs_user_name": False},
    {"name": "지하철 게임", "func": game4.play_subway, "needs_user_name": False},
    {"name": "베스킨라빈스 31 게임", "func": game5.play_game5, "needs_user_name": False}
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
        while True:
            print("=== [게임 선택 메뉴] ===")
            for idx, g in enumerate(AVAILABLE_GAMES, 1):
                print(f"{idx}. {g['name']}")
            print("종료하려면 'exit'를 입력하세요.")
            
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
        selected_game = random.choice(AVAILABLE_GAMES)
        print(f"{current_turn_player}(이)가 '{selected_game['name']}'을(를) 선택했습니다!")

    # 3. 선택된 게임 실행 
    print(f"\n{selected_game['name']} 시작합니다!")
    
    if selected_game["needs_user_name"]:
        loser = selected_game["func"](players_list, user_name)
    else:
        loser = selected_game["func"](players_list)
    
    return loser



def update_and_print_status(loser, player_status):
    """
    패배자의 마신 잔 수를 업데이트하고, 현재 모든 플레이어의 상태를 출력합니다.
    """
    if loser not in player_status:
        print(f"오류: {loser}는 참가자 명단에 없습니다.")
        return

    # 1. 패배자 잔 수 업데이트
    player_status[loser][0] += 1
    
    print("\n" + "="*40)
    print(f"🍺 [게임 결과] {loser}(이)가 패배하여 술을 마십니다! (+1잔)")
    print("="*40)
    
    # 2. 실시간 상태 테이블 출력    
    print(f"{'이름':<10} | {'마신 잔 수 / 치사량':<15} | {'상태':<15}")
    print("-" * 45)
    
    for name, cups in player_status.items():
        current_cups, max_cups = cups[0], cups[1]
        left_cups = max_cups - current_cups
        
        # 시각적인 게이지 바 생성 (예: ■■□□□)
        gauge = "■" * current_cups + "□" * left_cups if (left_cups > 0) else "■" * max_cups
        status_text = f"정상 ({left_cups}잔 남음)"
            
        print(f"{name:<10} | {current_cups}/{max_cups} 잔 {gauge:<10} | {status_text}")
    print("="*40 + "\n")



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
            print("""
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