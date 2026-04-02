SHELL := /bin/zsh

MINIMALDOC_VERSION ?= latest
TOOLS_DIR := ./.tools
BIN_DIR := $(TOOLS_DIR)/bin
MINIMALDOC := $(BIN_DIR)/minimaldoc
DOCS_DIR := ./docs
BUILD_DOCS_DIR := ./.build/docs
DIST_DIR := ./.build/site
PORT ?= 4173
BASE_URL ?= http://localhost:$(PORT)

.DEFAULT_GOAL := build

.PHONY: install build serve view preview clean clean-all doctor

$(MINIMALDOC):
	@mkdir -p $(BIN_DIR)
	@if test -x "$(MINIMALDOC)"; then \
		echo "Using existing MinimalDoc at $(MINIMALDOC)"; \
	elif command -v go >/dev/null 2>&1; then \
		echo "Installing MinimalDoc locally via go install..."; \
		GOBIN="$(abspath $(BIN_DIR))" go install github.com/studiowebux/minimaldoc/cmd/minimaldoc@$(MINIMALDOC_VERSION) || { \
			echo ""; \
			echo "Failed to install MinimalDoc."; \
			echo "If you are offline, reconnect and run 'make install' again."; \
			exit 1; \
		}; \
	else \
		echo "MinimalDoc was not found."; \
		echo "Install Go and run 'make install'."; \
		exit 1; \
	fi

install:
	@rm -f "$(MINIMALDOC)"
	@$(MAKE) $(MINIMALDOC)
	@echo "Installed MinimalDoc to $(MINIMALDOC)"

build: $(MINIMALDOC)
	python3 ./scripts/prepare_build_docs.py $(DOCS_DIR) $(BUILD_DOCS_DIR)
	$(MINIMALDOC) build $(BUILD_DOCS_DIR) --base-url $(BASE_URL) --output $(DIST_DIR)
	mkdir -p $(DIST_DIR)/brand
	cp $(BUILD_DOCS_DIR)/brand/* $(DIST_DIR)/brand/
	mkdir -p $(DIST_DIR)/img
	cp $(BUILD_DOCS_DIR)/img/* $(DIST_DIR)/img/
	cp $(BUILD_DOCS_DIR)/site.webmanifest $(DIST_DIR)/site.webmanifest
	python3 ./scripts/postprocess_landing.py $(DIST_DIR)

serve: build
	cd $(DIST_DIR) && python3 -m http.server $(PORT)

view:
	cd $(DIST_DIR) && { \
		python3 -m http.server $(PORT) & \
		server_pid=$$!; \
		trap 'kill $$server_pid 2>/dev/null || true' INT TERM EXIT; \
		sleep 1; \
		open http://localhost:$(PORT); \
		wait $$server_pid; \
	}

preview:
	@echo "Use 'make' to build the site."
	@echo "Use 'make view' to serve the built site and open http://localhost:$(PORT)."

clean:
	rm -rf ./.build

clean-all: clean
	rm -rf ./.tools

doctor:
	@echo "Go: $$(command -v go || echo missing)"
	@echo "MinimalDoc in repo: $$(test -x $(MINIMALDOC) && echo $(MINIMALDOC) || echo missing)"
	@echo "Docs source: $(DOCS_DIR)"
	@echo "Prepared docs: $(BUILD_DOCS_DIR)"
	@echo "Build output: $(DIST_DIR)"
