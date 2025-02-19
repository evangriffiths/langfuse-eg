# langfuse-eg

An example for demo-ing langfuse

## Setup

```bash
# Install deps
python3.12 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install

# Populate .env file with required keys
cp .env.example .env
```

## Run

```bash
python langfuse_eg/main.py
```

Now see the new trace in https://cloud.langfuse.com/ -> Tracing -> Traces
