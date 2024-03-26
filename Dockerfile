FROM varnish:7.1 AS varnish_mod_dev

USER root
RUN mkdir -p /home/varnish; chown -R varnish /home/varnish

RUN set -e; \
    apt-get update; \
    apt-get -y install apt-utils $VMOD_DEPS /pkgs/*.deb varnish-dev

RUN install-vmod https://github.com/varnish/varnish-modules/releases/download/0.20.0/varnish-modules-0.20.0.tar.gz
RUN apt-get -y install libmhash-dev && install-vmod https://github.com/varnish/libvmod-digest/releases/download/libvmod-digest-1.0.3/libvmod-digest-1.0.3.tar.gz

USER varnish

FROM varnish_mod_dev AS varnish_mod

USER root
# clean up and set the user back to varnish
RUN apt-get -y purge --auto-remove $VMOD_DEPS varnish-dev; \
    rm -rf /var/lib/apt/lists/*

USER varnish