import json
from pathlib import Path
from fastapi import HTTPException

ERROR_FILE = Path(__file__).parent / "error.json"
_errors = {}
if ERROR_FILE.exists():
	try:
		_errors = json.loads(ERROR_FILE.read_text(encoding="utf-8"))
	except Exception:
		_errors = {}


def to_http_exception(code: str, detail: str | None = None) -> HTTPException:
	info = _errors.get(code, {"status_code": 500, "message": "Internal error"})
	status = info.get("status_code", 500)
	msg = info.get("message", "Internal error")
	if detail:
		msg = f"{msg}: {detail}"
	return HTTPException(status_code=status, detail=msg)

