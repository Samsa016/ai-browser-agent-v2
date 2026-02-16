from app.services.browser import BrowserService
from app.services.llm import LLMService

import asyncio

class BrowserAgent:
    def __init__(self):
        self.browser = BrowserService()
        self.llm = LLMService()
    
    async def run(self, query: str):
        await self.browser.start()
        await self.browser.goto("https://ya.ru")
        try:
            history = []

            while True:
                await asyncio.sleep(3)

                await self.browser.check_new_page()

                try:
                    element_count = await self.browser.mark_page()
                except Exception:
                    continue
                
                print(f"Вижу {element_count} активных элементов.")

                screenshot_path = "screenshot.png"
                action = await self.browser.page.screenshot(path=screenshot_path)
                
                history_text = "\n".join(history[-5:])
                full_context = (
                    f"USER GOAL: {query}\n"
                    f"HISTORY OF ACTIONS:\n{history_text}"
                )

                print("Думаю...")
                action = await self.llm.get_action(screenshot_path, element_count, full_context)

                print(f"Мысль: {action.reasoning}")
                print(f"Действие: {action.action_type} -> ID {action.element_id}")
                current_log = f"Action: {action.action_type}, ID: {action.element_id}"
                
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
                        current_log += " (FAILED: No ID)"

                elif action.action_type == 'type':
                    if action.element_id is not None:
                        text_to_type = action.text_input
                        if not text_to_type:
                            print(f"AI не дал текст. Использую задачу: '{query}'")
                            text_to_type = query

                        await self.browser.page.evaluate(f"window.aiElements[{action.element_id}].click()")
                        await self.browser.page.keyboard.type(text_to_type)
                        await self.browser.page.keyboard.press("Enter")
                        current_log += f", Content: '{text_to_type}'"

                elif action.action_type == 'scroll':
                    await self.browser.page.mouse.wheel(0, 500)
                
                elif action.action_type == 'goto':
                    if action.url:
                        print(f"Переходим по URL: {action.url}")
                        await self.browser.goto(action.url)
                        current_log += f"Navigated to {action.url}"
                    else:
                        print("⚠️ AI хотел перейти, но не дал URL.")
                
                elif action.action_type == "extract":

                    if not action.extracted_content:
                        print("AI хотел хотел сохранить пустоту")
                        current_log += "Error: Cannot save empty data"
                    else:
                        with open("result.txt", "a", encoding="utf-8") as file:
                            file.write(f"--- DATA FOUND ---\n{action.extracted_content}\n------------------\n")
                        print("Данные сохранены!")
                        shorted_extracted = action.extracted_content[:50].replace("\n", " ")
                        current_log += f"SUCCESS: Saved data '{shorted_extracted}...'"
                            
                elif action.action_type == 'wait':
                        input("⏸️ Бот на паузе. Реши проблему в браузере и нажми Enter...")
                    
                history.append(current_log)
                
        except Exception as e:
             print(f"Критическая ошибка в цикле: {e}")
        finally:
            await self.browser.stop()