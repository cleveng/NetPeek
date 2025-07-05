# NetPeek

```bash
uv venv
uv pip sync pyproject.toml

uv pip install psutil
uv pip freeze > requirements.txt
uv pip install -r requirements.txt

uv add -r requirements.txt
uv run main.py
```

## build \*.exe

```bash
uv pip install pyinstaller
pyinstaller --clean --noconsole --onefile main.py
```
