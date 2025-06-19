import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox
)
import PyPDF2


def merge_duplex_pdfs(pdf1_path, pdf2_path, output_path):
    pdf1 = open(pdf1_path, 'rb')
    pdf2 = open(pdf2_path, 'rb')
    pdf1_reader = PyPDF2.PdfReader(pdf1)
    pdf2_reader = PyPDF2.PdfReader(pdf2)
    pdf_writer = PyPDF2.PdfWriter()

    pdf1_num_pages = len(pdf1_reader.pages)
    pdf2_num_pages = len(pdf2_reader.pages)

    for i in range(max(pdf1_num_pages, pdf2_num_pages)):
        if i < pdf1_num_pages:
            pdf_writer.add_page(pdf1_reader.pages[i])
        if i < pdf2_num_pages:
            pdf_writer.add_page(pdf2_reader.pages[pdf2_num_pages - 1 - i])

    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    pdf1.close()
    pdf2.close()


class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf1_path = ""
        self.pdf2_path = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Duplex PDF Merger")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label1 = QLabel("Select Front Side PDF")
        self.label2 = QLabel("Select Back Side PDF")

        self.btn1 = QPushButton("Choose Front PDF")
        self.btn1.clicked.connect(self.choose_pdf1)

        self.btn2 = QPushButton("Choose Back PDF")
        self.btn2.clicked.connect(self.choose_pdf2)

        self.merge_btn = QPushButton("Merge PDFs")
        self.merge_btn.clicked.connect(self.merge_pdfs)

        layout.addWidget(self.label1)
        layout.addWidget(self.btn1)
        layout.addWidget(self.label2)
        layout.addWidget(self.btn2)
        layout.addWidget(self.merge_btn)

        self.setLayout(layout)

    def choose_pdf1(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select Front Side PDF", "", "PDF files (*.pdf)")
        if fname:
            self.pdf1_path = fname
            self.label1.setText(f"Front PDF: {fname}")

    def choose_pdf2(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select Back Side PDF", "", "PDF files (*.pdf)")
        if fname:
            self.pdf2_path = fname
            self.label2.setText(f"Back PDF: {fname}")

    def merge_pdfs(self):
        if not self.pdf1_path or not self.pdf2_path:
            QMessageBox.warning(self, "Error", "Please select both PDF files.")
            return

        output_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "", "PDF files (*.pdf)")
        if output_path:
            try:
                merge_duplex_pdfs(self.pdf1_path, self.pdf2_path, output_path)
                QMessageBox.information(self, "Success", "PDFs merged successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to merge PDFs: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())
