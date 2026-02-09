import asyncio
import sys
from app.agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    task = str(input("Введите вашу задачу: "))
    await agent.run(task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Принудительная остановка.")
    except Exception as e:
        print(f"\n Ошибка: {e}")