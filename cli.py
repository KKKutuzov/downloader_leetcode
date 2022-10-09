import click
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


@click.command()
@click.option(
    "--login",
    "-l",
    required=True,
    help="Your login in leetcode",
)
@click.option("--password", "-p", required=True, help="Your password in leetcode")
def cli(login, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://leetcode.com/accounts/login/")
    time.sleep(5)
    driver.find_element(By.ID, "id_login").send_keys(login)
    driver.find_element(By.ID, "id_password").send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="signin_btn"]/div').click()
    time.sleep(5)
    anchor = "https://leetcode.com/submissions/#/1"
    driver.get(anchor)
    time.sleep(5)
    while True:
        links = list(
            map(
                lambda x: x.get_attribute("href"),
                driver.find_elements(By.CLASS_NAME, "text-success"),
            )
        )
        for link in links:
            driver.get(link)
            time.sleep(1.5)
            language = driver.find_element(By.ID, "result_language").text
            if language == "python3":
                filename = (
                    driver.find_element(By.CLASS_NAME, "inline-wrap").text.replace(
                        " ", "_"
                    )
                    + ".py"
                )
            elif language == "cpp":
                filename = (
                    driver.find_element(By.CLASS_NAME, "inline-wrap").text.replace(
                        " ", "_"
                    )
                    + ".cpp"
                )
            else:
                continue
            file_text = driver.find_element(By.CLASS_NAME, "ace_content").text
            print(filename)
            with open(filename, "w") as f:
                f.write(file_text)
        driver.get(anchor)
        time.sleep(1.5)
        if (
            driver.find_element(
                By.XPATH, '//*[@id="submission-list-app"]/div/nav/ul/li[2]'
            ).get_attribute("class")
            != "next"
        ):
            break
        anchor = driver.find_element(
            By.XPATH, '//*[@id="submission-list-app"]/div/nav/ul/li[2]/a'
        ).get_attribute("href")
        driver.get(anchor)
        time.sleep(1.5)


if __name__ == "__main__":
    cli()
