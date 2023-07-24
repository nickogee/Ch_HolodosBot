FROM python:3.9-slim
WORKDIR /usr/src/app
ENV PIP_ROOT_USER_ACTION=ignore
ARG token
ENV TOKEN=${token}
COPY requirements.txt ./
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt
RUN echo 1
COPY / .
CMD ["python", "./main.py"]
