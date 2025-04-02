"""
This module contains the functions for generating invoices. It includes a function for generating a
QR code, a function for rendering an HTML invoice, and a function for generating a PDF invoice.
"""

# CHANGE ADD UNDERSCORE TO INTERNAL FUNCTIONS
# CHANGE MAKE THIS A CLASS
import os
import datetime
import base64
import io
import logging
from jinja2 import Environment, FileSystemLoader, Template
from weasyprint import HTML  # type: ignore
import qrcode  # type: ignore
from app.model.mobile_data_sell_order import MobileDataSellOrder

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
logging.getLogger("fontTools.ttLib.ttFont").setLevel(logging.ERROR)
logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)


class InvoiceGenerator:
    """
    This class contains methods for generating invoices. It includes methods for generating a QR code,
    rendering an HTML invoice, and generating a PDF invoice.
    """

    def __init__(
        self, invoice_template_path: str, pdf_output_path: str, base_url: str
    ) -> None:
        """
        Initializes the InvoiceGenerator class with the paths for the invoice template and PDF output.
        """
        self.invoice_template_path: str = invoice_template_path
        self.pdf_output_path: str = pdf_output_path
        self.base_url: str = base_url

    def generate_qr_code(self, billing_account_number: str) -> str:
        """
        This function generates a QR code for a given billing account number. It generates the code,
        adds the URL with the billing account number, and returns the base64 encoded string of the
        qr code.
        """
        logger.info("Generating a QR code for the billing account number")
        url: str = f"{self.base_url}/{billing_account_number}"
        qr: qrcode.QRCode = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img: qrcode.image.pil.PilImage = qr.make_image(fill="black", back_color="white")

        buffer: io.BytesIO = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64: str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return qr_code_base64

    def render_html_invoice(
        self,
        sell_order: "MobileDataSellOrder",
    ) -> str:
        """
        This function renders an HTML invoice containing the proided data and generated QR code. It
        returns the rendered HTML as a string.
        """
        logger.info("Rendering the HTML invoice")

        template_env: Environment = Environment(
            loader=FileSystemLoader(self.invoice_template_path)
        )
        invoice_template: Template = template_env.get_template("invoice_template.html")
        qr_code: str = self.generate_qr_code(sell_order.billing_account_number)

        data: dict = {
            "name": sell_order.name,
            "credit_card_number": sell_order.credit_card_number[:-8],
            "billing_account_number": sell_order.billing_account_number,
            "requested_mobile_data": sell_order.requested_mobile_data,
            "status": sell_order.status,
            "validation_errors": sell_order.validation_errors,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "qr_code": qr_code,
        }

        html_invoice: str = invoice_template.render(data)

        return html_invoice

    def generate_pdf_invoice(
        self,
        sell_order: "MobileDataSellOrder",
    ) -> None:
        """
        This function generates a PDF invoice for a given mobile data purchase response. It renders the
        invoice as an HTML string, writes the HTML to a PDF file, and saves the file to the appdata/pdfs
        directory.
        """
        html_content: str = self.render_html_invoice(sell_order)
        filename: str = f"invoice_{sell_order.billing_account_number}.pdf"
        output_path: str = os.path.join(self.pdf_output_path, filename)
        HTML(string=html_content).write_pdf(target=output_path)

    def generate_pdf_invoices(
        self,
        sell_orders: list["MobileDataSellOrder"],
    ) -> None:
        """
        This function generates PDF invoices for a list of mobile data purchase responses. It iterates
        over the list, generates a PDF invoice for each response, and saves the invoices to the
        appdata/pdfs directory.
        """
        for sell_order in sell_orders:
            logger.info(
                f"Generating a PDF invoice for BAN {sell_order.billing_account_number
            }"
            )
            self.generate_pdf_invoice(sell_order)
