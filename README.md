# SeleniumPDFGen
Generates a PDF from images extracted from a lazy-scroll optimized web page. 

I created this library to download SVG/PNG/JPEG files from a lazy-scroll optimized website interface given the general CSS selector tag of the object.


Sample usage:
```
python main.py -l https://musescore.com/classicman/scores/77131 -sv "Chopin Nocturne No.20 in C# Minor" -v
```
`-l` or `--link` is the link to be downloaded from
`-sv` or `--save_name` is the name the PDF is to be saved as
`-v` or `--verbose` controls to verbosity of the output
`-t` or `--tag` is the CSS Selector tag in the webpage to be downloaded from.

Please let me know of any bugs in the code at shirshajit@gmail.com or open an issue here.
