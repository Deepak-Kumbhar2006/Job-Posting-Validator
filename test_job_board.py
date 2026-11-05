import pytest
from pydantic import ValidationError

from quests.day02.job_board import JobPosting, parse_postings

GOOD = {"title": "ML Engineer Intern", "company": "Rynovi", "url": "https://rynovi.dev/jobs/1", "remote": True}

RAW = [
    {"title": "AI Engineer", "company": "Sarvam", "url": "https://jobs.example.com/1", "salary_lpa": "24", "remote": True},
    {"title": "  Data   Scientist ", "company": "Zepto", "url": "https://jobs.example.com/2", "location": "Mumbai"},
    {"title": "ML Intern", "company": "Swiggy", "url": "https://jobs.example.com/3", "salary_lpa": -5, "remote": True},
    {"title": "LLM Engineer", "company": "Krutrim", "url": "not-a-link", "remote": True},
    {"title": "Applied Scientist", "company": "Flipkart", "url": "https://jobs.example.com/5", "location": "Bengaluru", "salary_lpa": 32.5},
    {"title": "   ", "company": "Razorpay", "url": "https://jobs.example.com/6", "remote": True},
    {"title": "Backend + AI", "company": "CRED", "url": "https://jobs.example.com/7"},
    {"title": "GenAI Developer", "company": "Freshworks", "url": "https://jobs.example.com/8", "remote": "yes"},
    {"title": "MLOps Engineer", "company": "Meesho", "url": "https://jobs.example.com/9", "location": "Bengaluru"},
    {"company": "Ola", "url": "https://jobs.example.com/10", "remote": True},
]


def test_2_1_fields_and_defaults():
    job = JobPosting(**GOOD)
    assert job.title == "ML Engineer Intern" and job.company == "Rynovi"
    assert str(job.url) == "https://rynovi.dev/jobs/1"
    assert job.salary_lpa is None and job.remote is True


def test_2_1_salary_is_a_number():
    assert JobPosting(**GOOD, salary_lpa="12.5").salary_lpa == 12.5


def test_2_1_rejects_bad_salary_and_url():
    with pytest.raises(ValidationError):
        JobPosting(**GOOD | {"salary_lpa": -1})
    with pytest.raises(ValidationError):
        JobPosting(**GOOD | {"url": "rynovi dot dev"})


def test_2_2_title_is_cleaned():
    assert JobPosting(**GOOD | {"title": "  ML   Engineer  "}).title == "ML Engineer"


def test_2_2_emp_title_rejected():
    with pytest.raises(ValidationError, match="title can't be empty"):
        JobPosting(**GOOD | {"title": "    "})


def test_2_3_onsite_needs_location():
    with pytest.raises(ValidationError, match="location is required"):
        JobPosting(**GOOD | {"remote": False})
    assert JobPosting(**GOOD | {"remote": False, "location": "Pune"}).location == "Pune"


def test_2_4_splits_good_and_bad():
    valid, errors = parse_postings(RAW)
    assert [j.company for j in valid] == ["Sarvam", "Zepto", "Flipkart", "Freshworks", "Meesho"]
    assert len(errors) == 5


def test_2_4_error_format():
    _, errors = parse_postings(RAW)
    assert errors[0].startswith("record 2: salary_lpa: ")
    assert errors[1].startswith("record 3: url: ")
    assert errors[2].startswith("record 5: title: ")
    assert errors[3].startswith("record 6: posting: ")
    assert errors[4].startswith("record 9: title: ")
