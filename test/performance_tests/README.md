## 1. How to conduct performance test


### 1.1 install and run conflux

Please refer [Conflux document](https://conflux-chain.github.io/conflux-doc/) for how to install and run Conflux first. 
The following is an example configuration:

```
port=15267
jsonrpc_local_http_port=8091
jsonrpc_http_port=8092
log_file='/Users/stplaydog/gitlocal/triasteam/conflux-rust/target/release/run_experiment/conflux.log'
test_mode=true
log_level="info"
storage_cache_size=200000
storage_cache_start_size=200000
storage_node_map_size=200000
start_mining=true
mining_author="e0063a386dd9e465b7b7a9270f50f9c309349fbf"
p2p_nodes_per_ip=0
enable_discovery=false
``` 

### 1.2 generate data

```
python3 data_generate.py
```

It will generate a data file namely 'data'.

### 1.3

Run performance test with jmeter.
Replace DATA in PerformanceTestConflux\_TPS.jmx with data file. 

```
jmeter -n -t PerformanceTestConflux_TPS.jmx 
```
