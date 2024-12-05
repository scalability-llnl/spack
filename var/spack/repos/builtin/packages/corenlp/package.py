# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Corenlp(Package):
    """Stanford CoreNLP provides a set of human language technology
    tools. It can give the base forms of words, their parts of speech,
    whether they are names of companies, people, etc., normalize
    dates, times, and numeric quantities, mark up the structure of
    sentences in terms of phrases and syntactic dependencies, indicate
    which noun phrases refer to the same entities, indicate sentiment,
    extract particular or open-class relations between entity
    mentions, get the quotes people said, etc."""

    homepage = "https://stanfordnlp.github.io/CoreNLP/index.html"
    url = "https://github.com/stanfordnlp/CoreNLP/archive/v4.0.0.tar.gz"

    license("GPL-3.0-only")

    version("4.0.0", sha256="07195eed46dd39bdc364d3988da8ec6a5fc9fed8c17613cfe5a8b84d649c8f0f")

    resources = [("4.0.0", "f45bde062fb368d72f7d3c7ac1ddc6cfb61d3badc1152572bde17f1a5ed9ec94")]
    for ver, checksum in resources:
        jarfile = "stanford-corenlp-{0}-models.jar".format(ver)
        resource(
            when="@{0}".format(ver),
            name=jarfile,
            url="https://repo1.maven.org/maven2/edu/stanford/nlp/stanford-corenlp/{0}/{1}".format(
                ver, jarfile
            ),
            expand=False,
            destination="",
            placement=jarfile,
            sha256=checksum,
        )

    depends_on("ant", type="build")

    def install(self, spec, prefix):
        ant = self.spec["ant"].command
        ant()

        with working_dir("classes"):
            jar = Executable("jar")
            jar("-cf", "../stanford-corenlp.jar", "edu")

        install_tree(".", prefix.lib)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        mkdirp(prefix.bin)
        script_sh = join_path(os.path.dirname(__file__), "corenlp.sh")
        script = prefix.bin.corenlp
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec["java"].prefix.bin.java
        kwargs = {"ignore_absent": False, "backup": False, "string": False}
        filter_file("^java", java, script, **kwargs)

    def setup_run_environment(self, run_env):
        class_paths = []
        class_paths.extend(find(prefix.lib, "*.jar"))
        classpath = os.pathsep.join(class_paths)
        run_env.prepend_path("CLASSPATH", classpath)
