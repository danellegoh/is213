FROM python:3-slim
WORKDIR /usr/src/app
COPY http.requirements.txt amqp.requirements.txt ./
RUN python -m pip install --no-cache-dir -r http.requirements.txt
RUN python -m pip install --no-cache-dir -r amqp.requirements.txt
COPY ./telegram.py ./tele_amqp_setup.py ./
CMD [ "python", "./telegram.py" ]