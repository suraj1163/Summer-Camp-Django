# Task List: Score.py Bug Fixes

- `[x]` Investigate ongoing errors in the `Score.py` project.
- `[x]` Discover that `verify_scorecard.py` fails due to improper instantiation of the `User` model, causing a conflict with `authentication.CustomUser`.
- `[x]` Update `verify_scorecard.py` to use `django.contrib.auth.get_user_model()` instead of directly importing `User`.
- `[x]` Verify that all dependencies and models are correctly utilizing the custom User model throughout the app.
- `[x]` Test the API using the verification script to ensure an entire innings logic flows without crashing.
- `[x]` Confirm 0 structural issues reported by `python manage.py check`.
- `[x]` Create documentation (`implementation_plan.md`, `walkthrough.md`, `task.md`) for the GitHub repository.
