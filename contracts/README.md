# Decentralized Grant Milestone Verifier

A standalone **GenLayer Intelligent Contract** primitive for verifying public milestone evidence and updating grant milestone states using consensus and equivalence checks.

## Overview
Grant programs and open-source bounties often rely on manual off-chain review to confirm whether a milestone deliverable has been published. This contract provides a reusable state and verification primitive where a milestone is registered on-chain and later evaluated against public web evidence.

## State Design
- `project_name`: Name of the grant or initiative.
- `owner`: Deployer/administrator address.
- `milestones`: `TreeMap[str, Milestone]` storing each milestone's ID, requirement description, submitted `evidence_url`, `approved` status, and `verification_summary`.

## Consensus & Equivalence Logic
- `verify_and_settle_milestone` fetches public text from `evidence_url` via `gl.get_webpage(...)` and evaluates completion against the milestone requirement using `gl.exec_prompt(...)`.
- Uses `gl.eq_principle.strict_eq(...)` on normalized JSON output (`approved` boolean and concise `reason`) so validators reach deterministic agreement on the structured verdict.

## Methods
- `register_milestone(milestone_id, description)`: Registers a new milestone in pending state.
- `verify_and_settle_milestone(milestone_id, evidence_url)`: Evaluates public evidence and updates milestone status.
- `get_milestone(milestone_id)`: Returns stored milestone details and verification verdict.
