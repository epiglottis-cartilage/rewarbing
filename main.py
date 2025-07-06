import selenium
from selenium import webdriver, common
import selenium.webdriver
from selenium.webdriver.common.by import By
import os
import time
import random

options = selenium.webdriver.EdgeOptions()
edge_profile_path = os.path.join(
    os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data"
)
options.add_argument(f"user-data-dir={edge_profile_path}")
driver = webdriver.Edge(options=options)
driver.implicitly_wait(10)


def daily_search():
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
            words = random.sample(words, int(len(words) / 1.5))
            return " ".join(words)

        titles = map(title_subseq, titles)

        return list(titles)

    contents = get_contents()
    print(contents)

    driver.get("https://rewards.bing.com/redeem/pointsbreakdown")
    cnt_txt = driver.find_element(
        By.XPATH,
        '//*[@id="userPointsBreakdown"]/div/div[2]/div/div/div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]',
    ).text
    cnt_curr, cnt_total = map(int, cnt_txt.split("/"))
    print(f"{cnt_curr}/{cnt_total}")
    remain_count = (cnt_total - cnt_curr) // 3

    random.shuffle(contents)
    contents = iter(contents)
    for i in range(remain_count):
        cnt_txt = driver.find_element(
            By.XPATH,
            '//*[@id="pointsCounters_pcSearchLevel1_0"]',
        ).click()
        driver.switch_to.window(driver.window_handles[-1])
        word = next(contents) + "\n"
        bar = driver.find_element(By.ID, "sb_form_q")
        bar.click()
        for c in word:
            bar.send_keys(c)
            time.sleep(random.randint(5, 15) / 100)
        # simulate mouse scroll down
        # for i in range(100):
        #     driver.execute_script(f"window.scrollTo(0, {10 * i});")
        # for i in range(100, 0, -1):
        #     driver.execute_script(f"window.scrollTo(0, {-10 * i});")
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, '//*[@id="algocore"]/div[3]').click()
            time.sleep(random.randint(5, 15))
            driver.close()
        except:
            pass
        driver.switch_to.window(driver.window_handles[-1])

        # close the last page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # driver.find_element(By.XPATH, '//input[@id="sb_form_go"]').click()

    driver.get("https://rewards.bing.com/redeem/pointsbreakdown")
    cnt_txt = driver.find_element(
        By.XPATH,
        '//*[@id="userPointsBreakdown"]/div/div[2]/div/div/div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]',
    ).text
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
        driver.close()

    time.sleep(2)


daily_sets()
remian = daily_search()
if remian > 0:
    raise RuntimeError("Wait before next run, please!")
