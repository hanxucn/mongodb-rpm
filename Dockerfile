FROM docker.io/library/ubuntu:16.04 as ubuntu16

RUN groupadd -r -g 184 mongodb && useradd -r -g mongodb -u 184 mongodb
RUN apt-get update
RUN apt-get install -y libssl1.0.0
RUN apt-get install -y libcurl3


FROM docker.io/library/ubuntu:18.04 as ubuntu18

RUN groupadd -r -g 184 mongodb && useradd -r -g mongodb -u 184 mongodb
RUN apt-get update
RUN apt-get install -y libcurl4
