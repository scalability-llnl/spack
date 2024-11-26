# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Unit tests for objects turning configuration into an intermediate format used by the solver."""
import pytest

import spack.compilers
import spack.spec
from spack.concretize import UnavailableCompilerVersionError
from spack.solver import asp


class TestCompilerParser:
    def test_expected_order_mock_config(self, config):
        """Tests the expected preference order in the mock compiler configuration"""
        parser = asp.CompilerParser(config)
        expected_order = ["gcc@=10.2.1", "gcc@=9.4.0", "gcc@=9.4.0", "clang@=15.0.0"]
        for c, expected in zip(parser.possible_compilers(), expected_order):
            assert c.spec.satisfies(expected)

    @pytest.mark.parametrize("spec_str", ["a %gcc@=13.2.0", "a ^b %gcc@=13.2.0"])
    def test_compiler_from_input_raise(self, spec_str, config):
        """Tests that having an unknown compiler in the input spec raises an exception, if we
        don't allow bootstrapping missing compilers.
        """
        spec = spack.spec.Spec(spec_str)
        with pytest.raises(UnavailableCompilerVersionError):
            asp.CompilerParser(config).with_input_specs([spec])

    def test_compilers_inferred_from_concrete_specs(self, mutable_config, mutable_database):
        """Test that compilers inferred from concrete specs, that are not in the local
        configuration too, are last in the preference order.
        """
        spack.compilers.remove_compiler_from_config("gcc@=10.2.1")
        assert not spack.compilers.compilers_for_spec("gcc@=10.2.1")

        parser = asp.CompilerParser(mutable_config)
        for reuse_spec in mutable_database.query():
            parser.add_compiler_from_concrete_spec(reuse_spec)

        expected_order = [
            ("gcc@=9.4.0", True),
            ("gcc@=9.4.0", True),
            ("clang@=15.0.0", True),
            ("gcc@=10.2.1", False),
        ]
        for c, (expected, available) in zip(parser.possible_compilers(), expected_order):
            assert c.spec.satisfies(expected)
            assert c.available is available
