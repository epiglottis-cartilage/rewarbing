import selenium
from selenium import webdriver, common
import selenium.webdriver
from selenium.webdriver.common.by import By
import os
import time
import random

driver: webdriver.Edge = None


def lunch_browser(mobile: bool):
    global driver
    if driver is not None:
        driver.quit()
    options = selenium.webdriver.EdgeOptions()
    edge_profile_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data"
    )
    options.add_argument(f"user-data-dir={edge_profile_path}")
    if mobile:
        options.add_argument(
            'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1"'
        )
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(10)


def get_contents():
    driver.get(
        f"https://www.google.com/search?q=news&tbm=nws&start={random.randint(0, 200)}"
    )
    titles = filter(
        lambda x: x,
        map(
            lambda r: r.text.strip().lower(),
            driver.find_elements(By.XPATH, '//div[@role="heading"]'),
        ),
    )

    def title_subseq(title: str):
        words = title.replace("'", "").split()
        # radom pick words
        words = random.sample(words, int(len(words) / 1.8))
        return " ".join(words)

    print("Titles found:", titles)

    titles = list(map(title_subseq, titles))
    random.shuffle(titles)

    return iter(titles)


def daily_search(mobile: bool):
    contents = get_contents()

    driver.get("https://rewards.bing.com/redeem/pointsbreakdown")
    cnt_txt = driver.find_elements(
        By.XPATH,
        '//*[@class="title-detail"]/p[2]',
    )[1 if mobile else 0].text
    cnt_curr, cnt_total = map(int, cnt_txt.split("/"))
    print(f"{cnt_curr}/{cnt_total}")
    remain_count = (cnt_total - cnt_curr) // 3
    remain_count = min(remain_count, 5)

    driver.get(
        "https://www.bing.com/news/?form=ml11z9&crea=ml11z9&wt.mc_id=ml11z9&rnoreward=1&rnoreward=1"
    )
    for i in range(remain_count):
        word = next(contents) + "\n"
        bar = driver.find_element(
            By.ID,
            "sb_form_q",
        )
        bar.click()
        bar.clear()
        for c in word:
            bar.send_keys(c)
            time.sleep(random.randint(5, 15) / 100)
        # simulate mouse scroll down
        # for i in range(100):
        #     driver.execute_script(f"window.scrollTo(0, {10 * i});")
        # for i in range(100, 0, -1):
        #     driver.execute_script(f"window.scrollTo(0, {-10 * i});")
        time.sleep(1)

        try:
            if mobile:
                driver.find_element(By.XPATH, '//div[@id="coreresults"]/div[2]').click()
            else:
                driver.find_element(By.XPATH, '//*[@id="algocore"]/div[2]').click()
            time.sleep(random.randint(3, 10))
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        except:
            pass
        driver.switch_to.window(driver.window_handles[0])

    driver.get("https://rewards.bing.com/redeem/pointsbreakdown")
    cnt_txt = driver.find_elements(
        By.XPATH,
        '//*[@class="title-detail"]/p[2]',
    )[1 if mobile else 0].text
    cnt_curr, cnt_total = map(int, cnt_txt.split("/"))
    print(f"{cnt_curr}/{cnt_total}")
    remain_count = (cnt_total - cnt_curr) // 3

    return remain_count


def daily_sets():
    driver.get("https://rewards.bing.com/")
    for card in driver.find_elements(
        By.XPATH,
        '//*[@id="daily-sets"]//card-content',
    )[:3]:
        if "mee-icon-SkypeCircleCheck" in card.find_element(
            By.XPATH,
            "./mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]",
        ).get_attribute("class"):
            print("Already done")
            continue
        card.click()
        time.sleep(4)
        driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)


remian = 0
# lunch_browser(False)
# daily_sets()
# remian = daily_search(0)
lunch_browser(True)
input()
# remian += daily_search(1)
if remian > 0:
    raise RuntimeError("Wait before next run, please!")
