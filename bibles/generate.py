import os
import cPickle as pickle
import argparse
arg_parser = argparse.ArgumentParser()

import requests

import known_versions
import parsers

def main():
    arg_parser.add_argument("-a", "--all", action="store_true",
        help="Find and parse as many versions as possible")
    
    arg_parser.add_argument("-p", "--parse", action="append",
        help="Parse only a specific version -- can be specified multiple times")
    
    arg_parser.add_argument("-o", "--output_dir",
        help="Output directory to put parsed Bibles in")
    
    global args
    args = arg_parser.parse_args()
    
    if args.all:
        print "Finding all"
        find_and_parse_all()
    elif args.parse:
        find_and_parse_all(args.parse)

def find_and_parse_all(version_list=known_versions.dict.keys()):
    for version in version_list:
        find_and_parse(version)

def find_and_parse(version):
    version_info = known_versions.dict[version]
    Parser, filetype = parsers.select_parser(version_info)
    file = requests.get(version_info[filetype]).content
    
    parser = Parser()
    parser.parse_zip(file)
    
    return output(version, parser.data)

def output(version, data, ext="pk1"):
    output_dir = "./output/"
    if args.output_dir:
        output_dir = args.output_dir
    
    output_dir = os.path.abspath(output_dir)
    filename = "{0}.{1}".format(version.lower(), ext)
    
    output_filename = os.path.join(output_dir, filename)
    with open(output_filename, "w") as output_file:
        pickle.dump(data, output_file, pickle.HIGHEST_PROTOCOL)
    
    return True

if __name__ == "__main__":
    main()