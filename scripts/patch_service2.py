import re
path = r"C:\Users\504508\PythonProject\PythonChatBot\ai_petcare_Assistant\app\services\services.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

def match_func(m):
    return m.group(1) + "\n            results = results[:5]\n" + m.group(2)

text = re.sub(r"(results\.sort\(key=lambda x: match_score\(x\), reverse=True\))(.*?return results)", match_func, text, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
