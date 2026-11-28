# Skill Update Check

## Purpose

> **Scope:** The once-per-session upstream check and fast-forward update of this skill

> **Key items:** triggers, check script, reported state, gated merge

This file defines when and how the skill checks its upstream and applies an update.

## When This Applies

Follow it when a request names `improvement`, `development`, or `training` as a working mode,
or makes an explicit `update` or upstream-check request.

## Procedure

Run the check once per session when the request names `improvement`, `development`, or
`training` as a working mode, or makes an explicit `update` or upstream-check request -
on the bare `use` that carries the mode or on the mode-carrying task.
Reuse a check already attempted for this exact checkout in the session, unless the user
explicitly requests another one. Record the attempted checkout and result in session state.
Catalog queries and requests naming no mode use the installed package.

Use the skill root, the directory containing `SKILL.md`. Verify that it is the root of its own Git checkout
before running `python <skill-root>/scripts/check-update.py` with the available Python 3 launcher.
If Git, an upstream, or authorized network access is unavailable, use the installed package.
Report the limitation on an explicit request.

For `UPDATE-AVAILABLE`, report the incoming `tip_sha`, `tip_date`, and working-tree state.
After the user approves the reported update, run `git -C <skill-root> merge --ff-only <tip_sha>`
only if `ahead=0` and `dirty=no`, then re-read `SKILL.md` and the active procedures.
If the check or merge cannot run, report it for the requested maintenance operation and use the
installed files. A separately requested merge or push follows repository rules.

The check may update remote-tracking refs but leaves the working tree intact.
Review incoming changes if the upstream is uncertain.
