FROM ubuntu:20.04

RUN apt update -y --fix-missing
RUN apt install -y python3 gcc python3-dev python3-pip ruby-full rubygems-integration musl-dev protobuf-compiler git ruby-full libmagic-dev strace curl
RUN gem install parser:3.0.0.0 google-protobuf:3.21.2 rubocop:1.31.1
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs

RUN groupadd -g 1001 ubuntu
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g ubuntu -u 1001 ubuntu

WORKDIR /home/ubuntu/packj

RUN git clone https://github.com/ossillate-inc/packj /home/ubuntu/packj
RUN chown -R ubuntu:ubuntu /home/ubuntu/packj && pip3 install -r requirements.txt

USER ubuntu
ENTRYPOINT ["python3", "main.py"]
