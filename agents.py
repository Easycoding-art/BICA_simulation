from huggingface_hub import InferenceClient
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

class GemmaAgent() :
    def __init__(self, key) :
        self.client = InferenceClient(api_key=key)
    def query(self, system_prompt, user_prompt) :
        messages = [
            { "role": "user", "content": user_prompt },
            { "role": "system", "content": system_prompt }
            ]
        output = self.client.chat.completions.create(
        model="google/gemma-1.1-7b-it",
        messages=messages, 
        stream=True, 
        temperature=0.5,
        max_tokens=2000,
        top_p=0.7
        )
        result = []
        for chunk in output:
            result.append(chunk.choices[0].delta.content)
        return ''.join(result)

class GigaChatAgent() :
    def __init__(self, key) :
        self.llm = GigaChat(
            credentials=key,
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            # Отключает проверку наличия сертификатов НУЦ Минцифры
            verify_ssl_certs=False,
            streaming=False,
            temperature=0.5
        )
    def query(self, system_prompt, user_prompt) :
        message = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        res = self.llm.invoke(message)
        return res.content

class GigaChatProAgent() :
    def __init__(self, key) :
        self.llm = GigaChat(
            credentials=key,
            scope="GIGACHAT_API_PERS",
            model="GigaChat-Pro",
            # Отключает проверку наличия сертификатов НУЦ Минцифры
            verify_ssl_certs=False,
            streaming=False,
            temperature=0.5
        )
    def query(self, system_prompt, user_prompt) :
        message = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        res = self.llm.invoke(message)
        return res.content
    
class UserAgent() :
    def __init__(self, key) :
        self.__unstruction_showed = False
    def query(self, system_prompt, user_prompt) :
        if not self.__unstruction_showed :
            print(system_prompt)
            self.__unstruction_showed = True
        print(user_prompt)
        res = input('Print your sentence: ')
        return res