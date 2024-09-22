# FROM python:3.10
FROM python:3.10-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y cmake make git wget curl
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Make sure your python version is later than 3.10
# You can use pyenv to manage multiple python verisons in your sytstem
RUN pip install pip-tools
# Configurate Poetry
RUN poetry config virtualenvs.create false

# Clone github repo
RUN git clone https://github.com/camel-ai/camel.git /camel
WORKDIR /camel
RUN poetry install --with dev,docs -E all

RUN pre-commit install

WORKDIR /

COPY requirements.in requirements.in
RUN pip-compile requirements.in && \
    pip install -r requirements.txt

WORKDIR /app
# Install other dependencies, if needed
COPY . .

# Entrypoint script to download datasets and start the app
# COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
