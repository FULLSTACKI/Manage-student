class AppError(Exception):
	"""Base application error containing a code and optional details."""
	def __init__(self, code: str, detail: str | None = None):
		self.code = code
		self.detail = detail
		super().__init__(f"{code}: {detail}")


class ValidationError(AppError):
	pass


class NotFoundError(AppError):
	pass


class ConflictError(AppError):
	pass


class DatabaseError(AppError):
	pass

