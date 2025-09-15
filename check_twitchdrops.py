import os
import requests
import sys

url = "https://www.rockstargames.com/ru/gta-online/twitch-drops"
file_path = "twitchdrops.html"

try:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    new_content = resp.text
except Exception as e:
    print("Ошибка при запросе страницы:", e)
    sys.exit(1)

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        old_content = f.read()
else:
    old_content = None

# Если файла с предыдущим содержимым нет, создаём его (первый запуск)
if old_content is None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Содержимое страницы сохранено для первого сравнения.")
    sys.exit(0)

# Сравниваем новое содержимое со старым
if new_content == old_content:
    print("Изменений не обнаружено.")
    sys.exit(0)
else:
    print("Страница изменилась! Отправляем оповещение в Discord.")
    webhook_url = os.environ.get("DISCORD_WEBHOOK")
    if not webhook_url:
        print("Не задан секрет DISCORD_WEBHOOK.")
        sys.exit(1)
    data = {"content": f"**Twitch Drops страница обновлена!** Проверьте: {url}"}
    try:
        resp2 = requests.post(webhook_url, json=data)
        resp2.raise_for_status()
        print("Сообщение отправлено.")
    except Exception as e:
        print("Не удалось отправить сообщение:", e)
    # Обновляем файл с содержимым
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Содержимое страницы обновлено в файле.")
