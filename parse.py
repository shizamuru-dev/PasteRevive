from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import sql_functions
import apprise


def parse():
    while True:
        day = int(datetime.datetime.now().day)
        date = str(datetime.date.today())
    
        if int(sql_functions.get_date()) == day:
            pass
        else:
            driver = webdriver.Chrome()
            driver.get("https://store.epicgames.com/ru/")
    
            assert "Epic" in driver.title
    
            name_elements = driver.find_elements(By.CLASS_NAME, "css-1h2ruwl")
            price_elemets = driver.find_elements(By.CLASS_NAME, "css-11xvn05")
            
            driver.close()

            names = []
            game_names = []
    
            count_price = 0
    
            for element in name_elements:
                game_names.append(element.text)
    
            for element in price_elemets:
                count_price += 1
    
            Duplicates = False
    
            for number in range(count_price):
                if not sql_functions.check_game(game_names[number]):
                    if sql_functions.sale_check(game_names[number],date):
                        Duplicates = True
                        names.append("-1")
                    else:
                        names.append("-12")
                else:
                    names.append(game_names[number])
    
            count = 0
            nomsg_count = 0
            for n in names:
                if n == '-1':
                    count += 1
                elif n == '-12':
                    nomsg_count += 1
                else:
                    pass
    
            AllDuplicates = False
            AllNoMessage = False
    
            if count == len(names):
                AllDuplicates = True
            elif nomsg_count == len(names):
                AllNoMessage = True
            else:
                pass
    
    
            out = []
            for output in names:
                output.replace(' ', '')
                if output == "-1":
                    pass
                else:
                    if output == "-12":
                        pass
                    else:
                        sql_functions.insert_game(output,date)
                        out.append(output)
            sql_functions.insert_date(day)
    
            notify = '\n'.join(out)
            apobj = apprise.Apprise()
            apobj.add("tgram://6273112342:AAFxxg6fELk6QHqP-Uf6TExRsipJUFMO8QA")
            if AllNoMessage:
                pass
            elif AllDuplicates:
                apobj.notify(
                    body=f'\nВсе игры раздавались ранее',
                    title='Халява от Epic Games!\n',
                )
            elif Duplicates:
                apobj.notify(
                    body=f'{notify}\nА также есть игры которые раздавались ранее',
                    title='Новая халява от Epic Games!\n',
                )
            else:
                apobj.notify(
                    body=f'{notify}\n',
                    title='Новая халява от Epic Games!\n',
                )
            time.sleep(3600)
