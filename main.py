from playwright.sync_api import Playwright, sync_playwright, expect
import asyncio


class CharacterAI:
    def __init__(self, page):
        # initialization
        self.charaid = ""
        self.url = ""
        self.chara_name = ""
        self.page = page

    async def set_id(self, charaid: str) -> None:
        # visit character.ai chat by charaid
        self.charaid = charaid
        self.url = "https://beta.character.ai/chat?char=" + charaid
        await self.page.goto(self.url)

        print(f"Waiting for {self.url}")

        # await self.page.get_by_role("button", name="Accept").click()
        # await self.page.get_by_placeholder("Type a message").fill("你好")
        self.chara_name = ""
        while self.chara_name == "":
            handle = await self.page.query_selector('div.chattitle.p-0.pe-1.m-0')
            while not handle:
                handle = await self.page.query_selector('div.chattitle.p-0.pe-1.m-0')
                await asyncio.sleep(0.5)
            self.chara_name = await handle.inner_text()
            await asyncio.sleep(0.5)
        return

    async def send_msg(self, msg: str) -> None:
        print(f"Sending msg : {msg}")
        ipt = self.page.get_by_placeholder("Type a message")
        await ipt.fill(msg)
        await ipt.press("Enter")
        print("Message sent")
        return

    async def get_msg(self, sleep_time) -> str:
        #xpath = '//*[@id="root"]/div[2]/div/div[3]/div/div/form/div/div/div[2]/button[1]/div'
        #lct = self.page.locator(xpath)
        #await lct.wait_for()
        print("Getting msg...")
        output_text = ""
        while True:
            await asyncio.sleep(sleep_time)
            div = await self.page.query_selector('div.msg.char-msg')
            if output_text == await div.inner_text():
                break
            output_text = await div.inner_text()
            print(f"Got response: {output_text}")
        return output_text


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        CAI = CharacterAI(page)
        CAI.set_id("5f8f3b3e2d2d2e0017e1c3a6")
        chara_name = CAI.chara_name
        print(f"Chara name: {chara_name}")
        CAI.send_msg("你好")
        CAI.get_msg(5)
        browser.close()