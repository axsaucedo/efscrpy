#!/usr/bin/env python3

from parser import get_argument_parser
from getem import main

if __name__ == '__main__':
	parser = get_argument_parser()
	args = parser.parse_args()
	main(args)