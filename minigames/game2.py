# 담당 부원 : 유채영
import time
import random

def play_initial(players, user_name):

    print("❗제시된 초성을 보고 올바른 단어를 입력하세요😊 마지막까지 남는 사람이 집니다❗")
    print("🎵 훈민정음~ 훈민정음~~")

    word_pool = {
        "ㄱㅂ": ["가방", "갈비", "공부", "김밥", "개발"],
        "ㅇㅅ": ["인생", "역사", "의사", "인쇄", "요소"],
        "ㅎㅅ": ["학설", "함선", "함성", "합석", "합성"],
        "ㅊㅅ": ["초성", "최소", "추석", "취소", "칫솔"],
        "ㅂㅇ": ["발아", "발언", "방언", "발열", "방역"]
    }


    selected_initial = random.choice(list(word_pool.keys()))
    valid_words = word_pool[selected_initial].copy()
    print(f"\n📢 이번 라운드 제시 초성: [ {selected_initial} ]")
    time.sleep(1)
    
    success_stack = []
    already_used_words = []
    total_needed = len(players) - 1


    while len(success_stack) < total_needed:
        survivors = [p for p in players if p not in success_stack]
        current_turn_player = random.choice(survivors)
        
        if current_turn_player != user_name:
            time.sleep(1)

            available_words = [w for w in valid_words if w not in already_used_words]
            
            if available_words:
                bot_word = random.choice(available_words)
                print(f"{current_turn_player}: \"{bot_word}!\"")
                success_stack.append(current_turn_player)
                already_used_words.append(bot_word)
            else:
                print(f"{current_turn_player}: \"어... 생각이 안 나!\"")
                return current_turn_player

        else:
            start_time = time.time()
            user_word = input(f"{user_name}: ").strip()
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if elapsed_time > 3.0:
                print(f"\n❌ [시간 초과!] 단어를 입력하는 데 {elapsed_time:.2f}초가 걸렸습니다.")
                return user_name
            
            if user_word in already_used_words:
                print("❌ 이미 다른 사람이 외친 단어입니다!")
                return user_name

    loser = [p for p in players if p not in success_stack][0]

    return loser