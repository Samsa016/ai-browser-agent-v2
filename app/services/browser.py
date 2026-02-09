from playwright.async_api import async_playwright, Browser, Playwright, Page, BrowserContext
from pathlib import Path
from app.config import settings
class BrowserService:
    def __init__(self):
        self.playwright: Playwright = None
        self.browser:  Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=settings.headless)
        storage_path = Path(settings.session_file)
        
        if storage_path.exists():
            print("Загружаю сессию...")
            self.context = await self.browser.new_context(storage_state=settings.session_file)
        else:
            print("Новая сессия...")
            self.context = await self.browser.new_context()

        self.page = await self.context.new_page()

        self.page = self.page

    async def goto(self, url: str):
        if self.page:
            await self.page.goto(url)
    
    async def mark_page(self) -> int:
        with open("app/scripts/mark_page.js", "r", encoding="utf-8") as f:
            js_code = f.read()
        return await self.page.evaluate(js_code)
    
    async def stop(self):
        await self.context.storage_state(path=settings.session_file)
        await self.page.close()
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()
        
    