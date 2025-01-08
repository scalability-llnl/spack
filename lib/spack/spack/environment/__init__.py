# -*- coding: utf-8 -*-
# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This package implements Spack environments.

.. _lockfile-format:

`spack.lock` format
===================

Spack environments have existed since Spack ``v0.12.0``, and there have been 4 different
``spack.lock`` formats since then. The formats are documented here.

The high-level format of a Spack lockfile hasn't changed much between versions, but the
contents have.  Lockfiles are JSON-formatted and their top-level sections are:

  1. ``_meta`` (object): this contains details about the file format, including:
      * ``file-type``: always ``"spack-lockfile"``
      * ``lockfile-version``: an integer representing the lockfile format version
      * ``specfile-version``: an integer representing the spec format version (since
        ``v0.17``)

  2. ``spack`` (object): optional, this identifies information about Spack
      used to concretize the environment:
      * ``type``: required, identifies form Spack version took (e.g., ``git``, ``release``)
      * ``commit``: the commit if the version is from git
      * ``version``: the Spack version

  3. ``roots`` (list): an ordered list of records representing the roots of the Spack
      environment. Each has two fields:
      * ``hash``: a Spack spec hash uniquely identifying the concrete root spec
      * ``spec``: a string representation of the abstract spec that was concretized

  4. ``concrete_specs``: a dictionary containing the specs in the environment.
  5. ``include_concrete`` (dictionary): an optional dictionary that includes the roots
     and concrete specs from the included environments, keyed by the path to that
     environment

Compatibility
-------------

New versions of Spack can (so far) read all old lockfile formats -- they are
backward-compatible. Old versions cannot read new lockfile formats, and you'll need to
upgrade Spack to use them.

.. list-table:: Lockfile version compatibility across Spack versions
   :header-rows: 1

   * - Spack version
     - ``v1``
     - ``v2``
     - ``v3``
     - ``v4``
     - ``v5``
   * - ``v0.12:0.14``
     - ✅
     -
     -
     -
     -
   * - ``v0.15:0.16``
     - ✅
     - ✅
     -
     -
     -
   * - ``v0.17``
     - ✅
     - ✅
     - ✅
     -
     -
   * - ``v0.18:``
     - ✅
     - ✅
     - ✅
     - ✅
     -
   * - ``v0.22:``
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅

Version 1
---------

When lockfiles were first created, there was only one hash in Spack: the DAG hash. This
DAG hash (we'll call it the old DAG hash) did *not* include build dependencies -- it
only included transitive link and run dependencies.

The spec format at this time was keyed by name. Each spec started with a key for its
name, whose value was a dictionary of other spec attributes. The lockfile put these
name-keyed specs into dictionaries keyed by their DAG hash, and the spec records did not
actually have a "hash" field in the lockfile -- you have to associate the hash from the
key with the spec record after the fact.

Dependencies in original lockfiles were keyed by ``"hash"``, i.e. the old DAG hash.

.. code-block:: json

    {
        "_meta": {
            "file-type": "spack-lockfile",
            "lockfile-version": 1
        },
        "roots": [
            {
                "hash": "<old_dag_hash 1>",
                "spec": "<abstract spec 1>"
            },
            {
                "hash": "<old_dag_hash 2>",
                "spec": "<abstract spec 2>"
            }
        ],
        "concrete_specs": {
            "<old_dag_hash 1>": {
                "... <spec dict attributes> ...": { },
                "dependencies": {
                    "depname_1": {
                        "hash": "<old_dag_hash for depname_1>",
                        "type": ["build", "link"]
                    },
                    "depname_2": {
                        "hash": "<old_dag_hash for depname_3>",
                        "type": ["build", "link"]
                    }
                },
                "hash": "<old_dag_hash 1>"
            },
            "<old_dag_hash 2>": {
                "... <spec dict attributes> ...": { },
                "dependencies": {
                    "depname_3": {
                        "hash": "<old_dag_hash for depname_3>",
                        "type": ["build", "link"]
                    },
                    "depname_4": {
                        "hash": "<old_dag_hash for depname_4>",
                        "type": ["build", "link"]
                    },
                },
                "hash": "<old_dag_hash 2>"
            },
        }
    }


Version 2
---------

Version 2 changes one thing: specs in the lockfile are now keyed by ``build_hash``
instead of the old ``dag_hash``. Specs have a ``hash`` attribute with their real DAG
hash, so you can't go by the dictionary key anymore to identify a spec -- you have to
read it in and look at ``"hash"``. Dependencies are still keyed by old DAG hash.

Even though we key lockfiles by ``build_hash``, specs in Spack were still deployed with
the old, coarser DAG hash. This means that in v2 and v3 lockfiles (which are keyed by
build hash), there may be multiple versions of the same spec with different build
dependencies, which means they will have different build hashes but the same DAG hash.
Spack would only have been able to actually install one of these.

.. code-block:: json

    {
        "_meta": {
            "file-type": "spack-lockfile",
            "lockfile-version": 2
        },
        "roots": [
            {
                "hash": "<build_hash 1>",
                "spec": "<abstract spec 1>"
            },
            {
                "hash": "<build_hash 2>",
                "spec": "<abstract spec 2>"
            }
        ],
        "concrete_specs": {
            "<build_hash 1>": {
                "... <spec dict attributes> ...": { },
                "dependencies": {
                    "depname_1": {
                        "hash": "<old_dag_hash for depname_1>",
                        "type": ["build", "link"]
                    },
                    "depname_2": {
                        "hash": "<old_dag_hash for depname_3>",
                        "type": ["build", "link"]
                    }
                },
                "hash": "<old_dag_hash 1>",
            },
            "<build_hash 2>": {
                "... <spec dict attributes> ...": { },
                "dependencies": {
                    "depname_3": {
                        "hash": "<old_dag_hash for depname_3>",
                        "type": ["build", "link"]
                    },
                    "depname_4": {
                        "hash": "<old_dag_hash for depname_4>",
                        "type": ["build", "link"]
                    }
                },
                "hash": "<old_dag_hash 2>"
            }
        }
    }


Version 3
---------

Version 3 doesn't change the top-level lockfile format, but this was when we changed the
specfile format. Specs in ``concrete_specs`` are now keyed by the build hash, with no
inner dictionary keyed by their package name. The package name is in a ``name`` field
inside each spec dictionary. The ``dependencies`` field in the specs is a list instead
of a dictionary, and each element of the list is a record with the name, dependency
types, and hash of the dependency. Instead of a key called ``hash``, dependencies are
keyed by ``build_hash``. Each spec still has a ``hash`` attribute.

Version 3 adds the ``specfile_version`` field to ``_meta`` and uses the new JSON spec
format.

.. code-block:: json

    {
        "_meta": {
            "file-type": "spack-lockfile",
            "lockfile-version": 3,
            "specfile-version": 2
        },
        "roots": [
            {
                "hash": "<build_hash 1>",
                "spec": "<abstract spec 1>"
            },
            {
                "hash": "<build_hash 2>",
                "spec": "<abstract spec 2>"
            },
        ],
        "concrete_specs": {
            "<build_hash 1>": {
                "... <spec dict attributes> ...": { },
                "dependencies": [
                    {
                        "name": "depname_1",
                        "build_hash": "<build_hash for depname_1>",
                        "type": ["build", "link"]
                    },
                    {
                        "name": "depname_2",
                        "build_hash": "<build_hash for depname_2>",
                        "type": ["build", "link"]
                    },
                ],
                "hash": "<old_dag_hash 1>",
            },
            "<build_hash 2>": {
                "... <spec dict attributes> ...": { },
                "dependencies": [
                    {
                        "name": "depname_3",
                        "build_hash": "<build_hash for depname_3>",
                        "type": ["build", "link"]
                    },
                    {
                        "name": "depname_4",
                        "build_hash": "<build_hash for depname_4>",
                        "type": ["build", "link"]
                    },
                ],
                "hash": "<old_dag_hash 2>"
            }
        }
    }


Version 4
---------

Version 4 removes build hashes and is keyed by the new DAG hash (``hash``). The ``hash``
now includes build dependencies and a canonical hash of the ``package.py`` file.
Dependencies are keyed by ``hash`` (DAG hash) as well. There are no more ``build_hash``
fields in the specs, and there are no more issues with lockfiles being able to store
multiple specs with the same DAG hash (because the DAG hash is now finer-grained).
An optional ``spack`` property may be included to track version information, such as
the commit or version.


.. code-block:: json

    {
        "_meta": {
            "file-type": "spack-lockfile",
            "lockfile-version": 4,
            "specfile-version": 3
        },
        "roots": [
            {
                "hash": "<dag_hash 1>",
                "spec": "<abstract spec 1>"
            },
            {
                "hash": "<dag_hash 2>",
                "spec": "<abstract spec 2>"
            }
        ],
        "concrete_specs": {
            "<dag_hash 1>": {
                "... <spec dict attributes> ...": { },
                "dependencies": [
                    {
                        "name": "depname_1",
                        "hash": "<dag_hash for depname_1>",
                        "type": ["build", "link"]
                    },
                    {
                        "name": "depname_2",
                        "hash": "<dag_hash for depname_2>",
                        "type": ["build", "link"]
                    }
                ],
                "hash": "<dag_hash 1>",
            },
            "<daghash 2>": {
                "... <spec dict attributes> ...": { },
                "dependencies": [
                    {
                        "name": "depname_3",
                        "hash": "<dag_hash for depname_3>",
                        "type": ["build", "link"]
                    },
                    {
                        "name": "depname_4",
                        "hash": "<dag_hash for depname_4>",
                        "type": ["build", "link"]
                    }
                ],
                "hash": "<dag_hash 2>"
            }
        }
    }


Version 5
---------

Version 5 doesn't change the top-level lockfile format, but an optional dictionary is
added. The dictionary has the ``root`` and ``concrete_specs`` of the included
environments, which are keyed by the path to that environment. Since this is optional
if the environment does not have any included environments ``include_concrete`` will
not be a part of the lockfile.

.. code-block:: json

    {
        "_meta": {
            "file-type": "spack-lockfile",
            "lockfile-version": 5,
            "specfile-version": 3
        },
        "roots": [
            {
                "hash": "<dag_hash 1>",
                "spec": "<abstract spec 1>"
            },
            {
                "hash": "<dag_hash 2>",
                "spec": "<abstract spec 2>"
            }
        ],
        "concrete_specs": {
            "<dag_hash 1>": {
                "... <spec dict attributes> ...": { },
                "dependencies": [
                    {
                        "name": "depname_1",
                        "hash": "<dag_hash for depname_1>",
                        "type": ["build", "link"]
                    },
                    {
                        "name": "depname_2",
                        "hash": "<dag_hash for depname_2>",
                        "type": ["build", "link"]
                    }
                ],
                "hash": "<dag_hash 1>",
            },
            "<daghash 2>": {
                "... <spec dict attributes> ...": { },
                "dependencies": [
                    {
                        "name": "depname_3",
                        "hash": "<dag_hash for depname_3>",
                        "type": ["build", "link"]
                    },
                    {
                        "name": "depname_4",
                        "hash": "<dag_hash for depname_4>",
                        "type": ["build", "link"]
                    }
                ],
                "hash": "<dag_hash 2>"
            }
        }
        "include_concrete": {
            "<path to environment>": {
                "roots": [
                    {
                        "hash": "<dag_hash 1>",
                        "spec": "<abstract spec 1>"
                    },
                    {
                        "hash": "<dag_hash 2>",
                        "spec": "<abstract spec 2>"
                    }
                ],
                "concrete_specs": {
                    "<dag_hash 1>": {
                        "... <spec dict attributes> ...": { },
                        "dependencies": [
                            {
                                "name": "depname_1",
                                "hash": "<dag_hash for depname_1>",
                                "type": ["build", "link"]
                            },
                            {
                                "name": "depname_2",
                                "hash": "<dag_hash for depname_2>",
                                "type": ["build", "link"]
                            }
                        ],
                        "hash": "<dag_hash 1>",
                    },
                    "<daghash 2>": {
                        "... <spec dict attributes> ...": { },
                        "dependencies": [
                            {
                                "name": "depname_3",
                                "hash": "<dag_hash for depname_3>",
                                "type": ["build", "link"]
                            },
                            {
                                "name": "depname_4",
                                "hash": "<dag_hash for depname_4>",
                                "type": ["build", "link"]
                            }
                        ],
                        "hash": "<dag_hash 2>"
                    }
                }
            }
        }
    }
"""

from .environment import (
    TOP_LEVEL_KEY,
    Environment,
    SpackEnvironmentConfigError,
    SpackEnvironmentError,
    SpackEnvironmentViewError,
    activate,
    active,
    active_environment,
    all_environment_names,
    all_environments,
    as_env_dir,
    create,
    create_in_dir,
    deactivate,
    default_manifest_yaml,
    default_view_name,
    display_specs,
    environment_dir_from_name,
    environment_from_name_or_dir,
    environment_path_scopes,
    exists,
    initialize_environment_dir,
    installed_specs,
    is_env_dir,
    is_latest_format,
    lockfile_name,
    manifest_file,
    manifest_name,
    no_active_environment,
    read,
    root,
    spack_env_var,
    spack_env_view_var,
    update_yaml,
)

__all__ = [
    "TOP_LEVEL_KEY",
    "Environment",
    "SpackEnvironmentConfigError",
    "SpackEnvironmentError",
    "SpackEnvironmentViewError",
    "activate",
    "active",
    "active_environment",
    "all_environment_names",
    "all_environments",
    "as_env_dir",
    "create",
    "create_in_dir",
    "deactivate",
    "default_manifest_yaml",
    "default_view_name",
    "display_specs",
    "environment_dir_from_name",
    "environment_from_name_or_dir",
    "environment_path_scopes",
    "exists",
    "initialize_environment_dir",
    "installed_specs",
    "is_env_dir",
    "is_latest_format",
    "lockfile_name",
    "manifest_file",
    "manifest_name",
    "no_active_environment",
    "read",
    "root",
    "spack_env_var",
    "spack_env_view_var",
    "update_yaml",
]
