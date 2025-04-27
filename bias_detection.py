import re
from typing import List, Tuple

class BiasDetector:
    def __init__(self):
        # Define patterns that might indicate gender bias
        self.bias_patterns = [
            r'(women|female|girls?)\s+(should|must|need to|ought to)',
            r'(men|male|boys?)\s+(should|must|need to|ought to)',
            r'(women|female|girls?)\s+(can\'t|cannot|shouldn\'t|should not)',
            r'(men|male|boys?)\s+(can\'t|cannot|shouldn\'t|should not)',
            r'(women|female|girls?)\s+(belong|belongs)',
            r'(men|male|boys?)\s+(belong|belongs)',
            r'(women|female|girls?)\s+(are|is)\s+(too|very)\s+(emotional|sensitive)',
            r'(men|male|boys?)\s+(are|is)\s+(too|very)\s+(aggressive|dominant)'
        ]
        
        # Define positive reinforcement patterns
        self.positive_patterns = [
            r'(women|female|girls?)\s+(can|are able to|have the ability to)',
            r'(men|male|boys?)\s+(can|are able to|have the ability to)',
            r'(women|female|girls?)\s+(excel|succeed|achieve)',
            r'(men|male|boys?)\s+(excel|succeed|achieve)'
        ]

    def detect_bias(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect potential gender bias in the given text.
        Returns a tuple of (has_bias, detected_patterns)
        """
        detected_patterns = []
        has_bias = False
        
        for pattern in self.bias_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                has_bias = True
                detected_patterns.append(match.group())
        
        return has_bias, detected_patterns

    def suggest_mitigation(self, text: str) -> str:
        """
        Suggest a more inclusive alternative for potentially biased text.
        """
        # Basic mitigation suggestions
        mitigation_suggestions = {
            "should": "can consider",
            "must": "may choose to",
            "need to": "have the option to",
            "ought to": "might want to",
            "can't": "can explore alternative approaches to",
            "cannot": "can explore alternative approaches to",
            "shouldn't": "might consider alternative approaches to",
            "should not": "might consider alternative approaches to",
            "belong": "can contribute to",
            "are too": "may experience",
            "is too": "may experience"
        }
        
        mitigated_text = text
        for pattern, suggestion in mitigation_suggestions.items():
            mitigated_text = re.sub(
                rf'\b{pattern}\b',
                suggestion,
                mitigated_text,
                flags=re.IGNORECASE
            )
        
        return mitigated_text

    def check_positive_reinforcement(self, text: str) -> bool:
        """
        Check if the text contains positive reinforcement patterns.
        """
        for pattern in self.positive_patterns:
            if re.search(pattern, text.lower()):
                return True
        return False 