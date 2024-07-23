from ..core.base import Preprocessor, Entity

class SimplePreprocessor(Preprocessor):
    def preprocess(self, entity: Entity) -> Entity:
        processed_attributes = {
            k: v.lower().strip() if isinstance(v, str) else v
            for k, v in entity.attributes.items()
        }
        return Entity(entity.id, processed_attributes)