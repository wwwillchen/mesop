# Used for huggingface space

FROM python:3.10

WORKDIR /code

COPY ./demo/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./demo .

CMD ["gunicorn", "--bind", ":7860", "main:me"]
