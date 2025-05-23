import pytest
from unittest.mock import patch, MagicMock
from line_bot.db import mongodb

def test_get_db_returns_database():
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_client.__getitem__.return_value = mock_db

    with patch("line_bot.db.mongodb.MongoClient", return_value=mock_client):
        db = mongodb.get_db()
        assert db == mock_db

def test_close_mongodb_client():
    mock_client = MagicMock()
    with patch("line_bot.db.mongodb.client", mock_client):
        mongodb.close_mongodb_client()
        mock_client.close.assert_called_once()
<<<<<<< HEAD
# ------------------------------------------------------------------------
# import pytest
# from unittest.mock import AsyncMock, patch, MagicMock
# from line_bot.db import mongodb

# @pytest.mark.asyncio
# async def test_get_db_returns_database():
#     mock_client = MagicMock()
#     mock_db = MagicMock()
#     mock_client.__getitem__.return_value = mock_db

#     with patch("line_bot.db.mongodb.AsyncIOMotorClient", return_value=mock_client):
#         db = mongodb.get_db()
#         assert db == mock_db

# def test_close_mongodb_client():
#     mock_client = MagicMock()
#     with patch("line_bot.db.mongodb.client", mock_client):
#         mongodb.close_mongodb_client()
#         mock_client.close.assert_called_once()
=======
>>>>>>> fed8e10df94937b7d798f9dbd6602bbda1e2c234
