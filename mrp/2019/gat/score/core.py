from graph import Graph;
from operator import itemgetter;

def intersect(golds, systems):
  gold = {};
  system = {};
  for graph in golds: gold[graph.id] = graph;
  for graph in systems: system[graph.id] = graph;
  for key in gold.keys():
    if key in gold and key in system:
      yield gold[key], system[key];

def anchor(node):
  result = list();
  if node.anchors != None:
    for anchor in node.anchors:
      if anchor and "from" in anchor and "to" in anchor:
        result.append((anchor["from"], anchor["to"]));
  return result;

def identify(graph, node, map = dict()):
  if node in map:
    return map;
  map[node] = anchor(graph.find_node(node));
  for edge in graph.edges:
    if node == edge.src:
      identify(graph, edge.tgt, map);
      map[node] += map[edge.tgt];
  for key in map:
    map[key] = tuple(sorted(map[key], key = itemgetter(0, 1)));
  return map;

def fscore(gold, system, correct):
  p = correct / system if system else 0.0;
  r = correct / gold if gold else 0.0;
  f = 2 * p * r / (p + r) if p + r != 0 else 0.0;
  return p, r, f;
