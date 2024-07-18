from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "preprocessing": {
        "lowercase": True,
        "remove_punctuation": True,
        "remove_whitespace": True
    },
    "blocking": {
        "method": "standard",
        "block_key": "name"
    },
    "similarity": {
        "method": "jaccard",
        "threshold": 0.7
    },
    "matching": {
        "method": "threshold",
        "threshold": 0.8
    },
    "evaluation": {
        "metrics": ["precision", "recall", "f1_score"]
    }
}

def get_config(user_config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Merge user-provided configuration with default configuration.
    """
    if user_config is None:
        return DEFAULT_CONFIG

    config = DEFAULT_CONFIG.copy()
    for key, value in user_config.items():
        if isinstance(value, dict) and key in config:
            config[key].update(value)
        else:
            config[key] = value

    return config