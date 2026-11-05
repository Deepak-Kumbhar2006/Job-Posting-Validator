# Job Posting Validator

A small Python project that demonstrates how to validate and clean job-posting
data with **Pydantic v2**. It models each posting, normalizes job titles, checks
cross-field rules, and reports why invalid records were rejected. You can try
the validator with sample postings or enter a posting interactively.

## What it validates

The `JobPosting` model has these fields:

| Field          | Type               | Rules                                                                               |
| -------------- | ------------------ | ----------------------------------------------------------------------------------- |
| `title`      | string             | Required; leading, trailing, and repeated whitespace is cleaned up; cannot be blank |
| `company`    | string             | Required                                                                            |
| `url`        | URL                | Required; must be a valid URL                                                       |
| `salary_lpa` | number or `None` | Optional; cannot be negative                                                        |
| `remote`     | boolean            | Defaults to `False`                                                               |
| `location`   | string or `None` | Optional for remote jobs; required for on-site jobs                                 |

`parse_postings()` processes a list of records and returns the valid
`JobPosting` objects and one readable validation error for each rejected record.

## Requirements

- Python 3.10 or newer
- Pydantic 2
- Pytest (only needed to run the tests)

## Setup

Run these commands from the project directory. Create and activate a virtual
environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install "pydantic>=2,<3" pytest
```

On macOS or Linux, activate the virtual environment with:

```sh
source .venv/bin/activate
```

## Run the project

Run the sample validation demo:

```sh
python -m quests.day02.run_board
```

Start the interactive validator and follow the prompts:

```sh
python -m quests.day02.run_interactive
```

The interactive program asks for a title, company, job URL, and optional salary,
remote status, and location. Enter `y` when prompted to validate another
posting; any other response exits.

## Run the tests

From the project directory, run:

```sh
python -m pytest -v
```

## Use the validator in Python

```python
from quests.day02.job_board import JobPosting, parse_postings

posting = JobPosting(
    title="  ML   Engineer ",
    company="Example",
    url="https://example.com/jobs/1",
    remote=True,
)
print(posting.title)  # ML Engineer

records = [
    {
        "title": "Data Scientist",
        "company": "Example",
        "url": "https://example.com/jobs/2",
        "location": "Mumbai",
    }
]
valid_postings, errors = parse_postings(records)
```

## Project layout

```text
quests/day02/job_board.py       Pydantic model and batch validation
quests/day02/run_board.py       Sample-data demo
quests/day02/run_interactive.py Interactive prompt
test_job_board.py               Automated tests
```
