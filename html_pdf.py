from argparse import ArgumentParser
from bs4 import BeautifulSoup as soup
import pdfkit 


def main():
    parser = ArgumentParser()
    
    parser.add_argument("path", help="Path to the html for conversion.", type=str)

    args = parser.parse_args()

    pdfkit.from_file(args.path, "quads_modified.pdf") 


if __name__ == '__main__':
	main()