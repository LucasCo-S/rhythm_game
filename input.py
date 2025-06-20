import queue

hit_pos = 700
class Input: 
    def __init__(self, key: int, start: float, end: float):
        self.key = key
        self.start = start
        self.end = end
        self.duration = end - start
        self.type_event = None
        self.hitbox = hit_pos
        self.reached = False
        
    def classify_input(self, time_pressed: float = 300):
        if self.duration < time_pressed: self.type_event = "#TAP"
        else: self.type_event = "#HOLD"

def input_listen(input_data: queue.Queue, input_info: queue.Queue):
    while True:
        while not input_data.empty():
            key, start, end = input_data.get()

            input = Input(key, start, end)
            input.classify_input()

            #resultado(input)
            input_info.put(input)

def resultado(input: Input):
    print(f"Tecla: {input.key}, Tipo: {input.type_event}, Começo/Fim: {input.start}/{input.end}, Duração: {input.duration}")