"""Shared service utilities under sigma_core.services.

This package centralizes cross-product services like io, policy, and audit.
Other modules (model_cards, lineage, brackets, signals_live) are available as
submodules but are not imported on package import to avoid heavy deps during
test collection.
"""

# Intentionally do not import submodules here to keep package import light.
# Import directly where needed, e.g.:
#   from sigma_core.services.io import workspace_paths
#   from sigma_core.services.policy import validate_policy_file

__all__ = []
