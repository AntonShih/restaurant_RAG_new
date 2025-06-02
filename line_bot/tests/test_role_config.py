import pytest
from config.role_config import ROLE_ACCESS_LEVEL, ROLE_TEXT_MAP

def test_role_access_structure():
    for role, level in ROLE_ACCESS_LEVEL.items():
        assert isinstance(role, str)
        assert isinstance(level, int)

def test_access_levels_are_unique():
    levels = list(ROLE_ACCESS_LEVEL.values())
    assert len(levels) == len(set(levels)), "access_level 有重複"

def test_text_map_matches_access_roles():
    for role_key in ROLE_TEXT_MAP:
        assert role_key in ROLE_ACCESS_LEVEL, f"{role_key} 在 ROLE_TEXT_MAP 裡，但不在 ROLE_ACCESS_LEVEL 裡"
