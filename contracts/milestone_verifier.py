# { "Depends": "py-genlayer:test" }

from dataclasses import dataclass
import json
from genlayer import *


@allow_storage
@dataclass
class Milestone:
    milestone_id: str
    description: str
    evidence_url: str
    approved: bool
    verification_summary: str


class GrantMilestoneVerifier(gl.Contract):
    project_name: str
    owner: Address
    milestones: TreeMap[str, Milestone]

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.owner = gl.message.sender_address

    @gl.public.write
    def register_milestone(self, milestone_id: str, description: str) -> None:
        if milestone_id in self.milestones:
            raise gl.vm.UserError("Milestone ID already exists")

        self.milestones[milestone_id] = Milestone(
            milestone_id=milestone_id,
            description=description,
            evidence_url="",
            approved=False,
            verification_summary="Pending verification",
        )

    @gl.public.write
    def verify_and_settle_milestone(self, milestone_id: str, evidence_url: str) -> dict:
        if milestone_id not in self.milestones:
            raise gl.vm.UserError("Milestone ID not found")

        milestone = self.milestones[milestone_id]

        def fetch_and_evaluate() -> str:
            page_content = gl.get_webpage(evidence_url, mode="text")
            clipped_content = page_content[:4000]

            prompt = f"""
You are a strict grant milestone evaluator.
Project: {self.project_name}
Milestone Requirement: {milestone.description}
Public Evidence URL: {evidence_url}
Extracted Page Content:
\"\"\"{clipped_content}\"\"\"

Determine whether the evidence clearly demonstrates completion of the milestone requirement.
Respond ONLY with valid JSON in this exact format:
{{"approved": true or false, "reason": "concise factual explanation in one sentence"}}
"""
            result = gl.exec_prompt(prompt)
            cleaned = result.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.strip("`").replace("json", "", 1).strip()
            parsed = json.loads(cleaned)
            return json.dumps(
                {
                    "approved": bool(parsed.get("approved", False)),
                    "reason": str(parsed.get("reason", "No reason provided"))[:240],
                }
            )

        verdict_raw = gl.eq_principle.strict_eq(fetch_and_evaluate)
        verdict = json.loads(verdict_raw)

        milestone.evidence_url = evidence_url
        milestone.approved = verdict["approved"]
        milestone.verification_summary = verdict["reason"]
        self.milestones[milestone_id] = milestone

        return {
            "milestone_id": milestone_id,
            "approved": milestone.approved,
            "summary": milestone.verification_summary,
        }

    @gl.public.view
    def get_milestone(self, milestone_id: str) -> dict:
        if milestone_id not in self.milestones:
            return {"found": False}

        m = self.milestones[milestone_id]
        return {
            "found": True,
            "milestone_id": m.milestone_id,
            "description": m.description,
            "evidence_url": m.evidence_url,
            "approved": m.approved,
            "verification_summary": m.verification_summary,
        }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
