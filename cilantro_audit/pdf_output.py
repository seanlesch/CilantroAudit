from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Table
from cilantro_audit.constants import PDF_OUTPUT_DIR
import os


""" Handles all pdf creation and output functionality."""
class PdfOutput():
    # Note: This is setup to overwrite any existing file with the same name
    def __init__(self, pdf_file_name):
        file = self.__establish_path(pdf_file_name)
        self.canvas = canvas.Canvas(file, pagesize=letter)

    # Sets up output directory if necessary, and returns
    # the full path + file_name
    def __establish_path(self, file_name):
        if (os.name == 'nt'): # Windows OS
            home_dir = os.getenv('HOMEPATH')
            home_dir += "\\Desktop\\"
            dir_path =  home_dir + PDF_OUTPUT_DIR + "\\"
        else: # Mac & Linux OS
            home_dir = os.environ['HOME']
            dir_path = home_dir + "/" + PDF_OUTPUT_DIR + "/"

        if os.access(dir_path, os.F_OK) is False: # If output dir doesn't already exist
            if os.access(home_dir, os.W_OK) is False: # If we have don't write access in home directory
                print("Can't create output folder; access denied.")
                exit()
            else: # create the output dir
                os.mkdir(dir_path)

        return dir_path + file_name

    def create_page(self, print_text):
        textbox = self.canvas.beginText()
        textbox.setTextOrigin(10, 700)
        textbox.textLine(text=print_text)

        self.canvas.drawText(textbox)


pdf = PdfOutput("Blank.pdf")
pdf.create_page("PRINT THIS OUT IT IS A TEST TO SEE WHAT HAPPENS WHEN THERE IS A REALLY LONG LINE LIKE WHAT HAPPENS")
pdf.canvas.save()
