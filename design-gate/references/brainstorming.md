# Design phase: turning a vague idea into a design

Adapted from obra/superpowers' `brainstorming`, rewritten to fit this project. Core idea: **think it through before acting, converge through dialogue, don't guess.**

## Block one anti-pattern first

> "This is too simple to need a design."

*"'Simple' projects are where unexamined assumptions cause the most wasted work."* The design can be short — a few sentences for a truly simple change — but you MUST present it and get approval. No matter how small, pass this gate.

## Explore context (before asking anything)

Read the relevant code, docs, and existing design first. Build your questions on top of "I've already looked at the current state" — don't ask about things that are already written in the files.

## How to ask

- **Only one question per message.** Draw out the real requirement; don't dump ten questions at once and let them get answered carelessly. If a topic needs more exploration, break it into multiple separate questions.
- **Prefer multiple-choice over open-ended.** Lower the decision cost; force a concrete answer.
- Aim questions at three things: **purpose** (what problem), **constraints** (what can't be touched, what must stay compatible), **success criteria** (what counts as done, how to verify).
- For this user's domain, common things to pin down: is this a one-off debug or a long-lived feature? Does it need to stay compatible with an existing protocol/interface? How long is data kept, and who sees it? What happens on failure?

## Propose approaches: 2–3, with trade-offs

Don't build the first idea. Propose 2–3 approaches and spell out each one's trade-offs (maintenance cost, compatibility, whether it means running a service, how well it fits the existing architecture). Let the user choose — don't decide for them.

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

Once that's clean and the user approves, pass the gate into the plan phase.
