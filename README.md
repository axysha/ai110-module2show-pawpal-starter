# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Buddy (Labrador):
# 08:00 — Morning walk (30 min) [priority: high]
# skipped Grooming — insufficient time remaining
# -----
# Daily plan for Whiskers (Tabby):
# 08:00 — Litter box cleaning (15 min) [priority: high]
# 08:15 — Feeding (10 min) [priority: medium]
# -----
```

## 🧪 Testing PawPal+
* test_sort_by_start_time_orders_chronologically — Confirms that a schedule with tasks in scrambled order is returned sorted earliest-to-latest by start time.

* test_sort_by_start_time_empty_schedule_returns_empty_list — Confirms sorting a pet's empty schedule returns [] without error.

* test_sort_by_start_time_tie_keeps_both_tasks_in_original_order — Confirms two tasks at the identical start time both remain in the sorted output, in their original relative order.

```bash
# Run the full test suite:
python -m pytest tests/test_pawpal.py -v

# Run with coverage:
pytest tests/test_pawpal.py --cov=pawpal_system
```

Sample test output:

```
# Paste your pytest output here
tests/test_pawpal.py::test_mark_complete PASSED                                                                                           [  9%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED                                                                       [ 18%]
tests/test_pawpal.py::test_sort_by_start_time_orders_chronologically PASSED                                                               [ 27%]
tests/test_pawpal.py::test_sort_by_start_time_empty_schedule_returns_empty_list PASSED                                                    [ 36%]
tests/test_pawpal.py::test_sort_by_start_time_tie_keeps_both_tasks_in_original_order PASSED                                               [ 45%]
tests/test_pawpal.py::test_mark_complete_daily_task_creates_next_day_task PASSED                                                          [ 54%]
tests/test_pawpal.py::test_mark_complete_non_recurring_task_returns_none PASSED                                                           [ 63%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_times PASSED                                                                [ 72%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_start_times PASSED                                                            [ 81%]
tests/test_pawpal.py::test_detect_conflicts_back_to_back_tasks_do_not_conflict PASSED                                                     [ 90%]
tests/test_pawpal.py::test_detect_conflicts_with_no_tasks_returns_empty_list PASSED                                                       [100%]

============================================================== 11 passed in 0.05s ===============================================================

My overall confidence level for this system is 4. 
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
