SHELL := /bin/zsh

MINIMALDOC_VERSION ?= latest
TOOLS_DIR := ./.tools
BIN_DIR := $(TOOLS_DIR)/bin
MINIMALDOC := $(BIN_DIR)/minimaldoc
DOCS_DIR := ./docs
DIST_DIR := ./.build/site
PORT ?= 4173
BASE_URL ?= http://localhost:$(PORT)

.DEFAULT_GOAL := preview

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
	$(MINIMALDOC) build $(DOCS_DIR) --base-url $(BASE_URL) --output $(DIST_DIR)

serve: build
	cd $(DIST_DIR) && python3 -m http.server $(PORT)

view:
	open http://localhost:$(PORT)

preview: build
	cd $(DIST_DIR) && python3 -m http.server $(PORT) & sleep 1 && open http://localhost:$(PORT) && wait

clean:
	rm -rf ./.build

clean-all: clean
	rm -rf ./.tools

doctor:
	@echo "Go: $$(command -v go || echo missing)"
	@echo "MinimalDoc in repo: $$(test -x $(MINIMALDOC) && echo $(MINIMALDOC) || echo missing)"
	@echo "Docs source: $(DOCS_DIR)"
	@echo "Build output: $(DIST_DIR)"
