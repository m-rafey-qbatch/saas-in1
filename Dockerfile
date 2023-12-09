FROM public.ecr.aws/sam/build-python3.10:1.104.0-20231206215006

WORKDIR /usr/src/app

RUN yum update -y && \
 yum install -y mesa-libGL mysql-devel

RUN export MYSQLCLIENT_CFLAGS=`pkg-config --cflags mysqlclient` && \
   export MYSQLCLIENT_LDFLAGS=`pkg-config --libs mysqlclient`

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
