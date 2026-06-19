FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y \
    && apt install -y --no-install-recommends software-properties-common gnupg ca-certificates curl \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt update && apt upgrade -y \
    && apt install -y python3.11 python3.11-dev python3.11-venv iputils-ping wget telnet iproute2 net-tools vim lsof unzip zip git jq ffmpeg \
    && git config --global user.email "95691624+tdragon6@users.noreply.github.com" \
    && git config --global user.name "tdragon6" \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 \
    && pip3 install requests beautifulsoup4 scrapy openpyxl pandas python-docx pypdf numpy \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt update && apt upgrade -y \
    && apt install -y --no-install-recommends nodejs \
    && npm install -g npm@latest \
    && npm install -g agent-browser \
    && agent-browser install --with-deps \
    && npm install -g skills \
    # && apt clean && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://raw.githubusercontent.com/tdragon6/AgBox/refs/heads/main/install.sh | bash

ENTRYPOINT ["agbox"]