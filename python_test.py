import hashlib
import hmac
import datetime

def generate_aws_signature(secret_key, service, region, method, path, query_str, headers, payload_hash, amzdate):
    headers['x-amz-content-sha256'] = payload_hash
    headers['x-amz-date'] = amzdate

    query_str_arr = query_str.split('&') if query_str != "" else []
    query_str_arr = [x if "=" in x else x + "=" for x in query_str_arr]

    canonical_request = f"{method}\n{path}\n"
    canonical_request += '&'.join(sorted(query_str_arr)) + "\n"
    canonical_request += "\n".join([f"{key}:{value}" for key, value in sorted(headers.items())]) + "\n\n"
    canonical_request += ';'.join(sorted(headers.keys())) + "\n"
    canonical_request += payload_hash
    print(f"  => canonical_request = {len(canonical_request)} {canonical_request}")

    timestamp = amzdate
    datestamp = amzdate[0:8]
    scope = f"{datestamp}/{region}/{service}/aws4_request"
    string_to_sign = f"AWS4-HMAC-SHA256\n{timestamp}\n{scope}\n" + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    print(f"  => string_to_sign = {string_to_sign}")

    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    k_date = sign(("AWS4" + secret_key).encode('utf-8'), datestamp)
    k_region = sign(k_date, region)
    k_service = sign(k_region, service)
    k_signing = sign(k_service, 'aws4_request')
    signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{scope}, "
        f"SignedHeaders={';'.join( sorted(headers.keys()) )}, \nSignature={signature}"
    )
    
    return authorization_header


# -----
access_key = "minioadmin"
secret_key = "minioadmin"
service = "s3"
region = "us-east-1"

print("-=" * 40)
print(generate_aws_signature(
    secret_key, service, region, 
    method="DELETE", path = "/test-bucket/t.obj", 
    query_str="uploadId=MGQ2YjgyZTItMzBjOC00M2RlLTkxMjAtNmMxODMzNGNmZTgyLjljM2JmZGZjLWRlMWQtNGQyOC04OGNhLTkwYmU2ODA4YmRlOQ",
    headers={
        "host": "localhost"
    }, 
    payload_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", 
    amzdate="20240403T133706Z"))
print("EXPECT   =927df033f9d3300efd166853f1e9cb918b4d68fda8a7b1b71884981a3850ce3d")

canonical_request = "DELETE" \
                  + "\n/test-bucket/t.obj" \
                  + "\nuploadId=MGQ2YjgyZTItMzBjOC00M2RlLTkxMjAtNmMxODMzNGNmZTgyLjljM2JmZGZjLWRlMWQtNGQyOC04OGNhLTkwYmU2ODA4YmRlOQ" \
                  + "\nhost:localhost" \
                  + "\nx-amz-content-sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" \
                  + "\nx-amz-date:20240403T133706Z" \
                  + "\n\nhost;x-amz-content-sha256;x-amz-date" \
                  + "\ne3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


print("\n\n" + canonical_request + "\n") 
print(hashlib.sha256(canonical_request.encode('utf-8')).hexdigest())