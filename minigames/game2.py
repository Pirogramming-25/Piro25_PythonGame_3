# 담당 부원 : 유채영
import time
import random


def initialize_game(players):
    total_mice = random.randint(3, 6)
    print(f"\n\n📢 이번 판에 잡아야 할 쥐는 총 [ {total_mice}마리 ] 입니다!")
    time.sleep(1)

    turn_order = players.copy()
    random.shuffle(turn_order)
    print(f"🔄 게임 순서 결정: {' -> '.join(turn_order)}\n")
    time.sleep(1)

    return [total_mice, turn_order]


def play_catch_mouse(players, user_name):

    # ============================= 게임 룰 출력 부분 =============================
    print("❗지정된 쥐 마릿수가 차기 전까지는 [잡았다] 또는 [놓쳤다]를 입력!\n목표 마릿수가 모두 차는 순간, 내 차례에 반드시 [만세]를 입력!\n⏱️ 모든 입력은 3초 제한! ❌ 오타 및 타이머 초과❗")
    print("🎵 쥐를 잡자~ 쥐를 잡자~ 찍찍찍! 🎵")


    # ============================= 게임 로직 부분 =============================
    total_mice, turn_order = initialize_game(players)
    current_caught = 0
    current_idx = 0

    while len(turn_order) > 1:
        current_idx %= len(turn_order)
        current_turn_player = turn_order[current_idx]
        
        # 목표 마릿수에 도달하지 않았을 때
        if current_caught < total_mice:
            
            if current_turn_player != user_name:
                time.sleep(1)
                bot_action = random.choice(["잡았다", "놓쳤다"])
                print(f"{current_turn_player}: \"{bot_action}!\"")
                
                if bot_action == "잡았다":
                    current_caught += 1
                    print(f" -> (현재 {current_caught}마리 잡음)")
                
                current_idx += 1

            else:
                start_time = time.time()
                user_action = input(f"{current_turn_player} (잡았다/놓쳤다): ").strip()
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                if elapsed_time > 5.0:
                    print(f"\n❌ [시간 초과!] 구호를 외치는 데 {elapsed_time:.2f}초가 걸렸습니다.")
                    return user_name
                
                if user_action not in ["잡았다", "놓쳤다"]:
                    print(f"\n❌ 잘못된 구호입니다! '잡았다' 또는 '놓쳤다'만 입력해야 합니다.")
                    return user_name
                
                if user_action == "잡았다":
                    current_caught += 1
                    print(f" -> (현재 {current_caught}마리 잡음)")
                
                current_idx += 1
                    
        # 목표 마릿수에 도달했을 때
        else:
            if current_turn_player != user_name:
                time.sleep(1)
                current_action = random.choices(
                    ["잡았다", "놓쳤다", "만세"],
                    weights=[15, 15, 70], k=1
                )[0]
                print(f"{current_turn_player}: \"{current_action}!\"")
            else:
                start_time = time.time()
                current_action = input(f"{current_turn_player} (만세 입력!): ").strip()
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                if elapsed_time > 5.0:
                    print(f"\n❌ [시간 초과!] 만세를 외치는 데 {elapsed_time:.2f}초가 걸렸습니다.")
                    return current_turn_player
                
            if current_action != "만세":
                print(f"\n❌ 쥐를 다 잡았는데 만세를 외치지 않았습니다!")
                return current_turn_player
                
            print(f"-> {current_turn_player} 탈출 성공!")    
            turn_order.remove(current_turn_player)
            
            total_mice, turn_order = initialize_game(turn_order)
            current_caught = 0
            current_idx = 0

    loser = turn_order[0]
    return loser


loser_result = play_catch_mouse(["은서", "하연", "연서", "예진"], "예진")
print(f"\n📢 최종 패배자(원샷): {loser_result}")