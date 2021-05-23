from pathlib import Path

from isort import Config, code
from isort.api import sort_stream


class IsortHandler:
    def __init__(self, *, cfg: Config) -> None:
        self.cfg = cfg

    def handle(self, in_: str, fp: str) -> str:
        """
        :param in_:  is the code that must be isorted
        :param fp: is the file path that is given by sort service
        :return:
        """
        # intentionally left with 2 lines, so it may be easily debugged
        out = code(code=in_, config=self.cfg, file_path=Path(fp) if fp else None)
        return out

    def handle_stream(self, in_, out) -> bool:
        return sort_stream(in_, out, config=self.cfg)
