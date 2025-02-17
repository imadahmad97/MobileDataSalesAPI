from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import datetime


def render_invoice(
    name,
    date_of_birth,
    credit_card_number,
    credit_card_expiration_date,
    credit_card_cvv,
    billing_account_number,
    requested_mobile_data,
    status,
    validation_errors,
):
    template_env = Environment(loader=FileSystemLoader("templates"))
    invoice_template = template_env.get_template("invoice_template.html")
    print("Validation Errors: ", validation_errors)
    data = {
        "name": name,
        "date_of_birth": date_of_birth,
        "credit_card_number": credit_card_number,
        "credit_card_expiration_date": credit_card_expiration_date,
        "credit_card_cvv": credit_card_cvv,
        "billing_account_number": billing_account_number,
        "requested_mobile_data": requested_mobile_data,
        "status": status,
        "validation_errors": validation_errors,
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }
    return invoice_template.render(data)


def generate_pdf(
    name,
    date_of_birth,
    credit_card_number,
    credit_card_expiration_date,
    credit_card_cvv,
    billing_account_number,
    requested_mobile_data,
    status,
    validation_errors,
):
    html_content = render_invoice(
        name,
        date_of_birth,
        credit_card_number,
        credit_card_expiration_date,
        credit_card_cvv,
        billing_account_number,
        requested_mobile_data,
        status,
        validation_errors,
    )
    filename = f"invoice_{billing_account_number}.pdf"
    output_path = os.path.join("appdata/pdfs", filename)
    print("Validation Errors: ", validation_errors)

    pdf = HTML(string=html_content).write_pdf(target=output_path)
    return pdf
