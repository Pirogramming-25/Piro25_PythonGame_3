# 담당 부원 : 유채영
import time
import random


def check_initial(word, target_initial):
    
    # 입력 글자가 2글자 아닌 경우
    if len(word) != 2:
        return False
        
    # 한글 초성 리스트 (유니코드 순서)
    INITIAL_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 
        'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]
    
    extracted_initial = ""
    for char in word:
        if '가' <= char <= '힣': # 한글일 경우
            # 초성 인덱스 추출
            char_code = ord(char) - ord('가')
            initial_index = char_code // 588
            extracted_initial += INITIAL_LIST[initial_index]
        else:
            return False
            
    return extracted_initial == target_initial


def play_initial(players, user_name):
    print("❗ 제시된 초성을 보고 올바른 단어를 입력하세요! 🍻\n⏱️  5초 초과, ❌ 이미 나온 단어/틀린 단어, 🏃‍♂️ 마지막까지 안 외치고 남은 사람은 원샷! 🔥❗")
    print("🎵 훈민정음~ 훈민정음~~")

    word_pool = {
        # [ㄱ 계열]
        "ㄱㄱ": ["가구", "고기", "경기", "감격"],
        "ㄱㄷ": ["가도", "구두", "기도", "감동"],
        "ㄱㄹ": ["거리", "기록", "가루", "고래"],
        "ㄱㅁ": ["가면", "고민", "가문", "과목"],
        "ㄱㅂ": ["가방", "갈비", "공부", "김밥"],
        "ㄱㅅ": ["가사", "감사", "교실", "계속"],
        "ㄱㅇ": ["거울", "고양", "겨울", "기억"],
        "ㄱㅈ": ["가지", "과자", "공장", "구조"],

        # [ㄴ/ㄷ 계열]
        "ㄴㄷ": ["노동", "늑대", "년도", "낙도"],
        "ㄴㄹ": ["나라", "노래", "누나", "논리"],
        "ㄷㄱ": ["동굴", "대구", "당근", "도구"],
        "ㄷㄷ": ["단도", "대두", "도둑", "당당"],
        "ㄷㅁ": ["다만", "도마", "동무", "동매"],
        "ㄷㅂ": ["담배", "도박", "두부", "답변"],

        # [ㅁ/ㅂ 계열]
        "ㅁㄱ": ["미국", "마구", "문구", "모기"],
        "ㅁㄷ": ["마당", "무대", "만두", "명당"],
        "ㅁㅂ": ["모방", "문방", "마법", "모범"],
        "ㅂㄱ": ["번개", "보고", "분기", "비극"],
        "ㅂㄷ": ["바다", "반도", "부두", "부담"],
        "ㅂㅂ": ["방법", "부부", "반발", "보복"],

        # [ㅅ/ㅇ 계열]
        "ㅅㄱ": ["사과", "소고", "시간", "세계"],
        "ㅅㄷ": ["수도", "식당", "속도", "상담"],
        "ㅅㅁ": ["사막", "선물", "식물", "소문"],
        "ㅅㅂ": ["수박", "신발", "새벽", "선배"],
        "ㅇㄱ": ["안경", "악기", "원고", "입구"],
        "ㅇㄷ": ["인도", "온도", "운동", "응답"],
        "ㅇㅈ": ["의자", "우주", "인재", "연재"],

        # [ㅈ/ㅊ/ㅎ 계열]
        "ㅈㄱ": ["지금", "조건", "지구", "제고"],
        "ㅈㄷ": ["지도", "잔디", "정답", "진도"],
        "ㅈㅁ": ["주말", "주민", "제목", "장면"],
        "ㅊㄱ": ["친구", "최고", "초가", "출구"],
        "ㅎㄱ": ["학교", "한국", "한강", "항공"],
        "ㅎㄷ": ["행동", "한도", "황토", "화단"]
    }


    selected_initial = random.choice(list(word_pool.keys()))
    valid_words = word_pool[selected_initial].copy()
    print(f"\n📢 이번 라운드 제시 초성: [ {selected_initial} ]")
    time.sleep(1)
    
    success_stack = []
    already_used_words = []

    while len(success_stack) < len(players):
        survivors = [p for p in players if p not in success_stack]
        current_turn_player = random.choice(survivors)
        
        if current_turn_player != user_name:
            time.sleep(1)

            available_words = [w for w in valid_words if w not in already_used_words]
            
            if available_words:
                current_word = random.choice(available_words)
                print(f"{current_turn_player}: \"{current_word}!\"")
            else:
                print(f"{current_turn_player}: \"어... 생각이 안 나!\"")
                return current_turn_player

        else:
            start_time = time.time()
            current_word = input(f"{current_turn_player}: ").strip()
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            if not check_initial(current_word, selected_initial) :
                print("❌ 입력 단어가 잘못되었습니다.")
                return current_turn_player
            
            if elapsed_time > 5.0:
                print(f"\n❌ 단어를 입력하는 데 {elapsed_time:.2f}초가 걸렸습니다.")
                return current_turn_player
            
            if current_word in already_used_words:
                print("❌ 이미 다른 사람이 외친 단어입니다!")
                return current_turn_player
            
        success_stack.append(current_turn_player)
        already_used_words.append(current_word)

    loser = success_stack[-1]

    return loser