# Database Configurations
PATH_TO_DB_FILE = r"sqlite:///C:\Users\t767284\Documents\repos\MobileDataSalesAPI\appdata\database\mobile_data_sales_api.db"

# Validation Variables
LEGAL_AGE: int = 18
DAYS_IN_YEAR: int = 365.25

MINIMUM_CARD_NUMBER_LENGTH: int = 13
MAXIMUM_CARD_NUMBER_LENGTH: int = 19

MINIMUM_CVV_LENGTH: int = 3
MAXIMUM_CVV_LENGTH: int = 4

# Invoice Generation Variables
INVOICE_TEMPLATE_PATH: str = "templates"
PDF_OUTPUT_PATH: str = "appdata/pdfs"
BASE_URL: str = "https://telus.com/user"
