import asyncio

import aiohttp

from raven.contrib.tornado import AsyncSentryClient

from jam import settings


class AioSentryClient(AsyncSentryClient):

    def send_remote(self, url, data, headers=None, callback=None):
        headers = headers or {}
        if not self.state.should_try():
            message = self._get_log_message(data)
            self.error_logger.error(message)
            return

        async def _future():
            resp = await aiohttp.request('POST', url, data=data, headers=headers)
            await resp.release()

        asyncio.ensure_future(_future())


def patch_sentry(app):
    app.sentry_client = AioSentryClient(settings.SENTRY_DSN)
    return app
