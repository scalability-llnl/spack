# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import re
import textwrap

import pytest

from llnl.util.filesystem import mkdirp

import spack.paths
from spack.main import SpackCommand

license = SpackCommand("license")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_list_files():
    files = license("list-files").strip().split("\n")
    assert all(f.startswith(spack.paths.prefix) for f in files)
    assert os.path.join(spack.paths.bin_path, "spack") in files
    assert os.path.abspath(__file__) in files


GOOD_HEADER = """\
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""


parameters = [
    (
        "wrong_spdx.py",
        r"files with wrong SPDX-License-Identifier:\s*1",
        textwrap.dedent(
            """\
            # Copyright Spack Project Developers. See COPYRIGHT file for details.
            #
            # SPDX-License-Identifier: LGPL-2.1-only
            """
        ),
        GOOD_HEADER,
        False,
    ),
    (
        "empty_lines.py",
        r"files without license in first 7 lines:\s*1",
        textwrap.dedent(
            """\
            #
            #
            #
            #
            #
            # Copyright Spack Project Developers. See COPYRIGHT file for details.
            #
            # SPDX-License-Identifier: (Apache-2.0 OR MIT)
            """
        ),
        GOOD_HEADER,
        False,
    ),
    (
        "wrong_devs.py",
        r"files not containing expected license:\s*1",
        textwrap.dedent(
            """\
            # Copyright Not The Right Developers. See BROKEN file for details.
            #
            # SPDX-License-Identifier: (Apache-2.0 OR MIT)
            """
        ),
        GOOD_HEADER,
        False,
    ),
    (
        "old_llnl.py",
        r"files not containing expected license:\s*1",
        textwrap.dedent(
            """\
            # Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
            # Spack Project Developers. See top-level COPYRIGHT file for details.
            #
            # SPDX-License-Identifier: (Apache-2.0 OR MIT)
            """
        ),
        GOOD_HEADER,
        False,
    ),
    ("no_header.py", r"files without license in first 7 lines:\s*1", "", GOOD_HEADER, False),
    (
        "test-script",
        "",
        "#!/usr/bin/env python3\n#\n" + GOOD_HEADER,
        "#!/usr/bin/env python3\n#\n" + GOOD_HEADER,
        True,
    ),
    (
        "python-lang-test-script",
        "",
        "#!/usr/bin/env python3\n# -*- python -*-\n#\n" + GOOD_HEADER,
        "#!/usr/bin/env python3\n# -*- python -*-\n#\n" + GOOD_HEADER,
        True,
    ),
    ("unfixable-test-script", "", "", "", False),  # because script + no shebang
    (
        "bad-test-script",
        r"files not containing expected license:\s*1",
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            #
            # Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
            # Spack Project Developers. See top-level COPYRIGHT file for details.
            #
            # SPDX-License-Identifier: (Apache-2.0 OR MIT)
            """
        ),
        "#!/usr/bin/env python3\n#\n" + GOOD_HEADER,
        False,
    ),
    (
        "bad-python-lang-test-script",
        r"files not containing expected license:\s*1",
        textwrap.dedent(
            """\
            #!/usr/bin/env python3
            # -*- python -*-
            #
            # Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
            # Spack Project Developers. See top-level COPYRIGHT file for details.
            #
            # SPDX-License-Identifier: (Apache-2.0 OR MIT)
            """
        ),
        "#!/usr/bin/env python3\n# -*- python -*-\n#\n" + GOOD_HEADER,
        False,
    ),
    ("good.py", "", GOOD_HEADER, GOOD_HEADER, True),
]


@pytest.mark.parametrize(
    "filename,expected_txt,header,fixed_header,good",
    parameters,
    ids=[param[0] for param in parameters],
)
class TestLicenses:

    def _setup_license_root(self, tmpdir, header, filename):
        source_dir = tmpdir / "lib" / "spack" / "spack"
        mkdirp(str(source_dir))

        source_file = source_dir / filename
        with source_file.open("w") as f:
            f.write(header)

        return source_file

    def test_license_verify(self, filename, expected_txt, header, fixed_header, good, tmpdir):
        source_file = self._setup_license_root(tmpdir, header, filename)

        out = license("--root", str(tmpdir), "verify", fail_on_error=False)

        if not good:
            assert str(source_file) in out
            assert "1 improperly licensed file" in out
            assert re.search(expected_txt, out)
            assert license.returncode == 1
        else:
            assert license.returncode == 0

    def test_license_fix(self, filename, expected_txt, header, fixed_header, good, tmpdir):
        source_file = self._setup_license_root(tmpdir, header, filename)

        out = license("--root", str(tmpdir), "fix", fail_on_error=False)

        if good:
            assert str(source_file) not in out
            assert license.returncode == 0
            return

        if fixed_header:
            assert f"Fixed {str(source_file)}" in out
            assert license.returncode == 0

            license("--root", str(tmpdir), "verify", fail_on_error=False)
            assert license.returncode == 0

        else:
            assert f"I don't know how to fix {str(source_file)}" in out
            assert license.returncode == 1
