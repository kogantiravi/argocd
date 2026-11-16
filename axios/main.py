from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()
client = httpx.AsyncClient()

# Add this root route to prevent 404s on health checks or root visits
@app.get("/")
async def root_health_check():
    return {"status": "healthy", "service": "axis-dynamic-proxy", "message": "Ready to proxy /t1 to /t100"}

@app.api_route("/t{service_id}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def dynamic_proxy(service_id: int, path: str, request: Request):
    # Enforce range check for t1 to t100
    if not (1 <= service_id <= 100):
        return Response(content="Service ID out of range (must be 1-100)", status_code=404)
    
    # Construct internal Kubernetes DNS target (assuming same namespace)
    target_service = f"http://service-t{service_id}.default.svc.cluster.local"
    target_url = f"{target_service}/{path}"
    
    # Extract headers and body, removing original host
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None) 
    
    try:
        # Forward request to the specific GKE docker service pod
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params,
            timeout=30.0
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as exc:
        return Response(content=f"Gateway Error: Could not reach service-t{service_id}", status_code=502)
