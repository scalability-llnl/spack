# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Manages the details on the images used in the various stages."""
import json
import os.path
import shlex
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.util.git

#: Global variable used to cache in memory the content of images.json
_data = None


def data():
    """Returns a dictionary with the static data on the images.

    The dictionary is read from a JSON file lazily the first time
    this function is called.
    """
    global _data
    if not _data:
        json_dir = os.path.abspath(os.path.dirname(__file__))
        json_file = os.path.join(json_dir, "images.json")
        with open(json_file) as f:
            _data = json.load(f)
    return _data


def build_info(image, spack_version):
    """Returns the name of the build image and its tag.

    Args:
        image (str): image to be used at run-time. Should be of the form
            <image_name>:<image_tag> e.g. "ubuntu:18.04"
        spack_version (str): version of Spack that we want to use to build

    Returns:
        A tuple with (image_name, image_tag) for the build image
    """
    # Don't handle error here, as a wrong image should have been
    # caught by the JSON schema
    image_data = data()["images"][image]
    build_image = image_data.get("build", None)
    if not build_image:
        return None, None

    return build_image, spack_version


def os_package_manager_for(image):
    """Returns the name of the OS package manager for the image
    passed as argument.

    Args:
        image (str): image to be used at run-time. Should be of the form
            <image_name>:<image_tag> e.g. "ubuntu:18.04"

    Returns:
        Name of the package manager, e.g. "apt" or "yum"
    """
    name = data()["images"][image]["os_package_manager"]
    return name


def all_bootstrap_os():
    """Return a list of all the OS that can be used to bootstrap Spack"""
    return list(data()["images"])


def commands_for(package_manager):
    """Returns the commands used to update system repositories, install
    system packages and clean afterwards.

    Args:
        package_manager (str): package manager to be used

    Returns:
        A tuple of (update, install, clean) commands.
    """
    info = data()["os_package_managers"][package_manager]
    return info["update"], info["install"], info["clean"]


def bootstrap_template_for(image):
    return data()["images"][image]["bootstrap"]["template"]


def _verify_ref(url, ref, enforce_sha):
    # Do a checkout in a temporary directory
    msg = 'Cloning "{0}" to verify ref "{1}"'.format(url, ref)
    tty.info(msg, stream=sys.stderr)
    git = spack.util.git.git(required=True)
    with fs.temporary_dir():
        git("clone", "-q", url, ".")
        sha = git(
            "rev-parse", "-q", ref + "^{commit}", output=str, error=os.devnull, fail_on_error=False
        )
        if git.returncode:
            msg = '"{0}" is not a valid reference for "{1}"'
            raise RuntimeError(msg.format(sha, url))

        if enforce_sha:
            ref = sha.strip()

        return ref


def checkout_command(url, ref, enforce_sha, verify):
    """Return the checkout command to be used in the bootstrap phase.

    Args:
        url (str): url of the Spack repository
        ref (str): either a branch name, a tag or a commit sha
        enforce_sha (bool): if true turns every
        verify (bool):
    """
    url = url or "https://github.com/spack/spack.git"
    ref = ref or "develop"
    enforce_sha, verify = bool(enforce_sha), bool(verify)
    # If we want to enforce a sha or verify the ref we need
    # to checkout the repository locally
    if enforce_sha or verify:
        ref = _verify_ref(url, ref, enforce_sha)

    return " && ".join(
        [
            "git init --quiet",
            f"git remote add origin {shlex.quote(url)}",
            f"git fetch --depth=1 origin {shlex.quote(ref)}",
            "git checkout --detach FETCH_HEAD",
        ]
    )
