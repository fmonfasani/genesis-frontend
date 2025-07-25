"""Frontend optimization utilities.

This module provides basic code analysis and optimization helpers
for frontend projects.
"""

from __future__ import annotations

import re
from typing import List


class FrontendOptimizer:
    """Simple optimizer for frontend code.

    Currently provides very small-scale optimizations such as
    JavaScript and CSS minification or basic HTML audits.
    """

    def minify_js(self, code: str) -> str:
        """Minify JavaScript code using naive rules."""
        # Remove single line comments
        code = re.sub(r"//.*?(?=\n|$)", "", code)
        # Remove block comments
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
        # Collapse whitespace
        code = re.sub(r"\s+", " ", code)
        return code.strip()

    def minify_css(self, code: str) -> str:
        """Minify CSS code using naive rules."""
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
        code = re.sub(r"\s+", " ", code)
        code = re.sub(r"\s*([{}:;,])\s*", r"\1", code)
        return code.strip()

    def audit_html(self, code: str) -> List[str]:
        """Return a list of basic audit issues for HTML code."""
        issues: List[str] = []
        for match in re.finditer(r"<img\b(?![^>]*\balt=)[^>]*>", code, flags=re.I):
            issues.append(f"Imagen sin alt en posición {match.start()}")
        return issues

    def optimize(self, code: str, language: str = "js") -> str:
        """Optimize code according to language."""
        if language == "js":
            return self.minify_js(code)
        if language == "css":
            return self.minify_css(code)
        return code
