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

install: ##@dev Install dependencies
	@cd src/ && pipenv install --dev --system

tests: test coverage
test: ##@dev Execute tests with pytest
	@cd src/ && pipenv run test
coverage:
	@cd src/ && pipenv run coverage

audit: ##@dev Scan for known vulnerabilities dependencies
	@cd src/ && pipenv check --system || true

dev: ##@dev Start development server with hotreloading
	@cd src/ && pipenv run dev

db: ##@dev CLI database connection
	@PGPASSWORD=secret psql -h postgres -d test_db -U root

wipe-db: ##@dev Removes all but default data on the database
	@PGPASSWORD=secret psql -h postgres -d test_db -U root -c "DELETE FROM users WHERE name NOT IN ('pepe');"