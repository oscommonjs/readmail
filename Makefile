# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/readmail
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

PROGRAM_NAME = readmail
readmail_LINTER_EXPORT_PATH ?= lint_output.txt

# path to installation record that gets written when performing:
# - make build

INSTALLED_FILES_RECORD := ./installed_files.txt

# invoke the specific executable command

PYTHON3  := $(shell command -v python3    2> /dev/null)
DANGER   := $(shell command -v danger     2> /dev/null)
GEM      := $(shell command -v gem        2> /dev/null)
FIND     := $(shell command -v find       2> /dev/null)
RM       := $(shell command -v rm         2> /dev/null)
WHICH    := $(shell command -v which      2> /dev/null)
XARGS    := $(shell command -v xargs      2> /dev/null)
PRINTF   := $(shell command -v printf     2> /dev/null)
TOUCH    := $(shell command -v touch      2> /dev/null)
CP       := $(shell command -v cp         2> /dev/null)
CAT      := $(shell command -v cat        2> /dev/null)
PIP3     := $(shell command -v pip3       2> /dev/null)
UNAME    := $(shell command -v uname      2> /dev/null)
EXIT     := $(shell command -v exit       2> /dev/null)
TPUT     := $(shell command -v tput       2> /dev/null)
TR       := $(shell command -v tr         2> /dev/null)
PYLINT   := $(shell command -v pylint     2> /dev/null)

SYSTEM := $(shell $(UNAME) -s)
ifeq ($(SYSTEM),Darwin)
	USER_FLAG := --user
else
	USER_FLAG :=
endif

TERM_COLUMNS := `$(TPUT) cols`
DISPLAY_SEPARATOR := $(PRINTF) "%*.s\n" $(TERM_COLUMNS) " " | $(TR) ' ' '='

# Targets

# ---

checkfor = @$(PRINTF) "Checking for $1..."; \
if [ -z `$(WHICH) $1` ]; then \
	$(PRINTF) " no\n"; \
	$(EXIT) 1;\
else \
	$(PRINTF) " yes\n"; \
fi

check:
	$(call checkfor, python3)
	$(call checkfor, pip3)
	$(call checkfor, pylint)
	$(call checkfor, gem)
	$(call checkfor, danger)
	@$(DISPLAY_SEPARATOR)

# ---

install-deps:
	$(PIP3) -r dependencies.txt
	$(GEM) install bundler $(USER_FLAG)
	@$(DISPLAY_SEPARATOR)

# ---

# this is for installing any tools that we don't already have

install-tools: check
	@$(PRINTF) "Installing git hooks..."
	@$(PYTHON3) ./tools/hooks-config.py
	@$(PRINTF) " done!\n"
	@$(DISPLAY_SEPARATOR)

# ---

removeall = $(RM) -rRf
cleanlocation = @$(FIND) $1 $2 -print0 | $(XARGS) -0 $(removeall)

clean: check
	@$(PRINTF) "Removing existing installation... "
	@$(TOUCH) $(INSTALLED_FILES_RECORD)
	@$(CAT) $(INSTALLED_FILES_RECORD) | $(XARGS) $(removeall)
	@$(removeall) ./*.egg-info
	@$(removeall) ./build
	@$(removeall) ./dist
	@$(removeall) ./.eggs
	@$(removeall) $(value $(PROGRAM_NAME)_LINTER_EXPORT_PATH)
	$(call cleanlocation, ., -name ".DS_Store")
	$(call cleanlocation, ., -name "*.pyc")
	$(call cleanlocation, ., -name "__pycache__" -type d)
	@$(PRINTF) "done!\n"
	@$(DISPLAY_SEPARATOR)
	
# ---

build: clean
	$(PYTHON3) ./setup.py install --record $(INSTALLED_FILES_RECORD)
	@$(DISPLAY_SEPARATOR)

# ---

artifacts:
ifdef CIRCLE_ARTIFACTS
	if [ -d $(CIRCLE_ARTIFACTS) ] ; then $(CP) lint_output.txt $(CIRCLE_ARTIFACTS) fi
	@$(DISPLAY_SEPARATOR)
endif

# ---

danger: check
	@$(PRINTF) "Running danger "
ifdef DANGER_GITHUB_API_TOKEN
	@$(PRINTF) "(PR)... \n"
	$(DANGER) --verbose
else
	@$(PRINTF) "(local)... \n"
	$(DANGER) local --verbose
endif
	@$(DISPLAY_SEPARATOR)
	
# ---

ci: lint danger artifacts

# ---

lint: check
	@$(TOUCH) $(value $(PROGRAM_NAME)_LINTER_EXPORT_PATH)
	@$(PRINTF) "Running linter... "
	@$(PYLINT) --rcfile=pylintrc ./readmail > $(value $(PROGRAM_NAME)_LINTER_EXPORT_PATH) || :
	@$(PRINTF) " done!\n"
	@$(PRINTF) "Generated linter report: $(value $(PROGRAM_NAME)_LINTER_EXPORT_PATH)\n"
	@$(DISPLAY_SEPARATOR)

# ---

.PHONY: danger lint ci build clean install-tools install-deps check
