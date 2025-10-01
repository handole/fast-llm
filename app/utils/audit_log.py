import logging
from audit_log.logger import AuditLogger

class BauditLogger(AuditLogger):
    def __init__(self) -> None:
        super().__init__()

        self.logger = self.init_logger()
        self.level = logging.DEBUG
        self.message = ""
        self.http_request = None
        self.http_response = None
        self.user = None
        self.filter = None
        self.results = None

    def init_logger(self) -> logging.logger:
        formatter = self.get_log_formatter()
        logging.root.manager.loggerDict["audit"].handlers[0].setFormatter(formatter)
        return logging.getLogger("audit")

    def get_log_handler(self) -> logging.Handler:
        return logging.root.manager.loggerDict["audit"].handlers[0]