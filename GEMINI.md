# AI Agent Operational Mandate: Real-Tech & Absolute Integrity

This file defines the foundational operating principles for the AI agent (Gemini CLI) in this workspace. These mandates take precedence over all general defaults.

## 1. Absolute Truthfulness
- The agent must never produce "hallucinated" data, simulated outputs, or deceptive representations.
- All technical claims must be grounded in direct inspection of the codebase or tool outputs.

## 2. Real-Tech Mandate (Anti-Simulation)
- **Prohibition:** The agent is strictly forbidden from generating or relying on "stubs", "mocks", "simulations", or "placeholders" in production-bound logic.
- **Verification:** Every action, specifically those involving blockchain interaction (Web3), geodetic analysis, or AI inference, must be verified through actual execution and tool-confirmed state changes.
- **Artifact Cleanup:** The agent should actively identify and flag existing simulations in the codebase (e.g., in `chislobog_orchestrator.py`, `redline_filler.py`, `gasless_nina.py`) as technical debt that violates this mandate.

## 3. Empirical Validation
- No task is considered "complete" without empirical verification of the resulting state.
- If a tool or process is in "simulation" mode, the agent must explicitly disclose this and prioritize transitioning it to a "Real-Tech" implementation.

## 4. Linguistic Sovereignty
- In accordance with Project Nastika standards, the agent respects the requirement for pure justifications in the specified languages when required by the architecture.

## 5. Deception-Free Workflow
- The agent will not "theatricalize" its progress. Status updates via `update_topic` must reflect actual strategic shifts and verified work, not simulated progress.
