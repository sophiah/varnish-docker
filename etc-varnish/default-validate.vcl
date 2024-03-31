vcl 4.0;

import awsrestv2;
import header;
import std;
import redis;

backend minio {
    .host = "minio";
    .port = "9000";
    .max_connections = 100;
    .probe = {
        .request =
            "HEAD /minio/health/live HTTP/1.1"
            "Host: localhost"
            "Connection: close"
            "User-Agent: Varnish Health Probe";
        .interval  = 10s;
        .timeout   = 5s;
        .window    = 5;
        .threshold = 3;
    }
    .connect_timeout        = 5s;
    .first_byte_timeout     = 90s;
    .between_bytes_timeout  = 2s;
}

sub vcl_init {
    new db = redis.db(
        location="redis1:6379",
        type=master,
        connection_timeout=500,
        shared_connections=true,
        max_connections=128,
        max_cluster_hops=16);
    db.add_server("redis2:6379", cluster);
}

sub vcl_recv {
    if (req.url == "/status") {
        return (synth(200, "OK"));
    }

    ## using the awsrestv2 to re-validate the incoming requests
    if (! awsrestv2.v4_validate(
        access_key = "minioadmin",
        secret_key = "minioadmin")) {
        return (synth(403, "Forbidden"));
    }
    else {
        db.query("GET", "cache:" + req.url);
    }
}

sub vcl_synth {
    if (resp.status == 200) {
        set resp.http.Content-Type = "text/plain; charset=utf-8";
        synthetic("OK");
        return (deliver);
    }
}
