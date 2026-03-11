def detect_language(query: str, code: str = None, selected_language: str = None) -> str:
    """
    Detects the programming language based on priority rules:
    1. If selected_language is provided → return it
    2. Detect from code patterns
    3. Detect from keywords in query
    4. Default to python
    """

    if selected_language:
        return selected_language.lower()


    query = (query or "").lower()
    code = (code or "").lower()

    if "def " in code:
        return "python"
    if "public static void main" in code:
        return "java"
    if "func main()" in code:
        return "go"

    if any(keyword in query for keyword in ["python", "django", "flask"]):
        return "python"
    if any(keyword in query for keyword in ["java", "spring", "jvm"]):
        return "java"
    if any(keyword in query for keyword in ["golang", "go language", "go "]):
        return "go"

  
    return "python"