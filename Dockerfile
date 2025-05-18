FROM python:3.12

WORKDIR /Ufanet_practice

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install uv
COPY pyproject.toml uv.lock requirements.txt ./
RUN uv pip install --system -r requirements.txt

COPY . .

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]