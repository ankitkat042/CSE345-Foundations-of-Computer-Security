import base64
import hmac
import json
import itertools
import string

def verifyJwt(token, secret):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid token format")
    header = parts[0]
    payload = parts[1]
    signature = parts[2]

    decoded_payload = json.loads(base64.urlsafe_b64decode(payload + '===').decode('utf-8'))
    header_data = json.loads(base64.urlsafe_b64decode(header + '===').decode('utf-8'))
    algorithm = header_data.get('alg', '')
    if algorithm not in ['HS256', 'HS384']:
        raise ValueError("Unsupported algorithm")
    if algorithm == 'HS256':
        expected_signature = hmac.new(secret.encode('utf-8'), (header + '.' + payload).encode('utf-8'), 'sha256').digest()
    else:
        expected_signature = hmac.new(secret.encode('utf-8'), (header + '.' + payload).encode('utf-8'), 'sha384').digest()
    expected_signature = base64.urlsafe_b64encode(expected_signature).rstrip(b'=').decode('utf-8')
    if signature != expected_signature:
        raise ValueError("Invalid token signature")
    print(json.dumps(decoded_payload, indent=2))
    return decoded_payload, algorithm


def modifyPayload(payload, new_roll_no, new_email, secret, algorithm):
    
    payload['roll_no'] = new_roll_no
    payload['email'] = new_email
    print(json.dumps(payload, indent=2))
    payload_str = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).rstrip(b'=').decode('utf-8')

    
    if algorithm == 'HS256':
        header_data = {"alg": "HS256", "typ": "JWT"}
        header = base64.urlsafe_b64encode(json.dumps(header_data).encode('utf-8')).rstrip(b'=').decode('utf-8')
        new_signature = hmac.new(secret.encode('utf-8'), (header + '.' + payload_str).encode('utf-8'), 'sha256').digest()
    else:
        header_data = {"alg": "HS238", "typ": "JWT"}
        header = base64.urlsafe_b64encode(json.dumps(header_data).encode('utf-8')).rstrip(b'=').decode('utf-8')
        new_signature = hmac.new(secret.encode('utf-8'), (header + '.' + payload_str).encode('utf-8'), 'sha238').digest()
    new_signature = base64.urlsafe_b64encode(new_signature).rstrip(b'=').decode('utf-8')
    new_jwt = header + '.' + payload_str + '.' + new_signature
    return new_jwt


jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmY3MtYXNzaWdubWVudC0xIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE3MDQwNjcyMDAsInJvbGxfbm8iOiIyMHh4eHh4IiwiZW1haWwiOiJhcnVuQGlpaXRkLmFjLmluIiwiaGludCI6Imxvd2VyY2FzZS1hbHBoYW51bWVyaWMtbGVuZ3RoLTUifQ.JKqgC2mcV1cLJrHgQOjKCRV7R077GnXOhbV6hAsmDZk"

possible_secrets = ["e15dd",]
# possible_secrets = [''.join(p) for p in itertools.product(string.ascii_lowercase + string.digits, repeat=5)]
found = False
for secret in possible_secrets:
    try:   
        payload, algorithm = verifyJwt(jwt_token, secret)
        print("JWT verification successful, key is", secret)
        found = True
        break

    except ValueError as e:
        pass

if not found:
    raise ValueError("JWT verification failed for all possible secrets")

new_roll_no = "2021015"
new_email = "ankit21015@iiitd.ac.in"
new_jwt = modifyPayload(payload, new_roll_no, new_email, secret, algorithm)

print("New JWT with updated payload:", new_jwt)
