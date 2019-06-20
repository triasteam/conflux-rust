#!/usr/bin/env python3

import time
import eth_utils
import rlp

import sys
sys.path.append("..")

from conflux.rpc import RpcClient
from test_framework.test_framework import DefaultConfluxTestFramework
from test_framework.util import assert_greater_than_or_equal, assert_equal
from test_framework.test_node import TestNode


class Account:
    def __init__(self, address:str, priv_key:bytes, balance:int, nonce:int=0):
        self.address = address
        self.priv_key = priv_key
        self.balance = balance
        self.nonce = nonce
        self.last_tx_hash = None


class Generator:

    def __init__(self, hosts_and_posts: list):
        self.nodes = []
        self.init_nodes(hosts_and_posts)

    def init_nodes(self, hosts_and_posts: list):
        MAX_NODES = 1
        for i in range(MAX_NODES):
            # datadir = initialize_datadir(self.options.cachedir, i)
            # args = [self.options.bitcoind, "-datadir=" + datadir]
            # if i > 0:
            #     args.append("-connect=127.0.0.1:" + str(p2p_port(0)))
            self.nodes.append(
                TestNode(
                    i,
                    "",  # get_datadir_path(self.options.cachedir, i),
                    rpchost=hosts_and_posts[i][0],
                    confluxd="",
                    rpcport=hosts_and_posts[i][1],
                    remote=True
                )
            )
            # self.nodes[i].args = args
            # self.start_node(i)
        # Wait for RPC connections to be ready
        for node in self.nodes:
            node.wait_for_rpc_connection()

    def init_senders(self, num_accounts):
        accounts = []
        client = RpcClient(self.nodes[0])
        init_balance = int(client.GENESIS_ORIGIN_COIN * 0.9 / num_accounts)
        assert_greater_than_or_equal(client.GENESIS_ORIGIN_COIN, num_accounts * (init_balance + client.DEFAULT_TX_FEE))
        for _ in range(num_accounts):
            to, priv_key = client.rand_account()
            tx = client.new_tx(receiver=to, value=init_balance)
            client.send_tx(tx, True)
            accounts.append(Account(to, priv_key, init_balance))
        return accounts

    def init_receivers(self, num_accounts):
        accounts = []
        client = RpcClient(self.nodes[0])
        for _ in range(num_accounts):
            accounts.append(Account(client.rand_addr(), None, 0))
        return accounts

    def generate_tx(self, num_of_transcations):
        senders = self.init_senders(num_of_transcations)
        receivers = self.init_receivers(1)
        txs = []
        for s in senders:
            for r in receivers:
                txs.append(self.convert_tx(s, r))
        return txs

    def convert_tx(self, sender: Account, receiver: Account):
        client = RpcClient(self.nodes[0])
        tx = client.new_tx(sender.address, receiver.address, sender.nonce, value=1, priv_key=sender.priv_key)
        return tx

    def write_to_file(self, txs):
        data_file = open("data", "w")

        id = 1
        for tx in txs:
            encoded = eth_utils.encode_hex(rlp.encode(tx))
            data_file.write(str(id)+","+encoded+"\n")
            id += 1

        data_file.close()


if __name__ == "__main__":
    g = Generator([("127.0.0.1", 8091)])
    g.write_to_file(g.generate_tx(1000))
