generate:
	alembic revision --m="$(NAME)" --autogenerate

migrate:
	run alembic upgrade head