from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# Load Jinja2 template environment


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
    pdf = HTML(string=html_content).write_pdf(target="appdata/invoice.pdf")
    return pdf


# Call generate_pdf() with all required variables to get the PDF directly.
