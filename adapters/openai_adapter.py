from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    """
    將文字轉換為向量嵌入
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[text]
    )
    return response.data[0].embedding

def generate_answer_from_matches(matches, query: str) -> str:
    """
    將 matches 內容組合成 context，再送入 GPT 生成回覆
    """
    context = "\n\n".join([m["metadata"]["answer"] for m in matches])
    prompt = f"根據以下資料回答問題：\n{context}\n\n問題：{query}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
