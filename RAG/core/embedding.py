import openai


def embed_faq_list_batch(faq_list):
    result = []
    for item in faq_list:
        response = openai.embeddings.create(
            input=item["question"],
            model="text-embedding-3-small"
        )
        item["embedding"] = response.data[0].embedding
        result.append(item)
    return result
