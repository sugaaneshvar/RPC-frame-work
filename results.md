# DA-1 RPC Marshalling Results

## What was implemented

- A lightweight Python RPC framework using JSON messages over TCP sockets.
- Remote invocation support for `calculate_grade_average(StudentProfile profile) -> float`.
- A `StudentProfile` data object with `name`, `id`, and `grades`.
- A marshalling-layer `validate_types()` function that validates incoming server-side payloads.

## Type validation behavior

`validate_types()` recursively checks the incoming payload against the expected schema.

- `name` must be a string
- `id` must be an integer
- `grades` must be a list of integers

If a client sends a string where an integer is expected, the server-side marshalling layer raises a `TypeError`.

Example invalid payload:

```python
{"name": "Bob", "id": "seven", "grades": [70, 80]}
```

Example error:

```text
payload.id expected int, received str
```

## Verification

Executed `python tests.py` locally.

Observed result:

```text
All tests passed.
```
