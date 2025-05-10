from linebot.models import FlexSendMessage

flex_message = FlexSendMessage(
    alt_text="這是 Flex Message",
    contents={
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "倒垃圾流程",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": "請於每日 22:30 前清出內場，23:00 前集中至後場。",
                    "wrap": True,
                    "margin": "md",
                    "size": "sm",
                    "color": "#666666"
                }
            ]
        }
    }
)

line_bot_api.reply_message(event.reply_token, flex_message)


{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "今日任務",
        "weight": "bold",
        "size": "lg"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "✔ 倒垃圾"
          },
          {
            "type": "text",
            "text": "✔ 補冰箱"
          },
          {
            "type": "text",
            "text": "✔ 刷地"
          }
        ],
        "spacing": "sm",
        "margin": "md"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "action": {
          "type": "message",
          "label": "我完成了",
          "text": "我完成了今日任務"
        }
      }
    ]
  }
}
