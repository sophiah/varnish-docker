#!/bin/bash

docker build --target varnish_mod_dev -t sophiah/varnish_mod_dev:7.3-1 .
docker build --target varnish_mod -t sophiah/varnish_mod:7.3-1 .

docker push sophiah/varnish_mod:7.3-1
docker push sophiah/varnish_mod_dev:7.3-1
