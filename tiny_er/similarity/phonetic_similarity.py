from typing import Dict, Any
from ..core.data_structures import Entity
from ..core.base_classes import SimilarityMeasure

class SoundexSimilarity(SimilarityMeasure):
    def __init__(self, config: Dict[str, Any]):
        self.field = config.get('field', 'name')

    def compute(self, entity1: Entity, entity2: Entity) -> float:
        code1 = self._soundex(str(entity1.attributes.get(self.field, '')))
        code2 = self._soundex(str(entity2.attributes.get(self.field, '')))
        return 1.0 if code1 == code2 else 0.0

    def _soundex(self, word: str) -> str:
        word = word.upper()
        soundex = word[0]
        
        # Soundex digit mappings
        digit_map = {'BFPV': '1', 'CGJKQSXZ': '2', 'DT': '3', 'L': '4', 'MN': '5', 'R': '6'}
        
        for char in word[1:]:
            for key in digit_map:
                if char in key:
                    if digit_map[key] != soundex[-1]:
                        soundex += digit_map[key]
                    break
        
        soundex = soundex.ljust(4, '0')[:4]
        return soundex

class MetaphoneSimilarity(SimilarityMeasure):
    def __init__(self, config: Dict[str, Any]):
        self.field = config.get('field', 'name')

    def compute(self, entity1: Entity, entity2: Entity) -> float:
        code1 = self._metaphone(str(entity1.attributes.get(self.field, '')))
        code2 = self._metaphone(str(entity2.attributes.get(self.field, '')))
        return 1.0 if code1 == code2 else 0.0

    def _metaphone(self, word: str) -> str:
        word = word.upper()
        # This is a simplified version of the Metaphone algorithm
        # A full implementation would be more complex
        result = ''
        skip_next = False
        for i, char in enumerate(word):
            if skip_next:
                skip_next = False
                continue
            if char in 'AEIOU':
                if i == 0:
                    result += char
            elif char == 'B':
                result += 'B'
            elif char == 'C':
                if i + 1 < len(word) and word[i+1] in 'EIY':
                    result += 'S'
                else:
                    result += 'K'
            elif char == 'D':
                result += 'T'
            elif char == 'G':
                if i + 1 < len(word) and word[i+1] in 'EIY':
                    result += 'J'
                else:
                    result += 'K'
            elif char in 'FJLMNR':
                result += char
            elif char == 'Q':
                result += 'K'
            elif char == 'V':
                result += 'F'
            elif char in 'WH':
                if i == 0:
                    result += 'W'
            elif char == 'X':
                result += 'KS'
            elif char == 'Y':
                if i == 0:
                    result += 'Y'
            elif char == 'Z':
                result += 'S'
            elif char == 'P':
                if i + 1 < len(word) and word[i+1] == 'H':
                    result += 'F'
                    skip_next = True
                else:
                    result += 'P'
            elif char == 'S':
                if i + 1 < len(word) and word[i+1] == 'H':
                    result += 'X'
                    skip_next = True
                else:
                    result += 'S'
            elif char == 'T':
                if i + 1 < len(word) and word[i+1] == 'H':
                    result += '0'
                    skip_next = True
                else:
                    result += 'T'
        return result

def create_phonetic_similarity_measure(config: Dict[str, Any]):
    method = config.get('method', 'soundex')
    if method == 'soundex':
        return SoundexSimilarity(config)
    elif method == 'metaphone':
        return MetaphoneSimilarity(config)
    else:
        raise ValueError(f"Unsupported phonetic similarity method: {method}")