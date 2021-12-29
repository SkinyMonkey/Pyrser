# ------------------------------------------------------------------------------
# unit tests
# ------------------------------------------------------------------------

if __name__ == "__main__":

    import unittest
    from unit_tests.internal_parse import InternalParse_Test as _01

    from unit_tests.capture import Capture_Test as _02
    from unit_tests.no_depth_generation import GeneratedCode as NoDepthGeneration
    from unit_tests.multi_generation import GeneratedCode as MultiDepthGeneration
    from unit_tests.rule_directives import GeneratedCode as RuleDirective
    from unit_tests.composition import GeneratedCode as CompositionGeneration
    from unit_tests.inheritance import GeneratedCode as InheritanceGeneration
    from unit_tests.hooks import GenericHookTests

    unittest.main(failfast=True)
