import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# noinspection PyPep8Naming
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import time


def _get_svg(link, tag, v=False):
    links = []
    driver = webdriver.Firefox()
    driver.get(link)
    elements = driver.find_elements_by_css_selector(tag)
    print(len(elements), " pages")
    for idx, elem in enumerate(elements):
        try:
            driver.execute_script("arguments[0].scrollIntoView(false);", elem)
            time.sleep(3)
            img_src = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "img")))

            text = img_src.get_attribute('alt')

            link = img_src.get_attribute('src')
            if v:
                print(text)
            links.append(link)
        except TimeoutException:
            print(f"Failed. Page not loaded: {idx + 1}")

    driver.__exit__()
    return links


def downloader(links):
    filenames = []
    save_path = Path.cwd() / '__pdf_temp'
    save_path.mkdir(exist_ok=True)
    for link in links:
        filenames.append(wget.download(link, out=str(save_path)))
    return filenames


def svg_driver(link, tag, v):
    urls = _get_svg(link=link, tag=tag, v=v)
    filenames = downloader(urls)
    if v:
        print("\nDownloaded SVGs")
        for file in filenames:
            print(file)
    return filenames


# svg_driver()

# def __process(url):
#     save_path = Path.cwd() / '__pdf_temp'
#     save_path.mkdir(exist_ok=True)
#     return wget.download(url, out=str(save_path))
#
#
# def downloader(links):
#     cpus = multiprocessing.cpu_count()
#     max_pool_size = 4
#     pool = multiprocessing.Pool(cpus if cpus < max_pool_size else max_pool_size)
#     filenames = []
#     for link in links:
#         filenames.append(pool.apply_async(__process, args=(link, )))
#     pool.close()
#     pool.join()
#     return filenames


def downloader_403(urls, save_path):
    import urllib.request
    opener = urllib.request.build_opener()
    # noinspection SpellCheckingInspection
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    save_path.mkdir(exist_ok=True)
    for i, url in enumerate(urls):
        out = f"{save_path}/{i}.jpg"
        urllib.request.urlretrieve(url, out)
