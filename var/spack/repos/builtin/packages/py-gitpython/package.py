# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGitpython(PythonPackage):
    """GitPython is a python library used to interact with Git repositories."""

    homepage = "https://gitpython.readthedocs.org"
    pypi = "GitPython/GitPython-3.1.12.tar.gz"

    license("BSD-3-Clause")

    version("3.1.43", sha256="35f314a9f878467f5453cc1fee295c3e18e52f1b99f10f6cf5b1682e968a9e7c")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2024-22190
        version(
            "3.1.40", sha256="22b126e9ffb671fdd0c129796343a02bf67bf2994b35449ffc9321aa755e18a4"
        )
        version(
            "3.1.34", sha256="85f7d365d1f6bf677ae51039c1ef67ca59091c7ebd5a3509aa399d4eda02d6dd"
        )
        version(
            "3.1.27", sha256="1c885ce809e8ba2d88a29befeb385fcea06338d3640712b59ca623c220bb5704"
        )
        version(
            "3.1.24", sha256="df83fdf5e684fef7c6ee2c02fc68a5ceb7e7e759d08b694088d0cacb4eba59e5"
        )
        version(
            "3.1.23", sha256="aaae7a3bfdf0a6db30dc1f3aeae47b71cd326d86b936fe2e158aa925fdf1471c"
        )
        version(
            "3.1.22", sha256="e1589f27c3cd1f33b22db1df194201b5abca6b4cc5450f13f9c371e099c1b24f"
        )
        version(
            "3.1.20", sha256="df0e072a200703a65387b0cfdf0466e3bab729c0458cf6b7349d0e9877636519"
        )
        version(
            "3.1.19", sha256="18f4039b96b5567bc4745eb851737ce456a2d499cecd71e84f5c0950e92d0e53"
        )
        version(
            "3.1.18", sha256="b838a895977b45ab6f0cc926a9045c8d1c44e2b653c1fcc39fe91f42c6e8f05b"
        )
        version(
            "3.1.17", sha256="ee24bdc93dce357630764db659edaf6b8d664d4ff5447ccfeedd2dc5c253f41e"
        )
        version(
            "3.1.16", sha256="2bfcd25e6b81fe431fa3ab1f0975986cfddabf7870a323c183f3afbc9447c0c5"
        )
        version(
            "3.1.15", sha256="05af150f47a5cca3f4b0af289b73aef8cf3c4fe2385015b06220cbcdee48bb6e"
        )
        version(
            "3.1.14", sha256="be27633e7509e58391f10207cd32b2a6cf5b908f92d9cd30da2e514e1137af61"
        )
        version(
            "3.1.13", sha256="8621a7e777e276a5ec838b59280ba5272dd144a18169c36c903d8b38b99f750a"
        )
        version(
            "3.1.12", sha256="42dbefd8d9e2576c496ed0059f3103dcef7125b9ce16f9d5f9c834aed44a1dac"
        )
        version(
            "3.1.11", sha256="befa4d101f91bad1b632df4308ec64555db684c360bd7d2130b4807d49ce86b8"
        )
        version(
            "3.1.10", sha256="f488d43600d7299567b59fe41497d313e7c1253a9f2a8ebd2df8af2a1151c71d"
        )
        version("3.1.9", sha256="a03f728b49ce9597a6655793207c6ab0da55519368ff5961e4a74ae475b9fa8e")
        version("3.1.8", sha256="080bf8e2cf1a2b907634761c2eaefbe83b69930c94c66ad11b65a8252959f912")
        version("3.1.7", sha256="2db287d71a284e22e5c2846042d0602465c7434d910406990d5b74df4afb0858")
        version("3.1.6", sha256="b54969b3262d4647f80ace8e9dd4e3f99ac30cc0f3e766415b349208f810908f")
        version("3.1.5", sha256="90400ecfa87bac36ac75dfa7b62e83a02017b51759f6eef4494e4de775b2b4be")
        version("3.1.4", sha256="fa98ce1f05805d59bbc3adb16c0780e5ca43b5ea9422feecf1cd0949a61d947e")
        version("3.1.3", sha256="e107af4d873daed64648b4f4beb89f89f0cfbe3ef558fc7821ed2331c2f8da1a")
        version("3.1.2", sha256="864a47472548f3ba716ca202e034c1900f197c0fb3a08f641c20c3cafd15ed94")
        version("3.1.1", sha256="6d4f10e2aaad1864bb0f17ec06a2c2831534140e5883c350d58b4e85189dab74")
        version("3.1.0", sha256="e426c3b587bd58c482f0b7fe6145ff4ac7ae6c82673fc656f489719abca6f4cb")
        version("3.0.9", sha256="7e5df21bfef38505115ad92544fb379e6fedb2753f3b709174c4358cecd0cb97")
        version("0.3.6", sha256="e6599fcb939cb9b25a015a429702db39de10f2b493655ed5669c49c37707d233")

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"), when="@3.1.15:")
    depends_on("python@3.6:", type=("build", "run"), when="@3.1.18:")
    depends_on("python@3.7:", type=("build", "run"), when="@3.1.22:")
    depends_on("py-setuptools", type="build")
    depends_on("py-gitdb@4.0.1:4", type=("build", "run"))
    depends_on(
        "py-typing-extensions@3.7.4.0:", type=("build", "run"), when="@3.1.16: ^python@:3.7"
    )
    depends_on(
        "py-typing-extensions@3.7.4.3:", type=("build", "run"), when="@3.1.19:3.1.26 ^python@:3.10"
    )
    depends_on(
        "py-typing-extensions@3.7.4.3:", type=("build", "run"), when="@3.1.27: ^python@:3.7"
    )
