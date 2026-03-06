# Contributing to FinNutriAgent

Thank you for your interest in contributing. This document outlines how to contribute effectively.

---

## Ways to Contribute

- **Bug reports** — Open a [GitHub Issue](https://github.com/aliakarma/FinNutriAgent/issues) describing the problem, your environment, and steps to reproduce.
- **Feature requests** — Open an Issue with the label `enhancement`.
- **Documentation** — Improve docstrings, README, or dataset documentation.
- **Code contributions** — Submit a Pull Request following the guidelines below.
- **Dataset extensions** — Propose new food items, regions, or nutritional attributes via an Issue.

---

## Development Setup

```bash
git clone https://github.com/aliakarma/FinNutriAgent.git
cd FinNutriAgent

# pip
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
# install dependencies (for reproducible results we recommend the lockfile)
pip install -r requirements.lock.txt

# or Conda
conda env create -f environment.yml
conda activate finnutriagent
```

---

## Pull Request Process

1. Fork the repository and create a branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make focused, well-described commits.
3. Ensure all tests pass:
   ```bash
   pytest tests/ -v --cov=scripts
   ```
4. Validate data integrity if any CSV files were modified:
   ```bash
   python scripts/validate_data.py
   ```
5. Update relevant documentation.
6. Submit a Pull Request with a clear description of the change and its motivation.

---

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Include docstrings (NumPy style) for all public functions and classes.
- Use type hints.
- Keep functions focused and under 60 lines where reasonable.

---

## Dataset Contributions

- Ensure new food IDs are consistent across `food_composition.csv` and `food_prices.csv`.
- Validate halal labels against a credible source.
- Update `docs/data_card.md` and `docs/dataset_documentation.md` accordingly.
- Run `python scripts/validate_data.py` before submitting.

---

## Licensing

By contributing, you agree that:
- Code contributions are licensed under the **MIT License**.
- Data and documentation contributions are licensed under **CC BY 4.0**.

---

## Code of Conduct

Contributors are expected to maintain a respectful, inclusive environment. Harassment of any kind will not be tolerated.
