FROM tiangolo/uvicorn-gunicorn-fastapi

COPY required_packages.txt required_packages.txt
RUN pip install -r required_packages.txt

ENV PORT 8000
EXPOSE $PORT

COPY ./application /app

CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]