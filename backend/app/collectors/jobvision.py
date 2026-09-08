import httpx


API_URL = "https://candidateapi.jobvision.ir/api/v1/JobPost/List"
PAGE_URL = "https://jobvision.ir/jobs/category/developer"


def get_jobs(
    page: int = 1,
    page_size: int = 30,
    limit: int | None = None,
    client: httpx.Client | None = None,
) -> list[dict[str, str]]:
    """Return normalized jobs from JobVision's developer category."""
    if limit is not None:
        page_size = limit

    request_client = client or httpx.Client(timeout=15.0)
    should_close = client is None

    try:
        response = request_client.post(
            API_URL,
            headers={
                "User-Agent": "job-aggregator-development/1.0",
                "Content-Type": "application/json",
                "page-route": PAGE_URL,
                "web-app-version": "19.0.164",
                "clientid": "60589589",
                "ngsw-bypass": "true",
            },
            json={
                "pageSize": page_size,
                "requestedPage": page,
                "jobCategoryUrlTitle": "developer",
                "sortBy": 1,
                "searchId": None,
            },
        )
        response.raise_for_status()
        payload = response.json()
        job_posts = payload.get("data", {}).get("jobPosts", [])

        return [_normalize_job(job) for job in job_posts[:limit]]
    finally:
        if should_close:
            request_client.close()


def _normalize_job(job: dict) -> dict[str, str]:
    return {
        "title": job.get("title", ""),
        "company": (job.get("company") or {}).get("nameFa", ""),
        "location": _format_location(job.get("location")),
        "url": f"https://jobvision.ir/jobs/{job.get('id')}",
        "source": "jobvision",
    }


def _format_location(location: object) -> str:
    if not isinstance(location, dict):
        return ""

    province = (location.get("province") or {}).get("titleFa", "")
    city = (location.get("city") or {}).get("titleFa", "")
    return ", ".join(part for part in (city, province) if part)