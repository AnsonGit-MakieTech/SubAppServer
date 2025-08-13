# middleware/rate_limit.py
import time
from django.http import HttpResponse
from django.core.cache import cache

# TEST IN CMD : for /l %i in (1,1,8) do curl -s -o NUL -w "HTTP %{http_code}\n" http://127.0.0.1:8000/test_action/
class PerHourRateLimit:
    # LIMIT = 100
    LIMIT = 5
    WINDOW = 3600  # seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = (request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR") or "").split(",")[0].strip()
        path = request.path
        store = request.GET.get("store", "")
        bucket = int(time.time() // self.WINDOW)

        key = f"rl:{ip}:{path}:{store}:{bucket}"

        current = cache.get(key)
        if current is None:
            added = cache.add(key, 1, timeout=self.WINDOW + 60)
            current = 1 if added else cache.incr(key)
        else:
            current = cache.incr(key)

        if current > self.LIMIT:
            resp = HttpResponse("Rate limit exceeded. Try again later.", status=429)
            resp["Retry-After"] = str(self.WINDOW)
            return resp

        return self.get_response(request)





"""
Here’s a clear, developer-friendly doc you can paste into your repo (e.g., `docs/rate_limit.md`) explaining exactly what the middleware does, how to wire it up, test it, and extend it.

# Per-IP, Per-Path, Per-Hour Rate Limiter (Redis/Django cache)

This middleware throttles excessive traffic to your Django app using a **counter in the cache** (Redis recommended). It limits **each IP** per **path** (and optional `store` query) within a **1-hour time window**. When a client exceeds the limit, it returns **HTTP 429** with a `Retry-After` header.

---

## Code (reference)

```python
# middleware/rate_limit.py
import time
from django.http import HttpResponse
from django.core.cache import cache

# TEST IN CMD:
# for /l %i in (1,1,8) do curl -s -o NUL -w "HTTP %{http_code}\n" http://127.0.0.1:8000/test_action/
class PerHourRateLimit:
    LIMIT = 5         # default: 5 for testing; use 100 in production
    WINDOW = 3600     # seconds (1 hour)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1) Identify client & scope
        ip = (request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR") or "").split(",")[0].strip()
        path = request.path
        store = request.GET.get("store", "")       # optional dimension
        bucket = int(time.time() // self.WINDOW)   # time bucket: current hour

        # 2) Compose a unique key per (ip, path, store, hour-bucket)
        key = f"rl:{ip}:{path}:{store}:{bucket}"

        # 3) Increment the counter atomically in cache (with TTL on first set)
        current = cache.get(key)
        if current is None:
            # add() only sets if the key is missing; sets TTL for auto-expiry
            added = cache.add(key, 1, timeout=self.WINDOW + 60)  # +60s buffer
            current = 1 if added else cache.incr(key)
        else:
            current = cache.incr(key)

        # 4) Enforce limit
        if current > self.LIMIT:
            resp = HttpResponse("Rate limit exceeded. Try again later.", status=429)
            resp["Retry-After"] = str(self.WINDOW)  # hint for clients
            return resp

        # 5) Pass request through
        return self.get_response(request)
```

---

## How it works (step-by-step)

1. **Scoping**

   * The limiter groups requests by:

     * **IP address** (from `X-Forwarded-For` or `REMOTE_ADDR`)
     * **Path** (e.g., `/test_action/`)
     * Optional **`store` query** (e.g., `?store=1223`)
     * **Hour bucket** (integer hour derived from `time.time() // 3600`)
2. **Key format**

   * `rl:{ip}:{path}:{store}:{bucket}`
   * Example: `rl:127.0.0.1:/test_action/::482736` (no `store` param → empty string)
3. **Counting**

   * On first hit in a bucket, it **creates** the key with value `1` and a **TTL \~ 1 hour**.
   * On subsequent hits, it **INCR**ements atomically.
4. **Enforcement**

   * If `current > LIMIT`, the middleware returns **HTTP 429** immediately.
   * The key auto-expires after the TTL → **no cleanup job** required.
5. **Response**

   * Returns `Retry-After: 3600`, telling clients when they can retry.

---

## Why Redis / cache?

* **Speed:** in-memory counter (µs–ms).
* **Atomicity:** `INCR` is atomic → correct under concurrency.
* **TTL:** Keys self-expire → no database cleanup.

> Works with any Django cache backend; use Redis in production for accuracy & throughput.

---

## Wiring it up

### 1) Install and configure Redis cache (recommended)

```bash
pip install django-redis
```

`settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:yourStrongPass@127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "myapp",  # optional namespace
    }
}
```

### 2) Enable the middleware

`settings.py`:

```python
MIDDLEWARE = [
    # put it near the top so it runs early
    "middleware.rate_limit.PerHourRateLimit",
    # ... the rest ...
]
```

> If you only want to protect certain paths, add at the start of `__call__`:
>
> ```python
> if not request.path.startswith("/test_action/"):
>     return self.get_response(request)
> ```

---

## Testing

### Lower the limit

Set `LIMIT = 5` for quick tests (default production value might be 100).

### CMD (Windows) loop

```cmd
for /l %i in (1,1,8) do curl -s -o NUL -w "HTTP %{http_code}\n" http://127.0.0.1:8000/test_action/
```

Expected: first \~5 → `HTTP 200`, then `HTTP 429`.

### Inspect counters (optional)

If using Dockerized Redis:

```bash
docker compose exec redis redis-cli KEYS "rl:*"
docker compose exec redis redis-cli GET "rl:127.0.0.1:/test_action/::<bucket>"
docker compose exec redis redis-cli TTL "rl:127.0.0.1:/test_action/::<bucket>"
```

---

## Production notes & gotchas

* **Proxies / real IPs:**
  If behind Nginx/Load Balancer, ensure it sets `X-Forwarded-For` and Django trusts it; otherwise, use `REMOTE_ADDR` only or parse the left-most IP safely.
* **Path granularity:**
  Current key includes `request.path`; `/test_action/` and `/test_action` are different. Normalize if needed.
* **Query param choice:**
  `store` is optional in the key. Remove it if you want a single bucket per path regardless of `store`.
* **Whitelisting:**
  Add a simple allowlist at the top:

  ```python
  WHITELIST = {"127.0.0.1"}  # or CIDRs with ipaddress module
  if ip in WHITELIST:
      return self.get_response(request)
  ```
* **Different limits per endpoint:**
  Use a mapping:

  ```python
  PER_PATH_LIMITS = {"/test_action/": 5, "/store": 100}
  limit = PER_PATH_LIMITS.get(path, self.LIMIT)
  ```
* **Separate windows:**
  If you need 1-minute bursts + 1-hour caps, create two keys (different `WINDOW`) and enforce both.

---

## FAQ

* **Why `> LIMIT` and not `>= LIMIT`?**
  So the client gets exactly `LIMIT` successful requests; the `(LIMIT+1)`th is blocked.
* **Why `WINDOW + 60` TTL?**
  Small buffer avoids edge collisions at the bucket boundary.
* **What if Redis goes down?**
  The cache backend will raise; you can wrap increments in try/except and fail-open or fail-closed depending on your policy.

---

## TL;DR

* Per-IP, per-path, per-hour throttling using cache keys.
* Atomic increments + TTL = fast, scalable, and self-cleaning.
* Return **HTTP 429** with `Retry-After` when limit is exceeded.

This is a solid first line of defense against abusive scraping or bots hitting a specific route.
"""