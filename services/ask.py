from ollama import chat, ChatResponse

class Ask:
  def question(self, query, context):
    response: ChatResponse = chat(model='qwen2.5:7b', messages=[
      {
        'role': 'user',
        'content': "with context:" + context + " | Tell me " + query 
      }
    ])

    return response['message']['content']