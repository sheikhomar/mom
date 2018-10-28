#!/usr/bin/env python
import json
import pydot

def load_config():
    with open('generated/simulation.json', 'r') as f:
        content = f.read()
    content = content[1:len(content)-1].replace('\\"', '"')
    return json.loads(content)


def generate_station(station):
    name = station['name']
    totes = station['totes']
    node = pydot.Node(name, shape='box')
    if len(totes) > 0:
        label = name
        for tote in totes:
            label += '\\nt' + str(tote['id'])
        node.set('label', label)
    return node


def generate_segment(graph, segment):
    src_node = graph.get_node(segment['source'])[0]
    trg_node = graph.get_node(segment['target'])[0]
    edge = pydot.Edge(src=src_node, dst=trg_node)
    totes = segment['totes']
    label = str(segment['distance'])
    for tote in totes:
        label += '\\nt{}:{}'.format(tote['id'], tote['position'])
    edge.set('label', label)
    return edge


def main():
    config = load_config()

    for index, run in enumerate(config):
        if 'stations' in run:
            graph = pydot.Dot(graph_type='digraph', rankdir='LR')
            graph.set('autosize', 'false')
            graph.set('size', '15,6!')
            graph.set('resolution', '100')
            for station in run['stations']:
                graph.add_node(generate_station(station))
            for segment in run['segments']:
                edge = generate_segment(graph, segment)
                graph.add_edge(edge)
            graph.write('generated/simulation_graph_{}.png'.format(index), format='png')
            graph.write('generated/simulation_graph_{}.xdot'.format(index))


if __name__ == '__main__':
    main()
