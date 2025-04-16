"""
This module contains the functions for generating invoices. It includes a function for generating a
QR code, a function for rendering an HTML invoice, and a function for generating a PDF invoice.
"""

import os
import datetime
import base64
import io
import logging
from jinja2 import Environment, Template
from weasyprint import HTML  # type: ignore
from app.model.mobile_data_sell_order import MobileDataSellOrder
import qrcode  # type: ignore
from typing import Callable

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
logging.getLogger("fontTools.ttLib.ttFont").setLevel(logging.ERROR)
logging.getLogger("weasyprint").setLevel(logging.ERROR)
logging.getLogger("PIL").setLevel(logging.ERROR)


# Change: Add params to docstring for both class instantiation and functions


class InvoiceGenerator:
    """
    This class contains methods for generating invoices. It includes methods for generating a QR code,
    rendering an HTML invoice, and generating a PDF invoice.
    """

    def __init__(
        self,
        invoice_template_path: str,
        pdf_output_path: str,
        qr_code_base_url: str,
        qr_code_template: qrcode.QRCode,
        html_template: str,
        html_template_environment: Environment,
        html_factory: Callable[[str], HTML] = HTML,
    ) -> None:
        self.invoice_template_path: str = invoice_template_path
        self.pdf_output_path: str = pdf_output_path
        self.qr_code_base_url: str = qr_code_base_url
        self.qr_code_template: qrcode.QRCode = qr_code_template
        self.html_template = html_template
        self.html_template_environment: Environment = html_template_environment
        self.html_factory: Callable[[str], HTML] = html_factory

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
                f"Generating a PDF invoice for BAN {sell_order.billing_account_number}"
            )
            self._generate_pdf_invoice(sell_order)

    def _generate_pdf_invoice(
        self,
        sell_order: "MobileDataSellOrder",
    ) -> None:
        """
        This function generates a PDF invoice for a given mobile data sell order. It renders the
        invoice as an HTML string, writes the HTML to a PDF file, and saves the file to the ourput path.
        """
        html_content: str = self._render_html_invoice(sell_order)
        filename: str = f"invoice_{sell_order.billing_account_number}.pdf"
        output_path: str = os.path.join(self.pdf_output_path, filename)
        html = self.html_factory(html_content)
        html.write_pdf(target=output_path)

    def _render_html_invoice(
        self,
        sell_order: "MobileDataSellOrder",
    ) -> str:
        """
        This function renders an HTML invoice containing the proided data and generated QR code. It
        returns the rendered HTML as a string.
        """
        logger.info("Rendering the HTML invoice")

        invoice_template: Template = self.html_template_environment.get_template(
            self.html_template
        )
        qr_code: str = self._generate_qr_code(sell_order.billing_account_number)

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

    def _generate_qr_code(self, billing_account_number: str) -> str:
        """
        This function generates a QR code for a given billing account number. It generates the code,
        adds the URL with the billing account number, and returns the base64 encoded string of the
        qr code.
        """
        logger.info("Generating a QR code for the billing account number")
        url: str = f"{self.qr_code_base_url}/{billing_account_number}"
        self.qr_code_template.add_data(url)
        self.qr_code_template.make(fit=True)

        img: qrcode.image.pil.PilImage = self.qr_code_template.make_image(
            fill="black", back_color="white"
        )

        buffer: io.BytesIO = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64: str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return qr_code_base64
