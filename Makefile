PKL ?= pkl
DOCKER ?= docker
CONFIG ?= examples/deployment.pkl
OUT ?= out
VERSION ?= 0.1.0

.PHONY: render test validate package
render:
	@mkdir -p "$(OUT)"
	@$(PKL) eval -o "$(OUT)/deployment.yaml" "$(CONFIG)"

test:
	@python3 -m unittest discover -s tests -v

validate: render test
	@$(DOCKER) compose -f "$(OUT)/deployment.yaml" config -q
	@echo "whisper.cpp configuration validation succeeded."

package:
	@PKL_PACKAGE_VERSION="$(VERSION)" $(PKL) project package --output-path dist
