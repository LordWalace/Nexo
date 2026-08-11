import logging
import re


class MaskingFilter(logging.Filter):
    def __init__(self) -> None:
        super().__init__()
        # Matches typical secret keywords in JSON or key=value formats
        self.pattern = re.compile(
            r"(password|token|secret|credentials)[\s]*[:=][\s]*([^\s,]+)", re.IGNORECASE
        )

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.pattern.sub(r"\1=***", record.msg)
        return True


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    for handler in logging.root.handlers:
        handler.addFilter(MaskingFilter())
