"""Pydantic model and batch validation for job postings."""

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    ValidationError,
    field_validator,
    model_validator,
)


class JobPosting(BaseModel):
    title: str
    company: str
    url: HttpUrl
    salary_lpa: float | None = Field(default=None, ge=0)
    remote: bool = False
    location: str | None = None

    @field_validator("title")
    @classmethod
    def title_validator(cls, value: str) -> str:
        final = " ".join(value.split())
        if not final:
            raise ValueError("title can't be empty")
        return final

    @model_validator(mode="after")
    def on_site_validator(self):
        if not self.remote and not self.location:
            raise ValueError("location is required for on-site jobs")
        return self


def parse_postings(raw: list[dict]) -> tuple[list[JobPosting], list[str]]:
    """Validate records and return valid postings plus one error per invalid record."""
    valid_postings: list[JobPosting] = []
    errors: list[str] = []

    for index, record in enumerate(raw):
        try:
            valid_postings.append(JobPosting.model_validate(record))
        except ValidationError as exc:
            first_error = exc.errors()[0]
            location = first_error["loc"]
            field = location[0] if location else "posting"
            errors.append(f"record {index}: {field}: {first_error['msg']}")

    return valid_postings, errors
