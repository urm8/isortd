FROM pypy:3.7-7.3.2
ENV PYTHONUNBUFFERED 1
RUN pypy -m pip install isortd
USER isortd
EXPOSE 47393
CMD ["pypy", "isortd", "--host", "0.0.0.0", "--port", "47393"]