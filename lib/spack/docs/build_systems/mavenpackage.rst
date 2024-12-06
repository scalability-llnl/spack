.. Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _mavenpackage:

-----
Maven
-----

Apache Maven is a general-purpose build system that does not rely
on Makefiles to build software. It is designed for building and
managing and Java-based project.

^^^^^^
Phases
^^^^^^

The ``MavenBuilder`` and ``MavenPackage`` base classes come with the following phases:

#. ``build`` - compile code and package into a JAR file
#. ``install`` - copy to installation prefix

By default, these phases run:

.. code-block:: console

   $ mvn package
   $ install . <prefix>


^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Maven packages can be identified by the presence of a ``pom.xml`` file.
This file lists dependencies and other metadata about the project.
There may also be configuration files in the ``.mvn`` directory.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

Maven requires the ``mvn`` executable to build the project. It also
requires Java at both build- and run-time. Because of this, the base
class automatically adds the following dependencies:

.. code-block:: python

   depends_on("java", type=("build", "run"))
   depends_on("maven", type="build")


In the ``pom.xml`` file, you may see sections like:

.. code-block:: xml

   <requireJavaVersion>
      <version>[1.7,)</version>
   </requireJavaVersion>
   <requireMavenVersion>
      <version>[3.5.4,)</version>
   </requireMavenVersion>


This specifies the versions of Java and Maven that are required to
build the package. See
https://docs.oracle.com/middleware/1212/core/MAVEN/maven_version.htm#MAVEN402
for a description of this version range syntax. In this case, you
should add:

.. code-block:: python

   depends_on("java@7:", type="build")
   depends_on("maven@3.5.4:", type="build")


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to the build phase
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default build and install phases should be sufficient to install
most packages. However, you may want to pass additional flags to
the build phase. For example:

.. code-block:: python

   def build_args(self):
       return [
           "-Pdist,native",
           "-Dtar",
           "-Dmaven.javadoc.skip=true"
       ]


^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on the Maven build system, see:
https://maven.apache.org/index.html
