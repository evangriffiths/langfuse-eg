# langfuse-eg

An example for demo-ing langfuse

See https://github.com/evangriffiths/langfuse-eg/commit/19b13d7ade19e02c0aefc25b7a88c61e0dbd8269 for the diff to add langfuse tracing to main.py

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
