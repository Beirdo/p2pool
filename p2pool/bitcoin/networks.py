import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack
from operator import *

def get_subsidy(nCap, nMaxSubsidy, bnTarget):
    bnLowerBound = 0.01
    bnUpperBound = bnSubsidyLimit = nMaxSubsidy
    bnTargetLimit = 0x00000fffff000000000000000000000000000000000000000000000000000000

    while bnLowerBound + 0.01 <= bnUpperBound:
        bnMidValue = (bnLowerBound + bnUpperBound) / 2
        if pow(bnMidValue, nCap) * bnTargetLimit > pow(bnSubsidyLimit, nCap) * bnTarget:
            bnUpperBound = bnMidValue
        else:
            bnLowerBound = bnMidValue

    nSubsidy = round(bnMidValue, 2)

    if nSubsidy > bnMidValue:
        nSubsidy = nSubsidy - 0.01

    return int(nSubsidy * 1000000)

nets = dict(
    MudCoin=math.Object(
        P2P_PREFIX='e8e9e6e5'.decode('hex'),
        P2P_PORT=8462,
        ADDRESS_VERSION=50,
        RPC_PORT=18462,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'mudcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(4, 50, target),
        BLOCKHASH_FUNC=data.hash256,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=60, # s
        SYMBOL='MUD',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'MudCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/MudCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.MudCoin'), 'MudCoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://novacoin.ru/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://novacoin.ru/address/',
        SANE_TARGET_RANGE=(2**256//2**20//1000 - 1, 2**256//2**20 - 1),
    ),
    MudCoin_testnet=math.Object(
        P2P_PREFIX='cbf2c0ef'.decode('hex'),
        P2P_PORT=8562,
        ADDRESS_VERSION=110,
        RPC_PORT=18562,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'mudcoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(4, 50, target),
        BLOCKHASH_FUNC=data.hash256,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=60, # s
        SYMBOL='tMUD',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'MudCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/MudCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.MudCoin'), 'MudCoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://nonexistent-novacoin-testnet-explorer/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://nonexistent-novacoin-testnet-explorer/address/',
        SANE_TARGET_RANGE=(2**256//2**20//1000 - 1, 2**256//2**20 - 1),
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
