from jinja2 import Environment, FileSystemLoader
import os
from weasyprint import HTML
import datetime
import qrcode
import base64
import io


def generate_qr_code(billing_account_number):
    url = f"https://telus.com/user/{billing_account_number}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return qr_code_base64


def render_html_invoice(
    name,
    credit_card_number,
    billing_account_number,
    requested_mobile_data,
    status,
    validation_errors,
):
    template_env = Environment(loader=FileSystemLoader("templates"))
    invoice_template = template_env.get_template("invoice_template.html")
    qr_code = generate_qr_code(billing_account_number)
    data = {
        "name": name,
        "credit_card_number": credit_card_number,
        "billing_account_number": billing_account_number,
        "requested_mobile_data": requested_mobile_data,
        "status": status,
        "validation_errors": validation_errors,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "qr_code": qr_code,
    }
    return invoice_template.render(data)


def generate_pdf_invoice(
    purchase_response,
):
    html_content = render_html_invoice(
        purchase_response.name,
        purchase_response.credit_card_number[8:],
        purchase_response.billing_account_number,
        purchase_response.requested_mobile_data,
        purchase_response.status,
        purchase_response.validation_errors,
    )
    filename = f"invoice_{purchase_response.billing_account_number}.pdf"
    output_path = os.path.join("appdata/pdfs", filename)

    HTML(string=html_content).write_pdf(target=output_path)
