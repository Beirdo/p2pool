from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    MudCoin=math.Object(
        PARENT=networks.nets['MudCoin'],
        SHARE_PERIOD=30, # seconds
        CHAIN_LENGTH=24*60*60//30, # shares
        REAL_CHAIN_LENGTH=24*60*60//30, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=3, # blocks
        IDENTIFIER='e037d5bc69823510'.decode('hex'),
        PREFIX='7208c1a3ef6549b0'.decode('hex'),
        P2P_PORT=28462,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=28463,
        BOOTSTRAP_ADDRS=['seed%s.mudcoin.mycryptocoins.net' % i for i in range(1, 6)],
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: v >= 60006,
    ),
    novacoin_testnet=math.Object(
        PARENT=networks.nets['MudCoin_testnet'],
        SHARE_PERIOD=3, # seconds
        CHAIN_LENGTH=20*60//3, # shares
        REAL_CHAIN_LENGTH=20*60//3, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='e037d5bc69823510'.decode('hex'),
        PREFIX='7208c1a3ef6549b0'.decode('hex'),
        P2P_PORT=38462,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=38463,
        BOOTSTRAP_ADDRS=['tnseed%s.mudcoin.mycryptocoins.net' % i for i in range(1, 6)],
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: v >= 60006,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
