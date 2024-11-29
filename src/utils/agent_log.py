import logging
from logging import Logger
from pathlib import Path


class AgentLogger(Logger):
    def __init__(
        self,
        output_dir: Path,
        game_id: str,
        name: str,
    ) -> None:
        super().__init__(name)
        super().setLevel(logging.DEBUG)
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        self.handler = logging.FileHandler(
            Path(output_dir, game_id + "_" + name + ".log"),
            encoding="utf-8",
        )
        self.handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        super().addHandler(self.handler)
