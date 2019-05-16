#!/bin/bash
# See Dockerfile and DOCKER.md for further info


exec /conflux/target/release/conflux --config /conflux/run_time/data/conflux.conf --public-address 127.0.0.1:14700 