from random import randint
import requests
import threading
import time
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer
        self.last_feed_time = datetime.now()   
        self.age = 0 
        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.birth_date = datetime.now()
        self.hp = randint(800, 1100)
        self.power = randint(100, 200)
        Pokemon.pokemons[pokemon_trainer] = self

    
    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']['front_default']
        else:
            return "Pikachu"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"


    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name}\nВозраст: {self.age} лет hp: {self.hp} power: {self.power}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    # Метода класса для увеличивает возраст
    def add_year(self):
        self.age += 1
        print(f"{self.name} стал старше! Теперь ему {self.age} лет.")

    # Функция для увеличения возраста всех покемонов
    def age_updater():
        while True:
            time.sleep(60)  
            for trainer, pokemon in Pokemon.pokemons.items():
                pokemon.add_year()

    age_thread = threading.Thread(target=age_updater, daemon=True)
    age_thread.start()

    # Логика аттаки
    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer} осталось HP {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "
        
    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = timedelta(seconds=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}"
        
class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp -= randint(100, 200)
        self.power += randint(100, 200)
        self.name += 'Fighter'

    def attack(self, enemy):
        bonus = randint(-200, 500)
        self.power += bonus
        super().attack

class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp -= randint(100, 200)
        self.power += randint(50, 100)
        self.name += 'Wizard'