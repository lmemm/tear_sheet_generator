# Backlog

This is the project's ticketing system. Each ticket is a unit of work that Claude can pick up and execute independently.

**Rules:**
- Tickets are worked in priority order (top = highest priority) unless the PM specifies otherwise.
- Only one ticket should be in `🔵 In Progress` at a time.
- When you pick up a ticket, change its status to `🔵 In Progress`.
- When you finish a ticket, change its status to `✅ Done` and add a completion note.
- If a ticket is blocked or needs PM input, change its status to `🟡 Blocked` and explain why.
- Never delete tickets — mark them `❌ Won't Do` with a reason if they're cancelled.

**Statuses:** `⬚ Open` → `🔵 In Progress` → `✅ Done` | `🟡 Blocked` | `❌ Won't Do`

---

## Active Tickets

_(Tickets will be added after build planning session)_

---

## Completed Tickets

_(Move completed tickets here to keep the Active section clean)_

---

## Ticket Template

Copy this when creating new tickets:

```markdown
### T-XXX: [Title]
- **Status:** ⬚ Open
- **Priority:** P1 / P2 / P3
- **Type:** Feature / Bug / Refactor / Chore
- **Description:**
- **Acceptance criteria:**
  - [ ]
  - [ ] Tests pass
- **Files likely involved:**
- **Notes:**
- **Completion note:**
```
