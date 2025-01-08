# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import re

import pytest

from llnl.util.filesystem import mkdirp, touch

import spack.paths
from spack.main import SpackCommand

license = SpackCommand("license")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_list_files():
    files = license("list-files").strip().split("\n")
    assert all(f.startswith(spack.paths.prefix) for f in files)
    assert os.path.join(spack.paths.bin_path, "spack") in files
    assert os.path.abspath(__file__) in files


def test_verify(tmpdir):
    source_dir = tmpdir.join("lib", "spack", "spack")
    mkdirp(str(source_dir))

    no_header = source_dir.join("no_header.py")
    touch(str(no_header))

    lgpl_header = source_dir.join("lgpl_header.py")
    with lgpl_header.open("w") as f:
        f.write(
            """\
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only
"""
        )

    not_in_first_n_lines = source_dir.join("not_in_first_n_lines.py")
    with not_in_first_n_lines.open("w") as f:
        f.write(
            """\
#
#
#
#
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
        )

    correct_header = source_dir.join("correct_header.py")
    with correct_header.open("w") as f:
        f.write(
            """\
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
        )

    out = license("--root", str(tmpdir), "verify", fail_on_error=False)

    assert str(no_header) in out
    assert str(lgpl_header) in out
    assert str(not_in_first_n_lines) in out
    assert str(correct_header) not in out
    assert "3 improperly licensed files" in out
    assert re.search(r"files not containing expected license:\s*1", out)
    assert re.search(r"files with wrong SPDX-License-Identifier:\s*1", out)
    assert re.search(r"files without license in first 6 lines:\s*1", out)

    assert license.returncode == 1
