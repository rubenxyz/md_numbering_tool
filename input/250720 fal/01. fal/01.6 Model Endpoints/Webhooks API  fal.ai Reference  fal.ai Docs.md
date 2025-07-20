Webhooks work in tandem with the queue system explained above, it is another way to interact with our queue. By providing us a webhook endpoint you get notified when the request is done as opposed to polling it.

Here is how this works in practice, it is very similar to submitting something to the queue but we require you to pass an extra `fal_webhook` query parameter.

To utilize webhooks, your requests should be directed to the `queue.fal.run` endpoint, instead of the standard `fal.run`. This distinction is crucial for enabling webhook functionality, as it ensures your request is handled by the queue system designed to support asynchronous operations and notifications.

```
curl --request POST \ --url 'https://queue.fal.run/fal-ai/flux/dev?fal_webhook=https://url.to.your.app/api/fal/webhook' \ --header "Authorization: Key $FAL_KEY" \ --header 'Content-Type: application/json' \ --data '{ "prompt": "Photo of a cute dog"}'
```

The request will be queued and you will get a response with the `request_id` and `gateway_request_id`:

```
{ "request_id": "024ca5b1-45d3-4afd-883e-ad3abe2a1c4d", "gateway_request_id": "024ca5b1-45d3-4afd-883e-ad3abe2a1c4d"}
```

These two will be mostly the same, but if the request failed and was retried, `gateway_request_id` will have the value of the last tried request, while `request_id` will be the value used in the queue API.

Once the request is done processing in the queue, a `POST` request is made to the webhook URL, passing the request info and the resulting `payload`. The `status` indicates whether the request was successful or not.

### Successful result

The following is an example of a successful request:

```
{ "request_id": "123e4567-e89b-12d3-a456-426614174000", "gateway_request_id": "123e4567-e89b-12d3-a456-426614174000", "status": "OK", "payload": { "images": [ { "url": "https://url.to/image.png", "content_type": "image/png", "file_name": "image.png", "file_size": 1824075, "width": 1024, "height": 1024 } ], "seed": 196619188014358660 }}
```

### Response errors

When an error happens, the `status` will be `ERROR`. The `error` property will contain a message and the `payload` will provide the error details. For example, if you forget to pass the required `model_name` parameter, you will get the following response:

```
{ "request_id": "123e4567-e89b-12d3-a456-426614174000", "gateway_request_id": "123e4567-e89b-12d3-a456-426614174000", "status": "ERROR", "error": "Invalid status code: 422", "payload": { "detail": [ { "loc": ["body", "prompt"], "msg": "field required", "type": "value_error.missing" } ] }}
```

### Payload errors

For the webhook to include the payload, it must be valid JSON. So if there is an error serializing it, `payload` is set to `null` and a `payload_error` will include details about the error.

```
{ "request_id": "123e4567-e89b-12d3-a456-426614174000", "gateway_request_id": "123e4567-e89b-12d3-a456-426614174000", "status": "OK", "payload": null, "payload_error": "Response payload is not JSON serializable. Either return a JSON serializable object or use the queue endpoint to retrieve the response."}
```

### Retry policy

If the webhook fails to deliver the payload, it will retry 10 times in the span of 2 hours.

### Verifying Your Webhook

To ensure the security and integrity of incoming webhook requests, you must verify that they originate from the expected source. This involves validating a cryptographic signature included in the request using a set of public keys. Below is a step-by-step guide to the verification process, followed by example implementations in Python and JavaScript.

#### Verification Process

1.  **Fetch the JSON Web Key Set (JWKS)**:
    
    -   Retrieve the public keys from the JWKS endpoint: `https://rest.alpha.fal.ai/.well-known/jwks.json`.
    -   The JWKS contains a list of public keys in JSON format, each with an `x` field holding a base64url-encoded ED25519 public key.
    -   **Note**: The JWKS is cacheable to reduce network requests. Ensure your implementation caches the keys and refreshes them after the cache duration expires. Do not cache longer than 24 hours since they can change.
2.  **Extract Required Headers**:
    
    -   Obtain the following headers from the incoming webhook request:
        -   `X-Fal-Webhook-Request-Id`: The unique request ID.
        -   `X-Fal-Webhook-User-Id`: Your user ID.
        -   `X-Fal-Webhook-Timestamp`: The timestamp when the request was generated (in Unix epoch seconds).
        -   `X-Fal-Webhook-Signature`: The cryptographic signature in hexadecimal format.
    -   If any header is missing, the request is invalid.
3.  **Verify the Timestamp**:
    
    -   Compare the `X-Fal-Webhook-Timestamp` with the current Unix timestamp.
    -   Allow a leeway of ±5 minutes (300 seconds) to account for clock skew and network delays.
    -   If the timestamp differs by more than 300 seconds, reject the request to prevent replay attacks.
4.  **Construct the Message**:
    
    -   Compute the SHA-256 hash of the request body (raw bytes, not JSON-parsed).
    -   Concatenate the following in strict order, separated by newline characters (`\n`):
        -   `X-Fal-Webhook-Request-Id`
        -   `X-Fal-Webhook-User-Id`
        -   `X-Fal-Webhook-Timestamp`
        -   Hex-encoded SHA-256 hash of the request body
    -   Encode the resulting string as UTF-8 bytes to form the message to verify.
5.  **Verify the Signature**:
    
    -   Decode the `X-Fal-Webhook-Signature` from hexadecimal to bytes.
    -   For each public key in the JWKS:
        -   Decode the `x` field from base64url to bytes.
        -   Use an ED25519 verification function (e.g., from PyNaCl in Python or libsodium in JavaScript) to verify the signature against the constructed message.
    -   If any key successfully verifies the signature, the request is valid.
    -   If no key verifies the signature, the request is invalid.

#### Example Implementations

Below are simplified functions to verify webhook signatures by passing the header values and request body directly. These examples handle the verification process as described above and include JWKS caching.

-   [python](https://docs.fal.ai/model-endpoints/webhooks#tab-panel-27)
-   [javascript](https://docs.fal.ai/model-endpoints/webhooks#tab-panel-28)

**Install dependencies**:

```
pip install pynacl requests
```

**Verification function**:

```
import base64import
hashlibimport timefrom typing import Optionalimport requestsfrom nacl.signing import VerifyKeyfrom nacl.exceptions import BadSignatureErrorfrom nacl.encoding import HexEncoderJWKS_URL = "https://rest.alpha.fal.ai/.well-known/jwks.json"JWKS_CACHE_DURATION = 24 * 60 * 60 # 24 hours in seconds_jwks_cache = None_jwks_cache_time = 0def fetch_jwks() 
-&gt; list: """Fetch and cache JWKS,
refreshing after 24 hours.""" global _jwks_cache,
_jwks_cache_time current_time = time.time() 
if _jwks_cache is None or (current_time - _jwks_cache_time) 
&gt; JWKS_CACHE_DURATION: response = requests.get(JWKS_URL, timeout=10) 
response.raise_for_status() 
_jwks_cache = response.json()
.get("keys", []) 
_jwks_cache_time = current_time return _jwks_cachedef verify_webhook_signature( request_id: str, user_id: str, timestamp: str, signature_hex: str, body: bytes) 
-&gt; bool: """ Verify a webhook signature using provided headers and body. Args: request_id: Value of X-Fal-Webhook-Request-Id header. user_id: Value of X-Fal-Webhook-User-Id header. timestamp: Value of X-Fal-Webhook-Timestamp header. signature_hex: Value of X-Fal-Webhook-Signature header (hex-encoded)
. body: Raw request body as bytes. Returns: bool: True if the signature is valid,
False otherwise. """ # Validate timestamp (within ±5 minutes) 
try: timestamp_int = int(timestamp) 
current_time = int(time.time()
) 
if abs(current_time - timestamp_int) 
&gt; 300: print("Timestamp is too old or in the future.") 
return False except ValueError: print("Invalid timestamp format.") 
return False # Construct the message to verify try: message_parts = [ request_id,
user_id,
timestamp,
hashlib.sha256(body)
.hexdigest() 
] if any(part is None for part in message_parts)
: print("Missing required header value.") 
return False message_to_verify = "\n".join(message_parts)
.encode("utf-8") 
except Exception as e: print(f"Error constructing message: {e}") 
return False # Decode signature try: signature_bytes = bytes.fromhex(signature_hex) 
except ValueError: print("Invalid signature format (not hexadecimal)
.") 
return False # Fetch public keys try: public_keys_info = fetch_jwks() 
if not public_keys_info: print("No public keys found in JWKS.") 
return False except Exception as e: print(f"Error fetching JWKS: {e}") 
return False # Verify signature with each public key for key_info in public_keys_info: try: public_key_b64url = key_info.get("x") 
if not isinstance(public_key_b64url, str)
: continue public_key_bytes = base64.urlsafe_b64decode(public_key_b64url) 
verify_key = VerifyKey(public_key_bytes.hex()
,
encoder=HexEncoder) 
verify_key.verify(message_to_verify, signature_bytes) 
return True except (BadSignatureError,
Exception) 
as e: print(f"Verification failed with a key: {e}") 
continue print("Signature verification failed with all keys.") 
return False
```

#### Usage Notes

-   **Caching the JWKS**: The JWKS can be cached for 24 hours to minimize network requests. The example implementations include basic in-memory caching.
-   **Timestamp Validation**: The ±5-minute leeway ensures robustness against minor clock differences. Adjust this value if your use case requires stricter or looser validation.
-   **Error Handling**: The examples include comprehensive error handling for missing headers, invalid signatures, and network issues. Log errors appropriately for debugging.
-   **Framework Integration**: For frameworks like FastAPI (Python) or Express (JavaScript), ensure the raw request body is accessible. For Express, use `express.raw({ type: 'application/json' })` middleware before JSON parsing.