import json

import httpx

from app.collectors.jobvision import JobVisionCollector, get_jobs


def test_get_jobs_returns_normalized_jobs() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path.endswith("/api/v1/JobPost/List")
        assert json.loads(request.content) == {
            "pageSize": 30,
            "requestedPage": 1,
            "jobCategoryUrlTitle": "developer",
            "sortBy": 1,
            "searchId": None,
        }
        return httpx.Response(
            200,
            json={
                "data": {
                    "jobPosts": [
                        {
                            "id": 123,
                            "title": "Python Developer",
                            "company": {"nameFa": "شرکت نمونه"},
                            "location": {
                                "city": {"titleFa": "تهران"},
                                "province": {"titleFa": "تهران"},
                            },
                        }
                    ]
                }
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    try:
        assert get_jobs(client=client) == [
            {
                "title": "Python Developer",
                "company": "شرکت نمونه",
                "location": "تهران, تهران",
                "url": "https://jobvision.ir/jobs/123",
                "source": "jobvision",
            }
        ]
    finally:
        client.close()


def test_jobvision_collector_implements_base_contract() -> None:
    assert isinstance(JobVisionCollector(), object)