FROM rust:1.34
  
WORKDIR /conflux
COPY . /conflux

RUN apt-get update
RUN apt-get install -y --no-install-recommends clang
RUN cargo build --release

WORKDIR /iri/run_time/
ENTRYPOINT [ "/entrypoint.sh" ]