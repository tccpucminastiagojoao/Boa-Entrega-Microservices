FROM python:3.10.2
WORKDIR /app
COPY app/requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY app/main.py /app/
EXPOSE 5000
CMD ["python", "/app/main.py"]