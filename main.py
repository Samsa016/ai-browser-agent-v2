import sys
from app.config import settings

def main():
    print("Инициализация Агента V2...")
    
    try:
        print(f"Конфигурация OK.")
        print(f"API Key: ...{settings.openai_api_key[-4:]}")
        print(f"Браузер: {'Headless' if settings.headless else 'Headful'}")
    except Exception as e:
        print(f"Ошибка старта: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()