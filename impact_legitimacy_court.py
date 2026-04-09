# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

import json
import typing


class ImpactLegitimacyCourt(gl.Contract):
    verdicts: DynArray[str]

    def __init__(self):
        pass

    @gl.public.write
    def investigate(
        self,
        project_name: str,
        project_website: str,
        impact_claim: str,
        category: str
    ) -> typing.Any:

        website = project_website
        name = project_name
        claim = impact_claim
        cat = category

        def get_verdict() -> typing.Any:
            web_data = gl.nondet.web.render(website, mode="text")

            task = f"""
You are a strict impact auditor for Web3 projects.

Project Name: {name}
Category: {cat}
Their Claim: {claim}

Website Content:
{web_data}
End of website content.

You MUST respond with ONLY this exact JSON structure and nothing else:
{{"score": 75, "rating": "Verified", "summary": "Your verdict here."}}

Rules:
- score is an integer 0-100
- rating is exactly one of: Verified, Suspicious, Fraud
- summary is one sentence only
- NO trailing commas
- NO line breaks inside the JSON
- NO extra text before or after
"""
            result = gl.nondet.exec_prompt(task)
            result = result.strip().replace("```json", "").replace("```", "").strip()
            print(result)
            return json.loads(result)

        result_json = gl.eq_principle.strict_eq(get_verdict)

        verdict_str = json.dumps({
            "project": project_name,
            "claim": impact_claim,
            "rating": result_json["rating"],
            "score": result_json["score"],
            "summary": result_json["summary"]
        })

        self.verdicts.append(verdict_str)

        return result_json

    @gl.public.view
    def get_verdicts(self) -> DynArray[str]:
        return self.verdicts