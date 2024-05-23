# Python exploration
the objective of this repository is to explore mecanism through python.
All tests generate markdown documentation to help visualize.

* exploring [JSON serialisation, filtering and sorting list, object extanding](documentation/test_json_pokemon-tcg-sdk-python.md)
  * it explore [pokémons card from pokemon-tcg-data](https://github.com/PokemonTCG/pokemon-tcg-data), it require `pip install pokemontcgsdk`
  * it show mapping informations from json data to python object using `from_dict()` from `dacite`
  * it show object extanding (extanding `Card` with object `CardExtanded` to map additional informations)
  * it show filtering and sorting list through object attribute



## requirement
`pip install -U pytest`