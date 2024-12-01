# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import re

import pytest

from llnl.util.filesystem import mkdirp, touch

import spack.cmd.license
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
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: LGPL-2.1-only
"""
        )

    old_lgpl_header = source_dir.join("old_lgpl_header.py")
    with old_lgpl_header.open("w") as f:
        f.write(
            """\
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
"""
        )

    correct_header = source_dir.join("correct_header.py")
    with correct_header.open("w") as f:
        f.write(
            """\
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
        )

    out = license("--root", str(tmpdir), "verify", fail_on_error=False)

    assert str(no_header) in out
    assert str(lgpl_header) in out
    assert str(old_lgpl_header) in out
    assert str(correct_header) not in out
    assert "3 improperly licensed files" in out
    assert re.search(r"files not containing expected license:\s*1", out)
    assert re.search(r"files with wrong SPDX-License-Identifier:\s*1", out)
    assert re.search(r"files with old license header:\s*1", out)

    assert license.returncode == 1


def test_update_copyright_year(tmpdir):
    source_dir = tmpdir.join("lib", "spack", "spack")
    mkdirp(str(source_dir))

    years = list(range(2018, 2021))

    for year in years:
        outdated = source_dir.join("header_%d.py" % year)
        with outdated.open("w") as f:
            f.write(
                """\
# Copyright 2013-%d Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
                % year
            )

    # add an old MIT license at top level
    mit_file = os.path.join(spack.paths.prefix, "LICENSE-MIT")
    test_mit_file = str(tmpdir.join("LICENSE-MIT"))
    with open(mit_file) as real:
        with open(test_mit_file, "w") as dummy:
            old_copyright = re.sub(r"\d{4}-\d{4}", "2018-2019", real.read())
            dummy.write(old_copyright)

    license("--root", str(tmpdir), "update-copyright-year")

    for year in years:
        outdated = source_dir.join("header_%d.py" % year)
        first_line = outdated.open().read().split("\n")[0]
        assert str(year) not in first_line
        assert spack.cmd.license.strict_date in first_line

    mit_date = spack.cmd.license.strict_date.replace("Copyright", "Copyright (c)")
    assert mit_date in open(test_mit_file).read()
