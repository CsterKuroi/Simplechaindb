import logging
import multiprocessing as mp

import bigchaindb
from bigchaindb.pipelines import vote, block, election, stale
from bigchaindb.web import server

from bigchaindb.localdb_pipelines import local_block,local_vote
from bigchaindb.localdb import utils as leveldb

logger = logging.getLogger(__name__)

BANNER = """
****************************************************************************
*                                                                          *
*   Initialization complete. BigchainDB is ready and waiting for events.   *
*   You can send events through the API documented at:                     *
*    - http://docs.bigchaindb.apiary.io/                                   *
*                                                                          *
*   Listening to client connections on: {:<15}                    *
*                                                                          *
****************************************************************************
"""


def start():
    logger.info('Initializing BigchainDB...')

    # init localdb with localdb utils
    logger.info('start localdb pipeline...')
    leveldb.init()
    local_block.start()
    local_vote.start()

    # start the processes
    logger.info('Starting block')
    block.start()

    logger.info('Starting voter')
    vote.start()

    logger.info('Starting stale transaction monitor')
    stale.start()

    logger.info('Starting election')
    election.start()

    # start the web api
    app_server = server.create_server(bigchaindb.config['server'])
    p_webapi = mp.Process(name='webapi', target=app_server.run)
    p_webapi.start()

    # start message
    logger.info(BANNER.format(bigchaindb.config['server']['bind']))
