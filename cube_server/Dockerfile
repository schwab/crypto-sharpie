FROM ubuntu
MAINTAINER Michael Schwab mike@mdmetrix.com
RUN apt-get update -y
RUN apt-get install -y python curl python-dev


# Install Pip
RUN apt-get install -y python-pip build-essential
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y net-tools
RUN pip install --upgrade pip
RUN apt-get install -y python3-pip



# Install Cubes
RUN pip install cubes
RUN pip install flask
RUN pip install sqlalchemy
RUN pip install pymysql
RUN pip install numpy==1.12.1
RUN pip install pandas==0.19.2
RUN pip install requests
RUN pip install scipy
RUN pip3 install jupyter
RUN pip install matplotlib
RUN pip install ipykernel
RUN python2 -m ipykernel install --user

COPY . /srv
WORKDIR /srv
# Mountpoint for the cubes project
VOLUME ["/srv"]

# Cubes port
EXPOSE 5000
EXPOSE 80

#CMD ["slicer","serve","slicer.ini"]
CMD ["./slicer_start.sh", "import"]
