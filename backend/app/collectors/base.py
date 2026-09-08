from abc import ABC, abstractmethod
from typing import TypedDict


class NormalizedJob(TypedDict):
    title: str
    company: str
    location: str
    url: str
    source: str


class BaseCollector(ABC):
    @abstractmethod
    def get_jobs(self, limit: int | None = None) -> list[NormalizedJob]:
        """Return normalized jobs from a single source."""