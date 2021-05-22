.DEFAULT_GOAL = help

CHANGELOG = CHANGELOG.md
CHANGELOG_TMP = CHANGELOG.tmp

README = README.md
README_TMP = README.tmp

define UNRELEASED
# [unreleased]
## added
## fixed
## changed
## removed

endef

help:
	@echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|help|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	@echo "~ exports - export requirements.txt "
	@echo "~ patch - bump patch version"
	@echo "~ minor - bump minor version and @changelog "
	@echo "~ patch - bump major version and @changelog "
	@echo "~ changelog - roll changelog "
	@echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

patch:
	@poetry version patch
	@git add pyproject.toml

minor:
	@poetry version minor
	$(MAKE) changelog
	@git add pyproject.toml

major:
	@poetry version major
	$(MAKE) changelog
	@git add pyproject.toml

push:
	@git checkout dev && git push && git checkout master && git push && git push origin --tags

pull:
	@git checkout dev && git pull && git checkout master && git pull

changelog:
	$(MAKE) patch_changelog
	$(MAKE) unreleased_section
	@git add $(CHANGELOG)

patch_changelog:
	$(shell sed "s/\[unreleased\]/[$(shell poetry version -s)] - $(shell date -u +'%Y-%m-%d')/g" $(CHANGELOG) > $(CHANGELOG_TMP))
	@mv $(CHANGELOG_TMP) $(CHANGELOG)

unreleased_section:
	$(shell mv $(CHANGELOG) $(CHANGELOG_TMP))
	$(file > $(CHANGELOG),$(UNRELEASED))
	$(shell cat CHANGELOG.tmp >> CHANGELOG.md)
	@rm $(CHANGELOG_TMP)
