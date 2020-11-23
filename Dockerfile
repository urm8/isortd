FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install
EXPOSE 47393
CMD ["poetry", "run", "python", "-m", "isortd"]

