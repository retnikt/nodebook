FROM python:3

ARG DEV_DEPS=false

WORKDIR /app/

COPY ./ /app/

# install dependencies - we need pipenv 2020.04.01.a1 which is not on normal pypi
# but the dependencies are only on normal pypi so install old pipenv + deps first
RUN sh -c 'pip install --no-cache-dir pipenv && \
pip install --no-cache-dir -i https://test.pypi.org/simple/ -U pipenv && \
[ "$DEV_DEPS" = true ] \
  && pipenv install --clear -d || \
  pipenv install --clear'

EXPOSE 80

# run inside virtual environment
ENTRYPOINT ["pipenv", "run"]

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/app/gunicorn_config.py", "notebook:app"]
