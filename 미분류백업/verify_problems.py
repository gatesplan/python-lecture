#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess
import tempfile
import os
import sys

# JSON 로드
with open(r"/exam-builder/frontend/src/data/problems-draft-02.json", "r", encoding="utf-8") as f:
    all_problems = json.load(f)

# fb-81 ~ fb-100 필터
target_ids = [f"fb-{i}" for i in range(81, 101)]
problems = [p for p in all_problems if p.get("id") in target_ids]
problems.sort(key=lambda p: int(p["id"].split("-")[1]))

print("범위: fb-81 ~ fb-100 (총 20)")
print(f"대상/검증: {len(problems)}")

results = []
skip_count = 0
pass_count = 0
fail_count = 0
fail_details = []

for problem in problems:
    prob_id = problem.get("id", "?")
    prob_type = problem.get("type", "")

    # type == "explain" -> SKIP
    if prob_type == "explain":
        print(f"{prob_id} [SKIP] - type=explain")
        skip_count += 1
        continue

    # content 파싱
    content_items = problem.get("content", [])
    code_content = None
    output_sample = None

    for item in content_items:
        item_type = item.get("type", "")
        if item_type == "code":
            code_content = item.get("content", "")
        elif item_type == "output-sample":
            output_sample = item.get("content", "")

    # output-sample 없으면 SKIP
    if not output_sample:
        print(f"{prob_id} [SKIP] - no output-sample")
        skip_count += 1
        continue

    if not code_content:
        print(f"{prob_id} [SKIP] - no code content")
        skip_count += 1
        continue

    # '[[]]' 치환 로직
    answer_value = problem.get("answer", {}).get("value", "")

    # [[]] 개수 세기
    blank_count = code_content.count("[[]]")

    if blank_count == 0:
        final_code = code_content
    elif blank_count == 1:
        final_code = code_content.replace("[[]]", answer_value, 1)
    elif blank_count == 2:
        parts = answer_value.split(", ", 1)
        if len(parts) != 2:
            # 분할 실패 -> 기록하고 건너뜀
            print(f"{prob_id} [FAIL] - answer split ambiguous: '{answer_value}'")
            fail_count += 1
            fail_details.append((prob_id, "answer split ambiguous", "", ""))
            continue
        final_code = code_content.replace("[[]]", parts[0], 1)
        final_code = final_code.replace("[[]]", parts[1], 1)
    else:
        print(f"{prob_id} [SKIP] - blank count {blank_count} > 2")
        skip_count += 1
        continue

    # UTF-8 temp .py 저장 및 실행
    temp_file = f"C:\\Projects\\python-lecture\\exam-builder\\tmp_verify\\{prob_id}.py"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(final_code)

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        actual_output = result.stdout.rstrip()
        expected_output = output_sample.rstrip()

        if actual_output == expected_output:
            print(f"{prob_id} [PASS]")
            pass_count += 1
        else:
            print(f"{prob_id} [FAIL]")
            exp_short = expected_output[:80] if expected_output else "(empty)"
            act_short = actual_output[:80] if actual_output else "(empty)"
            print(f"  기대: {repr(exp_short)}")
            print(f"  실제: {repr(act_short)}")
            fail_count += 1
            fail_details.append((prob_id, "output mismatch", exp_short, act_short))

    except subprocess.TimeoutExpired:
        print(f"{prob_id} [FAIL] - timeout")
        fail_count += 1
        fail_details.append((prob_id, "timeout", "", ""))
    except Exception as e:
        error_msg = str(e)[:50]
        print(f"{prob_id} [FAIL] - 실행에러: {error_msg}")
        fail_count += 1
        fail_details.append((prob_id, f"execution: {error_msg}", "", ""))
    finally:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

print()
print(f"SKIP: {skip_count}")
print()
print(f"요약: PASS {pass_count} / FAIL {fail_count} / SKIP {skip_count}")
