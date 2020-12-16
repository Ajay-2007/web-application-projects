#!/bin/bash

#ssh root@ip_address_of_production_env 'rm -rf ~/bookstore/bookstoreAPI'
#scp -r ../bookstoreAPI root@ip_address_of_production_env:~/bookstore
#
#ssh  root@ip_address_of_production_env 'docker stop bookstore-api'
#ssh  root@ip_address_of_production_env 'docker rm bookstore-api'
#ssh  root@ip_address_of_production_env 'docker build -t bookstore-build ~/bookstore/bookstoreAPI'
#ssh  root@ip_address_of_production_env 'docker run -idt -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 bookstore-build'

