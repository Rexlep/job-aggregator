import httpx

from app.collectors.base import BaseCollector, NormalizedJob


API_URL = "https://www.arbeitnow.com/api/job-board-api"


class ArbeitnowCollector(BaseCollector):
    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client

    def get_jobs(self, limit: int | None = None) -> list[NormalizedJob]:
        request_client = self.client or httpx.Client(timeout=15.0)
        try:
            response = request_client.get(API_URL)
            response.raise_for_status()
            jobs = response.json().get("data", [])
            normalized = [_normalize_job(job) for job in jobs]
            return normalized[:limit]
        finally:
            if self.client is None:
                request_client.close()


def _normalize_job(job: dict) -> NormalizedJob:
    return {
        "title": job.get("title", ""),
        "company": job.get("company_name", ""),
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        "source": "arbeitnow",
    }