HELP_FUN = \
         %help; \
         while(<>) { \
		 	push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z0-9_-]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/ \
		 }; \
         print "usage: make [target]\nexample: make help\n\n"; \
     	 for ( sort keys %help ) { \
         	print "$$_:\n"; \
        	printf("  %-20s %s\n", $$_->[0], $$_->[1]) for @{$$help{$$_}}; \
        	print "\n"; \
	 	 }

help: ##@miscellaneous Show this help
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

_poetry_config:
	@poetry config virtualenvs.create false

install: _poetry_config ##@dev Install dependencies
	@cd src/ && poetry install

tests: test coverage ##@dev Execute tests and coverage
test: 
	@cd src/ && coverage run -m pytest
coverage:
	@cd src/ && coverage report -m

audit: _poetry_config ##@dev Scan for known vulnerabilities dependencies
	@cd src/ && poetry export --without-hashes -f requirements.txt | safety check --full-report --stdin

dev: ##@dev Start development server with hotreloading
	@cd src/ && uvicorn app.main:app --reload

db: ##@dev CLI database connection
	@PGPASSWORD=secret psql -h postgres -d test_db -U root

wipe-db: ##@dev Removes all but default data on the database
	@PGPASSWORD=secret psql -h postgres -d test_db -U root -c "DELETE FROM users WHERE name NOT IN ('pepe');"