
import argparse

def get_argument_parser():
	parser = argparse.ArgumentParser(description='Get all data from people')

	parser.add_argument("--username", required=True,
    	help="Your EF username.")
	parser.add_argument("--password", required=True,
    	help="Your EF password.")
	parser.add_argument("--chrome",
        help='Location for chrome driver. Otherwise script will use PhantomJS.', default="")
	parser.add_argument("--waiting", type=int,
        help='Waiting time for script', default=10)

	return parser
