FROM rust:1.34

WORKDIR /conflux 
COPY . /conflux 
COPY ./entrypoint.sh /

RUN apt-get update 
RUN apt-get install -y --no-install-recommends clang
RUN cargo build --release 

EXPOSE 13700

WORKDIR /conflux/run_time/data/
ENTRYPOINT [ "/entrypoint.sh" ]