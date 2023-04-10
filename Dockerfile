FROM ubuntu:jammy AS base

WORKDIR /conventional_FL_MQ
ENV TZ=Etc/UTC
RUN apt-get update && \
    apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    python3-wheel \
    nano

FROM base as update-convflmq
WORKDIR /conventional_FL_MQ
ENV VIRTUAL_ENV=./venv
RUN python3.10 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 --cache-dir /var/cache/evio/ \
        install wheel && \
    pip3 --cache-dir /var/cache/evio/ \
        install -r /tmp/requirements.txt

FROM update-convflmq
RUN rm -rf /var/lib/apt/lists/* \
        /var/cache/evio/ && \
    apt-get autoclean
ARG USERNAME=evio
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

WORKDIR /conventional_FL_MQ
COPY ./src/ .


ENTRYPOINT ["./start_worker.sh"]