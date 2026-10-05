# Design phase: turning a vague idea into a design

Adapted from obra/superpowers' `brainstorming`, rewritten to fit this project. Core idea: **think it through before acting, converge through dialogue, don't guess.**

## Block one anti-pattern first

> "Too simple to need approval."

Simple tasks are where unexamined assumptions waste the most work. The design can be short — two sentences in chat for a bounded change — but you MUST present it and get approval. What scales with simplicity is the paperwork, never the approval. No matter how small, pass this gate.

The path you picked in SKILL.md Step 0 (spike / bounded / architectural) decides how much of this file applies: a spike stops after presenting the probe; a bounded change uses context exploration, the questions, and a short in-chat design; the sections from "Propose approaches" onward are architectural depth.

Thoughts that mean you're about to skip the gate:

| Thought | What's actually true |
|---|---|
| "I'll call it bounded and skip the spec" | Reaching for a label to skip work is the doubt; take the heavier path |
| "The design is obvious, I'll start while they read it" | The gate is the approval, not the design's length; present, then stop until you hear yes |
| "I understand this kind of app, so it's bounded" | Bounded measures the repo; a new project has no existing flow, so it's architectural |
| "The spike works, so I'll keep the code" | A spike's output is an answer; keeping the code is a new request to classify |
| "It grew, but I'm almost done" | Hidden complexity upgrades the path mid-task; stop and say so |

## Explore context (before asking anything)

Read the relevant code, docs, and existing design first. Build your questions on top of "I've already looked at the current state" — don't ask about things that are already written in the files.

## How to ask

- **Only one question per message.** Draw out the real requirement; don't dump ten questions at once and let them get answered carelessly. If a topic needs more exploration, break it into multiple separate questions.
- **Prefer multiple-choice over open-ended.** Lower the decision cost; force a concrete answer.
- Aim questions at three things: **purpose** (what problem), **constraints** (what can't be touched, what must stay compatible), **success criteria** (what counts as done, how to verify).
- For this user's domain, common things to pin down: is this a one-off debug or a long-lived feature? Does it need to stay compatible with an existing protocol/interface? How long is data kept, and who sees it? What happens on failure?

## Write back your understanding

Before proposing any approach, play the requirement back in a short note the user can check at a glance:

- **Outcome**: what they want to end up with, and for whom.
- **Constraints**: what can't move.
- **Success criteria**: how you'll both know it's done.

Mark each line as **stated** (they said it) or **assumed** (you inferred it), and ask them to correct it. Fold their answer in; that corrected note is the design brief, and every later approach and feature gets checked against it. If the request already gave you purpose and constraints, reflect them back instead of asking again — keep it short; the point is the chance to correct, not the length.

## Propose approaches: 2–3, with trade-offs

Don't build the first idea. Propose 2–3 approaches and spell out each one's trade-offs (maintenance cost, compatibility, whether it means running a service, how well it fits the existing architecture). Let the user choose — don't decide for them.

### Strip the false constraints first

Before generating approaches, separate the constraints that are **real** (protocol spec, backward compatibility, an existing deployment you can't take down, a regulatory limit) from the ones that are merely **current state** (which framework is in the repo today, which tool you happen to have installed, how the last version did it). Name both lists out loud, then generate with only the real ones binding.

This matters because current state arrives inside the problem statement and reads like a constraint. Left in, every approach anchors to it and the "2–3 approaches" collapse into three variations of what already exists.

### When the fork is high-stakes, widen before narrowing

Default is still 2–3 approaches in one pass. Escalate to a wider search only when **both** hold: the fork is genuinely open (more than one design could work), and picking wrong is expensive (protocol/interface others depend on, data migration, something hard to reverse).

To escalate: dispatch independent explorations — one per lens, each in its own context so they can't converge on each other — then score and prune yourself. Rule out the first three obvious answers explicitly; those are what a single pass already produces. Lenses that pay off in this user's domain:

- **Middlebox view** — what does a NAT, firewall, or proxy in the path see and do to this?
- **Loss/degradation view** — what happens at 1% packet loss, on the third retransmit, on a flapping link?
- **CI-vs-local view** — what differs on a CI runner (no IPv6, different clock, no privileged port) that won't show up on your machine?
- **Standards-review view** — how would a spec reviewer reject this?
- **3am on-call view** — what does the person paged at 3am need to see, and what will they do wrong?
- **$0/hour view** — the version with no new service, no new dependency, no budget.

Then converge normally: shortlist with trade-offs, and flag the traps you found as watch-outs rather than verdicts.

**Deliberately not adopted from the upstream this pattern came from** (see `attribution.md`): its weighted scoring formula (model-invented 0–10 scores combined by fixed weights — that is exactly the fabricated-input habit `decision-lens` forbids), and its claim to cover fuzzy debugging (generating N hypotheses and deepening the top three, with no loop that tests them one at a time, is the pattern `systematic-debugging` exists to stop — debugging does not come here).

## Present the design in sections, approve each

Split the design into sections and present them one at a time; get a nod on each before moving on. Typical sections (scaled to complexity — one or two sentences for simple, a few paragraphs for complex):

- **Architecture**: the overall shape, the big pieces.
- **Components**: what each piece owns, where its boundaries are.
- **Data flow**: how data comes in, changes, goes out.
- **Error handling**: what happens on failure, edge cases.
- **Testing**: how you'll verify it's correct.

Approving section by section catches a misunderstanding while it's still small, instead of discovering the wrong direction after the whole design is written.

## Flag oversized scope

If one sentence actually means building a whole system (spanning several independent subsystems), say so on the spot and help split it into sub-projects, each with its own design. Don't quietly treat it as one task.

## Write the design doc

Once converged, write it to `docs/specs/YYYY-MM-DD-<topic>-design.md`. The content is exactly the sections you got approved, scaled to complexity.

## Self-review

After the design doc is written, before handing off, scan it yourself:

- **Placeholder scan**: any "fill in later", "TBD", "see elsewhere" left unwritten.
- **Internal consistency**: any contradictions.
- **Ambiguity**: anything vague enough that an engineer would have to come back and ask.
- **Scope**: any scope drift (quietly did something that wasn't agreed).

Once that's clean, present the written design for approval. Agreement during the conversation only authorized writing this document; approval of the document is what passes the gate into the plan phase — and that approval covers writing the plan, not executing it.
