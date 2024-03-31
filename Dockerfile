FROM varnish:7.3 AS varnish_mod_dev

USER root
RUN mkdir -p /home/varnish; chown -R varnish /home/varnish

RUN set -e; \
    apt-get update; \
    apt-get -y install apt-utils $VMOD_DEPS /pkgs/*.deb varnish-dev \
    zip wget vim make git procps libmhash-dev libssl-dev libtool libpcre2-dev libedit-dev libev-dev

RUN install-vmod https://github.com/varnish/varnish-modules/releases/download/0.22.0/varnish-modules-0.22.0.tar.gz
RUN install-vmod https://github.com/varnish/libvmod-digest/releases/download/libvmod-digest-1.0.3/libvmod-digest-1.0.3.tar.gz

# install libvmon-redis
RUN cd /tmp \
    && wget --no-check-certificate https://github.com/redis/hiredis/archive/v1.2.0.zip -O hiredis-1.2.0.zip \
    && unzip hiredis-*.zip \
    && rm -f hiredis-*.zip \
    && cd hiredis* \
    && make USE_SSL=1 \
    && make USE_SSL=1 PREFIX='/usr/local' install \
    && ldconfig \
    && rm -rf /tmp/hiredis-1.2.0

RUN SKIP_CHECK=TRUE install-vmod https://github.com/carlosabalde/libvmod-redis/archive/refs/tags/7.3-17.1.tar.gz

# install aws auth
COPY plugins/ /home/varnish/plugins
RUN  cd /home/varnish/plugins/libvmod-awsrest && ./autogen.sh && ./configure && make install

COPY docker-varnish-entrypoint /usr/local/bin


USER varnish

FROM varnish_mod_dev AS varnish_mod

USER root
# clean up and set the user back to varnish
RUN apt-get -y purge --auto-remove $VMOD_DEPS varnish-dev  \
    zip wget make git libmhash-dev libssl-dev libtool libpcre2-dev libedit-dev libev-dev vim procps; \
    rm -rf /var/lib/apt/lists/*

USER varnish
