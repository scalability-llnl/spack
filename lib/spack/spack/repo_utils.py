# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#: Package modules are imported as spack.pkg.<repo-namespace>.<pkg-name>
ROOT_PYTHON_NAMESPACE = "spack.pkg"


def namespace_from_fullname(fullname):
    """Return the repository namespace only for the full module name.

    For instance:

        namespace_from_fullname('spack.pkg.builtin.hdf5') == 'builtin'

    Args:
        fullname (str): full name for the Python module
    """
    namespace, dot, module = fullname.rpartition(".")
    prefix_and_dot = "{0}.".format(ROOT_PYTHON_NAMESPACE)
    if namespace.startswith(prefix_and_dot):
        namespace = namespace[len(prefix_and_dot) :]
    return namespace


def python_package_for_repo(namespace):
    """Returns the full namespace of a repository, given its relative one

    For instance:

        python_package_for_repo('builtin') == 'spack.pkg.builtin'

    Args:
        namespace (str): repo namespace
    """
    return "{0}.{1}".format(ROOT_PYTHON_NAMESPACE, namespace)
