import structlog
from astraeus_common.decorator.logit import logit
from astraeus_common.io.database import Database
from astraeus_common.models.eddn_msg import EddnMsg

from ..client.eddn_client import EddnClient
from ..services.eddn_msg_service import EddnMessageService


# TODO: complete the process by:
# TODO: 1. reading messages in EDDN MSG table
# TODO: 2. getting nature of the update
# TODO: 3. update the entity in database

class EddnOrchestrator:
    _eddn_client: EddnClient

    def __init__(self, db: Database):
        self._eddn_msg_service = EddnMessageService(db)
        self._eddn_client = EddnClient()
        self._log = structlog.getLogger()

    def run_listener(self) -> None:
        self._eddn_client.run(self.__process_message)

    @logit
    def __process_message(self, msg: dict) -> None:
        self._log.info('Recording message')
        self._eddn_msg_service.create_eddn_message(
                EddnMsg(schema=msg['$schemaRef'],
                        header=msg['header'],
                        message=msg['message']))
