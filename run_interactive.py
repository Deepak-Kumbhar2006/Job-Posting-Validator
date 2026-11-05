from pydantic import ValidationError

from job_board import JobPosting

FIELDS = [
    ("title", "Job title"),
    ("company", "Company"),
    ("url", "Job link (URL)"),
    ("salary_lpa", "Salary in LPA (optional)"),
    ("remote", "Remote? e.g. yes/no (optional)"),
    ("location", "Location (optional)"),
]


def ask_for_record() -> dict:
    record = {}
    try:
        for key, label in FIELDS:
            value = input(f"{label}: ")
            if value != "":  # truly empty -> leave the key out so defaults/required checks apply
                record[key] = value
    except EOFError:
        raise KeyboardInterrupt from None
    return record


def main() -> None:
    print("Job board bouncer. Enter a posting and see how Pydantic reacts.\n")
    while True:
        try:
            record = ask_for_record()
            try:
                job = JobPosting.model_validate(record)
            except ValidationError as exc:
                print("\nREJECTED")
                for err in exc.errors():
                    loc = err["loc"]
                    field = loc[0] if loc else "posting"
                    print(f"  - {field}: {err['msg']}")
            else:
                print("\nACCEPTED (cleaned data below)")
                print(job.model_dump_json(indent=2))

            try:
                choice = input("\nTry another? (y/n): ").strip().lower()
            except EOFError:
                print("\nGoodbye!")
                break
            if choice != "y":
                break
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
