# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import shutil

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack
import spack.cmd
import spack.config
import spack.paths
import spack.util.git
import spack.util.gpg
from spack.cmd.common import arguments
from spack.util.spack_yaml import syaml_dict

description = "set up spack for our tutorial (WARNING: modifies config!)"
section = "config"
level = "long"


# tutorial configuration parameters
tutorial_branch = "releases/v0.22"
tutorial_mirror = "file:///mirror"
tutorial_key = os.path.join(spack.paths.share_path, "keys", "tutorial.pub")

# configs to remove
rm_configs = [
    "~/.spack/linux/compilers.yaml",
    "~/.spack/packages.yaml",
    "~/.spack/mirrors.yaml",
    "~/.spack/modules.yaml",
    "~/.spack/config.yaml",
]


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["yes_to_all"])


def tutorial(parser, args):
    if not spack.cmd.spack_is_git_repo():
        tty.die("This command requires a git installation of Spack!")

    if not args.yes_to_all:
        tty.msg(
            "This command will set up Spack for the tutorial at "
            "https://spack-tutorial.readthedocs.io.",
            "",
        )
        tty.warn(
            "This will modify your Spack configuration by:",
            "  - deleting some configuration in ~/.spack",
            "  - adding a mirror and trusting its public key",
            "  - checking out a particular branch of Spack",
            "",
        )
        if not tty.get_yes_or_no("Are you sure you want to proceed?"):
            tty.die("Aborted")

    rm_cmds = [f"rm -f {f}" for f in rm_configs]
    tty.msg("Reverting compiler and repository configuration", *rm_cmds)
    for path in rm_configs:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

    tty.msg(
        "Ensuring that the tutorial binary mirror is configured:",
        f"spack mirror add tutorial {tutorial_mirror}",
    )
    mirror_config = syaml_dict()
    mirror_config["tutorial"] = tutorial_mirror
    spack.config.set("mirrors", mirror_config, scope="user")

    tty.msg("Ensuring that we trust tutorial binaries", f"spack gpg trust {tutorial_key}")
    spack.util.gpg.trust(tutorial_key)

    # Note that checkout MUST be last. It changes Spack under our feet.
    # If you don't put this last, you'll get import errors for the code
    # that follows (exacerbated by the various lazy singletons we use)
    tty.msg(f"Ensuring we're on the {tutorial_branch} branch")
    git = spack.util.git.git(required=True)
    with working_dir(spack.paths.prefix):
        git("checkout", tutorial_branch)
    # NO CODE BEYOND HERE
