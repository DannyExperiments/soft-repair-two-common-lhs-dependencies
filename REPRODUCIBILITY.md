# Reproducibility

Run from the repository root using Python 3.9 or newer. The replay uses the Python standard library and exact integers.

```sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
```

Compare with [the checked log](verification/logs/replay.txt). The proof applies to arbitrary finite relations in the named model. The explorer evaluates the eight-fact worked case. [PDF build](paper/BUILD.md) · [Visualization build](visualization/README.md)
