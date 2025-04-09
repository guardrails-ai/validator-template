from typing import Any, Callable, Dict, Optional

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)

_DEFAULT_REQUEST = "Make one or more claims about information in the documents."

_CLAIM_FORMAT_STRING = """Claim: {claim_string}
Subclaims:
{subclaims_string}

Citations:
{citations_string}

Explanation: {explanation_string}"""

from nltk.tokenize import sent_tokenize

def create_prompt(context: str, request: str, response: str) -> str:
    """Generates a prompt for the generative HallOumi model."""

    def _split_into_sentences(text: str) -> list[str]:
        sentences = sent_tokenize(text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def _annotate_sentences(sentences: list[str], annotation_char: str) -> str:
        annotated_sentences = []
        for idx, sentence in enumerate(sentences, start=1):
            annotated_sentences.append(
                f"<|{annotation_char}{idx}|><{sentence}><end||{annotation_char}>"
            )
        return "".join(annotated_sentences)

    # Context: Split it into sentences and annotate them.
    context_sentences = _split_into_sentences(context)
    annotated_context_sentences = _annotate_sentences(context_sentences, "s")
    annotated_context = f"<|context|>{annotated_context_sentences}<end||context>"

    # Request: Annotate the request.
    annotated_request = f"<|request|><{request.strip()}><end||request>"

    # Response: Split it into sentences and annotate them.
    response_sentences = _split_into_sentences(response)
    annotated_response_sentences = _annotate_sentences(response_sentences, "r")
    annotated_response = f"<|response|>{annotated_response_sentences}<end||response>"

    # Combine all parts into the final prompt.
    return f"{annotated_context}{annotated_request}{annotated_response}", context_sentences, response_sentences

import contextlib
from dataclasses import dataclass, field


@dataclass
class Claim:
    claim_id: int = -1
    claim_string: str = ""
    subclaims: list[str] = field(default_factory=list)
    citations: list[int] = field(default_factory=list)
    rationale: str = ""
    supported: bool = True


def get_claims_from_response(response: str) -> list[Claim]:
    """Extracts claims from the response string."""

    def _get_claim_id_from_subsegment(subsegment: str) -> int:
        claim_id_part = subsegment.split("|")[1]
        claim_id_no_r = claim_id_part.lstrip("r")
        return int(claim_id_no_r)

    def _get_claim_citations_from_subsegment(subsegment: str) -> list[int]:
        citation_segments = subsegment.split(",")
        citations = []
        for citation_segment in citation_segments:
            citation = citation_segment.replace("|", "").replace("s", "").strip()
            if "-" in citation:
                start, end = map(int, citation.split("-"))
                citations.extend(range(start, end + 1))
            elif "to" in citation:
                start, end = map(int, citation.split("to"))
                citations.extend(range(start, end + 1))
            else:
                with contextlib.suppress(ValueError):
                    citation_int = int(citation)
                    citations.append(citation_int)
        return citations

    def _get_claim_from_segment(segment: str) -> Claim:
        claim_segments = segment.split("><")
        claim = Claim()
        claim.claim_id = _get_claim_id_from_subsegment(claim_segments[0])
        claim.claim_string = claim_segments[1]

        subclaims = []
        claim_progress_index = 3  # start parsing subclaims from index 3
        for i in range(claim_progress_index, len(claim_segments)):
            subsegment = claim_segments[i]
            if subsegment.startswith("end||subclaims"):
                claim_progress_index = i + 1
                break
            subclaims.append(subsegment)

        citation_index = -1
        rationale_index = -1
        label_index = -1

        for i in range(claim_progress_index, len(claim_segments)):
            subsegment = claim_segments[i]
            if subsegment.startswith("|cite|"):
                citation_index = i + 1
            elif subsegment.startswith("|explain|"):
                rationale_index = i + 1
            elif subsegment.startswith("|supported|") or subsegment.startswith(
                "|unsupported|"
            ):
                label_index = i

        claim.subclaims = subclaims
        claim.citations = (
            _get_claim_citations_from_subsegment(claim_segments[citation_index])
            if citation_index != -1
            else []
        )
        claim.rationale = (
            claim_segments[rationale_index] if rationale_index != -1 else ""
        )
        claim.supported = (
            claim_segments[label_index].startswith("|supported|")
            if label_index != -1
            else True
        )
        return claim

    segments = response.split("<end||r>")
    claims = []
    for segment in segments:
        if segment.strip():
            claim = _get_claim_from_segment(segment)
            claims.append(claim)
    return claims

@register_validator(name="oumi-ai/halloumi_validator", data_type="string")
class HallOumiValidator(Validator):
    """Validates that {fill in how you validator interacts with the passed value}.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `oumi-ai/halloumi_validator`   |
    | Supported data types          | `string`                          |
    """  # noqa

    def validate(self, context: str, response: str, request: str = _DEFAULT_REQUEST, metadata: Dict = {}) -> ValidationResult:
        """Validates that {fill in how you validator interacts with the passed value}."""
        # Add your custom validator logic here and return a PassResult or FailResult accordingly.
        prompt = create_prompt(context, request, response)
        # Call model
        response = "" # TODO: Clarify calling requirements
        claims = get_claims_from_response(response)
        unsupported_claims = [c for c in claims if not c.supported]
        if len(unsupported_claims) == 0:
            return PassResult()
        
        error_message = create_error_message(unsupported_claims)

        return FailResult(
            error_message=error_message,
        )

def create_error_message(unsupported_claims: list[Claim]):
    error_strings = [claim_to_string(c) for c in unsupported_claims]

    return f"Found {len(error_strings)} unsupported claim(s):\n\n{"\n\n".join(error_strings)}"

def claim_to_string(claim: Claim, context_sentences: list[str], response_sentences: list[str]):
    claim_text = response_sentences[claim.claim_id - 1]
    text_citations = []
    for c in claim.citations:
        text_citations.append(context_sentences[c-1])
    
    return _CLAIM_FORMAT_STRING.format(
        claim_string=claim_text,
        subclaims_string='- ' + "\n- ".join(claim.subclaims),
        citations_string='- ' + "\n- ".join(text_citations),
        explanation_string=claim.rationale
    )
    

