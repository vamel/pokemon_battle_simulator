from pokemon_team import PokemonTeam
from pokemon_class import Pokemon

class TestPokemon(Pokemon):
    def __init__(self, name, hp=100, attack=20, defense=30, special_attack=25, special_defense=30, speed=50, ID=1, types=["Grass", "Ground"]):
        super().__init__(name, hp, attack, defense, special_attack, special_defense, speed, ID, *types)

p1 = TestPokemon("p1")
p2 = TestPokemon("p2")
p3 = TestPokemon("p3")
p4 = TestPokemon("p4")
p5 = TestPokemon("p5")
p6 = TestPokemon("p6")
p7 = TestPokemon("p7")
p8 = TestPokemon("p8")

def test_empty_init_list():
    team1 = PokemonTeam()
    assert team1.get_party() == []
    assert team1.get_amount() == 0
    assert team1.show_party() == ""
    assert bool(team1) == False

team = PokemonTeam([p1, p2, p3, p4])

def test_init_list():
    assert len(team.get_party()) == 4
    assert team.get_amount() == 4
    assert team.get_first().name == "P1"
    assert team.show_party() == "P1 P2 P3 P4 "
    assert bool(team) == True

def test_remove_from_party():
    team1 = PokemonTeam([p1, p2, p3, p4])
    team1.remove_from_party(p1)
    assert team1.get_amount() == 3
    assert team1.get_first().name == "P2"
    assert team1.show_party() == "P2 P3 P4 "

def test_stat_reset():
    team1 = PokemonTeam([p1, p2, p3, p4])
    team1.get_first().raise_defense()
    assert team1.get_first().name == "P1"
    assert team1.get_first().defense() == 37
    team1.swap_pokemons(0, 1)
    assert team1.get_pokemon(1).defense() == 30
    assert team1.get_pokemon(1).name == "P1"
    assert team1.get_first().name == "P2"

def test_add_to_party():
    team1 = PokemonTeam([p1, p2, p3, p4])
    team1.add_to_party(p5)
    assert len(team1) == 5
    assert team1.get_pokemon(4).name == "P5"