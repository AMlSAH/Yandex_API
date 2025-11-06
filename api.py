import requests
import yadisk
import json
import os
from urllib.parse import quote

def main():
    text = input("Введите текст для картинки: ")
    token = input("Введите токен Яндекс.Диска: ")

    try:
        api_url = f"https://cataas.com/cat/says/{quote(text)}?json=true"
        print(f"Запрашиваем данные по URL: {api_url}")
        
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            print(f"Ошибка при получении данных с cataas.com: {response.status_code}")
            return

        data = response.json()
        print(f"Получены данные: {data}")
        
        image_url = data.get('url', '')
        if not image_url:
            print("Не удалось получить URL картинки из ответа API")
            return
            
        print(f"Загружаем картинку по URL: {image_url}")
        
        image_response = requests.get(image_url, timeout=30)
        if image_response.status_code != 200:
            print(f"Ошибка при загрузке картинки: {image_response.status_code}")
            return

        filename = f"{text.replace(' ', '_')}.jpg"
        with open(filename, "wb") as f:
            f.write(image_response.content)

        print(f"Картинка сохранена как: {filename} (размер: {os.path.getsize(filename)} байт)")

        y = yadisk.YaDisk(token=token)
        folder_name = "PD-134"  
        
        
        if not y.check_token():
            print("Неверный токен Яндекс.Диска!")
            os.remove(filename)
            return
            
        if not y.exists(folder_name):
            y.mkdir(folder_name)
            print(f"Создана папка {folder_name} на Яндекс.Диске")

        
        remote_path = f"{folder_name}/{filename}"
        
        
        if y.exists(remote_path):
            print(f"Файл {remote_path} уже существует на Яндекс.Диске")
        else:
            y.upload(filename, remote_path)
            print(f"Картинка загружена на Яндекс.Диск: {remote_path}")

        
        info = {
            "filename": filename,
            "size": os.path.getsize(filename),
            "remote_path": remote_path,
            "text": text,
            "source_url": image_url
        }
        
        with open("backup_info.json", "w", encoding='utf-8') as f:
            json.dump(info, f, indent=4, ensure_ascii=False)
            
        print("Информация сохранена в backup_info.json")

        
        os.remove(filename)
        print("Временный файл удален")

        print("Картинка успешно загружена на Яндекс.Диск!")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
    except yadisk.exceptions.YaDiskError as e:
        print(f"Ошибка Яндекс.Диска: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    main()
