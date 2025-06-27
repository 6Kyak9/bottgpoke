from random import randint
import requests
import threading
import time
from datetime import datetime

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   
        self.age = 0 
        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.birth_date = datetime.now()

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
        return f"Имя твоего покемона: {self.name}\nВозраст: {self.age} лет"

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
