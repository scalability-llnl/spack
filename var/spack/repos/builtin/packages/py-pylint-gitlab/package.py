# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPylintGitlab(PythonPackage):
    """This project provides pylint formatters for a nice integration with GitLab CI."""

    homepage = "https://gitlab.com/smueller18/pylint-gitlab"
    pypi = "pylint-gitlab/pylint-gitlab-2.0.0.tar.gz"

    git = "https://gitlab.com/smueller18/pylint-gitlab.git"

    # Unfortunately, this just installs from git.
    # The setup needs the file "Pipfile.lock" which is only
    # available in git, not in a tarball.
    version("2.0.0", tag="2.0.0")

    depends_on("py-setuptools", type="build")
    depends_on("py-pylint", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-anybadge", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-tomli", type=("build", "run"))
    depends_on("py-dill", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("CI_COMMIT_TAG", self.spec.version.string)
