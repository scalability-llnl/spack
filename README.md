# <img src="https://cdn.rawgit.com/spack/spack/develop/share/spack/logo/spack-logo.svg" width="64" valign="middle" alt="Spack"/> Spack

[![Unit Tests](https://github.com/spack/spack/workflows/linux%20tests/badge.svg)](https://github.com/spack/spack/actions)
[![Linux Builds](https://github.com/spack/spack/workflows/linux%20builds/badge.svg)](https://github.com/spack/spack/actions)
[![macOS Builds (nightly)](https://github.com/spack/spack/workflows/macOS%20builds%20nightly/badge.svg?branch=develop)](https://github.com/spack/spack/actions?query=workflow%3A%22macOS+builds+nightly%22)
[![codecov](https://codecov.io/gh/spack/spack/branch/develop/graph/badge.svg)](https://codecov.io/gh/spack/spack)
[![Read the Docs](https://readthedocs.org/projects/spack/badge/?version=latest)](https://spack.readthedocs.io)
[![Slack](https://spackpm.herokuapp.com/badge.svg)](https://spackpm.herokuapp.com)

Spack is a multi-platform package manager that builds and installs
multiple versions and configurations of software. It works on Linux,
macOS, and many supercomputers. Spack is non-destructive: installing a
new version of a package does not break existing installations, so many
configurations of the same package can coexist.

Spack offers a simple "spec" syntax that allows users to specify versions
and configuration options. Package files are written in pure Python, and
specs allow package authors to write a single script for many different
builds of the same package.  With Spack, you can build your software
*all* the ways you want to.

See the
[Feature Overview](https://spack.readthedocs.io/en/latest/features.html)
for examples and highlights.

To install spack and your first package, make sure you have Python.
Then:

    $ git clone https://github.com/spack/spack.git
    $ cd spack/bin
    $ ./spack install zlib

Documentation
----------------

[**Full documentation**](https://spack.readthedocs.io/) is available, or
run `spack help` or `spack help --all`.

Tutorial
----------------

We maintain a
[**hands-on tutorial**](https://spack.readthedocs.io/en/latest/tutorial.html).
It covers basic to advanced usage, packaging, developer features, and large HPC
deployments.  You can do all of the exercises on your own laptop using a
Docker container.

Feel free to use these materials to teach users at your organization
about Spack.

Community
------------------------

Spack is an open source project.  Questions, discussion, and
contributions are welcome. Contributions can be anything from new
packages to bugfixes, documentation, or even new core features.

Resources:

* **Slack workspace**: [spackpm.slack.com](https://spackpm.slack.com).
  To get an invitation, [**click here**](https://spackpm.herokuapp.com).
* **Mailing list**: [groups.google.com/d/forum/spack](https://groups.google.com/d/forum/spack)
* **Twitter**: [@spackpm](https://twitter.com/spackpm). Be sure to
  `@mention` us!

Contributing
------------------------
Contributing to Spack is relatively easy.  Just send us a
[pull request](https://help.github.com/articles/using-pull-requests/).
When you send your request, make ``develop`` the destination branch on the
[Spack repository](https://github.com/spack/spack).

Your PR must pass Spack's unit tests and documentation tests, and must be
[PEP 8](https://www.python.org/dev/peps/pep-0008/) compliant.  We enforce
these guidelines with our CI process. To run these tests locally, and for 
helpful tips on git, see our
[Contribution Guide](https://spack.readthedocs.io/en/latest/contribution_guide.html).

Spack's `develop` branch has the latest contributions. Pull requests
should target `develop`, and users who want the latest package versions,
features, etc. can use `develop`.

Releases
--------

For multi-user site deployments or other use cases that need very stable
software installations, we recommend using Spack's
[stable releases](https://github.com/spack/spack/releases).

Each Spack release series also has a corresponding branch, e.g.
`releases/v0.14` has `0.14.x` versions of Spack, and `releases/v0.13` has
`0.13.x` versions. We backport important bug fixes to these branches but
we do not advance the package versions or make other changes that would
change the way Spack concretizes dependencies within a release branch.
So, you can base your Spack deployment on a release branch and `git pull`
to get fixes, without the package churn that comes with `develop`.

The latest release is always available with the `releases/latest` tag.

See the [docs on releases](https://spack.readthedocs.io/en/latest/developer_guide.html#releases)
for more details.

Code of Conduct
------------------------

Please note that Spack has a
[**Code of Conduct**](.github/CODE_OF_CONDUCT.md). By participating in
the Spack community, you agree to abide by its rules.

Authors
----------------
Many thanks go to Spack's [contributors](https://github.com/spack/spack/graphs/contributors).

Spack was created by Todd Gamblin, tgamblin@llnl.gov.

### Citing Spack

If you are referencing Spack in a publication, please cite the following paper:

 * Todd Gamblin, Matthew P. LeGendre, Michael R. Collette, Gregory L. Lee,
   Adam Moody, Bronis R. de Supinski, and W. Scott Futral.
   [**The Spack Package Manager: Bringing Order to HPC Software Chaos**](https://www.computer.org/csdl/proceedings/sc/2015/3723/00/2807623.pdf).
   In *Supercomputing 2015 (SC’15)*, Austin, Texas, November 15-20 2015. LLNL-CONF-669890.

License
----------------

Spack is distributed under the terms of both the MIT license and the
Apache License (Version 2.0). Users may choose either license, at their
option.

All new contributions must be made under both the MIT and Apache-2.0
licenses.

See [LICENSE-MIT](https://github.com/spack/spack/blob/develop/LICENSE-MIT),
[LICENSE-APACHE](https://github.com/spack/spack/blob/develop/LICENSE-APACHE),
[COPYRIGHT](https://github.com/spack/spack/blob/develop/COPYRIGHT), and
[NOTICE](https://github.com/spack/spack/blob/develop/NOTICE) for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811652
