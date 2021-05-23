import os
from io import StringIO

from aiofile import AIOFile
from isort import settings
from loguru import logger
from watchgod import PythonWatcher, awatch

from isortd.isort_handler import IsortHandler

CUR_DIR = "."
PYPROJECT_TOML = "pyproject.toml"
ISORT_CFG = ".isort.cfg"
POSSIBLE_CFGS = [PYPROJECT_TOML, ISORT_CFG]


async def main():
    cfg = None
    curr_dir_contents = os.listdir(CUR_DIR)
    if not set(curr_dir_contents).intersection(POSSIBLE_CFGS):
        logger.warning("was not able to find any config file for isort daemon")
    else:
        cfg, *_ = set(POSSIBLE_CFGS).intersection(curr_dir_contents)

    if cfg is None:
        logger.warning("failed to find config file will use default settings")
    handler = IsortHandler(cfg=settings.Config(cfg))
    logger.info(f"start watching: {CUR_DIR}")
    async for changes in awatch(CUR_DIR, watcher_cls=PythonWatcher, debounce=100):
        for _, file_changed in changes:
            await try_isort(file_changed, handler)


async def try_isort(file_changed: str, handler: IsortHandler):
    try:
        fout = StringIO()
        with AIOFile(file_changed, "r") as fin:
            in_ = await fin.read()
            if out := handler.handle(fin):
                async with AIOFile(file_changed, "w") as wfout:
                    await wfout.write(fout.getvalue())
    except Exception as e:
        logger.error(f"shit happened: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
