FROM ubuntu:20.04

WORKDIR /packj

#RUN apt-get update -y
#RUN apt-get install -y python3 gcc python3-dev python3-pip strace vim #ruby-full rubygems-integration musl-dev protobuf-compiler git ruby-full libmagic-dev curl
#RUN gem install parser:3.0.0.0 google-protobuf:3.21.2 rubocop:1.31.1

#RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs

#RUN groupadd -g 1001 ubuntu
#RUN useradd -rm -d /home/ubuntu -s /bin/bash -g ubuntu -u 1001 ubuntu

#USER ubuntu
#WORKDIR /home/ubuntu/

#COPY --chown=ubuntu:ubuntu . .
COPY . .
RUN apt-get update -y && apt-get install -y python3 gcc python3-dev python3-pip python3.8-venv strace vim curl

#&& python3 -m venv venv && . venv/bin/activate && pip3 install -r requirements.txt && pip3 list

#RUN . venv/bin/activate && pip3 install -r requirements.txt

#ENTRYPOINT ["bash","./trace.sh"]
#CMD . venv/bin/activate && bash

#ruby-full rubygems-integration musl-dev protobuf-compiler git ruby-full libmagic-dev 
#RUN find /home/ubuntu -type f -exec touch {} + && pip3 install -r requirements.txt

#ENTRYPOINT ["./start.sh"]
#ENTRYPOINT ["python3", "main.py"]
#CMD ["python3", "main.py", "--dynamic", "pypi", "tensorflow"]

