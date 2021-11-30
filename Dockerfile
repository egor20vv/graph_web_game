FROM tiangolo/uvicorn-gunicorn-fastapi

COPY required_packages.txt required_packages.txt
RUN pip install -r required_packages.txt && rm required_packages.txt

EXPOSE $PORT

COPY ./application /home/app

WORKDIR /home/app