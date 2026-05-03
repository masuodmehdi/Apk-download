import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def fetch_and_save():
    url = "https://t.me/s/Begoo_VPN_Gp"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        messages = []
        for div in soup.find_all('div', class_='tgme_widget_message_text'):
            text = div.get_text(strip=True)
            if text:
                messages.append(text)
        
        if not messages:
            # fallback: گرفتن تمام متن‌های طولانی
            lines = [ln.strip() for ln in soup.get_text().split('\n') if ln.strip()]
            messages = [ln for ln in lines if len(ln) > 30 and not ln.startswith('http')]
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = f"📡 fetched at {timestamp}\n{'='*50}\n\n" + "\n\n---\n\n".join(messages)
        
        # ذخیره در ریشه
        with open('telegram_messages.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # ذخیره در پوشه ts
        os.makedirs('ts', exist_ok=True)
        with open('ts/telegram_messages.txt', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ {len(messages)} messages saved")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fetch_and_save()
