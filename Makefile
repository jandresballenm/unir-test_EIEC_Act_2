.PHONY: all build test-unit run server help

# PROJECT_PATH := D:/EIEC_Act2/unir-test-master
PROJECT_PATH := $(CURDIR)


build:
	docker build -t calculator-app .

run:
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest python -B app/calc.py

server:
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --name apiserver --network-alias apiserver --env PYTHONPATH=/opt/calc --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0

interactive:
	docker run -ti --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest bash

test-unit:
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest pytest --cov --cov-report=xml:results/coverage.xml --cov-report=html:results/coverage --junit-xml=results/unit_result.xml -m unit
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/unit_result.xml results/unit_result.html

test-behavior:
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest behave --junit --junit-directory results/ --tags ~@wip test/behavior/
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest bash test/behavior/junit-reports.sh
	
test-api:
	-docker network create calc-test-api
	-docker run -d --rm --volume "${PROJECT_PATH}:/opt/calc" --network calc-test-api --env PYTHONPATH=/opt/calc --name apiserver --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
	timeout /t 5 /nobreak > nul
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --network calc-test-api --env PYTHONPATH=/opt/calc --env BASE_URL=http://apiserver:5000/ -w /opt/calc calculator-app:latest pytest --junit-xml=results/api_result.xml -m api
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/api_result.xml results/api_result.html
	-docker stop apiserver
	-docker rm --force apiserver
	-docker network rm calc-test-api

test-e2e:
	docker network create calc-test-e2e
	docker stop apiserver 2>nul
	docker rm --force apiserver 2>nul
	docker stop calc-web 2>nul
	docker rm --force calc-web 2>nul
	docker run -d --rm --volume "${PROJECT_PATH}:/opt/calc" --network calc-test-e2e --env PYTHONPATH=/opt/calc --name apiserver --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
	docker run -d --rm --volume "${PROJECT_PATH}/web:/usr/share/nginx/html" --volume "${PROJECT_PATH}/web/constants.test.js:/usr/share/nginx/html/constants.js" --volume "${PROJECT_PATH}/web/nginx.conf:/etc/nginx/conf.d/default.conf" --network calc-test-e2e --name calc-web -p 80:80 nginx
	timeout /t 10 /nobreak > nul
	docker run --rm --volume "${PROJECT_PATH}/test/e2e/cypress.json:/cypress.json" --volume "${PROJECT_PATH}/test/e2e/cypress:/cypress" --volume "${PROJECT_PATH}/results:/results" --network calc-test-e2e cypress/included:4.9.0 --browser chrome
	docker rm --force apiserver
	docker rm --force calc-web
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/cypress_result.xml results/cypress_result.html
	docker network rm calc-test-e2e

test-e2e-wiremock:
	docker network create calc-test-e2e-wiremock
	docker stop apiwiremock 2>nul
	docker rm --force apiwiremock 2>nul
	docker stop calc-web 2>nul
	docker rm --force calc-web 2>nul
	docker run -d --rm --name apiwiremock --volume "${PROJECT_PATH}/test/wiremock/stubs:/home/wiremock" --network calc-test-e2e-wiremock -p 8080:8080 -p 8443:8443 calculator-wiremock
	docker run -d --rm --volume "${PROJECT_PATH}/web:/usr/share/nginx/html" --volume "${PROJECT_PATH}/web/constants.wiremock.js:/usr/share/nginx/html/constants.js" --volume "${PROJECT_PATH}/web/nginx.conf:/etc/nginx/conf.d/default.conf" --network calc-test-e2e-wiremock --name calc-web -p 80:80 nginx
	docker run --rm --volume "${PROJECT_PATH}/test/e2e/cypress.json:/cypress.json" --volume "${PROJECT_PATH}/test/e2e/cypress:/cypress" --volume "${PROJECT_PATH}/results:/results" --network calc-test-e2e-wiremock cypress/included:4.9.0 --browser chrome
	docker rm --force apiwiremock
	docker rm --force calc-web
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/cypress_result.xml results/cypress_result.html
	docker network rm calc-test-e2e-wiremock

run-web:
	docker run --rm --volume "${PROJECT_PATH}/web:/usr/share/nginx/html" --volume "${PROJECT_PATH}/web/constants.local.js:/usr/share/nginx/html/constants.js" --volume "${PROJECT_PATH}/web/nginx.conf:/etc/nginx/conf.d/default.conf" --name calc-web -p 80:80 nginx

stop-web:
	docker stop calc-web 2>nul

start-sonar-server:
	docker network create calc-sonar
	docker run -d --rm --stop-timeout 60 --network calc-sonar --name sonarqube-server -p 9000:9000 --volume "${PROJECT_PATH}/sonar/data:/opt/sonarqube/data" --volume "${PROJECT_PATH}/sonar/logs:/opt/sonarqube/logs" sonarqube:8.3.1-community

stop-sonar-server:
	docker stop sonarqube-server 2>nul
	docker network rm calc-sonar 2>nul

start-sonar-scanner:
	docker run --rm --network calc-sonar --volume "${PROJECT_PATH}:/usr/src" sonarsource/sonar-scanner-cli

pylint:
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest pylint app/ | tee results/pylint_result.txt

build-wiremock:
	docker build -t calculator-wiremock -f test/wiremock/Dockerfile test/wiremock/

start-wiremock:
	docker run -d --rm --name calculator-wiremock --volume "${PROJECT_PATH}/test/wiremock/stubs:/home/wiremock" -p 8080:8080 -p 8443:8443 calculator-wiremock

stop-wiremock:
	docker stop calculator-wiremock 2>nul

ZAP_API_KEY := my_zap_api_key
ZAP_API_URL := http://zap-node:8080/
ZAP_TARGET_URL := http://calc-web/
zap-scan:
	docker network create calc-test-zap
	docker run -d --rm --network calc-test-zap --volume "${PROJECT_PATH}:/opt/calc" --name apiserver --env PYTHONPATH=/opt/calc --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
	docker run -d --rm --network calc-test-zap --volume "${PROJECT_PATH}/web:/usr/share/nginx/html" --volume "${PROJECT_PATH}/web/constants.test.js:/usr/share/nginx/html/constants.js" --volume "${PROJECT_PATH}/web/nginx.conf:/etc/nginx/conf.d/default.conf" --name calc-web -p 80:80 nginx
	docker run -d --rm --network calc-test-zap --name zap-node -u zap -p 8080:8080 -i owasp/zap2docker-stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.key=$(ZAP_API_KEY)
	timeout /t 10 /nobreak > nul
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --network calc-test-zap --env PYTHONPATH=/opt/calc --env ZAP_API_KEY=$(ZAP_API_KEY) --env ZAP_API_URL=$(ZAP_API_URL) --env TARGET_URL=$(ZAP_TARGET_URL) -w /opt/calc calculator-app:latest pytest --junit-xml=results/sec_result.xml -m security
	docker run --rm --volume "${PROJECT_PATH}:/opt/calc" --env PYTHONPATH=/opt/calc -w /opt/calc calculator-app:latest junit2html results/sec_result.xml results/sec_result.html
	docker stop apiserver 2>nul
	docker stop calc-web 2>nul
	docker stop zap-node 2>nul
	docker network rm calc-test-zap 2>nul

build-jmeter:
	docker build -t calculator-jmeter -f test/jmeter/Dockerfile test/jmeter

start-jmeter-record:
	docker network create calc-test-jmeter
	docker run -d --rm --network calc-test-jmeter --volume "${PROJECT_PATH}:/opt/calc" --name apiserver --env PYTHONPATH=/opt/calc --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
	docker run -d --rm --network calc-test-jmeter --volume "${PROJECT_PATH}/web:/usr/share/nginx/html" --volume "${PROJECT_PATH}/web/constants.test.js:/usr/share/nginx/html/constants.js" --volume "${PROJECT_PATH}/web/nginx.conf:/etc/nginx/conf.d/default.conf" --name calc-web -p 80:80 nginx

stop-jmeter-record:
	docker stop apiserver 2>nul
	docker stop calc-web 2>nul
	docker network rm calc-test-jmeter 2>nul

JMETER_RESULTS_FILE := results/jmeter_results.csv
JMETER_REPORT_FOLDER := results/jmeter/
jmeter-load:
	del /f /q "$(JMETER_RESULTS_FILE)" 2>nul
	rmdir /s /q "$(JMETER_REPORT_FOLDER)" 2>nul
	docker network create calc-test-jmeter
	docker run -d --rm --network calc-test-jmeter --volume "${PROJECT_PATH}:/opt/calc" --name apiserver --env PYTHONPATH=/opt/calc --env FLASK_APP=app/api.py -p 5000:5000 -w /opt/calc calculator-app:latest flask run --host=0.0.0.0
	timeout /t 5 /nobreak > nul
	docker run --rm --network calc-test-jmeter --volume "${PROJECT_PATH}:/opt/jmeter" -w /opt/jmeter calculator-jmeter jmeter -n -t test/jmeter/jmeter-plan.jmx -l results/jmeter_results.csv -e -o results/jmeter/
	docker stop apiserver 2>nul
	docker network rm calc-test-jmeter 2>nul

# Comando de ayuda
help:
	@echo Comandos disponibles:
	@echo   make build        - Construir la imagen Docker
	@echo   make test-unit    - Ejecutar tests unitarios
	@echo   make test-api     - Ejecutar tests de API
	@echo   make run          - Ejecutar calculadora en consola
	@echo   make server       - Iniciar servidor API
	@echo   make run-web      - Servir frontend web
	@echo   make help         - Mostrar esta ayuda