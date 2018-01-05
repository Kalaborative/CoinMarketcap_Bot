from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from sys import exit

print("DISCLAIMER: This bot is experimental. It will NOT guarantee you results.")
print("By using this bot, you assume all responsibility and all liability.")
print("This bot makes no trades. It is only used to process information.")
start = input("Type 'start' to agree and continue. > ")
if start.lower() != "start":
	exit()

print("Let's begin!")
options = ChromeOptions()
options.add_argument('--silent')
options.add_argument('--log-level=3')
URL = {'gain-loss': 'https://coinmarketcap.com/gainers-losers/', 'all coins': 'https://coinmarketcap.com/all/views/all/'}
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(30)

driver.get(URL.get('gain-loss'))

threadOne = []
print("Beginning the first test...")
currencies = driver.find_elements_by_xpath('//tr[contains(@id, "24h")]')
for currency in currencies:
	volume = currency.find_element_by_class_name('text-right')
	volume_number = ''.join([v for v in volume.text if v.isdigit()])
	if int(volume_number) > 1000000:
		threadOne.append(currency.find_element_by_class_name('currency-name').text)

print("First test is complete. It found {} results.".format(len(threadOne)))

def number_filter(number):
	result = "".join([n for n in number if n.isdigit() or n == "."])
	return float(result)


def indicator_algorithm(circulating_supply, price, market_cap):
	num = abs(1 - ((circulating_supply * price) / market_cap))
	if num < 0.0005:
		return True
	else:
		return None


print("Waiting for connection...")
driver.get(URL.get('all coins'))
print("Now running the second test...")
threadTwo = []
for coin in threadOne:
	try:
		matched_coin = driver.find_element_by_xpath('//*[contains(text(), "{}")]/../..'.format(coin))
		percents = matched_coin.find_elements_by_xpath('td[contains(@class, "percent")]')
		status = "good"
		for percent in percents:
			if "-" in percent.text:
				status = "bad"
		if status == "good":
			threadTwo.append(coin)
	except:
		print('Could not find {} in listing.'.format(coin))

print("Second test is complete. Results narrowed down to {} results.".format(len(threadTwo)))

print("Running the third test...")
threadThree = []
for coin in threadTwo:
	matched_coin = driver.find_element_by_xpath('//*[contains(text(), "{}")]/../..'.format(coin))
	try:
		market_cap = number_filter(matched_coin.find_element_by_xpath('td[contains(@class, "market-cap")]').text)
		price = number_filter(matched_coin.find_element_by_xpath('td/a[@class="price"]').text)
		supply = number_filter(matched_coin.find_element_by_xpath('td[contains(@class, "circulating-supply")]').text)
		good = indicator_algorithm(supply, price, market_cap)
		if good:
			threadThree.append(coin)
	except:
		print("Missing information for {}. Skipping.".format(coin))

sleep(3)
print("All tests completed. We have found {} results.".format(len(threadThree)))
sleep(3)

cardinals = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth", 5: "sixth", 6: "seventh", 7: "eighth", 8: "ninth", 9: "tenth"}

print("You may now investigate the results.")
sleep(3)
matches = []
for t in threadThree:
	market_cap = driver.find_element_by_xpath('//*[contains(text(), "{}")]/../../td[contains(@class, "market-cap")]'.format(t))
	print("The {} result is {}. It has a market cap of {}. Would you like to know more about it?".format(cardinals.get(threadThree.index(t)), t, market_cap.text))
	know_more = input("yes/no > ")
	if know_more.lower() != "yes":
		print("Okay. Skipping {}.".format(t))
	else:
		driver.find_element_by_link_text(t).click()
		sleep(1)
		driver.find_element_by_link_text('Website').click()
		sleep(2)
		driver.switch_to_window(driver.window_handles[1])
		paragraphs = driver.find_elements_by_tag_name('p')
		print("Here's some information.")
		sleep(3)
		try:
			for paragraph in paragraphs:
				print(paragraph.text)
				sleep(1)
			add = input("Type enter to add {}. Type 'no' to not add it. > ".format(t))
			if add.lower() == "no":
				pass
			else:
				matches.append(t)
		except:
			print("There was a problem here. Moving on.")
		driver.close()
		driver.switch_to_window(driver.window_handles[0])
		driver.back()
print("Exhausted all options. Closing browser..")
sleep(1)
driver.quit()
def comma_formatter(words):
	if len(words) == 1:
		return words[0]
	elif len(words) == 2:
		return words[0] + " and " + words[1]
	elif len(words) > 2:
		last = words.pop()
		words.append("and")
		words.append(last)
		sentence = ", ".join(words)
		return " ".join([s[:-1] if s.startswith("and") else s for s in sentence.split()])

sleep(1)
if matches:
	final_set = comma_formatter(matches)
	print("Your matches have been set. We suggest trading on {}.".format(final_set))
else:
	print("Sorry. You have no matches!")
