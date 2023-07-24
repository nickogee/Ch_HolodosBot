FROM python:3.9-slim
WORKDIR /usr/src/app
ENV PIP_ROOT_USER_ACTION=ignore
ARG token
ENV TOKEN=${token}
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY / .
CMD ["python", "./main.py"]
