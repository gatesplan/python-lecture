"""삽입정렬 빈칸채우기 55문제 생성 후 problems-draft-03.json 에 append."""
import json
from itertools import combinations
from pathlib import Path

DRAFT = Path(__file__).resolve().parent.parent / "frontend" / "src" / "data" / "problems-draft-03.json"

original = {
    "S1": "len(arr)",
    "S2": "range(1, n)",
    "S3": "arr[i]",
    "S4": "i - 1",
    "S5": "j >= 0 and arr[j] > key",
    "S6": "arr[j]",
    "S7": "arr[j + 1]",
    "S8": "j -= 1",
    "S9": "key",
    "S10": "arr[j + 1]",
    "S11": "arr",
}

# 코드에 등장하는 순서 (답 작성 순서)
appearance_order = ["S1", "S2", "S3", "S4", "S5", "S7", "S6", "S8", "S10", "S9", "S11"]

slot_ids = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S11"]

explain_text = {
    "S1": "len(arr)는 리스트 arr의 원소 개수를 구해 n에 저장한다.",
    "S2": "외부 for는 range(1, n)으로 인덱스 1부터 끝까지 돌며 각 key를 정렬된 앞부분에 끼워넣는다.",
    "S3": "key = arr[i]는 현재 삽입 대상 값을 임시로 저장한다.",
    "S4": "j = i - 1은 정렬된 앞부분의 마지막 인덱스를 가리킨다.",
    "S5": "while 조건 j >= 0 and arr[j] > key는 key보다 큰 원소를 만나는 동안 뒤로 밀기를 계속한다.",
    "S6": "우변 arr[j]는 앞쪽 원소 값으로, 뒤로 한 칸 밀 때 대입할 값이다.",
    "S7": "좌변 arr[j + 1]은 현재 비교 지점보다 한 칸 뒤 위치로, 앞 원소를 덮어쓸 자리이다.",
    "S8": "j -= 1 (또는 j = j - 1)은 비교 지점을 왼쪽으로 한 칸 옮긴다.",
    "S9": "우변 key는 임시로 저장해둔 삽입 대상 값으로, 비어있는 자리에 최종적으로 놓는다.",
    "S10": "좌변 arr[j + 1]은 비교가 멈춘 지점 바로 뒤, 즉 key가 들어갈 빈 자리이다.",
    "S11": "정렬이 끝난 arr를 반환값으로 돌려준다.",
}


def render_code(selected):
    def v(sid):
        return "[[]]" if sid in selected else original[sid]

    lines = [
        "def insert_sort(arr):",
        f"    n = {v('S1')}",
        "",
        f"    for i in {v('S2')}:",
        f"        key = {v('S3')}",
        f"        j = {v('S4')}",
        f"        while {v('S5')}:",
        f"            {v('S7')} = {v('S6')}",
        f"            {v('S8')}",
        f"        {v('S10')} = {v('S9')}",
        "",
        f"    return {v('S11')}",
        "",
        "print(insert_sort([5, 2, 8, 1, 4]))",
    ]
    return "\n".join(lines)


def make_problem(pid, selected):
    ordered = [s for s in appearance_order if s in selected]
    answer_value = ", ".join(original[s] for s in ordered)
    code = render_code(selected)

    explain_items = [{"type": "text", "content": explain_text[s]} for s in ordered]
    explain_items.append({"type": "text", "content": f"정답: {answer_value}"})

    return {
        "id": pid,
        "type": "short",
        "content": [
            {
                "type": "text",
                "content": "다음 코드의 실행 결과가 <출력>과 같을 때 빈칸을 차례대로 채우시오.",
            },
            {"type": "code", "language": "python", "content": code},
            {"type": "output-sample", "content": "[1, 2, 4, 5, 8]"},
        ],
        "answer": {"type": "value", "value": answer_value},
        "explain": [
            {"type": "process-box", "title": "풀이", "content": explain_items}
        ],
    }


def main():
    data = json.loads(DRAFT.read_text(encoding="utf-8"))
    existing_ids = {p["id"] for p in data}

    combos = list(combinations(slot_ids, 2))
    assert len(combos) == 55

    start_num = 137
    new_problems = []
    for idx, combo in enumerate(combos):
        pid = f"fb-{start_num + idx}"
        if pid in existing_ids:
            raise SystemExit(f"duplicate id {pid}")
        new_problems.append(make_problem(pid, set(combo)))

    data.extend(new_problems)
    DRAFT.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"appended {len(new_problems)} problems, total {len(data)}")


if __name__ == "__main__":
    main()
