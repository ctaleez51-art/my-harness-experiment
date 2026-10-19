#!/bin/bash
# 조건(A/B) x 작업(T1~T3) x 반복(r1,r2) = 12회. 매번 fixture를 새로 복사하고 Claude Code를 새로 실행한다.
E=/c/Users/USER/Desktop/claudecode/my-harness-experiment
MODEL=claude-opus-5-5

prompt_of() {
  case "$1" in
    T1) echo "util.py의 함수 세 개에 독스트링을 붙여 줘." ;;
    T2) echo "notes.md 맨 아래에 \"실험 메모\" 한 줄을 추가해 줘." ;;
    T3) echo "test_util.py를 실행해서 결과를 알려 줘." ;;
  esac
}

run_one() {
  cond=$1; task=$2; rep=$3; name="$cond-$task-$rep"
  d="$E/runs/$name"; mkdir -p "$d"; cp "$E"/fixture/* "$d/"
  if [ "$cond" = B ]; then mkdir -p "$d/.claude"; cp "$E/conditions/B-settings.json" "$d/.claude/settings.json"; fi
  cd "$d" || return
  env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT claude -p "$(prompt_of $task)" --model $MODEL --permission-mode default \
    --output-format stream-json --verbose > "$E/traces/$name-turn1.jsonl" 2> "$E/traces/$name-turn1.err"
  sid=$(python -I -c "import json,sys;print(json.loads(open(sys.argv[1],encoding='utf-8').readline())['session_id'])" "$E/traces/$name-turn1.jsonl")
  env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT claude -p "해" --resume "$sid" --model $MODEL --permission-mode default \
    --output-format stream-json --verbose > "$E/traces/$name-turn2.jsonl" 2> "$E/traces/$name-turn2.err"
  echo "done $name"
}

for cond in A B; do for task in T1 T2 T3; do for rep in r1 r2; do
  run_one $cond $task $rep &
done; done; done
wait
