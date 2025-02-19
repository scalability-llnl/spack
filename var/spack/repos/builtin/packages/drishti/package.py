# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Drishti(PythonPackage):
    """
    Drishti is a command-line tool to guide end-users in optimizing I/O in their applications
    by detecting typical I/O performance pitfalls and providing a set of recommendations.
    """

    homepage = "https://github.com/hpc-io/drishti-io"
    git = "https://github.com/hpc-io/drishti-io"
    pypi = "drishti-io/drishti-io-0.6.tar.gz"

    maintainers("jeanbez", "sbyna")

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")

    version("0.6", sha256="f1883e48de4a863f284f9c54febd2b04d04456848aea3e34c355310a3336e3b8")
    version("0.5", sha256="08ae82dfa82872cde1f0a219e979b9c10d6c4a01f762066ea864a400cc144d78")
    version("0.4", sha256="bbbb272b4f6f44ae762f6cba28a2c589e15608691c559af0cc2f552590335d7b")

    # NOTE: py-darshan requires libdarshan-util.so to be loaded in the path
    depends_on("c", type="build")  # generated
    depends_on("darshan-util", type=("run", "test", "link"))

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-rich@12.5.1", type=("build", "run"))
    depends_on("py-darshan", type=("build", "run"))

    def test_help(self):
        """Run drishti help."""
        drishti = which(self.prefix.bin.drishti)
        drishti("-h")
