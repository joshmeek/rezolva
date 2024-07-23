from typing import List, Dict, Any
from start_er import Entity, EntityResolver
import json

class ResolutionVisualizer:
    def __init__(self, resolver: EntityResolver):
        self.resolver = resolver

    def visualize_resolution(self, entity: Entity) -> str:
        visualization = f"Resolution process for Entity {entity.id}\n"
        visualization += "=" * 60 + "\n\n"

        # Model Information
        visualization += "0. Model Information\n"
        visualization += self._visualize_model_info()

        # Preprocessing
        visualization += "\n1. Preprocessing\n"
        preprocessed_entity = self.resolver.preprocessor.preprocess(entity)
        visualization += self._visualize_preprocessing(entity, preprocessed_entity)

        # Blocking
        visualization += "\n2. Blocking\n"
        blocks = self.resolver.blocker.create_blocks([preprocessed_entity])
        visualization += self._visualize_blocking(blocks, preprocessed_entity)

        # Matching
        visualization += "\n3. Matching\n"
        matches = self.resolver.matcher.match(preprocessed_entity, self.resolver.model)
        visualization += self._visualize_matching(matches, preprocessed_entity)

        return visualization

    def _visualize_model_info(self) -> str:
        viz = f"   Total entities in model: {len(self.resolver.model['entities'])}\n"
        viz += f"   Preprocessor: {type(self.resolver.preprocessor).__name__}\n"
        viz += f"   Blocker: {type(self.resolver.blocker).__name__}\n"
        viz += f"   Matcher: {type(self.resolver.matcher).__name__}\n"
        if hasattr(self.resolver.matcher, 'threshold'):
            viz += f"   Matcher threshold: {self.resolver.matcher.threshold}\n"
        if hasattr(self.resolver.matcher, 'attribute_weights'):
            viz += f"   Attribute weights: {json.dumps(self.resolver.matcher.attribute_weights, indent=6)}\n"
        return viz

    def _visualize_preprocessing(self, original: Entity, preprocessed: Entity) -> str:
        viz = "   Original  ->  Preprocessed\n"
        for key in original.attributes:
            orig_value = original.attributes[key]
            prep_value = preprocessed.attributes[key]
            viz += f"   {key}: {orig_value} -> {prep_value}\n"
        viz += f"\n   Preprocessing functions applied:\n"
        for func in self.resolver.preprocessor.preprocessing_functions:
            viz += f"   - {func.__name__}\n"
        return viz

    def _visualize_blocking(self, blocks: Dict[Any, List[Entity]], entity: Entity) -> str:
        viz = "   Blocks created:\n"
        entity_block_key = None
        for block_key, entities in blocks.items():
            viz += f"   - Block '{block_key}': {len(entities)} entities\n"
            if entity in entities:
                entity_block_key = block_key
        
        if entity_block_key:
            viz += f"\n   Entity assigned to block: '{entity_block_key}'\n"
            viz += f"   Entities in the same block:\n"
            for e in blocks[entity_block_key]:
                viz += f"   - Entity {e.id}: {e.attributes.get('title', 'N/A')}\n"
        else:
            viz += "\n   Entity not assigned to any block.\n"
        return viz

    def _visualize_matching(self, matches: List[tuple], entity: Entity) -> str:
        viz = "   Top matches:\n"
        for i, (match_entity, score) in enumerate(matches[:5], 1):  # Show top 5 matches
            viz += f"   {i}. Entity {match_entity.id} (Score: {score:.4f})\n"
            for key, value in match_entity.attributes.items():
                viz += f"      {key}: {value}\n"
            viz += f"      Similarity breakdown:\n"
            for attr, weight in self.resolver.matcher.attribute_weights.items():
                entity_value = entity.attributes.get(attr, '')
                match_value = match_entity.attributes.get(attr, '')
                attr_sim = self.resolver.matcher._calculate_attribute_similarity(entity_value, match_value)
                viz += f"      - {attr}: {attr_sim:.4f} (weight: {weight})\n"
            viz += "\n"
        return viz

def visualize_resolution_process(resolver: EntityResolver, entity: Entity) -> str:
    visualizer = ResolutionVisualizer(resolver)
    return visualizer.visualize_resolution(entity)