.PHONY: test
test:
	@echo "Say Something for the next 5 seconds"
	@arecord -D plughw:1,0 --duration=5 test.wav
	@echo "You should hear your voice back"
	@aplay test.wav
	@rm -rf test.wav

.PHONY: authenticate
authenticate:
	@cd deployment && bash get_account_credentials.sh
