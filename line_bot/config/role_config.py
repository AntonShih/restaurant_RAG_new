# 每種角色對應的權限等級
ROLE_ACCESS_LEVEL = {
    "normal": 1,
    "reserve": 2,
    "leader": 3,
    "vice_manager": 4,
    "manager": 5,
    "guest": 0
}

# 每種角色的中文對照（UI 顯示用）
ROLE_TEXT_MAP= {
    "normal": "一般職員",
    "reserve": "儲備幹部",
    "leader": "組長",
    "vice_manager": "副店長",
    "manager": "店長",
    "guest": "訪客"
}

# 中文職位對應英文角色 key
ROLE_KEY_MAP = {
    "店長": "manager",
    "副店長": "vice_manager",
    "組長": "leader",
    "儲備幹部": "reserve",
    "一般職員": "normal",
    "訪客": "guest"
}
