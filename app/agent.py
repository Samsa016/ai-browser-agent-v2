from app.services.browser import BrowserService
from app.services.llm import LLMService

import asyncio

class BrowserAgent:
    def __init__(self):
        self.browser = BrowserService()
        self.llm = LLMService()
    
    async def run(self, query: str):
        await self.browser.start()
        await self.browser.goto("https://dzen.ru/?yredirect=true")
        try:
            while True:
                await asyncio.sleep(3)

                element_count = await self.browser.mark_page()
                print(f"Вижу {element_count} активных элементов.")

                screenshot_path = "screenshot.png"
                action = await self.browser.page.screenshot(path=screenshot_path)

                print("Думаю...")
                action = await self.llm.get_action(screenshot_path, element_count)

                print(f"Мысль: {action.reasoning}")
                print(f"Действие: {action.action_type} -> ID {action.element_id}")

                if action.action_type == "finish":
                    print("Задача выполнена!")
                    break
                elif action.action_type == "fail":
                        print("Не могу выполнить задачу.")
                        break
                elif action.action_type == "click":
                    if action.element_id is not None:
                        await self.browser.page.evaluate(f"window.aiElements[{action.element_id}].click()")
                    else:
                        print("Ошибка: AI хотел кликнуть, но не дал ID.")

                elif action.action_type == 'type':
                    if action.element_id is not None:
                        await self.browser.page.evaluate(f"window.aiElements[{action.element_id}].click()")
                        await self.browser.page.keyboard.type(action.text_input or "")
                        await self.browser.page.keyboard.press("Enter")
                    
                elif action.action_type == 'scroll':
                    await self.browser.page.mouse.wheel(0, 500)

                elif action.action_type == 'wait':
                        print("Жду...")
                        await asyncio.sleep(2)
        except Exception as e:
             print(f"Критическая ошибка в цикле: {e}")
        finally:
            await self.browser.stop()