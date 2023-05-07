FROM python:3-slim
WORKDIR /usr/src/app
COPY amqp.requirements.txt ./
RUN python -m pip install --no-cache-dir -r amqp.requirements.txt
COPY ./emailProcessing.py ./email_amqp_setup.py ./
CMD [ "python", "./emailProcessing.py" ]