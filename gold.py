import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# Webhook URL từ Discord
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1361161043396530357/BkP1Z7OYTOLYI5DZDSxtjBGm-sXTSag7mXXOHO7kbGlotvDabf38nYfcNieLbTd1MQ5o'

def send_discord_message(content):
    data = {
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("✅ Tin nhắn đã được gửi đến Discord!")
    else:
        print(f"❌ Lỗi gửi Discord: {response.status_code} - {response.text}")

def get_btmc_price():
    url = 'https://btmc.vn/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    if len(rows) > 2:
        row = rows[2]
        cells = row.find_all('td')
        if len(cells) > 2:
            gold_price = cells[2].text.strip()
            return f"Bảo Tín: {gold_price}"
    return None

def get_phuquy_price():
    url_phuquy = 'https://phuquygroup.vn/'
    response = requests.get(url_phuquy)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    if len(rows) > 2:
        row = rows[2]
        cells = row.find_all('td')
        if len(cells) > 1:
            gold_price = cells[1].text.strip()
            gold_price = gold_price.replace(',', '')
            gold_price = int(gold_price) / 1000
            return f"Phú Quý: {int(gold_price)}"
    return None

def main():
    hanoi_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time = datetime.now(hanoi_tz).strftime('%H:%M:%S %d/%m/%Y')
    btmc_price = get_btmc_price()
    phuquy_price = get_phuquy_price()

    message = f"🕓 {current_time}\n"

    if btmc_price:
        message += f"🔴 {btmc_price}\n"
    if phuquy_price:
        message += f"❤️ {phuquy_price}\n"

    send_discord_message(message)

if __name__ == "__main__":
    main()
