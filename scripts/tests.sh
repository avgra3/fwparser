#!/bin/bash

uv run pytest tests --ignore-glob="bench/*.py"
