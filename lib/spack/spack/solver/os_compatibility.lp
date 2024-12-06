% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% OS compatibility rules for reusing solves.
% os_compatible(RecentOS, OlderOS)
% OlderOS binaries can be used on RecentOS
%
% These rules are used on every platform, but Linux
%=============================================================================

% macOS
os_compatible("sequoia", "sonoma").
os_compatible("sonoma", "ventura").
os_compatible("ventura", "monterey").
os_compatible("monterey", "bigsur").
os_compatible("bigsur", "catalina").

% can't have dependencies on incompatible OS's
error(100, "{0} and dependency {1} have incompatible operating systems 'os={2}' and 'os={3}'", Package, Dependency, PackageNodeOS, DependencyOS)
  :- depends_on(node(X, Package), node(Y, Dependency)),
     attr("node_os", node(X, Package), PackageNodeOS),
     attr("node_os", node(Y, Dependency), DependencyOS),
     not os_compatible(PackageNodeOS, DependencyOS),
     build(node(X, Package)).

% We can select only operating systems compatible with the ones
% for which we can build software. We need a cardinality constraint
% since we might have more than one "buildable_os(OS)" fact.
:- not 1 { os_compatible(CurrentOS, ReusedOS) : buildable_os(CurrentOS) },
   attr("node_os", Package, ReusedOS).
