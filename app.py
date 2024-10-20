import os
from dotenv import load_dotenv

load_dotenv()

import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from flask import Flask, jsonify, request

app = Flask(__name__)

def init_driver():
    driver = webdriver.Chrome()
    driver.get('https://www.nepalstock.com.np/')
    time.sleep(5)
    return driver

def scrape_top_gainers(driver):
    gainer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "nepsemarket_gl"))
    )

    top_gainer_button = gainer_button.find_element(By.ID, 'gainers_tab')
    top_gainer_button.click()

    table1 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "(//table[contains(@class, 'table')])[3])"))
    )

    top_gainer = []

    body = table1.find_element(By.TAG_NAME, 'tbody')
    rows = body.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        try:
            columns = row.find_elements(By.TAG_NAME, 'td')

            if len(columns) >= 4:
                company_details = {
                    'name': columns[0].find_element(By.TAG_NAME, 'a').text,
                    'LTP': columns[1].text,
                    'Pt. change': columns[2].text,
                    '% change': columns[3].text
                }
                top_gainer.append(company_details)

        except StaleElementReferenceException:
            continue

        return top_gainer

    def scrape_top_losers(driver):
        # Wait for the loser button to be visible and clickable
        loser_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'losers-tab'))
        )

        # Click the 'Top Losers' tab
        loser_button.click()

        # Wait for the table to load
        tablel = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//table[contains(@class, 'table')])[4]"))
        )

        # Initialize list to store top losers
        top_loser = []
        bodyl = tablel.find_element(By.TAG_NAME, "tbody")
        rowsl = bodyl.find_elements(By.TAG_NAME, 'tr')

        for row in rowsl:
            try:
                columns = row.find_elements(By.TAG_NAME, 'td')
                if len(columns) >= 4:
                    company_details = {
                        'name': columns[0].find_element(By.TAG_NAME, 'a').text,
                        'LTP': columns[1].text,
                        'Pt. change': columns[2].text,
                        '% change': columns[3].text
                    }
                    top_loser.append(company_details)
            except StaleElementReferenceException:
                continue

        return top_loser

    def scrape_top_turnover(driver):
        # Wait for the "Top Turnover" table to load
        table_t = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "(//table[contains(@class, 'table')])[5]"))
        )

        top_turnover = []
        body_t = table_t.find_element(By.TAG_NAME, "tbody")
        rows_t = body_t.find_elements(By.TAG_NAME, 'tr')

        for row in rows_t:
            try:
                columns = row.find_elements(By.TAG_NAME, 'td')
                if len(columns) >= 3:
                    company_details = {
                        'name': columns[0].find_element(By.TAG_NAME, 'a').text,
                        'turnover': columns[1].text,
                        'LTP': columns[2].text
                    }
                    top_turnover.append(company_details)
            except StaleElementReferenceException:
                continue

        return top_turnover

    @app.route('/top_gainers', methods=['GET'])
    def top_gainers():
        driver = init_driver()
        gainers = scrape_top_gainers(driver)
        driver.quit()
        return jsonify(gainers)

    @app.route('/top_losers', methods=['GET'])
    def top_losers():
        driver = init_driver()
        losers = scrape_top_losers(driver)
        driver.quit()
        return jsonify(losers)

    @app.route('/top_turnover', methods=['GET'])
    def top_turnover():
        driver = init_driver()
        turnover = scrape_top_turnover(driver)
        driver.quit()
        return jsonify(turnover)

    if __name__ == '__main__':
        app.run(debug=True)
