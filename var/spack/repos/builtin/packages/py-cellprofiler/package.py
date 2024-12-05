# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCellprofiler(PythonPackage):
    """CellProfiler cell image analysis software.

    CellProfiler is a free open-source software designed to enable biologists
    without training in computer vision or programming to quantitatively
    measure phenotypes from thousands of images automatically.

    """

    homepage = "https://cellprofiler.org"
    pypi = "cellprofiler/CellProfiler-4.2.6.tar.gz"
    git = "https://github.com/CellProfiler/CellProfiler.git"

    maintainers("omsai")

    license("BSD-3-Clause", checked_by="omsai")

    version("4.2.6", sha256="37e2a35dccff456afda96a4442dff2d23809c8ee271607a347e386aeb4af2628")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")

    depends_on("py-boto3@1.12.28:", type=("build", "run"))
    depends_on("py-cellprofiler-core@4.2.6", type=("build", "run"))
    depends_on("py-centrosome@1.2.2:", type=("build", "run"))
    depends_on("py-docutils@0.15.2:", type=("build", "run"))
    # More recent versions of h5py cause:
    #   AttributeError: module 'h5py' has no attribute 'Dataset
    depends_on("py-h5py@3.6:3.7~mpi", type=("build", "run"))
    depends_on("py-imageio@2.5:", type=("build", "run"))
    depends_on("py-inflect@2.1:6", type=("build", "run"))
    depends_on("py-jinja2@2.11.2:", type=("build", "run"))
    depends_on("py-joblib@0.13:", type=("build", "run"))
    depends_on("py-mahotas@1.4:", type=("build", "run"))
    # matplotlib.cm.get_cmap does not exist in 3.9.0 onwards.
    depends_on("py-matplotlib@3.1.3:3.8", type=("build", "run"))
    depends_on("py-mysqlclient@1.4.6", type=("build", "run"))
    depends_on("py-numpy@1.20.1:", type=("build", "run"))
    depends_on("py-pillow@7.1:", type=("build", "run"))
    depends_on("py-prokaryote@2.4.4:", type=("build", "run"))
    depends_on("py-python-bioformats@4.0.7:", type=("build", "run"))
    depends_on("py-python-javabridge@4.0.3:", type=("build", "run"))
    depends_on("py-pyzmq@22.3:22", type=("build", "run"))
    depends_on("py-sentry-sdk@0.18:", type=("build", "run"))
    depends_on("py-requests@2.22:", type=("build", "run"))
    depends_on("py-scikit-image@0.18.3:", type=("build", "run"))
    depends_on("py-scikit-learn@0.20:0", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-tifffile@:2022.4.21", type=("build", "run"))
    depends_on("py-wxpython@4.1.0:4", type=("build", "run"))

    depends_on("py-pytest", type=("run", "test"), when="@4.2.6 +tests")

    # Run the post-install tests with `spack test run py-cellprofiler`.  We
    # need the variant to add the pytest executable to the PATH.
    variant("tests", default=False, description="Post-install tests.")

    # The pypi tests directory is incomplete.
    resource(
        name="tests-upstream",
        destination="",
        placement={
            "tests/conftest.py": "tests/conftest.py",
            "tests/gui": "tests/gui",
            "tests/__init__.py": "tests/__init__.py",
            "tests/modules": "tests/modules",
            "tests/resources": "tests/resources",
            "tests/test_cellprofiler.py": "tests/test_cellprofiler.py",
            "tests/test_haralick.py": "tests/test_haralick.py",
            "tests/test_knime_bridge.py": "tests/test_knime_bridge.py",
            "tests/test_main.py": "tests/test_main.py",
            "tests/test_nowx.py": "tests/test_nowx.py",
            "tests/utilities": "tests/utilities",
        },
        git=git,
        tag="v4.2.6",
        sha256="5fb562774044d1dc8cffcddf6072d706f71e6649d566980efaab5b30f52ddfa2",
        when="@4.2.6 +tests",
    )

    dir_tests = "tests"

    # Leave 'gui' out of 'import_modules' to avoid the curently broken wxpython
    # dependency.
    import_modules = [
        "cellprofiler",
        "cellprofiler.icons",
        "cellprofiler.library",
        "cellprofiler.library.functions",
        "cellprofiler.library.modules",
        # "cellprofiler.gui",
        # "cellprofiler.gui.html",
        # "cellprofiler.gui.help",
        # "cellprofiler.gui.module_view",
        # "cellprofiler.gui.constants",
        # "cellprofiler.gui.figure",
        # "cellprofiler.gui.workspace_view",
        # "cellprofiler.gui.preferences_view",
        # "cellprofiler.gui.utilities",
        # "cellprofiler.gui.preferences_dialog",
        "cellprofiler.modules",
        "cellprofiler.modules.plugins",
        "cellprofiler.utilities",
    ]

    @when("+tests")
    def patch(self):
        """Install tests from git."""
        # Install the tests module.  Using a module name like "tests" may
        # create a namespace collision with other spack packages in the DAG,
        # but the alternative would moving tests into cellprofiler and
        # extensively patching the tests to be a submodule of cellprofiler
        # instead of a standalone module.
        filter_file(r"find_packages\([^)]+\)", "find_packages()", "setup.py")
        # Include required test data files.
        with open("MANIFEST.in", "a") as h:
            h.writelines("graft tests")

    # For interactive unittest debugging, run:
    #
    # spack env create cp
    # spack env activate cp
    # spack add cellprofiler+tests ^hdf5~mpi
    # spack install
    # git clone --branch v4.2.6 --depth 1 \
    #     https://github.com/cellprofiler/cellprofiler
    # cd cellprofiler/
    # pytest --pdb -k "not TestExportToDatabase" tests/
    #
    # [...]
    # 1412 passed, 16 skipped, 75 deselected
    def test_cellprofiler_no_gui(self):
        """Test installed package."""
        pytest = which("pytest")
        prefix = join_path(python_purelib, self.dir_tests)
        pytest(
            "-v",
            # Don't test against the live MySQL database.
            "-k",
            "not TestExportToDatabase",
            prefix,
        )
