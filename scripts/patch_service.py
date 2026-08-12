import re
path = r"C:\Users\504508\PythonProject\PythonChatBot\ai_petcare_Assistant\app\services\services.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old = """        if query:
            words = query.lower().split()
            # Try to match products where any of the significant words match
            def match_score(p):
                text = (p['name'] + " " + p['description']).lower()
                return sum(1 for w in words if w in text and len(w) > 3)

            # Sort results by match score
            scored_results = [(p, match_score(p)) for p in results]
            # Only keep results that have at least one significant word match
            results = [p for p, score in scored_results if score > 0]
            # Optionally sort them by score descending
            results.sort(key=lambda x: match_score(x), reverse=True)

        return results"""

new = """        if query:
            words = query.lower().split()
            # Try to match products where any of the significant words match
            def match_score(p):
                text = (p['name'] + " " + p['description']).lower()
                return sum(1 for w in words if w in text and len(w) > 3)

            # Sort results by match score
            scored_results = [(p, match_score(p)) for p in results]
            # Only keep results that have at least one significant word match
            results = [p for p, score in scored_results if score > 0]
            # Optionally sort them by score descending
            results.sort(key=lambda x: match_score(x), reverse=True)
            results = results[:5]

        return results"""

if old in text:
    print("Found exact block, replacing...")
    text = text.replace(old, new)
else:
    print("Exact block not found! Trying fallback approach...")
    text = text.replace("results.sort(key=lambda x: match_score(x), reverse=True)\n\n        return results", "results.sort(key=lambda x: match_score(x), reverse=True)\n            results = results[:5]\n\n        return results")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)
