FROM selenium/standalone-chrome

USER root

RUN apt-get update
RUN apt-get install -y python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD ["python3", "main.py"]
