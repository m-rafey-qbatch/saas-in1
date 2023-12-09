   FROM python:3.10

   WORKDIR /usr/src/app

   RUN apt-get update && \
       apt-get install -y libgl1-mesa-glx

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]