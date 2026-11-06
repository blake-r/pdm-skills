# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0", "openpyxl>=3.1"]
# ///
"""Dev-only builder for the tool templates. Not shipped.

Spec classes live in build/templates/<category>.py; shared base classes,
helpers and ROOT live in build/templates/base.py."""

from templates.base import *  # noqa: F401,F403

import templates.product_analysis  # noqa: F401
import templates.development_execution  # noqa: F401
import templates.development_planning  # noqa: F401
import templates.product_planning  # noqa: F401
import templates.business_research  # noqa: F401
import templates.business_planning  # noqa: F401
import templates.business_analysis  # noqa: F401
import templates.product_research  # noqa: F401
import templates.product_validation  # noqa: F401
import templates.product_handoff  # noqa: F401
import templates.development_validation  # noqa: F401
import templates.development_handoff  # noqa: F401
import templates.business_validation  # noqa: F401
import templates.pdm_brief  # noqa: F401


if __name__ == "__main__":
    import sys
    wanted = sys.argv[1:]
    specs = [cls() for cls in concrete_specs()]
    for spec in specs:
        if wanted and not any(w in spec.rel for w in wanted):
            continue
        Builder(spec).build(ROOT / spec.rel)
    print("ok", len(specs))
