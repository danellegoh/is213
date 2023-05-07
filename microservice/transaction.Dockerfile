FROM python:3-slim
WORKDIR /usr/src/app
COPY http.requirements.txt ./
RUN python -m pip install --no-cache-dir -r http.requirements.txt
COPY ./transaction.py .
CMD [ "python", "./transaction.py" ]