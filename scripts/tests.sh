#!/bin/bash

uv run pytest tests --ignore-glob="*/test_large_dataset.py"
