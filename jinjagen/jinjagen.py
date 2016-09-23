#!/usr/bin/env python

import jinja2
import json
import yaml
import logging
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', 
                        nargs='+',
                        help='template file(s)')
    parser.add_argument('-d', '--data',
                        help='template data')
    parser.add_argument('-o', '--out',
                        help='specify output file, if set only 1 template is processed')
    parser.add_argument('-i', '--inplace',
                        action='store_true',
                        help='inplace editing, if the file ext is .j2, then it is removed')
    parser.add_argument('-V', '--verbose', 
                        action='store_true',
                        help='verbose mode, off by default')
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)

    if args.out and args.inplace:
        logging.error('-i and -o are incompatible')
        return 1

    if len(args.template) > 1 and args.out:
        logging.error('can\'t have more than 1 templace and -o')
        return 1

    if args.data == '-':
        rawdata = sys.stdin.read()
        ext = '.yaml'
    else:
        with open(args.data) as fl:
            _, ext = os.path.splitext(args.data)
            rawdata = fl.read()

    if ext == '.yaml':
        load = yaml.load
    elif ext == '.json':
        load = json.loads

    data = load(rawdata)

    for template in args.template:
        head, tail = os.path.split(os.path.realpath(template))
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(head))
        tpl = env.get_template(tail)
        out = tpl.render(data)

        if args.inplace:
            base, tplext = os.path.splitext(tail)
            if tplext == '.j2':
                outname = base
            else:
                outname = tail + '.new'
            outname = os.path.join(head, outname)
            stdout = None
        elif args.out:
            outname = args.out
            stdout = None
        else:
            stdout = sys.stdout

        if stdout:
            stdout.write(out)
            stdout.flush()
        else:
            with open(outname, 'w') as fl:
                fl.write(out)

    return 0

if __name__ == '__main__':
    sys.exit(main())

