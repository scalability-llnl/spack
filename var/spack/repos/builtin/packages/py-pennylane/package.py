# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPennylane(PythonPackage):
    """PennyLane is a Python quantum machine learning library by Xanadu Inc."""

    homepage = "https://docs.pennylane.ai/"
    git = "https://github.com/PennyLaneAI/pennylane.git"
    url = "https://github.com/PennyLaneAI/pennylane/archive/refs/tags/v0.37.0.tar.gz"

    maintainers("mlxd", "AmintorDusko", "marcodelapierre", "vincentmr")

    license("Apache-2.0")

    version("master", branch="master")
    version("0.37.0", sha256="3e5eaab9da28ac43099e5850fde0c5763bc4e37271804463fc35dab8b08e2f15")
    version("0.36.0", sha256="10ae174b8fd47de12c1174fd5236c26b50ff40e679b658b3446660e063fb64e1")
    version("0.35.1", sha256="5a234d0605012f3d0201fdcfd2bfe84205a09c8ac42801fe7123eddddec71366")
    version("0.35.0", sha256="3b99185661e8a0d0f7bc2dcc9cfa51dde20e99708c3c7d858c4732f0eb774716")
    version("0.34.0", sha256="f76f544212c028a8f882ce7f66639e7f7c4c9213277bde0454c7f3a7d9d46538")
    version("0.33.1", sha256="89d02bfe3a37abd13dcdb2f34f00a38e9e60a13af66a97911c8558f77ff4e32e")
    version("0.33.0", sha256="b41c843a432c5869fc63dc35c9e9d53bec64d296ca0e0eeb1c9b83d95a68c3f1")
    version("0.32.0", sha256="8a2206268d7cae0a59f9067b6075175eec93f4843519b371f02716c49a22e750")
    version("0.31.0", sha256="f3b68700825c120e44434ed2b2ab71d0be9d3111f3043077ec0598661ec33477")
    version("0.30.0", sha256="7fe4821fbc733e3e40d7011e054bd2e31edde3151fd9539025c827a5a3579d6b")
    version("0.29.1", sha256="6ecfb305a3898347df8c539a89a67e748766941d159dbef9e34864872f13c45c")

    depends_on("python@3.8:", type=("build", "run"), when="@:0.31.0")
    depends_on("python@3.9:", type=("build", "run"), when="@0.32.0:")
    depends_on("py-pip", type=("build", "run"))  # Runtime req for pennylane.about()
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools", type=("build", "run"), when="@0.33")

    depends_on("py-numpy@:1.23", type=("build", "run"), when="@:0.32.0")
    depends_on("py-numpy@:1.26", type=("build", "run"), when="@0.33.0:")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scipy@:1.10.0", type=("build", "run"), when="@:0.31")
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-rustworkx", type=("build", "run"), when="@0.30.0:")
    depends_on("py-retworkx", type=("build", "run"), when="@0.28.0:0.29.1")
    depends_on("py-autograd@:1.5", type=("build", "run"), when="@:0.32.0")
    depends_on("py-autograd", type=("build", "run"), when="@0.33.0:")
    depends_on("py-toml", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-semantic-version@2.7:", type=("build", "run"))
    depends_on("py-autoray@0.3.1:", type=("build", "run"), when="@:0.32.0")
    depends_on("py-autoray@0.6.1:", type=("build", "run"), when="@0.33.0:")
    depends_on("py-autoray@0.6.11:", type=("build", "run"), when="@0.37.0:")
    depends_on("py-cachetools", type=("build", "run"))
    depends_on(
        "py-pennylane-lightning@0.28.0:0.29.0", type=("build", "run"), when="@0.28.0:0.29.1"
    )
    for v in range(30, 38):
        depends_on(f"py-pennylane-lightning@0.{v}:", type=("build", "run"), when=f"@0.{v}:")
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"), when="@0.32.0:")
    depends_on("py-packaging", type=("build", "run"), when="@0.37.0:")

    # The following packages are required by the `pl-device-test binary`
    depends_on("py-pytest", type="test")
    depends_on("py-pytest-mock", type="test")
    depends_on("py-flaky", type="test")
    depends_on("py-pytest-benchmark", type="test", when="@0.34.0:")
    # Additional test deps
    depends_on("py-pytest-xdist@3.2:", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("tests"):
            pl_dev_test = Executable(join_path(self.prefix, "bin", "pl-device-test"))
            pl_dev_test("--device", "default.qubit", "--shots", "None", "--skip-ops")
            pl_dev_test("--device", "default.qubit", "--shots", "10000", "--skip-ops")
            pl_dev_test("--device", "lightning.qubit", "--shots", "None", "--skip-ops")
            pl_dev_test("--device", "lightning.qubit", "--shots", "10000", "--skip-ops")
