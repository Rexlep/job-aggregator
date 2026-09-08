import sys

import httpx

from app.collectors.jobvision import get_jobs


def main() -> None:
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        jobs = get_jobs()
        print(f"Fetched jobs: {len(jobs)}")
        for job in jobs:
            print(job)
    except httpx.HTTPStatusError as error:
        print(f"HTTP error: {error}")
    except httpx.RequestError as error:
        print(f"Request error: {error}")


if __name__ == "__main__":
    main()