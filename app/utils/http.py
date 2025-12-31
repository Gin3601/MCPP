# app/utils/http.py
import time
import requests
from app.config import settings


class APIRequestError(RuntimeError):
    """302 API 请求失败（网络 / 5xx / 4xx / 非预期响应）"""

    def __init__(self, message: str, status_code: int | None = None, response_text: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


session = requests.Session()
# 避免容器/宿主机的代理环境变量影响请求（特别是 corporate proxy / mitm）
session.trust_env = False


def _clean_str(v: str | None) -> str:
    return (v or "").strip().strip('"').strip("'")


def _clean_url(url: str | None) -> str:
    u = _clean_str(url)
    return u


def _clean_key(key: str | None) -> str:
    k = _clean_str(key)
    # 兼容用户误把 "Bearer xxx" 写进 env
    if k.lower().startswith("bearer "):
        k = k.split(" ", 1)[1].strip()
    return k


def _headers(api_key: str | None) -> dict:
    k = _clean_key(api_key or settings.API_KEY)
    return {
        "Authorization": f"Bearer {k}",
        "Content-Type": "application/json",
    }


def post_edit(
    payload: dict,
    api_url: str | None = None,
    api_key: str | None = None,
    timeout: int = 180,
) -> dict:
    """
    调用 302 的 edit 接口。

    兼容两种调用方式：
    - post_edit(payload)  -> 使用 settings.API_URL / settings.API_KEY
    - post_edit(payload=..., api_url=..., api_key=...) -> 调用方显式指定
    """
    url = _clean_url(api_url or settings.API_URL)
    if not url:
        raise APIRequestError("API_URL is empty. Check your .env / settings loading.")
    if not (url.startswith("http://") or url.startswith("https://")):
        raise APIRequestError(f"Invalid API_URL: {url!r}")

    headers = _headers(api_key)

    try:
        resp = session.post(url, headers=headers, json=payload, timeout=timeout)
    except requests.RequestException as e:
        raise APIRequestError(f"Network error: {e}") from e

    if resp.status_code >= 500:
        raise APIRequestError(
            message=f"Upstream API returned {resp.status_code}: {(resp.text or '')[:1500]}",
            status_code=resp.status_code,
            response_text=(resp.text or "")[:1500],
        )

    if resp.status_code >= 400:
        text = (resp.text or "")[:1500]
        raise APIRequestError(
            message=f"Upstream API returned {resp.status_code}: {text}",
            status_code=resp.status_code,
            response_text=text,
        )

    try:
        return resp.json()
    except ValueError:
        raise APIRequestError(
            message="Invalid JSON response",
            status_code=resp.status_code,
            response_text=(resp.text or "")[:500],
        )


def get_json(
    url: str,
    api_key: str | None = None,
    timeout: int = 60,
) -> dict:
    """
    GET 一个 JSON（用于轮询 result_url）
    """
    u = _clean_url(url)
    if not u:
        raise APIRequestError("result_url is empty")
    if not (u.startswith("http://") or u.startswith("https://")):
        raise APIRequestError(f"Invalid result_url: {u!r}")

    headers = _headers(api_key)

    try:
        resp = session.get(u, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        raise APIRequestError(f"Network error: {e}") from e

    if resp.status_code >= 400:
        text = (resp.text or "")[:1500]
        raise APIRequestError(
            message=f"Upstream GET returned {resp.status_code}: {text}",
            status_code=resp.status_code,
            response_text=text,
        )

    try:
        return resp.json()
    except ValueError:
        raise APIRequestError(
            message="Invalid JSON response (GET)",
            status_code=resp.status_code,
            response_text=(resp.text or "")[:500],
        )


def wait_for_outputs(
    result_url: str,
    api_key: str | None = None,
    timeout_seconds: int = 180,
    poll_interval: float = 1.0,
) -> dict:
    """
    轮询 302 的 result_url，直到 outputs 有内容或失败/超时。
    返回最终的 JSON 响应（和 post_edit 返回结构一致，通常包含 data）。
    """
    start = time.time()
    last: dict | None = None

    while True:
        last = get_json(result_url, api_key=api_key, timeout=60)

        data = last.get("data") if isinstance(last, dict) else None
        if not isinstance(data, dict):
            # 兜底：有些返回可能不包 data
            data = last if isinstance(last, dict) else {}

        status = (data.get("status") or "").lower()
        outputs = data.get("outputs") or []

        if outputs:
            return last

        if status in {"completed", "succeeded"}:
            # completed 但 outputs 为空，视为异常
            raise APIRequestError(f"Task completed but outputs empty: {data}")

        if status in {"failed", "canceled", "cancelled", "error"}:
            raise APIRequestError(f"Upstream task {status}: {data.get('error') or data}")

        if time.time() - start > timeout_seconds:
            raise APIRequestError(f"Timeout waiting for outputs. Last status={status}, data={data}")

        time.sleep(poll_interval)


def download_file(url: str, timeout: int = 180) -> bytes:
    u = _clean_url(url)
    if not u:
        raise APIRequestError("download url is empty")
    try:
        r = session.get(u, timeout=timeout)
        r.raise_for_status()
        return r.content
    except requests.RequestException as e:
        raise APIRequestError(f"Download failed: {e}") from e
