from ollama import chat, ChatResponse

class LLMService:
  def question(self, query: str, context: str):
    system_prompt = (
      "You are a document Q&A assistant.\n"
      "Rules:\n"
      "- Use ONLY the provided CONTEXT.\n"
      "- If the answer is not explicitly in the CONTEXT, reply exactly: Not found in document.\n"
      "- Be concise and direct.\n"
      "- Do NOT mention the context, retrieval, embeddings, or sources.\n"
    )

    user_prompt = (
      f"QUESTION:\n{query}\n\n"
      "CONTEXT:\n"
      "<<<CONTEXT_START>>>\n"
      f"{context}\n"
      "<<<CONTEXT_END>>>\n"
    )

    response: ChatResponse = chat(
      model='qwen2.5:7b',
      messages=[
      {'role': 'system', 'content': system_prompt},
      {'role': 'user','content': user_prompt }
      ],
      options={
        "temperature": 0.2,
        "top_p": 0.9,
        "num_predict": 220
      }
    )

    return response['message']['content']