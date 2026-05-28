# Walkthrough: Cricket Scorecard API Fixes

This document provides a summary of the bug fixes made to the `Score.py` Cricket Scorecard API project, restoring its ability to simulate and record scorecards properly.

## What Was Fixed
1. **Custom User Model Compatibility**
   - **The Bug**: The file `verify_scorecard.py` was directly importing Django's default `User` model, which caused crashes because the project uses a custom user model located in `authentication.CustomUser`.
   - **The Fix**: The code was updated to use `get_user_model()` from `django.contrib.auth`. This ensures that the custom user model is fetched dynamically and safely.

## How to Verify
If you wish to test the functionality and see the final generated scorecard, you can run the provided verification script using the Django shell:

```bash
python manage.py shell -c "from verify_scorecard import run_verification; run_verification()"
```

You should see a successful run simulating an innings, capturing wickets and boundaries, and finally printing out a complete formatted scorecard without any errors!
