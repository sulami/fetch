FROM python:3.9

RUN pip install poetry

COPY . /mnt
WORKDIR /mnt

RUN poetry install

ENTRYPOINT ["/bin/bash"]
