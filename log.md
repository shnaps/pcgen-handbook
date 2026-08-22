# Log

Append-only record of ingest and lint runs. Newest last.

Each entry records what was scanned, at which upstream commit, and what changed.
This is what answers "is this current, and when was it last checked?".

Format:

```
## YYYY-MM-DD  <operation>
- upstream: PCGen @ <sha>
- <what changed>
```

---
