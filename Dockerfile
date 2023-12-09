FROM public.ecr.aws/sam/build-python3.10:1.104.0-20231206215006

WORKDIR /usr/src/app

RUN yum update -y && \
    yum install -y mesa-libGL pkg-config mariadb-connector-c mariadb-connector-c-devel

# Specify MySQL client flags and linker flags manually
RUN export MYSQLCLIENT_CFLAGS="-I/usr/include/mysql" && \
    export MYSQLCLIENT_LDFLAGS="-L/usr/lib64/mysql -lmysqlclient"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
