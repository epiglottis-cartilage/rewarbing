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
    remain = (cnt_total - cnt_curr) // 3
    remain += 1
    random.shuffle(contents)
    contents = iter(contents)
    while remain > 0:
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
            time.sleep(random.randint(5, 25))
            driver.close()
        except:
            pass
        driver.switch_to.window(driver.window_handles[-1])

        # close the last page
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
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
        time.sleep(1)

    time.sleep(5)


daily_search()
earn()
