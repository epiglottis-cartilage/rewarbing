from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import random

driver: webdriver.Edge | webdriver.Firefox = None
headless = False
RATE_LIMIT = 4
rate_limit = 4
proxy: str | None = "http://127.0.0.1:7890"
point_per_search = 5


def launch_browser_edge(mobile: bool):
    global driver
    if driver is not None:
        driver.quit()
    os.system("taskkill /f /im msedge.exe")
    options = webdriver.EdgeOptions()
    edge_profile_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data"
    )
    options.add_argument(f"user-data-dir={edge_profile_path}")
    options.add_argument("log-level=3")
    if headless:
        options.add_argument("headless=new")
    options.add_argument("disable-audio-output")
    if proxy:
        options.add_argument(f"proxy-server={proxy}")
    if mobile:
        options.add_argument(
            'user-agent="Mozilla/5.0 (Linux; Android 13; PGIM10 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36 BingWeb/6.9.8"'
        )
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(8)


launch_browser = launch_browser_edge


def get_contents():
    # new table
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
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
        words = ("".join(filter(lambda c: c not in ",\"'.", title))).split()
        # radom pick words
        words = random.sample(words, int(len(words) / 2))
        return " ".join(words)

    titles = list(map(title_subseq, titles))
    print("titles:", titles)
    random.shuffle(titles)
    driver.switch_to.window(driver.window_handles[0])
    return iter(titles)


def daily_search(mobile: bool):
    global rate_limit

    driver.get("https://rewards.bing.com/pointsbreakdown")
    cnt_txt = driver.find_elements(
        By.XPATH,
        '//*[@class="title-detail"]/p[2]',
    )[1 if mobile else 0].text
    try:
        cnt_curr, cnt_total = map(int, cnt_txt.split("/"))
        print(f"current point: {cnt_curr}/{cnt_total}")
        remain_count = (cnt_total - cnt_curr) // point_per_search
        if remain_count == 0:
            return 0
    except ValueError:
        print("Failed to parse current points from:", cnt_txt)
        remain_count = 3

    contents = get_contents()

    remain_count = max(1, min(remain_count, rate_limit))
    rate_limit -= remain_count
    driver.find_element(By.XPATH, '//*[@id="modal-host"]/div[2]/button').click()

    for i in range(remain_count):
        word = next(contents)
        bar = driver.find_element(
            By.ID,
            "rewards-suggestedSearch-searchbox",
        )
        bar.click()
        bar.clear()
        for c in word:
            bar.send_keys(c)
            time.sleep(random.randint(5, 15) / 100)
        driver.find_element(
            By.XPATH,
            '//*[@id="rewards-suggestedSearch-searchbox-form"]/div/div',
        ).click()
        # simulate mouse scroll down
        # for i in range(100):
        #     driver.execute_script(f"window.scrollTo(0, {10 * i});")
        # for i in range(100, 0, -1):
        #     driver.execute_script(f"window.scrollTo(0, {-10 * i});")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(random.randint(2, 3))
        # driver.find_element(By.XPATH, '//*[@id="b_results"]/li[3]').click()
        # time.sleep(random.randint(1, 4))
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("Search completed:", word)

    driver.get("https://rewards.bing.com/redeem/pointsbreakdown")
    cnt_txt = driver.find_elements(
        By.XPATH,
        '//*[@class="title-detail"]/p[2]',
    )[1 if mobile else 0].text

    try:
        cnt_curr, cnt_total = map(int, cnt_txt.split("/"))
        print(f"current point: {cnt_curr}/{cnt_total}")
        remain_count = (cnt_total - cnt_curr) // 3

        return remain_count
    except ValueError:
        print("Failed to parse current points from:", cnt_txt)
        return 1


def daily_sets():
    driver.get("https://rewards.bing.com/")
    for card in driver.find_elements(
        By.XPATH,
        '//*[@id="daily-sets"]//card-content',
    )[:3]:
        if (
            marker := card.find_element(
                By.XPATH,
                "./mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]",
            ).get_attribute("class")
        ) is None or "mee-icon-SkypeCircleCheck" in marker:
            print("Already done")
            continue
        card.click()
        time.sleep(4)
        driver.switch_to.window(driver.window_handles[0])

    time.sleep(2)


def check_running():
    # if edge is running before our script, then we should not run the script
    for proc in os.popen("tasklist").read().splitlines():
        if "msedge.exe" in proc:
            return True
    return False


def main():
    # if check_running():
    #     raise RuntimeError("Edge is running, please close it completely!")
    print("Starting Bing Rewards script...")
    remain = 0
    launch_browser(False)
    daily_sets()
    remain = daily_search(False)
    launch_browser(True)
    remain += daily_search(True)
    # if remain > 0:
    #     raise RuntimeError("Wait before next run, please!")
    driver.quit()
    return remain


if __name__ == "__main__":
    remain = 1
    while remain > 0:
        try:
            remain = main()
        except Exception as e:
            print(e)
        print("Waiting for next run...")
        for i in range(15):
            print(f"{i}..", end="", flush=True)
            time.sleep(60)
        print()
        rate_limit = RATE_LIMIT
