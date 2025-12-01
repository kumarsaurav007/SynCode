from fastapi import APIRouter
from ..schemas import AutocompleteRequest, AutocompleteResponse

router = APIRouter()

@router.post("/autocomplete", response_model=AutocompleteResponse)
async def autocomplete(req: AutocompleteRequest):
    """
    Mocked rule-based autocomplete. Not a real AI; simple heuristics only.
    """
    code = req.code or ""
    pos = req.cursorPosition if req.cursorPosition is not None else len(code)

    left = code[:pos].rstrip()
    last_token = ""
    if left:
        parts = left.split()
        if parts:
            last_token = parts[-1]

    suggestion = ""
    # Very lightweight heuristics
    if last_token.endswith("pr") or last_token == "print":
        suggestion = 'print("hello")'
    elif last_token == "def":
        suggestion = "def function_name(params):\n    pass"
    elif last_token == "for":
        suggestion = "for i in range(n):\n    pass"
    elif left.endswith(":"):
        suggestion = "    pass"
    else:
        suggestion = "# suggestion: consider extracting a helper function"

    return {"suggestion": suggestion}
