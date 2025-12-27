import re

def is_comparative_claim(claim: str) -> bool:
    """
    Detects whether a claim is comparative (AND) or disjunctive (OR).
    Used to decide whether claim decomposition should be applied.
    """
    comparative_patterns = [
        r"and.*share\s+the\s+same",
        r"and.*both",
        r"and.*located\s+in\s+the\s+same",
        r"and.*same",
        r"one\s+of\s+.+\s+or\s+.+",
    ]
    
    for pattern in comparative_patterns:
        if re.search(pattern, claim, re.IGNORECASE):
            return True
    
    return False


def extract_property(claim: str) -> str:
    """
    Extracts a coarse-grained property from a disjunctive claim
    to formulate property-based sub-claims for NLI validation.
    """
    claim_lower = claim.lower()
    
    if 'older' in claim_lower or 'younger' in claim_lower:
        return 'age'
    if 'born' in claim_lower and ('earlier' in claim_lower or 'later' in claim_lower):
        return 'birth date'
    if 'from' in claim_lower or 'england' in claim_lower:
        return 'origin'
    if 'members' in claim_lower or 'had more' in claim_lower:
        return 'number of members'
    if 'instrument' in claim_lower and 'ratio' in claim_lower:
        return 'instrument-to-person ratio'
    if 'ancestors' in claim_lower:
        return 'ancestors'
    if 'animation' in claim_lower or 'known for' in claim_lower:
        return 'domain'
    
    return 'attribute'


def decompose_comparative_claim(claim: str) -> list[str]:
    """
    Decomposes comparative (AND) and disjunctive (OR) claims into simpler sub-claims.
    
    Comparative examples:
    - "X and Y share the same ATTRIBUTE"
      → ["X has ATTRIBUTE", "Y has ATTRIBUTE"]
    
    Disjunctive examples:
    - "One of X or Y ..."
      → ["There is information about PROPERTY X",
         "There is information about PROPERTY Y"]
    
    If no pattern matches, the original claim is returned.
    """
    
    sub_claims = []

    # -------- Comparative (AND) patterns --------
    
    match = re.match(
        r"^(.+?)\s+and\s+(.+?)\s+share\s+the\s+same\s+(.+?)\.?$",
        claim,
        re.IGNORECASE
    )
    if match:
        s1, s2, attr = map(str.strip, match.groups())
        return [f"{s1} has {attr}", f"{s2} has {attr}"]

    match = re.match(
        r"^(.+?)\s+and\s+(.+?)\s+are\s+both\s+(.+?)\.?$",
        claim,
        re.IGNORECASE
    )
    if match:
        s1, s2, pred = map(str.strip, match.groups())
        article = "an" if pred[0].lower() in "aeiou" else "a"
        return [f"{s1} is {article} {pred}", f"{s2} is {article} {pred}"]

    match = re.match(
        r"^(.+?)\s+and\s+(.+?)\s+are\s+located\s+in\s+the\s+same\s+(.+?)\.?$",
        claim,
        re.IGNORECASE
    )
    if match:
        s1, s2, loc = map(str.strip, match.groups())
        return [f"{s1} is located in {loc}", f"{s2} is located in {loc}"]

    match = re.match(
        r"^(.+?)\s+and\s+(.+?)\s+are\s+the\s+same\s+(.+?)\.?$",
        claim,
        re.IGNORECASE
    )
    if match:
        s1, s2, attr = map(str.strip, match.groups())
        return [f"{s1} is {attr}", f"{s2} is {attr}"]

    # -------- Disjunctive (OR) pattern --------
    
    match = re.match(
        r"^One\s+of\s+(.+?)\s+or\s+(.+?)\s+(?:is|was|has|have|had|does|do|did).+",
        claim,
        re.IGNORECASE
    )
    if match:
        s1, s2 = map(str.strip, match.groups())
        prop = extract_property(claim)
        return [
            f"There is information about {prop} {s1}.",
            f"There is information about {prop} {s2}."
        ]

    # -------- Fallback --------
    return [claim]
