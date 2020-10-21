from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
from PIL import Image
from reportlab.lib.pagesizes import A3
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import shutil
import cv2


def _pdf_concat(in_files, out_name, v):
    if v:
        print("\nPDF Concatenation started")
    in_streams = []
    out_path = Path.cwd() / 'output'
    out_path.mkdir(exist_ok=True)
    out_stream = open(str(out_path/out_name), 'wb')
    for f in in_files:
        in_streams.append(open(f, 'rb'))
    writer = PdfFileWriter()
    for idx, f in enumerate(in_streams):
        if v:
            print(f"Concatenation: Page {idx + 1}")
        reader = PdfFileReader(f)
        for n in range(reader.getNumPages()):
            writer.addPage(reader.getPage(n))
        writer.write(out_stream)
    for f in in_streams:
        f.close()
    out_stream.close()


def _make_pdfs(images, v):
    if v:
        print('\nPDF page generation started')
    temp_path = Path.cwd() / '__pdf_temp'
    temp_path.mkdir(exist_ok=True)
    path_list = []
    for idx, image in enumerate(images):
        save_name = f"{temp_path}/pdf_temp_{idx}.pdf"
        if str(image).endswith('.svg'):
            drawing = svg2rlg(str(image))
            renderPDF.drawToFile(drawing, save_name)
        else:
            img = cv2.imread(str(image))
            img = cv2.resize(img, (827, 1169))
            im_file = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            drawing = ImageReader(im_file)

            canv = canvas.Canvas(save_name, pagesize=A3)
            canv.setPageCompression(0)
            canv.drawImage(drawing, 0, 0)
            canv.showPage()
            canv.save()

        if v:
            print(f"PDF page {idx+1} generated")
        path_list.append(save_name)
    return path_list


def housekeeping(folder='__pdf_temp'):
    shutil.rmtree(folder, ignore_errors=True)


def run(file_name, paths, v=False):
    # paths = sorted(list(Path('__pdf_temp').glob('*.png')))
    pdf_list = _make_pdfs(paths, v)
    _pdf_concat(pdf_list, file_name, v)
    housekeeping()


# run("Nocturne", [])
