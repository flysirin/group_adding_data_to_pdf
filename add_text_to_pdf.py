from PyPDF2 import PdfWriter, PdfReader, Transformation
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path


class GenerateFromTemplate:
    """ Use as:
        gen = GenerateFromTemplate("template.pdf")
        gen.addText("Hello!",(100,200))
        gen.addText("PDF!",(100,300))
        gen.merge()
        gen.generate("Output.pdf")"""

    def __init__(self, template: str):
        self.template_pdf = PdfReader(open(template, "rb"))
        self.output = PdfWriter()
        self.template_page = self.template_pdf.pages[0]
        self.packet = io.BytesIO()
        self.c = Canvas(self.packet, pagesize=(self.template_page.mediabox.width, self.template_page.mediabox.height))
        #  Tahoma Bolt  - current font
        font_path = "C:\\python_projects\\Education\\Sending of pdf tickets\\TahomaBolt.ttf"
        pdfmetrics.registerFont(TTFont("TahomaBolt", font_path))
        self.c.setFont("TahomaBolt", 18)  # Selecting font and size

    def add_text(self, text: str, point: tuple):
        text_object = self.c.beginText(point[0], point[1])
        text_object.textLines(text)  # Can accept multiline text
        self.c.drawText(text_object)
        # self.c.drawString(point[0], point[1], text)

    def merge(self):
        self.c.save()
        self.packet.seek(0)
        result_pdf = PdfReader(self.packet)
        result = result_pdf.pages[0]
        # op = Transformation().rotate(0).translate(tx=0, ty=0)
        # result.add_transformation(op)
        self.template_page.merge_page(result)
        self.template_page.compress_content_streams()
        self.output.add_page(self.template_page)

    def generate(self, destination: str):
        output_stream = open(destination, "wb")
        self.output.write(output_stream)
        output_stream.close()


def compress_pdf(input_pdf_path, output_pdf_path):
    pdf = PdfReader(input_pdf_path)
    output_pdf = PdfWriter()
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        page.compress_content_streams()
        output_pdf.add_page(page)
    with open(output_pdf_path, "wb") as output_stream:
        output_pdf.write(output_stream)


def compressed_pdf_files_from_folder(folder_path: str):
    pdf_folder_path = Path(folder_path)
    for pdf_file in pdf_folder_path.glob("*.pdf"):
        compress_pdf(str(pdf_file), str(pdf_file))

# input_pdf = "output_compressed.pdf"
# output_pdf = "output_compressed.pdf"
# folder_pdf_path = "C:/.../FOLDER"

# compress_pdf(input_pdf, output_pdf)
# compressed_pdf_files_from_folder(folder_pdf_path)

# gen = GenerateFromTemplate(template="C:path_to_pdf.pdf")
# _text = "TEXT\nFIRSTNAME SURNAME\n+112345678"
# tel = "Phone: +1 123 234 123"
# gen.add_text(_text, (49, 800))
# gen.merge()
# gen.generate('output.pdf')



