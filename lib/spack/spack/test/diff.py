# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.config
import spack.store
import spack.cmd.diff
import spack.main
import spack.diff
import spack.spec

install = spack.main.SpackCommand('install')
diff = spack.main.SpackCommand('diff')


def test_spec_differ(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that we can install two packages and diff them"""

    # Specs should be the same as themselves
    differ = spack.diff.SpecDiff('mpileaks', 'mpileaks')
    assert len(differ.a_not_b) == 0
    assert len(differ.b_not_a) == 0

    # Calculate the comparison to a different spec
    differ = spack.diff.SpecDiff('mpileaks', 'mpileaks+debug')
    assert len(differ.a_not_b) == 1
    assert len(differ.b_not_a) == 1

    # Make sure all prints work
    print(differ.a_name)
    print(differ.b_name)
    print(differ)
    print(differ.tree())
    print(differ.colored_diff())

    # make sure json output has proper attributes
    output = differ.to_json()
    for key in ['intersect', 'a_not_b', 'b_not_a', 'a_name', 'b_name']:
        assert key in output

    # A and b should be specs
    assert isinstance(differ.a, spack.spec.Spec)
    assert isinstance(differ.b, spack.spec.Spec)
