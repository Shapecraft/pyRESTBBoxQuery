# Create Ubuntu Container
FROM ubuntu:14.04

# Author
MAINTAINER Dathan Romstad "tstardom@gmail.com"

# Update Ubuntu repos
RUN apt-get update

# Install Python.
RUN apt-get install -y python-gdal 
RUN apt-get install -y python-simplejson
RUN apt-get install -y python python-pip wget
RUN apt-get install -y python-all-dev
RUN apt-get install -y python-flask

RUN mkdir querypoints

RUN mkdir /querypoints/web

WORKDIR /querypoints/web

COPY app.py /querypoints/web/

COPY sample_data.dbf /querypoints/web/sample_data.dbf

COPY sample_data.prj /querypoints/web/sample_data.prj

COPY sample_data.shp /querypoints/web/sample_data.shp

COPY sample_data.shx /querypoints/web/sample_data.shx

COPY docker-compose.yml /querypoints/

# Add requirements file.
ADD requirements.txt /querypoints/web/requirements.txt

RUN pip install -r /querypoints/web/requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

