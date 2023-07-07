ifeq "$(APPLICATION_CONFIG)" "production"
	COMPOSE_FILE := docker-compose.prod.yml
	ENV_FILE := config/.env.production
else
	COMPOSE_FILE := docker-compose.yml
	ENV_FILE := config/.env.development
endif

.PHONY: sbul
sbul: stop build up logs

.PHONY: build
build:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) build $(c)

.PHONY: up
up:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d $(c)

.PHONY: restart
restart:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) restart $(c)

.PHONY: stop
stop:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) stop $(c)

.PHONY: down
down:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) down

.PHONY: logs
logs:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) logs --tail=100 -f $(c)

.PHONY: login-backend
login-backend:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) exec backend bash

.PHONY: login-db
login-db:
	docker compose --file $(COMPOSE_FILE) --env-file $(ENV_FILE) exec db bash

# .PHONY: config
# config:
# 	# Run and remove instantly
# 	-docker run --rm -it --volume `pwd`/data:/app/data microblogpub/microblogpub inv configuration-wizard

# .PHONY: update
# update:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv update --no-update-deps

# .PHONY: prune-old-data
# prune-old-data:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv prune-old-data

# .PHONY: webfinger
# webfinger:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv webfinger $(account)

# .PHONY: move-to
# move-to:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv move-to $(account)

# .PHONY: self-destruct
# self-destruct:
# 	-docker run --rm --it --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv self-destruct

# .PHONY: reset-password
# reset-password:
# 	-docker run --rm -it --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv reset-password

# .PHONY: check-config
# check-config:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv check-config

# .PHONY: compile-scss
# compile-scss:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv compile-scss

# .PHONY: import-mastodon-following-accounts 
# import-mastodon-following-accounts:
# 	-docker run --rm --volume `pwd`/data:/app/data --volume `pwd`/app/static:/app/app/static microblogpub/microblogpub inv import-mastodon-following-accounts $(path)
