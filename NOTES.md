# Notes

Personal learning log for the Wallet Ledger project. Each entry is something that actually clicked that day — this is raw material for later blog posts, not polished writing.

---

## 2026-06-28 — Day 1

### asyncpg vs psycopg2 (blocking vs non-blocking I/O)

While setting up Wallet Ledger's dependencies, I learned about `psycopg2` vs `asyncpg` for talking to PostgreSQL. `psycopg2` is the classic, most common driver — but it's **synchronous (blocking I/O)**. I didn't actually install it; it came up as the example of what *not* to do.

Since I'm building this with async FastAPI endpoints to handle I/O-bound work efficiently, a blocking driver would be a real problem: if `psycopg2` were called inside an `async def` endpoint, it wouldn't just block *that one request* — it would freeze the **entire single-threaded event loop**, so *every other concurrent request*, even ones completely unrelated to the database, would stall until that one query returned.

That's why I chose `asyncpg` instead — it's a non-blocking, async-native driver, so the event loop can keep serving other requests while waiting on the database.

### Layered vs vertical-slice architecture

When structuring the project, I had to choose between a **layered architecture** (`api/`, `services/`, `repositories/` — organized by technical concern) and a **vertical-slice architecture** (each feature, like accounts or transfers, gets its own self-contained module with its own router, service, and repository).

I was initially drawn to vertical slices because each feature is self-contained — no jumping between folders to understand one piece of functionality.

But I realized it's overkill for Stage 1 — and not just because I only have two or three features right now. The real reason: accounts, ledger entries, and transfers aren't actually *independent* features — they're all facets of **one aggregate** (the ledger). A transfer is literally two account balances plus a set of entries, so slicing it away from "accounts" would just mean constantly importing across "separate" modules anyway — fake decoupling, not real decoupling. Vertical slicing earns its cost when slices are genuinely independent domains; mine isn't yet.

Also worth remembering: choosing layers doesn't mean giving up dependency injection. DI (via FastAPI's `Depends()`) happens either way — folder layout and DI are two separate decisions. What I'm actually skipping is a dedicated DI-container library, which would solve a coupling problem this project doesn't have yet.

This won't be layered forever — once Stage 2 (webhooks/messaging) and Stage 3 (the AI feature) add genuinely separate concerns that don't share the ledger's aggregate, those are good candidates to become their own modules.
