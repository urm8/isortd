import logging
import sys
from concurrent import futures
from typing import Mapping

import aiohttp_cors
import click
from aiohttp import web
from isort import api, settings

from isortd import __version__ as ver


@click.command(context_settings={"help_option_names": ["-h --help"]})
@click.option("--host", type=str, help="App host", default="localhost")
@click.option("--port", type=int, help="App port", default=47393)
def main(host, port):
    logging.basicConfig(level=logging.INFO)
    with futures.ProcessPoolExecutor() as executor:
        app = factory(executor)
        app.logger.info(f"isortd version {ver} istening on {host} port {port}")
        web.run_app(app, host=host, port=port, handle_signals=True) or 0
    return 0


def factory(executor: futures.ProcessPoolExecutor) -> web.Application:
    app = web.Application()
    cors = aiohttp_cors.setup(app)
    handler = Handler(executor)
    cors.add(
        app.router.add_route("POST", "/", handler.handle),
        {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers=('Content-Type', *Handler.KNOWN_HEADERS)),
        })
    return app


class Handler:
    headers_mapping = {
        'profile': "X-PROFILE",
        'line_length': "X-MAX-LINE-LENGTH",
        'wrap_length': 'X-WRAP-LENGTH',
        'sections': 'X-SECTIONS',
        'no_sections': 'X-NO-SECTIONS',
        'multi_line_output': 'X-MULTI_LINE_OUTPUT'
    }
    KNOWN_HEADERS = [*headers_mapping.values()]

    def __init__(self, executor: futures.ProcessPoolExecutor):
        self.executor = executor

    async def handle(self, request: web.Request):
        in_ = await request.text()
        config = self._parse(request.headers)
        out = api.sort_code_string(in_, config=config)
        if out:
            return web.Response(text=out, content_type=request.content_type, charset=request.charset)
        print(out)
        return web.Response(status=201)

    def _parse(self, headers: Mapping) -> settings.Config:
        cfg = settings.Config(
            **{ckey: headers[hkey] for ckey, hkey in self.headers_mapping.items() if hkey in headers})
        return cfg


