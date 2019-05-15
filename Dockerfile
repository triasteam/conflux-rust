FROM rust:1.31

WORKDIR /conflux 
COPY . /conflux 

RUN cargo build --release 

WORKDIR /iri/run_time/
ENTRYPOINT [ "/entrypoint.sh" ]
