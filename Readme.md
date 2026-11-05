# Job Posting Validator (Pydantic v2)

A "bouncer" for a job board: it takes messy scraped job postings, lets clean ones
through as typed models, and rejects bad ones with a clear reason.

## Features

- `JobPosting` model with typed fields, non-negative salary and URL validation
- Field validator that cleans titles (`"  ML   Engineer "` -> `"ML Engineer"`)
- Model validator: on-site jobs must have a location
- `parse_postings()` returns valid postings plus one error line per bad record
- Extras: all errors per record, JSON in/out (`clean.json`, `rejected.txt`), interactive CLI

## Run it

    pytest quests/day02 -v
    python -m quests.day02.run_board
    python -m quests.day02.run_interactive

## What I learned

- **Type coercion:** in lax mode `"24"` becomes `24.0` and `"yes"` becomes `True`;
  invalid values like `"abc"` or `"maybe"` are rejected. `strict=True` would reject
  the strings too.
- **Field vs model validator:** a field validator checks or cleans one field
  (the title). A model validator is needed when a rule compares several fields
  (`remote` and `location`). It runs after the field checks pass, so a record with
  a bad URL and a missing location reports only the URL error first.

---
