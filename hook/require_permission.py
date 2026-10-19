# PreToolUse 훅: 도구를 쓰기 전에 "설명하고 허락을 받았는지" 확인한다.
# 허락으로 보는 조건: 바로 앞 Claude의 글 끝부분에 질문(?)이 있고, 그 뒤 사용자의 말이 허락하는 말이다.
import json, os, re, sys, datetime

APPROVE = re.compile(r"^\s*(해|해라|해 ?줘|진행|진행해|응|네|예|ㅇㅇ|좋아|그래|ok)", re.I)

d = json.load(sys.stdin)
msgs = []
try:
    for line in open(d.get("transcript_path", ""), encoding="utf-8"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        t = e.get("type")
        if t not in ("user", "assistant"):
            continue
        c = e.get("message", {}).get("content")
        if isinstance(c, str):
            text = c
        elif isinstance(c, list):
            if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
                continue
            text = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
        else:
            continue
        if text.strip():
            msgs.append((t, text.strip()))
except Exception:
    pass

last_user = max((i for i, m in enumerate(msgs) if m[0] == "user"), default=None)
allowed = False
if last_user is not None:
    prev = [m for m in msgs[:last_user] if m[0] == "assistant"]
    if prev and "?" in prev[-1][1][-200:] and APPROVE.match(msgs[last_user][1]):
        allowed = True

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "traces")
run = os.path.basename(d.get("cwd", "unknown"))
with open(os.path.join(log_dir, f"hook-{run}.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps({"time": datetime.datetime.now().isoformat(), "tool": d.get("tool_name"),
                        "allowed": allowed}, ensure_ascii=False) + "\n")

if not allowed:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "막음: 이 일을 하기 전에 무엇을 할지 설명하고 사용자의 허락을 받으세요. (규칙 5, 9)"}},
        ensure_ascii=False))
sys.exit(0)
