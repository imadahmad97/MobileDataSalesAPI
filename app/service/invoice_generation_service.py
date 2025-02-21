"""
This module contains the functions for generating invoices. It includes a function for generating a
QR code, a function for rendering an HTML invoice, and a function for generating a PDF invoice.

Functions:
    generate_qr_code
    render_html_invoice
    generate_pdf_invoice
"""

from jinja2 import Environment, FileSystemLoader, Template
from app.model.mobile_data_purchase_response import MobileDataPurchaseResponse
import os
from weasyprint import HTML  # type: ignore
import datetime
import qrcode
import base64
import io
import logging


def generate_qr_code(billing_account_number: str) -> str:
    """
    This function generates a QR code for a given billing account number. It generates the code,
    adds the URL with the billing account number, and returns the base64 encoded string of the
    qr code.
    """
    logging.info("Generating a QR code for the billing account number")
    url: str = f"https://telus.com/user/{billing_account_number}"
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
    name: str,
    credit_card_number: str,
    billing_account_number: str,
    requested_mobile_data: str,
    status: str,
    validation_errors: str,
) -> str:
    """
    This function renders an HTML invoice containing the proided data and generated QR code. It
    returns the rendered HTML as a string.
    """
    logging.info("Rendering the HTML invoice")
    template_env: Environment = Environment(loader=FileSystemLoader("templates"))
    invoice_template: Template = template_env.get_template("invoice_template.html")
    qr_code: str = generate_qr_code(billing_account_number)
    data: dict = {
        "name": name,
        "credit_card_number": credit_card_number,
        "billing_account_number": billing_account_number,
        "requested_mobile_data": requested_mobile_data,
        "status": status,
        "validation_errors": validation_errors,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "qr_code": qr_code,
    }
    html_invoice: str = invoice_template.render(data)

    return html_invoice


def generate_pdf_invoice(
    purchase_response: "MobileDataPurchaseResponse",
) -> None:
    """
    This function generates a PDF invoice for a given mobile data purchase response. It renders the
    invoice as an HTML string, writes the HTML to a PDF file, and saves the file to the appdata/pdfs
    directory.
    """
    html_content: str = render_html_invoice(
        purchase_response.name,
        purchase_response.credit_card_number[8:],
        purchase_response.billing_account_number,
        purchase_response.requested_mobile_data,
        purchase_response.status,
        purchase_response.validation_errors,
    )
    filename: str = f"invoice_{purchase_response.billing_account_number}.pdf"
    output_path: str = os.path.join("appdata/pdfs", filename)

    HTML(string=html_content).write_pdf(target=output_path)
