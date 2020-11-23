FROM pypy:3.7-7.3.2
ENV PYTHONUNBUFFERED 1
RUN pypy -m pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install -vv --no-dev
WORKDIR /app
COPY . /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
EXPOSE 47393
CMD ["pypy", "isortd", "--host", "0.0.0.0", "--port", "47393"]