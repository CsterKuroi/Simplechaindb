"""
This module  takes care of all the changes for bigchain and votes.
"""

import logging
from multipipes import Pipeline, Node
from bigchaindb.localdb_pipelines.utils import ChangeFeed

logger = logging.getLogger(__name__)


class LocalBlock(Node):
    """This class monitor the change for block.

    Note:
        Methods of this class will be executed in different processes.
    """

    INSERT = 1
    DELETE = 2
    UPDATE = 4

    def __init__(self):
        pass

def create_pipeline():
    localBlock = LocalBlock()
    localBlock__pipeline = Pipeline([])
    return localBlock__pipeline


def initial():
    return None

def get_changefeed():
    """Create and return the changefeed for the bigchain."""
    return ChangeFeed('bigchain',ChangeFeed.INSERT | ChangeFeed.UPDATE,prefeed=initial())


def start():
    """Create, start, and return the localBlock pipeline."""
    pipeline = create_pipeline()
    pipeline.setup(indata=get_changefeed())
    pipeline.start()
    return pipeline
