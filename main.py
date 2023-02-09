import time

from playwright.sync_api import Playwright, sync_playwright, expect
import asyncio


class CharacterAI:
    def __init__(self, page):
        # initialization
        self.charaid = ""
        self.url = ""
        self.chara_name = ""
        self.page = page

    def set_id(self, charaid: str) -> None:
        # visit character.ai chat by charaid
        self.charaid = charaid
        self.url = "https://beta.character.ai/chat?char=" + charaid
        self.page.goto(self.url)

        print(f"Waiting for {self.url}")

        self.page.get_by_role("button", name="Accept").click()
        # await self.page.get_by_placeholder("Type a message").fill("你好")
        self.chara_name = ""
        while self.chara_name == "":
            handle = self.page.query_selector('div.chattitle.p-0.pe-1.m-0')
            while not handle:
                handle = self.page.query_selector('div.chattitle.p-0.pe-1.m-0')
                time.sleep(0.5)
            self.chara_name = handle.inner_text()
            self.chara_name = "".join(self.chara_name.split("  ")[:-1])
            time.sleep(0.5)
        return

    def send_msg(self, msg: str) -> None:
        # print(f"Sending msg : {msg}")
        ipt = self.page.get_by_placeholder("Type a message")
        ipt.fill(msg)
        ipt.press("Enter")
        # print("Message sent")
        return

    def get_msg(self, sleep_time) -> str:
        #print("Getting msg...")
        output_text = ""
        while True:
            time.sleep(sleep_time)
            div = self.page.query_selector('div.msg.char-msg')
            if output_text == div.inner_text():
                break
            output_text = div.inner_text()
            print(f"Got response: {output_text}")
        return output_text

    def get_msg2(self) -> str:
        # print("Getting msg...")

        # locate the button with class "btn py-0"
        lct = self.page.locator("button.btn.py-0").nth(0)

        expect(lct).to_be_enabled(timeout=0)

        div = self.page.query_selector('div.msg.char-msg')
        output_text = div.inner_text()
        print(f"{self.chara_name}: {output_text}")
        return output_text


if __name__ == "__main__":
    with sync_playwright() as p:

        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        CAI = CharacterAI(page)
        CAI.set_id("RRGejclDCpSjxWDH4TnwCd_C9NuzlcQXADKfdI-1qhk") # 米浴
        chara_name = CAI.chara_name
        print(f"Chara name:\n {chara_name}")
        CAI.get_msg2()
        while True:
            msg = input("> ")
            if msg == "exit":
                break
            CAI.send_msg(msg)
            CAI.get_msg2()
        # CAI.get_msg(5)
        browser.close()