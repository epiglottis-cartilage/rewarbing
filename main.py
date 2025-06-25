import selenium
from selenium import webdriver, common
import selenium.webdriver
from selenium.webdriver.common.by import By
import os
import time

options = selenium.webdriver.EdgeOptions()
edge_profile_path = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data"
)
options.add_argument(f"user-data-dir={edge_profile_path}")
driver = webdriver.Edge(options=options)
driver.implicitly_wait(10)

Contents = [
    "Trump news",
    "Israel news",
    "How to set google default",
    "Cheapest PC",
    "How to learn python",
    "rust in 1 second",
    "java job Minecraft",
    "keep your hear while writing C",
    "embedded systems using C#",
    "can haskell programmers have a waifu",
    "linus fk invida",
    "how can Avali talk",
    "how to cool down things with microwave",
    "Bishop of Proletariats",
    "How to make a website",
    "Worst password",
    "Is Qwertyuiop a good password?How to make a discord bot",
    "How to make a discord bot",
    "How high can a tree grow",
    "Is climate change real",
    "shark a thread or not",
    "make cake at home",
    "where is my dog",
    "hacimi meme",
    "map of South Pole Wall",
    "evidence showing earth flat",
    "what is my ip",
    "hide my ip to everyone",
    "boot pc without cpu",
    "hacked by memz",
    "Arch Linux is best",
]


def daily_search():
    driver.get("https://rewards.bing.com/redeem/pointsbreakdown")
    cnt_txt = driver.find_element(
        By.XPATH,
        '//*[@id="userPointsBreakdown"]/div/div[2]/div/div/div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]',
    ).text
    cnt_curr, cnt_total = map(int, cnt_txt.split("/"))
    print(f"{cnt_curr}/{cnt_total}")
    remain = cnt_total - cnt_curr

    while remain > 0:
        driver.get("https://www.bing.com/")
        driver.find_element(By.ID, "sb_form_q").send_keys(
            Contents[remain % len(Contents)] + "\n"
        )
        time.sleep(0.5)
        # driver.find_element(By.XPATH, '//input[@id="sb_form_go"]').click()
        remain -= 1


def earn():
    driver.get("https://rewards.bing.com/")
    daily_set = driver.find_element(
        By.XPATH,
        '//*[@id="daily-sets"]/mee-card-group[1]/div',
    )
    for job in daily_set.find_elements(
        By.XPATH,
        "//card-content",
    )[:3]:
        job.click()
        time.sleep(0.5)


daily_search()
earn()
