import pytest
from unittest.mock import MagicMock, patch
from line_bot.services import user_service

@pytest.fixture
def mock_collection():
    return MagicMock()

@patch("line_bot.services.user_service.get_db")
def test_save_user_role(mock_get_db, mock_collection):
    mock_get_db.return_value = {"user_roles": mock_collection}
    mock_collection.update_one.return_value.acknowledged = True

    result = user_service.save_user_role("test_user", "店長")
    assert result is True

    mock_collection.update_one.assert_called_once()
    args, kwargs = mock_collection.update_one.call_args
    assert args[0] == {"user_id": "test_user"}
    assert "$set" in args[1]
    assert kwargs["upsert"] is True

@patch("line_bot.services.user_service.get_db")
def test_get_user_role_found(mock_get_db, mock_collection):
    expected_user = {"user_id": "test_user", "role": "店長", "access_level": 3}
    mock_collection.find_one.return_value = expected_user
    mock_get_db.return_value = {"user_roles": mock_collection}

    result = user_service.get_user_role("test_user")
    assert result == expected_user

@patch("line_bot.services.user_service.get_db")
def test_get_user_role_not_found(mock_get_db, mock_collection):
    mock_collection.find_one.return_value = None
    mock_get_db.return_value = {"user_roles": mock_collection}

    result = user_service.get_user_role("unknown_user")
    assert result is None
<<<<<<< HEAD
# # ----------------------------------------------------------------------------------------------------
# import pytest
# from unittest.mock import AsyncMock, patch
# from line_bot.services import user_service

# @pytest.mark.asyncio
# @patch("line_bot.services.user_service.get_db")
# async def test_save_user_role(mock_get_db):
#     mock_collection = AsyncMock()
#     mock_collection.update_one.return_value.acknowledged = True
#     mock_get_db.return_value = {"user_roles": mock_collection}

#     result = await user_service.save_user_role("test_user", "店長")
#     assert result is True

#     mock_collection.update_one.assert_called_once()
#     args, kwargs = mock_collection.update_one.call_args
#     assert args[0] == {"user_id": "test_user"}
#     assert "$set" in args[1]
#     assert kwargs["upsert"] is True

# @pytest.mark.asyncio
# @patch("line_bot.services.user_service.get_db")
# async def test_get_user_role_found(mock_get_db):
#     expected_user = {"user_id": "test_user", "role": "店長", "access_level": 3}
#     mock_collection = AsyncMock()
#     mock_collection.find_one.return_value = expected_user
#     mock_get_db.return_value = {"user_roles": mock_collection}

#     result = await user_service.get_user_role("test_user")
#     assert result == expected_user

# @pytest.mark.asyncio
# @patch("line_bot.services.user_service.get_db")
# async def test_get_user_role_not_found(mock_get_db):
#     mock_collection = AsyncMock()
#     mock_collection.find_one.return_value = None
#     mock_get_db.return_value = {"user_roles": mock_collection}

#     result = await user_service.get_user_role("unknown_user")
#     assert result is None
=======
>>>>>>> fed8e10df94937b7d798f9dbd6602bbda1e2c234
