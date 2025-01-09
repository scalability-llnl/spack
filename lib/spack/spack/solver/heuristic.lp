% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% Heuristic to speed-up solves
%=============================================================================

#heuristic attr("node", PackageNode). [300, init]
#heuristic attr("node", PackageNode). [  2, factor]
#heuristic attr("node", PackageNode). [ -1, sign]
#heuristic attr("node", node(0, Dependency)) : attr("dependency_holds", ParentNode, Dependency, Type), not virtual(Dependency). [1@2, sign]

#heuristic attr("virtual_node", node(X, Virtual)). [60, init]
#heuristic attr("virtual_node", node(X, Virtual)). [-1, sign]
#heuristic attr("virtual_node", node(0, Virtual)) : node_depends_on_virtual(PackageNode, Virtual). [1@2, sign]

#heuristic attr("depends_on", ParentNode, ChildNode, Type). [150, init]
#heuristic attr("depends_on", ParentNode, ChildNode, Type). [4,  factor]
#heuristic attr("depends_on", ParentNode, ChildNode, Type). [-1, sign]
#heuristic attr("depends_on", ParentNode, node(0, Dependency), Type) : attr("dependency_holds", ParentNode, Dependency, Type), not virtual(Dependency). [1@2, sign]
#heuristic attr("depends_on", ParentNode, ProviderNode       , Type) : node_depends_on_virtual(ParentNode, Virtual, Type), provider(ProviderNode, node(VirtualID, Virtual)). [1@2, sign]

#heuristic attr("version", node(PackageID, Package), Version). [30, init]
#heuristic attr("version", node(PackageID, Package), Version). [-1, sign]
#heuristic attr("version", node(PackageID, Package), Version) : pkg_fact(Package, version_declared(Version, 0)), attr("node", node(PackageID, Package)). [ 1@2, sign]

#heuristic version_weight(node(PackageID, Package), Weight).                                          [30, init]
#heuristic version_weight(node(PackageID, Package), Weight).                                          [-1  , sign]
#heuristic version_weight(node(PackageID, Package), 0     ) : attr("node", node(PackageID, Package)). [ 1@2, sign]

% Use default variants
#heuristic attr("variant_value", PackageNode, Variant, Value). [30, init]
#heuristic attr("variant_value", PackageNode, Variant, Value). [-1, sign]
#heuristic attr("variant_value", PackageNode, Variant, Value) : variant_default_value(PackageNode, Variant, Value), attr("node", PackageNode). [1@2, sign]

% Use default targets
#heuristic attr("node_target", node(PackageID, Package), Target). [-1, sign]
#heuristic attr("node_target", node(PackageID, Package), Target) : target_weight(Target, 0), attr("node", node(PackageID, Package)). [1@2, sign]

% Use the default compilers
#heuristic node_compiler(node(PackageID, Package), ID) : compiler_weight(ID, 0), compiler_id(ID), attr("node", node(PackageID, Package)). [30, init]
