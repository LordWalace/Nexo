from unittest.mock import AsyncMock, patch

import pytest
from app.core.redis import close_redis, ping_redis


@pytest.mark.asyncio
async def test_redis_ping_success(mock_env_vars):
    with patch("app.core.redis.from_url") as mock_from_url:
        mock_client = AsyncMock()
        mock_client.ping.return_value = True
        mock_from_url.return_value = mock_client

        result = await ping_redis()
        assert result is True

        await close_redis()


@pytest.mark.asyncio
async def test_redis_ping_failure(mock_env_vars):
    with patch("app.core.redis.from_url") as mock_from_url:
        mock_client = AsyncMock()
        mock_client.ping.side_effect = Exception("Connection Error")
        mock_from_url.return_value = mock_client

        result = await ping_redis()
        assert result is False

        await close_redis()
