.PHONY: help install install-dev run lint format check clean

PYTHON := python3
PIP := $(PYTHON) -m pip

help: ## Tampilkan daftar perintah yang tersedia
	@echo "Perintah yang tersedia:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies produksi
	$(PIP) install -r requirements.txt

install-dev: ## Install dependencies produksi + development
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 isort mypy

run: ## Jalankan bot Telegram
	$(PYTHON) -m src.bot

lint: ## Cek kualitas kode dengan flake8
	$(PYTHON) -m flake8 src/

format: ## Format kode dengan black dan isort
	$(PYTHON) -m black src/
	$(PYTHON) -m isort src/

check: ## Cek format tanpa mengubah file (untuk CI)
	$(PYTHON) -m black --check src/
	$(PYTHON) -m isort --check-only src/
	$(PYTHON) -m flake8 src/

clean: ## Bersihkan file cache dan temporary
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

