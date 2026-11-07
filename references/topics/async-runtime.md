# Async Runtime Baseline

## Purpose

> **Scope:** Checkable constraints for projects built on an async task runtime - lock discipline,
> cancellation safety, bounded channels, backpressure, blocking work placement,
> shutdown ordering **Key items:** mutex-across-await, cancel-safe select branches, bounded queues,
> spawn-blocking, drain order

This file distills the Tokio tutorial and API documentation, the cancellation-safety literature,
and the async-pitfalls engineering guidance listed in `references/source-catalog.md` into
constraints an audit can verify from repository source.

Snapshot date: 2026-11-05.

Feeds `assessment/best-practices.md`, `assessment/design-principles.md`, `assessment/nfr-review.md`,
and `assessment/baseline-conformance.md` for subjects classified `service` or otherwise
async-runtime-bearing in `references/domain-profiles.md`.

The rules name Tokio because it dominates the Rust async service stack the corpus covers.
The same checks generalize to other task runtimes when the subject names a different one.

## Lock Discipline

From https://tokio.rs/tokio/tutorial/shared-state and
https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html.

- A blocking-mutex guard (`std::sync::Mutex`, `parking_lot`) is never held across an `.await`.
  The compiler only rejects the pattern when a `Send` bound forces it,
  and guard types that implement `Send` compile yet still deadlock or starve the worker thread.
  Restructure so the guard drops before the await,
  or wrap the state so only synchronous methods touch it.
- Locking never reenters: a function holding a lock must not call another function that
  takes the same lock.
  Locks live at the leaf, wrappers delegate,
  and lock-derived snapshots bind to `let` so the guard drops before further work.
- `tokio::sync::Mutex` is for state that must stay locked across an `.await` - a shared I/O
  resource, not plain data.
  It costs more than a blocking mutex and acquires in FIFO order,
  so its use on pure data paths is a finding when contention matters.
- Shared mutable state defaults to the actor pattern - a task owns the state and peers send messages
  - rather than a lock reached from many tasks.

## Cancellation Safety

From https://tokio.rs and https://sunshowers.io/posts/cancelling-async-rust/.

- Every `select!` branch resolves to a cancel-safe operation or documents why it may
  be dropped mid-flight.
  Cancelling loses queue position or partially consumed state on operations that are not
  cancel-safe, so branch choices carry a stated drop behavior.
- Dropped futures leave no broken invariant:
  code that must finish a critical section uses a completion mechanism (channel reply, guard object,
  or a task that owns the work) rather than relying on the future reaching its end.
- Timeouts bound waits; an unbounded `.await` on a peer, queue,
  or lock without a timeout or cancellation path is an operational finding.

## Channels And Backpressure

- Work queues between producers and consumers are bounded - `mpsc::channel(N)`, semaphore permits,
  or an equivalent limit.
  An `unbounded` channel on a load-bearing path converts slow consumers into
  unbounded memory growth.
- Slow-consumer policy is explicit: drop, disconnect,
  or block - each bounded endpoint names its overflow behavior.
- Connection, stream, and task counts carry caps enforced before resource allocation,
  matching the bounded-resource expectations of the service profile.

## Blocking Work Placement

- CPU-bound or blocking-syscall work runs off the async threads - `spawn_blocking`,
  a dedicated thread pool, or an equivalent seam.
  A blocking call on a worker thread stalls every task scheduled there.
- Blocking sections inside request handling are justified in-place or moved.

## Shutdown Ordering

- Shutdown is a sequence, not a flag: stop accepting new work, drain or cancel in-flight tasks,
  then join - with a stated bound on the drain wait.
- A `CancellationToken` or equivalent cooperative signal propagates to spawned tasks
  abrupt `abort()` on state-bearing tasks is a finding unless recorded.
- Persistent writers flush before exit - a graceful path that skips a durable commit
  loses acknowledged state.

## Live Check

The digested sources are live documents.

When a fetched version is available, fresh rules supersede this snapshot.
