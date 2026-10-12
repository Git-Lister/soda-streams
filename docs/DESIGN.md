# Final Core Documents (v1.0)

All personal MMU names removed. "Git-Lister" used as the GitHub handle. "The maintainer" used for role-based references. "SODA" and "MMU" retained as institutional context. All four documents printed in full for the record.

---

# DESIGN.md

```markdown
# Soda-Streams — Design Specification

> A shared repository of AI workflows and processes — by SODA, for SODA —
> that makes sincere experimentation possible across teaching, research,
> and knowledge exchange.

## 1. Problem Statement

SODA has the culture, the people, and the infrastructure for creative
technology. It has VR labs, virtual production studios, motion capture,
and a community of staff and students who are already experimenting with AI.

What's missing is the **connective tissue** — a way to share *processes*,
not just outputs. Right now, if a student figures out a ComfyUI workflow
for character design, that knowledge lives in their head, in a Discord
message, or in a file on their laptop. It doesn't become part of SODA's
shared capability.

AI is the connective tissue. Soda-Streams is the repository that makes it
visible, versioned, and co-creatable. It's not a platform. It's not a
service. It's a convention — a way of working that makes SODA's AI practice
legible and shareable.

## 2. Design Principles

**Porous edges.** Low-friction access. GitHub-based contribution. No maze
of permissions. Anyone at SODA can browse, run, and fork a workflow
without asking.

**Defined boundaries.** A metadata schema. A three-tier system. A
governance framework. Not to prevent exploration, but to make it safe.

**Prepared cleanup.** Provenance tracking. Incident response. Clear
escalation paths. We expect some sand to fall outside the box — the
question is whether we're ready when it does.

**Make the meal, not the menu.** Every workflow is a complete, runnable
thing — not a tutorial, not a diagram, not a link to a tool. The user can
run it, modify it, and extend it.

## 3. User Stories

1. **As a games design student**, I want to generate character concept
   art using AI so I can iterate quickly before committing to Blender.
2. **As a filmmaking lecturer**, I want to demonstrate AI-assisted
   storyboarding so students understand the workflow and its limits.
3. **As a researcher**, I want a RAG pipeline for literature review so I
   can synthesise sources with citations.
4. **As an audio student**, I want voice synthesis for a project so I can
   prototype dialogue without recording.
5. **As a motion capture student**, I want webcam-based pose capture for
   previsualisation so I can rough out a scene before booking the Vicon
   studio.
6. **As a student contributor**, I want to share my own workflow so others
   can build on it.
7. **As a member of staff**, I want to see what AI workflows exist at SODA
   so I can point students to them.
8. **As an external partner**, I want to understand SODA's AI capabilities
   so I can explore collaboration.

## 4. Scope Boundaries

**Soda-Streams is not:**
- A platform or service in the traditional sense
- A replacement for institutional AI platforms
- A physical space
- A top-down institutional initiative
- A collection of outputs
- A proprietary tool
- A research project
- A teaching module

**Soda-Streams is:**
- A repository and a convention
- A specialist complement to institutional platforms
- A shared working environment
- A grassroots, community-driven resource
- A collection of processes
- Open-source first, pragmatic about paid tools
- A support structure for research
- A resource for teaching

## 5. Constraint Register

**Compute.** Unknown at SODA scale. Prototype runs local-first; production
scales to SODA infrastructure.

**Policy.** Must align with MMU AI guidance, GDPR, IT acceptable use. The
governance framework references institutional policy without requiring
top-down approval for community/experimental tiers.

**Politics.** Position as a SODA-specific implementation of the university's
AI strategy, not a parallel initiative. Complementary to central IT, not
competitive.

**Time.** Prototype for demonstration credibility, not production readiness.

## 6. Success Criteria

1. Four workflows packaged and runnable (ComfyUI, RAG, audio, MediaPipe)
2. A student or staff member can discover and run a workflow without
   guidance
3. Provenance metadata is captured for every workflow
4. The LLM assistant can answer questions about repository contents
5. The governance framework is documented and legible
```
