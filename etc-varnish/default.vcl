vcl 4.0;

import awsrest;

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


sub vcl_recv {
    if (! awsrest.v4_validate(
        access_key = "minioadmin",
        secret_key = "minioadmin")) {
        return (synth(403, "Forbidden"));
    }
    # change key 
    # awsrest.v4_generic(
    #     service           = "s3",
    #     region            = "us-east-1",
    #     access_key        = "minioadmin",
    #     secret_key        = "minioadmin",
    #     signed_headers    = "host;",
    #     canonical_headers = "host:" + req.http.host + awsrest.lf()
    # );
}

