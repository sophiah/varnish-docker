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
    print(f"  => canonical_request = {canonical_request}")

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
        f"SignedHeaders={';'.join( sorted(headers.keys()) )}, Signature={signature}"
    )
    
    return authorization_header


# -----
access_key = "minioadmin"
secret_key = "minioadmin"
service = "s3"
region = "us-east-1"

print("-=" * 40)
print("EXPECT => f4be4110a956483a39a20c37939428b83cbc7e180d7ae967ab51e4c5918118eb")
print(generate_aws_signature(
    secret_key, service, region, 
    method="GET", path = "/", query_str="", 
    headers={
        "host": "localhost", 
    }, 
    payload_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", 
    amzdate="20240331T061930Z"))

print("-=" * 40)
print("EXPECT => 90bba57b0b42e834b95864e693ed82c260e8e3cd98cfc3dc1491c6610fb27f6f")
print(
    generate_aws_signature(
        secret_key, service, region, 
         method = "POST",
         path = "/test-bucket/t.obj",
         query_str = "uploads",
         headers = {
            "content-type": "application/x-tgif",
            "host": "localhost",
         },
         payload_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", 
         amzdate = "20240331T061934Z"))

print("-=" * 40)
print("EXPECT => 828a61c748cb6a8d8518a61b7b0e2afbcfc85f88281419f1b3a07c63551a9fa0")
print(generate_aws_signature(
    secret_key, service, region, 
    method="DELETE", path = "/test-bucket/t.obj", 
    query_str="uploadId=MGQ2YjgyZTItMzBjOC00M2RlLTkxMjAtNmMxODMzNGNmZTgyLjBhMTU1MThlLTg3YTItNGUyZS1hYmJkLTRjMjAyNzM3OTM4Mg", 
    headers={
        "host": "localhost", 
    }, 
    payload_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", 
    amzdate="20240331T063452Z"))


print("-=" * 40)
print("EXPECT => afea3471591c959a1d8714daefd7af64b09e2ff28ba0f1fa2534f7700913c085")
print(generate_aws_signature(
    secret_key, service, region, 
    method="PUT", path = "/test-bucket/t.obj", 
    query_str="uploadId=MGQ2YjgyZTItMzBjOC00M2RlLTkxMjAtNmMxODMzNGNmZTgyLjBhMTU1MThlLTg3YTItNGUyZS1hYmJkLTRjMjAyNzM3OTM4Mg&partNumber=2",
    headers={
        "host": "localhost",
        "content-md5": "lplbWNTL9qqpBBtPAMf2rg=="
    }, 
    payload_hash = "2daeb1f36095b44b318410b3f4e8b5d989dcc7bb023d1426c492dab0a3053e74", 
    amzdate="20240331T063452Z"))


