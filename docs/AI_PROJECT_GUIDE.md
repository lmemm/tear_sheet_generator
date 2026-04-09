# AI-Managed Project System — How This Works

Use this document as context when starting a new project with Claude. It explains the system, your role, and how all the pieces fit together.

---

## The Mental Model

You are the project manager. Claude agents are your development team. Like any real team, the quality of the output depends on how clearly you define what needs to be built and how well the team's processes keep things on track.

Your job is to decide **what** gets built and **why**. Claude's job is to figure out **how** and to execute. The system described below is the structure that makes this work reliably.

---

## Your Role as PM

You are responsible for:

- **Defining the project** — Fill in `docs/ARCHITECTURE.md` with what you're building, what tech you're using, and how things connect. This doesn't need to be perfect on day one. Start rough and refine it.
- **Writing tickets** — Break the work into discrete tasks in `BACKLOG.md`. Each ticket should be small enough that Claude can complete it in a single session. Good tickets have clear acceptance criteria — specific, testable conditions that prove the work is done.
- **Prioritizing** — Order the backlog so Claude always knows what to work on next.
- **Reviewing** — Check the work after each session. Run the code. Look at the outputs. If something isn't right, write a bug ticket or refine the next ticket.
- **Requesting maintenance** — Periodically ask Claude to do a "review pass" to find bugs, dead code, duplication, and improvement opportunities.

You are **not** responsible for:

- Writing code
- Making implementation decisions (unless you want to — document them in `docs/DECISIONS.md`)
- Remembering what happened last session (that's what the project log and changelog are for)

---

## The Files and What They Do

### `CLAUDE.md` — The Employee Handbook
This is the first file Claude reads in every session. It contains:
- Instructions for how to pick up, implement, and complete tickets
- Project conventions (naming, linting, testing, commit style)
- The periodic review checklist for maintenance passes
- File layout reference

**When to edit:** When you want to change how Claude works — add a new convention, adjust the workflow, or add project-specific rules.

### `BACKLOG.md` — The Ticketing System
This is your task backlog. Every piece of work is a ticket with a status, priority, description, and acceptance criteria. Claude picks up the highest-priority open ticket, works it, and marks it done.

**When to edit:** Before every session. Add new tickets, reprioritize, or refine ticket descriptions based on what you've seen so far.

**How to write good tickets:**
- Be specific. "Build a dashboard" is bad. "Build a page that shows a table of all users with columns for name, email, and last login date, using the data from `src/users.py`" is good.
- Acceptance criteria are the most important part. These are the checklist Claude uses to know when it's done. Make them concrete and testable.
- Include which files are likely involved so Claude doesn't have to guess.
- Reference `docs/ARCHITECTURE.md` for context if the ticket touches a specific component.

### `docs/ARCHITECTURE.md` — The Knowledge Base
This is the persistent memory for the project. Since Claude doesn't remember previous sessions, this document is how it understands the system. It covers the tech stack, components, data flow, schemas, configuration, and constraints.

**When to edit:** At project start (fill in the basics) and whenever the architecture changes. If you find yourself re-explaining something to Claude, put it here instead.

### `docs/DECISIONS.md` — The Decision Log
Records why key choices were made. This prevents Claude from revisiting settled decisions or accidentally contradicting past choices.

**When to edit:** Whenever a significant "why" decision is made — choosing a framework, deciding on a data format, picking an approach over alternatives.

### `docs/CHANGELOG.md` — What Changed and When
Claude updates this automatically after each ticket. It gives you a quick way to see what's been done without reading the full project log.

### `docs/PROJECT_LOG.md` — Session History
Claude appends to this after every session. It records what was done, decisions made, and what to pick up next. It lives in `docs/` so it's committed to the repo and accessible to Claude across sessions (including Claude Code on the web).

**You shouldn't need to edit this** — Claude maintains it. But it's useful to read before a session to remember where things left off.

---

## The Workflow — Step by Step

### Starting a New Project

1. Copy the project template into a new repo.
2. Fill in `docs/ARCHITECTURE.md` with what you know so far — even a rough version is valuable.
3. Write your first few tickets in `BACKLOG.md`. Start with setup tasks (project skeleton, dependencies, config) before feature work.
4. Review `CLAUDE.md` and adjust any conventions for this specific project.
5. Hand it to Claude with a prompt like: *"Read CLAUDE.md and get oriented. Then pick up the first open ticket and implement it."*

### Running a Build Session

1. **Before the session:** Review `BACKLOG.md`. Make sure the next tickets are well-defined and prioritized.
2. **Start the session:** Point Claude at the repo. It will read `CLAUDE.md`, then `docs/ARCHITECTURE.md`, then `BACKLOG.md`, and start working.
3. **After the session:** Review what Claude built. Check the changelog and project log. Test the code. If something needs fixing, write a ticket for it.

### Running a Maintenance Pass

Periodically (every few sessions, or when the codebase feels messy), start a session with:

*"Read CLAUDE.md and do a full maintenance review. Check for bugs, consolidation opportunities, improvements, and dead code. Create tickets for anything you find."*

Claude will scan the codebase, and for each finding it will create a new ticket in `BACKLOG.md`. You then prioritize those tickets alongside feature work.

---

## Tips for Success

**Start small.** Your first few tickets should be simple and well-defined. This lets you calibrate how detailed your tickets need to be for Claude to execute well.

**Acceptance criteria are everything.** Vague criteria produce vague results. "It works" is not acceptance criteria. "Returns a list of dicts with keys `name`, `email`, `created_at`; returns empty list if no results; raises `ValueError` if connection fails" is acceptance criteria.

**One ticket, one concern.** A ticket that says "build the API and also set up the database and also write the tests for the user module" is three tickets. Break them apart.

**Update the architecture doc.** This is the one that people (including you) skip, and it's the one that causes the most problems. Every time Claude doesn't know how something connects, it's because the architecture doc is missing that information.

**Review the work.** This system is not "set and forget." You're the PM — your job is to check the output, catch issues early, and course-correct. The better you get at reviewing, the better your tickets get, and the better Claude's output gets. It's a feedback loop.

**Don't over-engineer the process.** This system is four markdown files. If you find yourself spending more time managing tickets than building, your tickets are too granular. If Claude keeps going off-track, your tickets aren't specific enough. Find the middle ground for your project.

---

## Quick Reference — Session Prompts

**Normal build session:**
> Read CLAUDE.md and get started. Pick up the next open ticket and implement it.

**Continue from last session:**
> Read CLAUDE.md and check the project log for where we left off. Continue with the next open ticket.

**Maintenance review:**
> Read CLAUDE.md and do a full maintenance review of the codebase. Create tickets for anything you find.

**Specific task outside the backlog:**
> Read CLAUDE.md and get oriented. Then [describe what you need]. When you're done, add a ticket to the backlog if there's follow-up work.

**Multiple tickets in one session:**
> Read CLAUDE.md and work through the open tickets in priority order. Complete as many as you can.
