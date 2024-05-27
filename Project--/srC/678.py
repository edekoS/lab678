import argparse
import json
import yaml
import xml.etree.ElementTree as ET

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data conversion tool')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    return parser.parse_args()

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return None

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        return None

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file)

def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Error reading XML file: {e}")
        return None

def xml_to_dict(element):
    data = {}
    for child in element:
        if len(child):
            data[child.tag] = xml_to_dict(child)
        else:
            data[child.tag] = child.text
    return data

def dict_to_xml(data, root_tag='root'):
    root = ET.Element(root_tag)
    _dict_to_xml_recurse(data, root)
    return root

def _dict_to_xml_recurse(data, parent):
    for key, value in data.items():
        if isinstance(value, dict):
            child = ET.SubElement(parent, key)
            _dict_to_xml_recurse(value, child)
        else:
            child = ET.SubElement(parent, key)
            child.text = str(value)

def save_xml(data, file_path):
    tree = ET.ElementTree(data)
    tree.write(file_path)

if __name__ == "__main__":
    args = parse_arguments()
    
    data = None

    if args.input_file.endswith('.json'):
        data = load_json(args.input_file)
    elif args.input_file.endswith('.yaml') or args.input_file.endswith('.yml'):
        data = load_yaml(args.input_file)
    elif args.input_file.endswith('.xml'):
        data = load_xml(args.input_file)
        if data is not None:
            data = xml_to_dict(data)
    else:
        print("Unsupported input file format")

    if data is not None:
        if args.output_file.endswith('.json'):
            save_json(data, args.output_file)
        elif args.output_file.endswith('.yaml') or args.output_file.endswith('.yml'):
            save_yaml(data, args.output_file)
        elif args.output_file.endswith('.xml'):
            xml_data = dict_to_xml(data)
            save_xml(xml_data, args.output_file)
        else:
            print("Unsupported output file format")
    else:
        print("Failed to load input file")
