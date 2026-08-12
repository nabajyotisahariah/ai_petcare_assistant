import re
path = r"C:\Users\504508\PythonProject\PythonChatBot\ai_petcare_Assistant\app\tools\crew_tools.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old = """@tool("search_products")
def search_products(query: str = None, category: str = None, max_price: float = None) -> str:
    \"\"\"Searches for pet products based on query, category, and max price.\"\"\"
    results = product_svc.search_products(query=query, category=category, max_price=max_price)"""

new = """@tool("search_products")
def search_products(query: str = None, category: str = None, max_price: float = None) -> str:
    \"\"\"Searches for pet products based on query, category, and max price.\"\"\"
    print(f">>>> SEARCH PRODUCTS CALLED WITH query={query}, category={category}, max_price={max_price}")
    results = product_svc.search_products(query=query, category=category, max_price=max_price)"""

text = text.replace(old, new)
with open(path, "w", encoding="utf-8") as f:
    f.write(text)
