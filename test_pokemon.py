import pytest
from pokemon_class import Pokemon

class TestPokemon(Pokemon):
    def __init__(self, name, hp, attack, defense, special_attack, special_defense, speed, ID, *types):
        super().__init__(name, hp, attack, defense, special_attack, special_defense, speed, ID, *types)

name = "Test"
special_pok_name = "Shedinja"
hp = 100
atk = 10
defense = 20
spatk = 15
spdef = 10
speed = 40
u_id = 1
types = ['Grass']

P = TestPokemon(name, hp, atk, defense, spatk, spdef, speed, u_id, types)

def test_name():
    assert P.name == name
    assert str(P) == "Test"

def test_hp(monkeypatch):
    P = TestPokemon(name, hp, atk, defense, spatk, spdef, speed, u_id, types)
    def mockreturn():
        return 318

    monkeypatch.setattr(P, 'hp', mockreturn)
    x = P.hp()
    assert x == 318

def test_max_hp(monkeypatch):
    P = TestPokemon(name, hp, atk, defense, spatk, spdef, speed, u_id, types)
    def mockreturn():
        return 318

    monkeypatch.setattr(P, 'max_hp', mockreturn)
    x = P.max_hp()
    assert x == 318

def test_defense():
    assert P.defense() == 20

def test_spatk():
    assert P.special_attack() == 15

def test_spdef():
    assert P.special_defense() == 10

def test_speed():
    assert P.speed() == 40

def test_types():
    assert len(P.types()) == 1
    assert P.types() == ['Grass']

def test_id():
    assert P.id() == 1

def test_raise_defense():
    P1 = TestPokemon(name, hp, atk, defense, spatk, spdef, speed, u_id, types)
    P1.raise_defense()
    assert P1.defense() == 25
    assert P1.special_defense() == 12
    P1.reset_stat_changes()
    assert P1.defense() == 20
    assert P1.special_defense() == 10

def receive_damage():
    P1 = TestPokemon(name, hp, atk, defense, spatk, spdef, speed, u_id, types)
    P2 = TestPokemon(name, hp, atk, defense, spatk, spdef, speed, u_id, types)
    P1.receive_normal_damage(0)
    assert P1.hp() == P1.max_hp()
    P2.receive_special_damage(0)
    assert P2.hp() == P2.max_hp()
    P1.receive_normal_damage(100)       # minimum damage dealt is 170
    assert P1.hp() == 0
    P2.receive_special_damage(100)      # minimum damage dealt is 340
    assert P2.hp() == 0

def test_shedinja():
    Shedinja = TestPokemon('Shedinja', 1100, 50, 20, 10, 10, 100, 2, ['Bug', 'Ghost'])
    Shedinja2 = TestPokemon('Shedinja', 1100, 50, 20, 10, 10, 100, 2, ['Bug', 'Ghost'])
    assert Shedinja.name == 'Shedinja'
    assert Shedinja.hp() == 1
    assert Shedinja.max_hp() == 1
    assert Shedinja.types() == ['Bug', 'Ghost']
    assert len(Shedinja.types()) == 2
    Shedinja.receive_normal_damage(1)
    Shedinja2.receive_special_damage(1)
    assert Shedinja.hp() == 0
    assert Shedinja2.hp() == 0