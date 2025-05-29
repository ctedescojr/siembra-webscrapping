from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
)  # Removed NoSuchElementException
import time
import pandas as pd
from datetime import datetime
import random
import sys
import os


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    # Prioritize the MEIPASS_PARENT environment variable passed from the GUI
    if "MEIPASS_PARENT" in os.environ:
        base_path = os.environ["MEIPASS_PARENT"]
    else:
        try:
            # Fallback to current process's _MEIPASS if running as a frozen child directly
            base_path = sys._MEIPASS
        except Exception:
            # Fallback to current working directory for development
            base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- USER CREDENTIALS (REPLACE WITH YOUR ACTUAL CREDENTIALS) ---
USER_EMAIL = "YOUR_USERNAME_HERE"
USER_PASSWORD = "YOUR_PASSWORD_HERE"
# ---------------------------------------------------------------


def handle_login(driver_instance, wait_instance, long_wait_instance, email, password):
    try:
        login_popup_selector = "div.box-fixed__login.active"
        WebDriverWait(driver_instance, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, login_popup_selector))
        )
        print("Login pop-up detected.", flush=True)

        email_input_selector = 'div.box-fixed__login.active input[type="email"]'
        email_field = wait_instance.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, email_input_selector))
        )
        email_field.clear()
        email_field.send_keys(email)
        print("Email entered.", flush=True)
        time.sleep(0.5)

        password_input_selector = 'div.box-fixed__login.active input[type="password"]'
        password_field = wait_instance.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, password_input_selector))
        )
        password_field.clear()
        password_field.send_keys(password)
        print("Password entered.", flush=True)
        time.sleep(0.5)

        print("\n" + "=" * 60)
        print("IMPORTANT ACTION REQUIRED:", flush=True)
        print("1. Manually solve the reCAPTCHA in the browser window.", flush=True)
        print(
            "2. Manually CLICK THE 'Entrar' BUTTON in the browser window.", flush=True
        )
        print(
            "The script will wait for up to 60 seconds for you to complete this.",
            flush=True,
        )
        print("=" * 60 + "\n")

        WebDriverWait(driver_instance, 60).until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, login_popup_selector))
        )
        print(
            "Login pop-up no longer detected. Assuming login was successful.",
            flush=True,
        )
        time.sleep(3)

    except TimeoutException:
        print(
            "Login pop-up was not detected initially, "
            "or it did not disappear after the manual login period. Proceeding...",
            flush=True,
        )
    except Exception as e:
        print(f"An error occurred during the login attempt: {e}", flush=True)
        print(
            "Proceeding with scraping, but it may not work if login failed.", flush=True
        )


def run_nortel_scraper():
    # --- Configuration ---
    service = Service(
        executable_path=resource_path(
            "chromedriver-win64/chromedriver.exe"
        )  # Fixed path
    )

    chrome_options = Options()
    # Keep headless mode disabled for manual CAPTCHA solving during login
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    )
    chrome_options.add_argument("--start-maximized")

    # --- Base URL and Parameters ---
    base_url = "https://shop.nortel.com.br/produtos"
    url_params = (  # Fixed line length
        "text=&categories=&brands=&pdmsModifiers="
        "&pdmsParticulars=&type=&order=relevance&isFilterUpdate=1"
        "&minPrice=&maxPrice=&limit=16&greenIndicators="
    )

    # --- Initialize WebDriver ---
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)  # General wait
    long_wait = WebDriverWait(driver, 60)  # For manual login step

    all_products_data = []

    try:
        # Define the first products page URL
        first_products_page_url = f"{base_url}?page=1&{url_params}"

        print(
            f"Attempting to open initial products page: {first_products_page_url}",
            flush=True,
        )
        driver.get(first_products_page_url)

        # --- Handle Login ---
        if (
            USER_EMAIL == "YOUR_EMAIL@example.com" or USER_PASSWORD == "YOUR_PASSWORD"
        ):  # Default check
            print("\n" + "!" * 60)
            print(
                "WARNING: The script is using default placeholder credentials. "
                "Please update USER_EMAIL and USER_PASSWORD with your actual credentials.",
                flush=True,
            )
            print("!" * 60 + "\n")
        else:
            handle_login(driver, wait, long_wait, USER_EMAIL, USER_PASSWORD)
            print(
                f"Ensuring we are on the products page. Re-navigating to: {first_products_page_url}",
                flush=True,
            )
            driver.get(first_products_page_url)
            try:
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-list"))
                )
                print("Successfully (re-)navigated to products page.", flush=True)
                time.sleep(2)
            except TimeoutException:
                print(
                    "Error: Could not confirm navigation to product list after login. "
                    "Page might not have loaded correctly.",
                    flush=True,
                )

        # --- Determine Total Number of Pages ---
        total_pages = 1  # Default
        print("Attempting to determine total pages...", flush=True)
        try:
            pagination_ul_xpath = (
                "//div[contains(@class, 'search-products__pagination')]/ul"
            )
            wait.until(EC.presence_of_element_located((By.XPATH, pagination_ul_xpath)))
            time.sleep(1)

            # Link in 2nd to last li
            last_page_number_candidate_xpath = (
                f"{pagination_ul_xpath}/li[position() = last()-1]/a"
            )

            try:
                last_page_link_element = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, last_page_number_candidate_xpath)
                    )
                )
                page_text = last_page_link_element.text.strip()
                page_aria_label = last_page_link_element.get_attribute("aria-label")

                parsed_from_text = False
                if page_text.isdigit():
                    total_pages = int(page_text)
                    parsed_from_text = True
                    print(
                        f"Total pages from text of second-to-last link: {total_pages}",
                        flush=True,
                    )

                if (
                    not parsed_from_text
                    and page_aria_label
                    and "Page " in page_aria_label
                ):
                    num_part = page_aria_label.split("Page ")[-1].split()[0]
                    if num_part.isdigit():
                        total_pages = int(num_part)
                        print(
                            f"Total pages from aria-label of second-to-last link: {total_pages}",
                            flush=True,
                        )
                    else:
                        raise ValueError(
                            f"Could not parse page from aria-label: {page_aria_label}"
                        )
                elif not parsed_from_text:
                    raise ValueError(
                        "Second-to-last link was not a direct page number by text or aria-label."
                    )

            except Exception as e_strat1:
                print(
                    f"Strategy 1 (second-to-last link) for total pages failed: {e_strat1}. "
                    "Trying Strategy 2 (scan all page links).",
                    flush=True,
                )
                page_links_xpath = f"{pagination_ul_xpath}/li/a[@aria-label and starts-with(@aria-label, 'Page ')]"
                page_number_elements = driver.find_elements(By.XPATH, page_links_xpath)

                max_page_found = 0
                if page_number_elements:
                    for el in page_number_elements:
                        try:
                            aria_label = el.get_attribute("aria-label")
                            num_str = aria_label.replace("Page ", "").split(" ")[0]
                            if num_str.isdigit():
                                max_page_found = max(max_page_found, int(num_str))
                        except (ValueError, AttributeError):
                            pass

                    if max_page_found > 0:
                        total_pages = max_page_found
                        print(
                            f"Total pages from scanning all aria-labels: {total_pages}",
                            flush=True,
                        )
                    else:
                        print(
                            "Strategy 2 also failed to find a valid max page number. Defaulting total_pages to 1.",
                            flush=True,
                        )
                        total_pages = 1
                else:
                    print(
                        "No page links with aria-label found for Strategy 2. Defaulting total_pages to 1.",
                        flush=True,
                    )
                    total_pages = 1

        except Exception as e_pagination_detection:
            print(
                f"Could not determine total number of pages due to error: {e_pagination_detection}. "
                "Defaulting to 1 page.",
                flush=True,
            )
            total_pages = 1

        # Final check and warning if total_pages is still 1 but pagination looks like there are more
        if total_pages == 1:
            try:
                pagination_li_elements = driver.find_elements(
                    By.XPATH, f"{pagination_ul_xpath}/li"
                )
                if len(pagination_li_elements) > 3:
                    print(
                        "WARNING: Total pages is 1, but the pagination bar seems to show multiple page elements. "
                        "Page detection might be inaccurate.",
                        flush=True,
                    )
            except Exception:
                pass

        print(
            f"Final total pages to be used for scraping: {total_pages}",
            flush=True,
        )  # Fixed line length

        max_pages_to_scrape = 2
        actual_pages_to_scrape = min(max_pages_to_scrape, total_pages)
        if total_pages > max_pages_to_scrape:
            print(
                f"NOTE: Total pages found is {total_pages}, "
                "but script is limited to scrape only {max_pages_to_scrape} pages for testing.",
                flush=True,
            )
        print(f"Will attempt to scrape {actual_pages_to_scrape} pages.", flush=True)

        for page_num in range(1, actual_pages_to_scrape + 1):
            current_page_url = f"{base_url}?page={page_num}&{url_params}"
            if page_num > 1 or driver.current_url != current_page_url:
                print(
                    f"\n--- Navigating to Page {page_num}: {current_page_url} ---",
                    flush=True,
                )
                driver.get(current_page_url)
            else:
                print(
                    f"\n--- Scraping Page {page_num} (already on this page or initial load) ---",
                    flush=True,
                )

            try:
                product_container_selector = "div.product"
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-list"))
                )
                wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, product_container_selector)
                    )
                )
                time.sleep(random.uniform(1.0, 2.0))

                product_elements = driver.find_elements(
                    By.CSS_SELECTOR, product_container_selector
                )
                print(
                    f"Found {len(product_elements)} product(s) on page {page_num}.",
                    flush=True,
                )

                if not product_elements:
                    print(f"No product elements found on page {page_num}.", flush=True)
                    continue

                for product_element in product_elements:
                    product_name, product_price, product_link = "N/A", "N/A", "N/A"
                    try:
                        link_element = product_element.find_element(
                            By.CSS_SELECTOR, "a.p-link"
                        )
                        product_link = link_element.get_attribute("href")

                        name_element = product_element.find_element(
                            By.CSS_SELECTOR, "span.description_product"
                        )
                        product_name = name_element.text.strip()

                        price_element = product_element.find_element(
                            By.CSS_SELECTOR, "div.productPrice span.price"
                        )
                        product_price = price_element.text.strip()

                        all_products_data.append(
                            {
                                "Name": product_name,
                                "Price": product_price,
                                "Link": product_link,
                                "Page": page_num,
                            }
                        )
                    except Exception as e_detail:
                        print(
                            f"Error scraping a product detail on page {page_num}: {e_detail}",
                            flush=True,
                        )

                if page_num < actual_pages_to_scrape:
                    sleep_duration = random.uniform(2, 4)
                    print(
                        f"Sleeping for {sleep_duration:.2f} seconds before next page...",
                        flush=True,
                    )
                    time.sleep(sleep_duration)
            except Exception as e_page:
                print(f"Error loading/processing page {page_num}: {e_page}", flush=True)
                continue

        # --- Save data to Excel ---
        if all_products_data:
            df = pd.DataFrame(all_products_data)
            current_date_str = datetime.now().strftime("%Y-%m-%d")
            excel_filename = f"Nortel_{current_date_str}.xlsx"
            df.to_excel(excel_filename, index=False)
            print(
                f"\nSuccessfully scraped {len(all_products_data)} products.", flush=True
            )
            print(f"Data saved to {excel_filename}", flush=True)
        else:
            print("\nNo data was scraped to save to Excel.", flush=True)

    except Exception as e_overall:
        print(f"An overall script error occurred: {e_overall}", flush=True)

    finally:
        if driver:
            print("Closing browser...", flush=True)
            time.sleep(5)
            driver.quit()
