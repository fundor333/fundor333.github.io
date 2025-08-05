.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Intall
	@npm install
	@hugo mod get -u
	@poetry install --no-root
	@poetry run pre-commit install
	@poetry run pre-commit autoupdate

send_webmention: ## Send webmention from feed
	@poetry run python send_webmention.py

develop: ## Run the site localy
	@hugo server  --minify --disableFastRender --renderToMemory

developfuture: ## Run the site localy with all the future article
	@hugo server  --minify --disableFastRender --buildFuture --renderToMemory

developall: ## Run the site localy with all the article, future or drafts
	@hugo server  --minify --disableFastRender --buildFuture --buildDrafts --renderToMemory

.PHONY: gomodule
gomodule: ## Update Go Module
	@hugo mod get -u ./...
	@hugo mod tidy
	@hugo mod get -u

.PHONY: hydra
hydra: ## Check links
	@python hydra.py http://localhost:1313/ --config ./hydra-config.json
	@python hydra.py http://fundor333.com/ --config ./hydra-config.json

.PHONY: syntax
syntax: ## Build the style of the code
	@hugo gen chromastyles --style=dracula > themes/fugu/assets/css/_syntax.scss

cache: ## Clean the cache
	@hugo --gc

clean: cache gomodule ## Clean the directory of the project of chache e meta file and other things
	@find . -type d -empty -delete

.PHONY: run
run: clean  ## Build the site cleaning all
	@hugo --minify

.PHONY: new
new: ## Make new object for the blog
	@poetry run python3 make-post.py

characters: ## Sorting characters
	@python3 sorting_characters.py

.PHONY: build
build: clean ## Build for dev
	@hugo mod get -u
	@hugo

.PHONY: syndication
syndication: ## Syndication script
	@poetry run python action_script/syndication-adder.py

.PHONY: webmention
webmention: ## Webmention script
	@poetry run python action_script/webmention.py

deploy: clean characters webmention syndication## Ready to deploy
	@npm update
	@poetry export --without-hashes --format=requirements.txt > requirements.txt
	@hugo mod get -u
	@hugo --minify
	@python mastodon2hugo.py @fundor333@mastodon.social
	@poetry run pre-commit autoupdate


brodcast: clean ## Brodcast the site
	@hugo server --disableFastRender --buildFuture --buildDrafts -bind=0.0.0.0

deploy_prod:  ## Ready to deploy
	@npm update
	@hugo mod get -u
	@hugo --minify


.PHONY: submodule
submodule: ## Get submodule for this repo
	git submodule update --init --recursive

.PHONY: weekly
weekly: ## Weekly script
	@weeknote -config weeknote-config.json
	@python3 make-post.py weekly_cover

precommit: ## Run pre-commit hooks
	@git add . & poetry run pre-commit run

micro: ## Run microblog script
	@poetry run python3 make-post.py micro

now: ## Run now script
	@poetry run python3 make-post.py now
