import re

def detect_language(query, code=None):
    query = (query or "").lower()
    code = (code or "").lower()

    manual_match = re.search(r'language\s*:\s*(\w+)', query)
    if manual_match:
        return manual_match.group(1)

    if "def " in code:
        return "python"
    if "public static void main" in code:
        return "java"
    if "func main()" in code:
        return "go"

    keywords = {
        "python": ["print(", "import ", "lambda ", "self"],
        "java": ["system.out.println", "class ", "new ", "extends"],
        "go": ["fmt.", "package main", "chan ", "goroutine"],
        "javascript": ["console.log", "function ", "=>", "var ", "let ", "const "],
        "c++": ["#include", "std::", "cout", "cin"],
        "c": ["#include", "printf(", "scanf("]
    }

    combined_text = query + " " + code

    for language, terms in keywords.items():
        for term in terms:
            if term in combined_text:
                return language

    return "unknown"