.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Intall
	@npm install 
	@hugo mod get -u

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
	@poetry run python hydra.py http://localhost:1313/ --config ./hydra-config.json

.PHONY: syntax
syntax: ## Build the style of the code
	@hugo gen chromastyles --style=dracula > themes/fugu/assets/css/_syntax.scss

cache: ## Clean the cache
	@hugo --gc

clean: cache gomodule ## Clean the directory of the project of chache e meta file and other things

.PHONY: run
run: clean  ## Build the site cleaning all
	@hugo --minify

.PHONY: new
new: ## Make new object for the blog
	@python3 make-post.py

characters: ## Sorting characters
	@python3 sorting_characters.py

.PHONY: build
build: clean ## Build for dev
	@hugo mod get -u
	@hugo

deploy: clean characters ## Ready to deploy
	@npm update
	@hugo mod get -u
	@hugo --minify

brodcast: clean ## Brodcast the site
	@hugo server --disableFastRender --buildFuture --buildDrafts -bind=0.0.0.0

deploy_prod:  ## Ready to deploy
	@npm update
	@hugo mod get -u
	@hugo --minify
