# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class PyMatplotlib(PythonPackage):
    """Matplotlib is a comprehensive library for creating static, animated,
    and interactive visualizations in Python."""

    homepage = "https://matplotlib.org/"
    pypi = "matplotlib/matplotlib-3.3.2.tar.gz"

    skip_modules = [
        "matplotlib.tests",
        "mpl_toolkits.axes_grid1.tests",
        "mpl_toolkits.axisartist.tests",
        "mpl_toolkits.mplot3d.tests",
    ]

    license("Apache-2.0")
    maintainers("adamjstewart", "rgommers")

    version("3.9.2", sha256="96ab43906269ca64a6366934106fa01534454a69e471b7bf3d79083981aaab92")
    version("3.9.1", sha256="de06b19b8db95dd33d0dc17c926c7c9ebed9f572074b6fac4f65068a6814d010")
    version("3.9.0", sha256="e6d29ea6c19e34b30fb7d88b7081f869a03014f66fe06d62cc77d5a6ea88ed7a")
    version("3.8.4", sha256="8aac397d5e9ec158960e31c381c5ffc52ddd52bd9a47717e2a694038167dffea")
    version("3.8.3", sha256="7b416239e9ae38be54b028abbf9048aff5054a9aba5416bef0bd17f9162ce161")
    version("3.8.2", sha256="01a978b871b881ee76017152f1f1a0cbf6bd5f7b8ff8c96df0df1bd57d8755a1")
    version("3.8.1", sha256="044df81c1f6f3a8e52d70c4cfcb44e77ea9632a10929932870dfaa90de94365d")
    version("3.8.0", sha256="df8505e1c19d5c2c26aff3497a7cbd3ccfc2e97043d1e4db3e76afa399164b69")
    version("3.7.5", sha256="1e5c971558ebc811aa07f54c7b7c677d78aa518ef4c390e14673a09e0860184a")
    version("3.7.4", sha256="7cd4fef8187d1dd0d9dcfdbaa06ac326d396fb8c71c647129f0bf56835d77026")
    version("3.7.3", sha256="f09b3dd6bdeb588de91f853bbb2d6f0ff8ab693485b0c49035eaa510cb4f142e")
    version("3.7.2", sha256="a8cdb91dddb04436bd2f098b8fdf4b81352e68cf4d2c6756fcc414791076569b")
    version("3.7.1", sha256="7b73305f25eab4541bd7ee0b96d87e53ae9c9f1823be5659b806cd85786fe882")
    version("3.7.0", sha256="8f6efd313430d7ef70a38a3276281cb2e8646b3a22b3b21eb227da20e15e6813")
    version("3.6.3", sha256="1f4d69707b1677560cd952544ee4962f68ff07952fb9069ff8c12b56353cb8c9")
    version("3.6.2", sha256="b03fd10a1709d0101c054883b550f7c4c5e974f751e2680318759af005964990")
    version("3.6.1", sha256="e2d1b7225666f7e1bcc94c0bc9c587a82e3e8691da4757e357e5c2515222ee37")
    version("3.6.0", sha256="c5108ebe67da60a9204497d8d403316228deb52b550388190c53a57394d41531")
    version("3.5.3", sha256="339cac48b80ddbc8bfd05daae0a3a73414651a8596904c2a881cfd1edb65f26c")
    version("3.5.2", sha256="48cf850ce14fa18067f2d9e0d646763681948487a8080ec0af2686468b4607a2")
    version("3.5.1", sha256="b2e9810e09c3a47b73ce9cab5a72243a1258f61e7900969097a817232246ce1c")
    version("3.5.0", sha256="38892a254420d95594285077276162a5e9e9c30b6da08bdc2a4d53331ad9a6fa")
    version("3.4.3", sha256="fc4f526dfdb31c9bd6b8ca06bf9fab663ca12f3ec9cdf4496fb44bc680140318")
    version("3.4.2", sha256="d8d994cefdff9aaba45166eb3de4f5211adb4accac85cbf97137e98f26ea0219")
    version("3.4.1", sha256="84d4c4f650f356678a5d658a43ca21a41fca13f9b8b00169c0b76e6a6a948908")
    version("3.4.0", sha256="424ddb3422c65b284a38a97eb48f5cb64b66a44a773e0c71281a347f1738f146")
    version("3.3.4", sha256="3e477db76c22929e4c6876c44f88d790aacdf3c3f8f3a90cb1975c0bf37825b0")
    version("3.3.3", sha256="b1b60c6476c4cfe9e5cf8ab0d3127476fd3d5f05de0f343a452badaad0e4bdec")
    version("3.3.2", sha256="3d2edbf59367f03cd9daf42939ca06383a7d7803e3993eb5ff1bee8e8a3fbb6b")
    version("3.3.1", sha256="87f53bcce90772f942c2db56736788b39332d552461a5cb13f05ff45c1680f0e")
    version("3.3.0", sha256="24e8db94948019d531ce0bcd637ac24b1c8f6744ac86d2aa0eb6dbaeb1386f82")
    version("3.2.2", sha256="3d77a6630d093d74cbbfebaa0571d00790966be1ed204e4a8239f5cbd6835c5d")
    version("3.2.1", sha256="ffe2f9cdcea1086fc414e82f42271ecf1976700b8edd16ca9d376189c6d93aee")
    version("3.2.0", sha256="651d76daf9168250370d4befb09f79875daa2224a9096d97dfc3ed764c842be4")
    version("3.1.3", sha256="db3121f12fb9b99f105d1413aebaeb3d943f269f3d262b45586d12765866f0c6")
    version("3.1.2", sha256="8e8e2c2fe3d873108735c6ee9884e6f36f467df4a143136209cff303b183bada")
    version("3.1.1", sha256="1febd22afe1489b13c6749ea059d392c03261b2950d1d45c17e3aed812080c93")
    version("3.1.0", sha256="1e0213f87cc0076f7b0c4c251d7e23601e2419cd98691df79edb95517ba06f0c")
    version("3.0.3", sha256="e1d33589e32f482d0a7d1957bf473d43341115d40d33f578dad44432e47df7b7")
    version("3.0.2", sha256="c94b792af431f6adb6859eb218137acd9a35f4f7442cea57e4a59c54751c36af")
    version("3.0.1", sha256="70f8782c50ac2c7617aad0fa5ba59fc49f690a851d6afc0178813c49767644dd")
    version("3.0.0", sha256="b4e2333c98a7c2c1ff6eb930cd2b57d4b818de5437c5048802096b32f66e65f9")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # https://matplotlib.org/stable/users/explain/figure/backends.html
    # matplotlib 3.9+: lib/matplotlib/backends/registry.py
    # matplotlib 3.8-: lib/matplotlib/rcsetup.py
    all_backends = [
        # GTK
        "gtk3agg",
        "gtk3cairo",
        conditional("gtk4agg", when="@3.5:"),
        conditional("gtk4cairo", when="@3.5:"),
        # Cocoa
        "macosx",
        # Jupyter Notebook
        "nbagg",
        conditional("notebook", when="@3.9:"),
        # Qt
        conditional("qtagg", when="@3.5:"),
        conditional("qtcairo", when="@3.5:"),
        conditional("qt4agg", when="@:3.4"),
        conditional("qt4cairo", when="@:3.4"),
        "qt5agg",
        "qt5cairo",
        # Tk
        "tkagg",
        "tkcairo",
        # WebAgg
        "webagg",
        # Wx
        "wx",
        "wxagg",
        "wxcairo",
        # Headless
        "agg",
        "cairo",
        "pdf",
        "pgf",
        "ps",
        "svg",
        "template",
    ]

    default_backend = "agg"
    if sys.platform == "darwin":
        default_backend = "macosx"

    variant(
        "backend",
        default=default_backend,
        description="Default backend. All backends are installed and "
        + "functional as long as dependencies are found at run-time",
        values=all_backends,
        multi=False,
    )
    variant("movies", default=False, description="Enable support for saving movies")
    variant("animation", default=False, description="Enable animation support")
    variant(
        "image",
        default=True,
        when="@:3.2",
        description="Enable reading/saving JPEG, BMP and TIFF files",
    )
    variant("latex", default=False, description="Enable LaTeX text rendering support")
    variant("fonts", default=False, description="Enable support for system font detection")

    # https://matplotlib.org/stable/install/dependencies.html
    # Runtime dependencies
    # Mandatory dependencies
    depends_on("python@3.9:", when="@3.8:", type=("build", "link", "run"))
    depends_on("python@3.8:", when="@3.6:", type=("build", "link", "run"))
    depends_on("python", type=("build", "link", "run"))
    depends_on("py-contourpy@1.0.1:", when="@3.6:", type=("build", "run"))
    depends_on("py-cycler@0.10:", type=("build", "run"))
    depends_on("py-fonttools@4.22:", when="@3.5:", type=("build", "run"))
    depends_on("py-kiwisolver@1.3.1:", when="@3.8.1:", type=("build", "run"))
    depends_on("py-kiwisolver@1.0.1:", type=("build", "run"))
    depends_on("py-numpy@1.23:", when="@3.9:", type=("build", "link", "run"))
    depends_on("py-numpy@1.21:", when="@3.8", type=("build", "link", "run"))
    depends_on("py-numpy@1.20:", when="@3.7", type=("build", "link", "run"))
    depends_on("py-numpy@1.19:", when="@3.6", type=("build", "link", "run"))
    depends_on("py-numpy@1.17:", when="@3.5", type=("build", "link", "run"))
    depends_on("py-numpy@1.16:", when="@3.4", type=("build", "link", "run"))
    depends_on("py-numpy@1.15:", when="@3.3", type=("build", "link", "run"))
    depends_on("py-numpy@1.11:", when="@:3.2", type=("build", "link", "run"))
    # https://github.com/matplotlib/matplotlib/issues/26778
    depends_on("py-numpy@:1", when="@:3.8.3", type=("build", "link", "run"))
    depends_on("py-packaging@20:", when="@3.6:", type=("build", "run"))
    depends_on("py-packaging", when="@3.5:", type=("build", "run"))
    depends_on("pil@8:", when="@3.8.1:", type=("build", "run"))
    depends_on("pil@6.2:", when="@3.3:", type=("build", "run"))
    depends_on("py-pyparsing@2.3.1:3.0", when="@3.7.2", type=("build", "run"))
    depends_on("py-pyparsing@2.3.1:", when="@3.7:", type=("build", "run"))
    depends_on("py-pyparsing@2.2.1:", when="@3.4:", type=("build", "run"))
    depends_on("py-pyparsing@2.0.3,2.0.5:2.1.1,2.1.3:2.1.5,2.1.7:", type=("build", "run"))
    depends_on("py-python-dateutil@2.7:", when="@3.4:", type=("build", "run"))
    depends_on("py-python-dateutil@2.1:", type=("build", "run"))
    depends_on("py-importlib-resources@3.2:", when="@3.7: ^python@:3.9", type=("build", "run"))

    # Optional dependencies
    # Backends
    # Tk
    for backend in ["tkagg", "tkcairo"]:
        depends_on("tk@8.5:", when="@3.8: backend=" + backend, type="run")
        depends_on("tk@8.4:", when="@3.5: backend=" + backend, type="run")
        depends_on("tk@8.3:", when="backend=" + backend, type="run")
        depends_on("python+tkinter", when="backend=" + backend, type="run")
    # Qt
    # matplotlib/backends/qt_compat.py
    for backend in ["qt4agg", "qt4cairo"]:
        depends_on("py-pyqt4@4.6:", when="backend=" + backend, type="run")
        depends_on("qt+gui", when="backend=" + backend, type="run")
    for backend in ["qt5agg", "qt5cairo"]:
        depends_on("py-pyqt5", when="backend=" + backend, type="run")
        depends_on("qt+gui", when="backend=" + backend, type="run")
    for backend in ["qtagg", "qtcairo"]:
        depends_on("py-pyqt6@6.1:", when="backend=" + backend, type="run")
        depends_on("qt-base+gui+widgets", when="backend=" + backend, type="run")
    # GTK
    for backend in ["gtk3agg", "gtk3cairo", "gtk4agg", "gtk4cairo"]:
        depends_on("py-pygobject", when="backend=" + backend, type="run")
        depends_on("py-pycairo@1.14:", when="@3.6: backend=" + backend, type="run")
        depends_on("py-pycairo@1.11:", when="@3.3: backend=" + backend, type="run")
        depends_on("py-pycairo", when="backend=" + backend, type="run")
    # Cairo
    for backend in [
        "gtk3cairo",
        "gtk4cairo",
        "qtcairo",
        "qt4cairo",
        "qt5cairo",
        "tkcairo",
        "wxcairo",
        "cairo",
    ]:
        depends_on("py-pycairo@1.14:", when="@3.6: backend=" + backend, type="run")
        depends_on("py-pycairo@1.11:", when="@3.3: backend=" + backend, type="run")
        depends_on("py-pycairo", when="backend=" + backend, type="run")
    # Wx
    for backend in ["wx", "wxagg", "wxcairo"]:
        depends_on("py-wxpython@4:", when="backend=" + backend, type="run")
    # Other
    depends_on("py-tornado@5:", when="@3.5: backend=webagg", type="run")
    depends_on("py-tornado", when="backend=webagg", type="run")
    depends_on("py-ipykernel", when="backend=nbagg", type="run")

    # Optional dependencies
    depends_on("ffmpeg", when="+movies")
    depends_on("imagemagick", when="+animation")
    depends_on("pil@3.4:", when="+image", type=("build", "run"))
    depends_on("texlive", when="+latex", type="run")
    depends_on("ghostscript@9:", when="+latex", type="run")
    depends_on("fontconfig@2.7:", when="+fonts")
    depends_on("pkgconfig", type="build")

    # C libraries
    depends_on("freetype@2.3: build_system=autotools")
    depends_on("qhull@2020.2:", when="@3.4:")
    # starting from qhull 2020.2 libqhull.so on which py-matplotlib@3.3 versions
    # rely on does not exist anymore, only libqhull_r.so
    depends_on("qhull@2015.2:2020.1", when="@3.3")
    depends_on("libpng@1.2:")

    # Dependencies for building matplotlib
    # Setup dependencies
    depends_on("py-meson-python@0.13.1:", when="@3.9:", type="build")
    depends_on("ninja@1.8.2:", when="@3.9:", type="build")
    depends_on("py-pybind11@2.6:", when="@3.7:", type=("build", "link"))
    depends_on("py-setuptools-scm@7:", when="@3.6:", type="build")
    depends_on("py-setuptools-scm@4:6", when="@3.5", type="build")

    # Historical dependencies
    depends_on("py-certifi@2020.6.20:", when="@3.3.1:3.8", type="build")
    depends_on("py-setuptools@64:", when="@3.8.1:3.8", type="build")
    depends_on("py-setuptools@42:", when="@3.8.0", type="build")
    depends_on("py-setuptools@42:", when="@3.7.2:3.7", type=("build", "run"))
    depends_on("py-setuptools", when="@:3.7.1", type=("build", "run"))
    depends_on("py-setuptools-scm-git-archive", when="@3.5", type="build")

    # Testing dependencies
    # Required
    # https://github.com/spack/spack/issues/43597
    # depends_on("freetype@2.6.1 build_system=autotools", type="test")
    depends_on("py-pytest@7:", type="test")

    msg = "MacOSX backend requires macOS 10.12+"
    conflicts("platform=linux", when="backend=macosx", msg=msg)
    conflicts("platform=windows", when="backend=macosx", msg=msg)

    conflicts("^tk@8.6.0:8.6.1")

    # https://github.com/matplotlib/matplotlib/pull/21662
    patch("matplotlibrc.patch", when="@3.5.0")

    @property
    def archive_files(self):
        if self.spec.satisfies("@3.9:"):
            return [os.path.join(self.stage.source_path, "build", "meson-logs", "meson-log.txt")]
        elif self.spec.satisfies("@3.5:"):
            return [os.path.join(self.build_directory, "mplsetup.cfg")]
        else:
            return [os.path.join(self.build_directory, "setup.cfg")]

    def flag_handler(self, name, flags):
        if name == "cxxflags":
            if self.spec.satisfies("%oneapi"):
                flags.append("-Wno-error=register")
        return (flags, None, None)

    @when("@3.9:")
    def config_settings(self, spec, prefix):
        return {
            "builddir": "build",
            "compile-args": f"-j{make_jobs}",
            "setup-args": {
                "-Dsystem-freetype": True,
                "-Dsystem-qhull": True,
                "-DrcParams-backend": spec.variants["backend"].value,
                # Avoids error where link time opt is used for compile but not link
                "-Db_lto": not (self.spec.satisfies("%clang") or self.spec.satisfies("%oneapi")),
            },
        }

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def copy_reference_images(self):
        # https://matplotlib.org/devdocs/devel/testing.html#obtain-the-reference-images
        install_tree(
            join_path("lib", "matplotlib", "tests", "baseline_images"),
            join_path(python_platlib, "matplotlib", "tests", "baseline_images"),
        )
        if self.spec.satisfies("@3.7:"):
            for toolkit in ["axes_grid1", "axisartist", "mplot3d"]:
                install_tree(
                    join_path("lib", "mpl_toolkits", toolkit, "tests", "baseline_images"),
                    join_path(python_platlib, "mpl_toolkits", toolkit, "tests", "baseline_images"),
                )
        else:
            install_tree(
                join_path("lib", "mpl_toolkits", "tests", "baseline_images"),
                join_path(python_platlib, "mpl_toolkits", "tests", "baseline_images"),
            )

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        # https://matplotlib.org/devdocs/devel/testing.html#run-the-tests
        python("-m", "pytest", "--pyargs", "matplotlib.tests")
        if self.spec.satisfies("@3.7:"):
            for toolkit in ["axes_grid1", "axisartist", "mplot3d"]:
                python("-m", "pytest", "--pyargs", f"mpl_toolkits.{toolkit}.tests")
        else:
            python("-m", "pytest", "--pyargs", "mpl_toolkits.tests")

    @when("@:3.8")
    def setup_build_environment(self, env):
        include = []
        library = []
        for dep in self.spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            include.extend(query.headers.directories)
            try:
                library.extend(query.libs.directories)
            except spack.error.NoLibrariesError:
                pass

        # Build uses a mix of Spack's compiler wrapper and the actual compiler,
        # so this is needed to get parts of the build working.
        # See https://github.com/spack/spack/issues/19843
        env.set("CPATH", ":".join(include))
        env.set("LIBRARY_PATH", ":".join(library))

    @when("@:3.8")
    @run_before("install")
    def configure(self):
        """Set build options with regards to backend GUI libraries."""

        backend = self.spec.variants["backend"].value

        if self.spec.satisfies("@3.5:"):
            config_file = "mplsetup.cfg"
        else:
            config_file = "setup.cfg"

        with open(config_file, "w") as config:
            # Default backend
            config.write("[rc_options]\n")
            config.write("backend = " + backend + "\n")

            # Starting with version 3.3.0, freetype is downloaded by default
            # Force matplotlib to use Spack installations of freetype and qhull
            if self.spec.satisfies("@3.3:"):
                config.write("[libs]\n")
                config.write("system_freetype = True\n")
                config.write("system_qhull = True\n")
                # avoids error where link time opt is used for compile but not link
                if self.spec.satisfies("%clang") or self.spec.satisfies("%oneapi"):
                    config.write("enable_lto = False\n")
