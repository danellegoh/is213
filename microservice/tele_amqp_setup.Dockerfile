FROM python:3-slim
WORKDIR /usr/src/app
COPY amqp.requirements.txt ./
RUN python -m pip install --no-cache-dir -r amqp.requirements.txt
COPY ./tele_amqp_setup.py .
CMD [ "python", "./tele_amqp_setup.py" ]