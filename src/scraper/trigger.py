import undetected_chromedriver as uc

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.get("https://www.google.com")
input("Press Enter to quit...")
driver.quit()
