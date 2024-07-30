from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
async def call_backend_service(client, method, url, **kwargs):
    response = await client.request(method, url, **kwargs)
    response.raise_for_status()
    return response