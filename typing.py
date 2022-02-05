import json

TypeList = []

class Typing:
    def __init__(self, name, resistances, weaknesses, immunities):
        self.name = name
        self.immunities = immunities
        self.resistances = resistances
        self.weaknesses = weaknesses
        self.append()

    def resistances(self, *res):
        self.resistances = res
        return self.resistances

    def weaknesses(self, *weak):
        self.weaknesses = weak
        return self.weaknesses
    
    def append(self):
        TypeList.append(self)

class database:
    def __init__(self):
        self.type = TypeList

    def save_to_json(self):
        type_data = []
        for typing in self.type:
            typ = {}
            typ['Name'] = typing.name
            typ['Resistances'] = typing.resistances
            typ['Weaknesses'] = typing.weaknesses
            typ['Immunities'] = typing.immunities
            type_data.append(typ)
        
        with open('typings.json', 'w') as f:
            f.write(json.dumps(type_data, indent=4))

Normal = Typing('Normal', "None", 'Fighting', 'Ghost')
Ghost = Typing('Ghost', ['Poison', 'Bug'], ['Ghost', 'Dark'], ['Normal', 'Fighting'])
Fighting = Typing('Fighting', ['Rock', 'Bug', 'Dark'], ['Flying', 'Fairy', 'Psychic'], "None")
Flying = Typing('Flying', ['Fighting', 'Grass', 'Bug'], ['Rock', 'Electric', 'Ice'], 'Ground')
Poison = Typing('Poison', ['Fighting', 'Grass', 'Bug', 'Poison', 'Fairy'], ['Ground', 'Psychic'], "None")
Ground = Typing('Ground', ['Poison', 'Rock'], ['Water', 'Grass', 'Ice'], 'Electric')
Rock = Typing('Rock', ['Normal', 'Flying', 'Poison', 'Fire'], ['Fighting', 'Ground', 'Steel', 'Water', 'Grass'], "None")
Bug = Typing('Bug', ['Fighting', 'Ground', 'Grass'], ['Flying', 'Rock', 'Fire'], "None")
Steel = Typing('Steel', ['Normal', 'Flying', 'Steel', 'Bug', 'Rock', 'Grass', 'Psychic', 'Ice', 'Dragon', 'Fairy'], ['Fighting', 'Fire', 'Ground'], 'Poison')
Fire = Typing('Fire', ['Bug', 'Steel', 'Fire', 'Grass', 'Ice', 'Fairy'], ['Ground', 'Rock', 'Water'], "None")
Water = Typing('Water', ['Steel', 'Fire', 'Ice', 'Water'], ['Grass', 'Electric'], "None")
Grass = Typing('Grass', ['Ground', 'Water', 'Grass', 'Electric'], ['Flying', 'Poison', 'Bug', 'Ice', 'Fire'], "None")
Electric = Typing('Electric', ['Flying', 'Steel'], 'Ground', "None")
Psychic = Typing('Psychic', ['Psychic', 'Fighting'], ['Bug', 'Ghost', 'Dark'], "None")
Ice = Typing('Ice', 'Ice', ['Fighting', 'Rock', 'Steel', 'Fire'], "None")
Dragon = Typing('Dragon', ['Fire', 'Water', 'Grass', 'Electric'], ['Ice', 'Dragon', 'Fairy'], "None")
Dark = Typing('Dark', ['Dark', 'Psychic'], ['Fighting', 'Bug', 'Fairy'], 'Psychic')
Fairy = Typing('Fairy', ['Fighting', 'Bug', 'Dark'], ['Poison', 'Steel'], 'Dragon')

Database = database()
Database.save_to_json()