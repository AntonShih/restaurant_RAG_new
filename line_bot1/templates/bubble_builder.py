# line_bot1/templates/bubble_builder.py

def generate_flex_answer_bubble(user_query: str, gpt_answer: str, matches: list) -> dict:
    """
    將使用者提問 + GPT 回答 + 來源 matches 整合成 LINE Flex Bubble 格式。
    """
    source_texts = []
    for i, m in enumerate(matches[:3], 1):
        q = m["metadata"].get("question", "（未提供）")
        cat = m["metadata"].get("category", "未分類")
        lvl = m["metadata"].get("access_level", "?")
        updated = m["metadata"].get("last_updated")
        line = f"{i}️⃣ 「{q}」｜分類：{cat}｜等級：{lvl}"
        if updated:
            line += f"｜更新：{updated}"
        source_texts.append({
            "type": "text",
            "text": line,
            "wrap": True,
            "size": "xs",
            "color": "#777777"
        })
# 保底處理（若沒有任何匹配資料）
    if not source_texts:
        source_texts.append({
            "type": "text",
            "text": "（查無相關資料）",
            "wrap": True,
            "size": "xs",
            "color": "#AAAAAA"
        })

    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "📘 AI 知識回覆", "weight": "bold", "size": "xl", "color": "#1DB446"},
                {"type": "text", "text": f"🔍 問題：「{user_query}」", "wrap": True, "size": "sm", "color": "#333333"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": "💡 回答摘要", "weight": "bold", "size": "md"},
                        {"type": "text", "text": gpt_answer, "wrap": True, "size": "sm", "color": "#555555"}
                    ]
                },
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "📚 資料來源", "weight": "bold", "size": "md", "margin": "md"},
                {"type": "box", "layout": "vertical", "spacing": "xs", "contents": source_texts},
                {
                    "type": "text",
                    "text": "🛡 注意：實際操作請依照現場主管或最新 SOP 為準。",
                    "wrap": True,
                    "size": "xs",
                    "color": "#AAAAAA",
                    "margin": "md"
                }
            ]
        }
    }
