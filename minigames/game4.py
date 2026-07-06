# 담당 부원 : 강성훈
# 기본 함수 구조는 README.md 참고해주세요.

"""
지하철 게임 (game4.py) - 담당: 강성훈

규칙:
- 첫 번째 플레이어가 정한 노선의 역 이름을 돌아가며 외친다. (NPC가 첫 번째면 랜덤 선택)
- 그 노선에 없는 역 or 이미 나온 역을 말하면 패배.
- 환승역을 말하면 다른 노선으로 갈아탈 수 있다.
- 노선 별칭 인정 (예: 경의중앙선 = 경의선), 역 이름 뒤에 '역'을 붙여도 인정 (예: 노량진역 = 노량진)
"""

import csv
import glob
import os
import random
import time

# minigames/files 폴더 안에서 '지하철역'이 이름에 포함된 CSV를 자동으로 찾기
_candidates = glob.glob(os.path.join(os.path.dirname(__file__), "files", "*지하철역*.csv"))
if not _candidates:
    raise SystemExit("minigames/files 폴더에 지하철역 CSV 파일이 없습니다!")
CSV_FILE = _candidates[0]

# 초대하는 컴퓨터 NPC 이름 목록
NPC_NAMES = {"은서", "하연", "연서", "예진", "헌도"}

NPC_MISTAKE_RATE = 0.15  # NPC가 실수할 확률
NPC_TRANSFER_RATE = 0.25 # NPC가 환승역에서 환승할 확률
TIME_LIMIT = 10          # 입력 제한 시간 (초)


# TIME_LIMIT 재면서 입력받기. 초과되면 안내 출력 후 None 반환
def timed_input(prompt):
    start = time.time()
    answer = input(prompt).strip()
    elapsed = time.time() - start
    if elapsed > TIME_LIMIT:
        print(f"\n{elapsed:.1f}초! 제한 시간 {TIME_LIMIT}초 초과!")
        return None
    return answer

# CSV 파일 읽어오기
def load_data(filename):
    """
    CSV -> 1열은 lines, 4열은 aliases
    lines   = 정식 노선명: [역, 역, ...]
    aliases = 다른이름: 정식 노선명 / EX) 경의중앙선 = 경의선도 인정
    """
    lines = {}
    aliases = {}
    for encoding in ("utf-8-sig", "cp949"):
        try:
            with open(filename, encoding=encoding) as f:
                for row in csv.DictReader(f):
                    line = row["호선"].strip()
                    station = row["전철역명"].strip()
                    lines.setdefault(line, []).append(station)

                    other = (row.get("다른이름") or "").strip()
                    if other:
                        aliases[other] = line
            return lines, aliases
        except UnicodeDecodeError:
            lines, aliases = {}, {}
    raise SystemExit("CSV 파일을 읽지 못했습니다. 파일을 확인해주세요.")


def build_transfer_map(lines):
    # 역이름은 속한 정식 노선명. 같은 이름이 2개 이상 존재하면 환승역으로 판정
    station_lines = {}
    for line, stations in lines.items():
        for station in stations:
            station_lines.setdefault(station, []).append(line)
    return station_lines


def resolve_line(name, lines, aliases):
    # 노선 이름은 별칭도 인정, 없으면 None
    name = name.strip()
    if name in lines:
        return name
    if name in aliases:
        return aliases[name]
    return None


def resolve_station(name, station_pool):
    # 이름 + 역 입력 시 '역' 지우고 본래 이름으로 판정 EX) 노량진역 = 노량진.
    name = name.strip()
    if name in station_pool:
        return name
    if name.endswith("역") and name[:-1] in station_pool:
        return name[:-1]  # 노량진역 -> 노량진
    return None


def npc_answer(current_line, lines, used):
    # NPC의 역 선택. NPC_MISTAKE_RATE 확률로 실수로 틀린 답 선택
    remaining = [s for s in lines[current_line] if s not in used]
    used_on_line = [s for s in lines[current_line] if s in used]

    if used_on_line and random.random() < NPC_MISTAKE_RATE:
        return random.choice(used_on_line)  # 실수 - 이미 나온 역 선택
    if remaining:
        return random.choice(remaining)     # 정상 - 남은 역 중 랜덤
    return None  # 노선의 모든 역이 소진됨


def play_subway(players):
    """
    :param players: 현재 게임에 참여 중인 플레이어들의 이름 리스트
    :return: 최종적으로 패배하여 술을 마셔야 하는 플레이어의 이름 (str)
    """
    lines, aliases = load_data(CSV_FILE)
    station_lines = build_transfer_map(lines)

    # 1. 게임 인트로 및 규칙 출력
    print("\n" + "=" * 50)
    print("  지~ 하 철!  지 하 철 ~ 지~ 하 철! 지 하 철 ~  ")
    print("=" * 50)
    print("규칙: 정해진 노선의 역 이름을 돌아가며 외치세요!")
    print("노선에 없는 역 / 이미 나온 역 = 벌주")
    print("환승역을 말하면 노선을 갈아탈 수 있습니다")
    print("=" * 50)

    # 시작 노선은 첫 번째 플레이어가 결정
    first = players[0]
    if first in NPC_NAMES:
        current_line = random.choice(list(lines.keys()))
        time.sleep(1)
        print(f"\n{first}: \"[{current_line}]~ [{current_line}]~!\"")
    else:
        print(f"\n노선 목록: {', '.join(lines.keys())}")
        while True:
            raw = input(f"{first}, 몇호선~ 몇호선~!: ").strip()
            resolved = resolve_line(raw, lines, aliases)
            if resolved:
                if raw != resolved:
                    print(f"({raw} = {resolved})")
                current_line = resolved
                break
            print("없는 노선입니다! 다시 입력해주세요.")

    used = set()
    loser = None
    turn = 0

    print(f"\n[{current_line}]! [{current_line}]! 이쪽으로~ 이쪽으로~ \n")
    time.sleep(1)

    # 2. 턴제(Turn-based) 로직 수행 (사용자는 input() 활용, 컴퓨터 NPC는 랜덤 액션 자동 출력)
    while loser is None:
        player = players[turn % len(players)]
        is_npc = player in NPC_NAMES

        # ---------- 역 이름 말하기 ----------
        if is_npc:
            time.sleep(1)
            answer = npc_answer(current_line, lines, used)
            if answer is None:
                print(f" {player}: \"...\" ({current_line})")  # NPC가 답할 역이 없는 경우
                loser = player
                break
            print(f" {player}: \"{answer}!\"")
        else:
            answer = timed_input(f" {player}의 차례 ({current_line}) [{TIME_LIMIT}초 안에!]: ")
            if answer is None:  # 시간 초과
                loser = player
                break

        # ---------- 판정 ----------
        station = resolve_station(answer, station_lines)  # 전체 역 기준 정규화

        # 판정 1: 현재 노선에 있는 역인가?
        if station is None or station not in lines[current_line]:
            print(f"\n [{answer}]은(는) {current_line} 역이 아닙니다! 원샷!")
            loser = player
            break

        # 판정 2: 이미 나온 역인가?
        if station in used:
            print(f"\n [{station}]은(는) 이미 나온 역! 원샷!")
            loser = player
            break

        if not is_npc and answer != station:
            print(f" ({answer} = {station})")
        used.add(station)

        # ---------- 환승 ----------
        other_lines = [l for l in station_lines[station] if l != current_line]
        if other_lines:
            print(f"  [{station}]은(는) 환승역! ({', '.join(station_lines[station])})")

            if is_npc:
                if random.random() < NPC_TRANSFER_RATE:
                    current_line = random.choice(other_lines)
                    time.sleep(0.5)
                    print(f" {player}: \" [{current_line}](으)로 환승!\"")
            else:
                choice = timed_input(f"   갈아탈 노선 입력 (그대로 가려면 엔터) [{TIME_LIMIT}초 안에!]: ")
                if choice is None:  # 시간 초과
                    loser = player
                    break
                if choice != "":
                    resolved = resolve_line(choice, lines, aliases)
                    if resolved in other_lines:
                        if choice != resolved:
                            print(f" ({choice} = {resolved})")
                        current_line = resolved
                        print(f" [{current_line}](으)로 환승!")
                    else:
                        print(f" [{station}]에서 {choice}(으)로는 환승 불가! 원샷!")
                        loser = player
                        break

        turn += 1

    # 3. 패배자(loser) 선정
    print(f"\n {loser} 원샷~!!")
    return loser