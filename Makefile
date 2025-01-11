.PHONY: build up

all: build up

build:
	@docker compose build

up:
	@docker compose up

