from genesis_frontend.core import FrontendOptimizer


def test_optimize_js():
    optimizer = FrontendOptimizer()
    code = "function add(a, b) { // comment\n return a + b; }"
    result = optimizer.optimize(code, language="js")
    assert "//" not in result
    assert "\n" not in result
