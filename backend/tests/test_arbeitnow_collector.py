import httpx

from app.collectors.arbeitnow import ArbeitnowCollector


def test_arbeitnow_collector_returns_normalized_jobs() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        return httpx.Response(
            200,
            json={
                "data": [
                    {
                        "title": "Backend Developer",
                        "company_name": "Example GmbH",
                        "location": "Berlin",
                        "url": "https://arbeitnow.com/jobs/123",
                    }
                ]
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    try:
        assert ArbeitnowCollector(client).get_jobs(limit=1) == [
            {
                "title": "Backend Developer",
                "company": "Example GmbH",
                "location": "Berlin",
                "url": "https://arbeitnow.com/jobs/123",
                "source": "arbeitnow",
            }
        ]
    finally:
        client.close()