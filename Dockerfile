FROM python:3.9-slim
WORKDIR /usr/src/app
ENV PIP_ROOT_USER_ACTION=ignore
ARG token
ARG pass_1c
ENV TOKEN=${token}
ENV PASS_1C=${pass_1c}
COPY requirements.txt ./
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Almaty /etc/localtime
RUN echo "Asia/Almaty" > /etc/timezone
COPY / .
CMD ["python", "./main.py"]
