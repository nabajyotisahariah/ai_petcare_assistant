import re
path = r"C:\Users\504508\PythonProject\PythonChatBot\ai_petcare_Assistant\app\services\services.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old = """        if category:
            results = [p for p in results if p['category'].lower() == category.lower()]"""

new = """        if category:
            # Check if there is an exact match for category, if not try substring, if not, ignore category
            exact_match = [p for p in results if p['category'].lower() == category.lower()]
            if exact_match:
                results = exact_match
            else:
                sub_match = [p for p in results if category.lower() in p['category'].lower()]
                if sub_match:
                    results = sub_match"""

text = text.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(text)
