#!/usr/bin/env python
import json
import pydot
import glob
from PIL import Image

TOTE_COLORS = {
    1: 'green',
    2: 'blue',
    3: 'red',
    4: 'purple'
}


def load_config():
    with open('generated/simulation.json', 'r') as f:
        content = f.read()
    content = content[1:len(content)-1].replace('\\"', '"')
    obj = json.loads(content)
    print(json.dumps(obj, indent=2))
    return obj


def get_tote_label(tote):
    id = tote['id']
    color = TOTE_COLORS[id]
    label = f'<br/><font color="{color}">t{id}</font>'
    if 'position' in tote:
        label += f':{tote["position"]}'
    return label


def generate_station(station):
    name = station['name']
    totes = station['totes']
    node = pydot.Node(name, shape='box')
    if len(totes) > 0:
        label = f'<{name}'
        for tote in totes:
            label += get_tote_label(tote)
        label += '>'
        node.set('label', label)
    return node


def generate_segment(graph, segment):
    src_node = graph.get_node(segment['source'])[0]
    trg_node = graph.get_node(segment['target'])[0]
    edge = pydot.Edge(src=src_node, dst=trg_node)
    totes = segment['totes']
    label = '<' + str(segment['length'])
    for tote in totes:
        label += get_tote_label(tote)
    label += '>'
    edge.set('label', label)
    return edge


def concat_images(file_pattern='generated/simulation_graph_*.png'):
    image_paths = sorted(glob.glob(file_pattern))
    images = list(map(Image.open, image_paths))
    widths, heights = zip(*(i.size for i in images))

    new_width = max(widths)
    new_height = sum(heights)
    new_img = Image.new(images[0].mode, (new_width, new_height))

    y_offset = 0
    for img in images:
        new_img.paste(img, (0, y_offset))
        y_offset += img.size[1] + 2
    new_img.save('generated/done.png')


def generate_graphs(simulation_data):
    for index, run in enumerate(simulation_data):
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


def main():
    simulation_data = load_config()
    generate_graphs(simulation_data)
    # concat_images()
    print('Done!')


if __name__ == '__main__':
    main()
