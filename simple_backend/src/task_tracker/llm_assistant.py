import requests



class LLMAssistant:

    def __init__(self, api_token: str, account_id: str, model: str = "@cf/meta/llama-3-8b-instruct"): 
        self.api_token = api_token
        self.account_id = account_id
        self.model = model

        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def task_llm(self, task_text: str) -> str:
        input = {"messages": [
            {"role": "system", 
             "content": f"Напиши короткое решение задачи (до 150 символов): {task_text}"}
        ]}
        response = requests.post(f"{self.base_url}{self.model}", headers=self.headers, json=input)
        if response.status_code == 200:
            return response.json().get("result", {}).get("response", "")
        return f"Ошибка LLM: {response.status_code} {response.text}"