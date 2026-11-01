import asyncio
import signal
import time
from typing import Any

import jotaro_code
from jotaro_code.core.bus.cmd import PongResult
from jotaro_code.core.config import get_config
from jotaro_code.core.logging_setup import setup_logging
from jotaro_code.core.trans.socket_server import SocketServer
import logging
import datetime

logger = logging.getLogger(__name__)

class CoreApp:

    async def run(self) -> None:
        self._start_time = time.monotonic()
        config = get_config()
        setup_logging(config)

        server = SocketServer(config.host, config.port)
        server.register("core.ping",self._ping_handler)
        addr = await server.start()

        shutdown = asyncio.Event()
        loop = asyncio.get_event_loop()

        # 监听cmd 的指定命令，触发shutdown的函数
        loop.add_signal_handler(signal.SIGINT,shutdown.set)
        loop.add_signal_handler(signal.SIGTERM,shutdown.set)

        await shutdown.wait()
        await server.stop()




    # 处理 core.ping 请求，返回服务版本、运行时长和接收时间
    async def _ping_handler(self, params: dict[str, Any]) -> PongResult:
        client = params.get("client", "unknown")
        logger.debug("ping from %s", client)
        return PongResult(
            server_version=jotaro_code.__version__,
            uptime_ms=int((time.monotonic() - self._start_time) * 1000),
            received_at=datetime.datetime.now(datetime.UTC).isoformat(),
            )