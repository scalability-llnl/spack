# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.main import SpackCommand


audit = SpackCommand('audit')


def test_audit_packages(mutable_config, mock_packages):
    """Sanity check ``spack audit packages`` to make sure it works."""
    audit('packages', fail_on_error=False)
    # Some mock packages have issues by design, to check what would
    # be Spack behavior in those cases. Ensure that the command returns
    # non-zero exit code
    assert audit.returncode == 1


def test_audit_configs(mutable_config, mock_packages):
    """Sanity check ``spack audit packages`` to make sure it works."""
    audit('configs', fail_on_error=False)
    # The mock configuration has duplicate definitions of some compilers
    assert audit.returncode == 1
