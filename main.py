import argparse
from svg_driver import svg_driver
import pdf_maker

parser = argparse.ArgumentParser(description="Downloads SVG files"
                                             " from a lazy-loader interface and converts them to PDF."
                                             "Can be used to download free PDFs from MuseScore.")
parser.add_argument('-l', "--link", help="Link to download page", required=True, type=str)
parser.add_argument('-sv', "--save_name", help='PDF to be saved as', required=True, type=str)
parser.add_argument('-t', '--tag', help="CSS selector tag to be pointed to", default="div.gXB83")
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
args = parser.parse_args()

if args.verbose:
    print("Verbosity is turned on")
filenames = svg_driver(args.link, args.tag, args.verbose)

if not args.save_name.endswith(".pdf"):
    args.save_name += ".pdf"
pdf_maker.run(args.save_name, filenames, args.verbose)

print(f"PDF generated:  /output/{args.save_name}")
