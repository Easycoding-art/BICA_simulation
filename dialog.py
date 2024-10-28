import random

class Agent() :
    def __init__(self, llm_pylot, name, task_file_path, character_file_path):
        self.__pylot = llm_pylot
        self.agent_name = name
        with open(task_file_path, 'r') as f1 :
            task = f1.read()
        with open(character_file_path, 'r') as f2 :
            character = f2.read()
        #подумать над промтом
        self.__system_promt = f'name: {self.agent_name}; task: {task};\ncharacter: {character}'

    def get_name(self) :
        return self.agent_name
    
    def speak(self, query_text) :
        return self.__pylot.query(self.__system_promt, query_text)

class Dialog() :
    def __init__(self, experiment_name, character_arr):
        self.__experiment_name = experiment_name
        self.__characters = {character.get_name() : character for character in character_arr}
        self.__character_names = self.__characters.keys()
        self.__dialog_field = ''
        self.__dialog_continue = [True] * len(self.__character_names)

    def __iteration(self, queue) :
        for name in queue :
            speaker = self.__characters.get(name)
            answer = speaker.speak(self.__dialog_field)
            self.__dialog_field+=f'\n{name}: {answer}'
        self.__break_discussion()

    def __break_discussion(self) :
        #Подобрать нормальный промт
        promt = 'Print True if you want to continue dialog and False if not'
        for name in self.__character_names :
            speaker = self.__characters.get(name)
            answer = speaker.speak(promt)
            self.__dialog_continue[self.__character_names.index(name)] = bool(answer)

    def dialog_cycle(self) :
        initiator = random.choice(self.__character_names)
        answer = initiator.speak(self.__dialog_field)
        self.__dialog_field = f'{initiator}: {answer}'
        other = self.__character_names - [initiator]
        for name in other :
            speaker = self.__characters.get(name)
            answer = speaker.speak(self.__dialog_field)
            self.__dialog_field+=f'\n{name}: {answer}'
        while all(self.__dialog_continue) :
            random.shuffle(self.__character_names)
            queue = self.__character_names#подумать как еще можно определить очередность
            self.__iteration(queue)
        with open(f'{self.__experiment_name}.txt', 'w') as f :
            f.write(self.__dialog_field)
        #Подобрать нормальный промт
        promt = 'Your opinion about your dialogmates'
        for name in self.__character_names :
            speaker = self.__characters.get(name)
            answer = speaker.speak(promt)
            with open(f'{self.__experiment_name}_{name}.txt', 'w') as f :
                f.write(answer)