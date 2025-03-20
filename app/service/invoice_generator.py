"""
This module contains the functions for generating invoices. It includes a function for generating a
QR code, a function for rendering an HTML invoice, and a function for generating a PDF invoice.
"""

import os
import datetime
import base64
import io
import logging
from fastapi import HTTPException
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


def generate_qr_code(billing_account_number: str) -> str:
    """
    This function generates a QR code for a given billing account number. It generates the code,
    adds the URL with the billing account number, and returns the base64 encoded string of the
    qr code.
    """
    try:
        logger.info("Generating a QR code for the billing account number")
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
    except Exception as e:
        logger.error("Failed to generate the QR code")
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to generate the QR code",
        )


def render_html_invoice(
    sell_order: "MobileDataSellOrder",
) -> str:
    """
    This function renders an HTML invoice containing the proided data and generated QR code. It
    returns the rendered HTML as a string.
    """
    try:
        logger.info("Rendering the HTML invoice")

        template_env: Environment = Environment(loader=FileSystemLoader("templates"))
        invoice_template: Template = template_env.get_template("invoice_template.html")
        qr_code: str = generate_qr_code(sell_order.billing_account_number)

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
    except Exception as e:
        logger.error("Failed to render the HTML invoice")
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to render the HTML invoice",
        )


def generate_pdf_invoice(
    sell_order: "MobileDataSellOrder",
) -> None:
    """
    This function generates a PDF invoice for a given mobile data purchase response. It renders the
    invoice as an HTML string, writes the HTML to a PDF file, and saves the file to the appdata/pdfs
    directory.
    """
    try:
        html_content: str = render_html_invoice(sell_order)
        filename: str = f"invoice_{sell_order.billing_account_number}.pdf"
        output_path: str = os.path.join("appdata/pdfs", filename)

        HTML(string=html_content).write_pdf(target=output_path)
    except Exception as e:
        logger.error("Failed to generate the PDF invoice")
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: Failed to generate the PDF invoice",
        )


def generate_pdf_invoices(
    sell_orders: list["MobileDataSellOrder"],
) -> None:
    """
    This function generates PDF invoices for a list of mobile data purchase responses. It iterates
    over the list, generates a PDF invoice for each response, and saves the invoices to the
    appdata/pdfs directory.
    """
    for sell_order in sell_orders:
        generate_pdf_invoice(sell_order)
