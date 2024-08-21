import requests
import json
from config import API_TOKEN, EMAIL_ADDRESS, EMAIL_PASSWORD
import locale
import re
import smtplib
from email.message import EmailMessage
import os
from time import sleep
from datetime import datetime
import schedule

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


print("#"*15, "Seja bem-vindo ao monitoramento de Bitcoins", "#"*15, "\n")

####################### INPUT SECTION #######################
while True:
    print("Digite abaixo o valor em R$ que deseja como ponto de referência para ser alertado \nvia e-mail caso o valor da criptomoeda esteja abaixo do informado.\n")
    # Prompt the user for Bitcoin value and validate allowed characters
    user_value = input(
        "Digite o valor desejado: R$ ")

    # Check if all characters are digits, dots, or commas
    if all(char.isdigit() or char in {'.', ','} for char in user_value):
        # Format and display the value
        formatted_user_value = format_currency(user_value)
        print(f"Valor escolhido: R$ {formatted_user_value}")
        break
    else:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    print("###### Digite apenas números ######\n")

while True:
    # Prompt user for email and validate
    global user_email
    user_email = input(
        "\nDigite o e-mail que deseja receber as informações: ")
    if is_valid_email(user_email):
        break
    else:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print(
            "###### Digite um e-mail válido no formato email@email.com ou email@email.com.br ######\n")
        print(f"Valor escolhido: R$ {formatted_user_value}")


# Main function
def main():
    print("\nValor do Bitcoin sendo monitorado...")
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
        date_now = datetime.now().strftime("%d/%m/%Y")
        time_now = datetime.now().strftime("%H:%M:%S")

        # Value format as Brazilian currency
        formatted_btc_value = locale.currency(btc_value, grouping=True)
    else:
        print("Erro ao fazer a requisição: ", response.status_code)
        return

    ####################### VALUE COMPARE AND EMAIL SEND #######################
    # Convert formatted values back to numbers for comparison
    user_value_num = parse_currency(formatted_user_value)

    if btc_value < user_value_num:

        # Read html template
        with open("template_html.html", "r", encoding="utf-8") as file:
            html_content = file.read()

        # Change html placeholder
        html_content = html_content.replace(
            "{{btc_value_html}}", formatted_btc_value)
        html_content = html_content.replace("{{date_html}}", date_now)
        html_content = html_content.replace("{{time_html}}", time_now)

        # Send email
        mail = EmailMessage()
        mail['Subject'] = 'Alerta de valor do Bitcoin'
        mail['From'] = EMAIL_ADDRESS
        mail['To'] = user_email
        mail.set_content(html_content, subtype="html")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as email:
            email.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            email.send_message(mail)
        print("\nDados coletados e e-mail enviado.")


if __name__ == "__main__":
    main()
    schedule.every(10).minutes.do(main)

    last_printed_run = None

    while True:
        schedule.run_pending()
        next_run = schedule.next_run()
        if next_run != last_printed_run:
            print(f"\nPróximo agendamento em {next_run}")
            last_printed_run = next_run
        sleep(1)
