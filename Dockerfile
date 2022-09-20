FROM python:3
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt
WORKDIR ./
EXPOSE 5000
CMD python3 app.py
