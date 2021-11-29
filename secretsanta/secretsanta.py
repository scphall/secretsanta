#!/usr/bin/env python3

import argparse
from itertools import chain, combinations
import random
from datetime import datetime
import os
import logging

FORMAT = '%(levelname)-8s- %(message)s'
logging.basicConfig(format=FORMAT)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)


def get_parser():
    parser = argparse.ArgumentParser(description='Secret Santa time!')
    parser.add_argument(
        '-k', '--kids',
        nargs='+',
        type=str,
        required=True,
        help='List of kids that need presents',
    )
    parser.add_argument(
        '-n', '--name',
        type=str,
        required=True,
        help='Name of the secret santa event',
    )
    parser.add_argument(
        '-d', '--debug',
        required=False,
        default=False,
        action='store_true',
        help='Name of the secret santa event',
    )
    return parser


def get_pairs(kids):
    _logger.debug('Entering get_pairs')
    indices = list(range(len(kids)))
    random.shuffle(indices)
    if any([x == i for (i, x) in enumerate(indices)]):
        return get_pairs(kids)
    return {kid: kids[indices[i]] for (i, kid) in enumerate(kids)}


def get_directory(name):
    path = os.path.join(str(datetime.now().year), name)
    if not os.path.exists(path):
        os.makedirs(path)
    _logger.info(f'Secret Santa path: {path}')
    return path


def output(name, pairs):
    path = get_directory(name)
    for (sender, kid) in pairs.items():
        text = f'Hi {sender}, you will play Santa for {kid}!'
        _logger.debug(text)
        filename = os.path.join(path, f'{sender}.txt')
        with open(filename, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.debug:
        _logger.setLevel(logging.DEBUG)

    kids = args.kids
    if len(kids) < 2:
        print('Need to give more than one child')

    pairs = get_pairs(kids)
    output(args.name, pairs)
