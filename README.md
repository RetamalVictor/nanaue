# Nanaue

A private collection of experiments.

Name is inspired by King Shark announcing _bird_ to the squad.

## Running the experiments

1. Install [Poetry](https://python-poetry.org/docs/)
2. Clone and cd into this repo, then run `poetry install`

Now to run e.g. the `flocking.py` experiment, you can run:

```bash
poetry run python nanaue/flocking.py
```

### Flocking LIVE

A bird flocking experiment with config settings that you can adjust on-the-fly!

Key mapping:
- `1`: select the alignment weight
- `2`: select the cohesion weight
- `3`: select the separation weight
- `arrow up`: increase the selected weight by 0.1
- `arrow down`: decrease the selected weight by 0.1