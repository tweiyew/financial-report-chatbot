from langchain.agents import Tool

def safe_eval(expression: str) -> float:
    """Safely evaluate a basic arithmetic expression like '10 + 5 * (2 - 1)'."""
    try:
        return eval(expression, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

calculator = Tool(
    name="Calculator",
    func=safe_eval,
    description="Safely evaluate arithmetic expressions like '2 + 2 * (3 - 1)'."
)
