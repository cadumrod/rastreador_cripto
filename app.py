import requests
import json
from config import API_TOKEN
import locale
import re

# Set locale for Brazil
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


# Function to format Bitcoin value as Brazilian currency
def format_currency(value):
    # Remove dots and commas to process the number
    clean_value = value.replace('.', '').replace(',', '')

    # Ensure there are always at least two decimal places
    if len(clean_value) < 3:
        clean_value = clean_value.zfill(3)

    # Split the integer and decimal parts
    integer_part = clean_value[:-2]
    decimal_part = clean_value[-2:]

    # Add thousand separators
    integer_part = re.sub(r'\B(?=(\d{3})+(?!\d))', '.', integer_part)

    # Rejoin the integer and decimal parts
    formatted_value = f"{integer_part},{decimal_part}"

    return formatted_value


# Function to convert a formatted currency string into a float number
def parse_currency(value):
    # Remove thousand separators and replace comma with a dot for the decimal point
    clean_value = value.replace('.', '').replace(',', '.')
    return float(clean_value)


# Function to validate email using regex
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|com\.br)$'
    return re.match(pattern, email)


# Main function
def main():
    while True:
        while True:
            # Prompt the user for Bitcoin value and validate allowed characters
            user_value = input(
                "Digite o valor desejado do Bitcoin para receber atualizações: R$ ")

            # Check if all characters are digits, dots, or commas
            if all(char.isdigit() or char in {'.', ','} for char in user_value):
                # Format and display the value
                formatted_user_value = format_currency(user_value)
                print(f"Valor formatado: R$ {formatted_user_value}")
                break
            else:
                print("#### Digite apenas números. ####\n")

        while True:
            # Prompt user for email and validate
            user_email = input(
                "\nDigite o e-mail que deseja receber as informações: ")
            if is_valid_email(user_email):
                break
            else:
                print(
                    "#### Digite um e-mail válido no formato email@email.com ou email@email.com.br. ####")

        ####################### API SECTION #######################
        # Base URL
        url = f"http://api.coinlayer.com/live?access_key={
            API_TOKEN}&target=BRL&symbols=BTC"

        # API request
        response = requests.get(url)

        # Request check
        if response.status_code == 200:
            data = response.json()
            btc_value = data["rates"]["BTC"]

            # Value format as Brazilian currency
            formatted_btc_value = locale.currency(btc_value, grouping=True)

            print(f"O valor atual do Bitcoin em reais é: {
                  formatted_btc_value}")
        else:
            print("Erro ao fazer a requisição: ", response.status_code)
            return

        ####################### VALUE COMPARE AND EMAIL SEND #######################
        # Convert formatted values back to numbers for comparison
        user_value_num = parse_currency(formatted_user_value)

        if btc_value < user_value_num:
            # Enviar email
            pass


if __name__ == "__main__":
    main()
