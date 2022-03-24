FROM python:3.10
WORKDIR /app
COPY app/requirements.txt /app/
COPY app/main.py /app/
COPY app/models.py /app/
COPY app/cadastros_exemplo.py /app/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]