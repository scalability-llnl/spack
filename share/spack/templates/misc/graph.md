flowchart TD

{% for node, node_options in nodes %}
{% if node_options %}
  {{ node }}{{ node_options }}
{% else %}
  {{ node }}
{% endif %}
{% endfor %}
{% for edge_parent, edge_child, edge_options in edges %}
{% if edge_options %}
  {{ edge_parent }} --> {{ edge_child }}{{ edge_options }}
{% else %}
  {{ edge_parent }} --> {{ edge_child }}
{% endif %}
{% endfor %}