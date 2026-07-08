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

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority sorting | `Scheduler.sort_by_priority()` | Orders tasks high → medium → low priority, breaking ties by shorter duration first. |
| Chronological sorting | `Scheduler.sort_by_start_time()` | Re-sorts an already-scheduled plan by `start_time` (HH:MM string comparison), independent of priority order. |
| Time-budget filtering | `Scheduler.filter_by_time_budget()` | Greedily fills the day from `available_minutes`, skipping any task that no longer fits and recording it in `_skipped`. |
| Start-time assignment | `Scheduler._assign_start_times()` | Stamps each included task with a sequential clock time starting from `day_start_time`, based on cumulative duration. |
| Conflict detection | `Scheduler.detect_conflicts()` | Compares this plan's scheduled tasks against another pet's scheduled tasks and flags any overlapping `[start, start+duration)` time ranges as warnings. |
| Recurring tasks | `Task.mark_complete()` | Marks a task complete and, for `frequency="daily"`/`"weekly"` tasks, returns a new `Task` due one day/week later; non-recurring tasks return `None`. |
| Task filtering/aggregation | `Owner.get_all_tasks()`, `Owner.filter_tasks()` | Flattens tasks across all of an owner's pets, optionally narrowed by completion status and/or pet name. |

## 📸 Demo Walkthrough

**Main UI features:**
- Enter an owner name and add one or more pets (name, age, breed), shown in a live table.
- Select a pet and add care tasks (title, duration, priority), shown in that pet's task table.
- Set the available minutes for the day and generate a schedule for every pet at once.
- View each pet's plan as a table sorted by start time, with success/info/warning banners
  showing how many tasks were scheduled and which were skipped for lack of time.
- See a conflict-check section that flags any overlapping tasks between pets in red warning text.

**Example workflow:**
1. Enter an owner name (e.g., "Jordan") and add a pet (e.g., "Mochi", age 1, Tabby).
2. Select Mochi and add a few tasks with different priorities and durations
   (e.g., "Morning walk" - high, "Grooming" - low).
3. Set "Available minutes today" (e.g., 60) and click "Generate schedule."
4. Review Mochi's plan: tasks appear in a table ordered by start time, with any
   tasks that didn't fit in the time budget called out in a warning.
5. Add a second pet with an overlapping task time to see the conflict-check
   section flag the overlap in red.

**Key Scheduler behaviors demonstrated:**
- **Priority-first ordering**: `sort_by_priority()` puts high-priority tasks first when
  building the plan, so time-limited days favor what matters most.
- **Time-budget filtering**: `filter_by_time_budget()` greedily fits tasks into
  `available_minutes` and tracks anything that didn't fit as skipped.
- **Chronological sorting**: `sort_by_start_time()` re-orders the generated plan by
  clock time for display, independent of the priority order used to build it.
- **Conflict warnings**: `detect_conflicts()` compares two pets' scheduled plans and
  surfaces any overlapping time ranges as red warning messages in the UI.
- **Recurring tasks**: `mark_complete()` (exercised in `main.py`) advances a daily/weekly
  task's due date to generate its next occurrence when completed.

**Sample CLI output from running `main.py`:**

```bash
$ python main.py

Daily plan for Buddy (Labrador):
08:00 — Morning walk (30 min) [priority: high]
skipped Evening walk — insufficient time remaining
Reversed, then re-sorted by start_time:
  08:00 - Morning walk
-----
Daily plan for Whiskers (Tabby):
08:00 — Litter box cleaning (15 min) [priority: high]
08:15 — Nail trim (20 min) [priority: low]
Reversed, then re-sorted by start_time:
  08:00 - Litter box cleaning
  08:15 - Nail trim
-----
Checking for schedule conflicts between Buddy and Whiskers:
  Conflict: 'Morning walk' (Buddy) overlaps with 'Litter box cleaning' (Whiskers) at 08:00
  Conflict: 'Morning walk' (Buddy) overlaps with 'Nail trim' (Whiskers) at 08:00
Completed tasks across all pets:
  Grooming
  Feeding
Incomplete tasks for Buddy only:
  Evening walk
  Morning walk
  Grooming
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
