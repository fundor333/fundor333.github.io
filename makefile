MAKE_POST := uv run python3 action_script/make_post

.PHONY: help install cache clean run gomodule update sync_taxonomy submodule \
	develop developfuture developall broadcast build \
	new micro now notebook notebook_editor weekly characters meet event eventi \
	anime photo_exif automation autotag send_webmention weeknote_webmentions \
	weeknote_webmentions_year hydra deploy deploy_prod precommit changelog

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## --- Setup ------------------------------------------------------------

install: sync_taxonomy ## Install project dependencies
	@npm install
	@hugo mod get -u
	@uv sync
	@uv run pre-commit install
	@uv run pre-commit autoupdate

update: clean sync_taxonomy ## Update the site requirements
	@npm update
	@uv lock --upgrade
	@uv sync
	@uv run pre-commit autoupdate

gomodule: ## Update Go modules
	@hugo mod get -u ./...
	@hugo mod tidy
	@hugo mod get -u

submodule: ## Get submodules for this repo
	git submodule update --init --recursive

sync_taxonomy: ## Sync known series, tags and categories into the post archetype
	@$(MAKE_POST) series
	@$(MAKE_POST) tags
	@$(MAKE_POST) categories

## --- Build & clean ------------------------------------------------------

cache: ## Clean the Hugo cache
	@hugo --gc

clean: cache gomodule ## Clean cache, meta files and other build artifacts
	@find . -type d -empty -delete

build: clean ## Build for dev
	@hugo mod get -u
	@hugo

run: clean ## Build the site, cleaning everything first
	@hugo --minify

## --- Develop ------------------------------------------------------------

develop: ## Run the site locally
	@hugo server --disableFastRender --renderToMemory

developfuture: ## Run the site locally, including future posts
	@hugo server --disableFastRender --buildFuture --renderToMemory

developall: ## Run the site locally, including future posts and drafts
	@hugo server --disableFastRender --buildFuture --buildDrafts --renderToMemory

broadcast: clean ## Broadcast the site on the local network
	@hugo server --disableFastRender --buildFuture --buildDrafts -bind=0.0.0.0

## --- Content ------------------------------------------------------------

new: sync_taxonomy ## Make a new object for the blog
	@$(MAKE_POST)

micro: ## Run the microblog script
	@$(MAKE_POST) micro

now: ## Run the now script
	@$(MAKE_POST) now

notebook: ## Run the notebook script
	@$(MAKE_POST) notebook

notebook_editor: ## Run the notebook editor
	@uv run jupyter lab .

weekly: ## Weekly script
	@uv run weeknote -config weeknote-config.json
	@$(MAKE_POST) weekly_cover

characters: ## Sorting characters
	@python3 action_script/sorting_characters.py

meet: ## Run meet script
	@uv run python3 action_script/micro_meetup.py --memory True

event: ## Run event script (passa URL con: make event URL="https://meetup.com/...")
	@echo "Script per i nuovi eventi, usa meet per gli eventi in memoria"
	@uv run python3 action_script/micro_meetup.py $(URL)

eventi: event ## Alias for event

## --- Automation & syndication ---------------------------------------------

anime: ## Anime script
	@uv run python action_script/aniist_run.py

photo_exif: ## Extract EXIF data from all photo posts and save exif.json
	@uv run python action_script/photo_exif.py

automation: anime photo_exif ## Run all the automation scripts
	@uv run python -m syndication_cli all-cmd

autotag: ## Run autotag script
	@uv run python -m syndication_cli tag-cmd

send_webmention: ## Send webmention from feed
	@uv run python action_script/send_webmention.py

weeknote_webmentions: ## Send webmentions for the latest weeknote post
	@uv run python action_script/send_weeknote_webmentions.py

weeknote_webmentions_year: ## Send webmentions for all weeknote posts of the current year
	@uv run python action_script/send_weeknote_webmentions.py $$(date +%Y)

hydra: ## Check links
	@python hydra.py http://localhost:1313/ --config ./hydra-config.json
	@python hydra.py http://fundor333.com/ --config ./hydra-config.json

## --- Deploy ------------------------------------------------------------

deploy: update characters meet automation ## Ready to deploy
	@hugo --minify
	@python action_script/mastodon2hugo.py @fundor333@mastodon.social
	@git add .
	@uv run pre-commit run
	@git add .

deploy_prod: sync_taxonomy ## Ready to deploy to prod
	@npm update
	@uv sync
	@uv lock --upgrade
	@hugo mod get -u
	@hugo --minify

## --- Misc ------------------------------------------------------------------

precommit: ## Run pre-commit hooks
	@git add . && uv run pre-commit run

changelog: ## Update CHANGELOG.md and amend it onto the last commit
	git-cliff --config pyproject.toml --output CHANGELOG.md
	git add CHANGELOG.md
	git commit --amend --no-edit
