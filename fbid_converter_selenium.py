import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

print("【自動化轉換Facebook ID】by KAI")
print("Version：0.3")

print("開啟自動化Chrome視窗...")
driver = webdriver.Chrome()

print("開始讀取來源清單，檔名：fb_convert_target.txt")
f = open('fb_convert_target.txt','r',encoding='utf-8')
lines = f.readlines()
target_url = []
for i in lines:
    target_url.append(i.rstrip('\n'))
print("讀取完畢！")


url = "https://findmyfbid.com/"
convert_id = []
count = 1
error_count = 0

print("本次預計轉換：" + str(len(target_url)) + " 個網址")
print(" ")
print("==================我是分隔線==================")
print(" ")


for i in target_url:
    print("開始轉換第 " + str(count) + " 個網址...")
    print("目標網址：" + i)
    driver.get(url)
    try:
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder = "https://www.facebook.com/YourProfileName"]')))
        driver.find_element_by_css_selector('input[placeholder = "https://www.facebook.com/YourProfileName"]').send_keys(i)
        driver.find_element_by_css_selector('input[value = "Find numeric ID →"]').click()

        WebDriverWait(driver, 10, 0.5).until((EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id = "success-wrap"]'))))
        result_url = driver.current_url
        facebook_id = result_url.split('/')[4]
        convert_id.append(facebook_id)
        print("轉換成功！")
        print("此網址 Facebook ID：" + facebook_id)
        print(" ")
        print("==================我是分隔線==================")
        print(" ")
    except Exception as e:
        convert_id.append("Error")
        print("遭遇錯誤！")
        print("錯誤訊息：")
        print(e)
        print("==================我是分隔線==================")
        print(" ")
        error_count += 1
        pass

    count += 1

print("轉換查詢已全部結束！")
print("本次成功轉換：" + str(len(convert_id)-error_count) + " 個")
print("本次遭遇錯誤：" + str(error_count) + " 個")
print("==================我是分隔線==================")
print("關閉自動化視窗...")
driver.quit()
print("==================我是分隔線==================")
print("轉換成CSV檔...")
out = {"原始網址" : target_url,
       "Facebook ID" :convert_id
       }
df = pd.DataFrame(out)
df.to_csv('FacebookID_ConvertResult.csv', sep = ',', encoding= "utf_8_sig")
print("轉換成功！檔名：FacebookID_ConvertResult.csv")
print("==================我是分隔線==================")
print(" ")

print("程式結束！可喜可賀！")
print(" ")
print("【請按Enter結束程式】")
end = input()

# with open('test123.csv', 'w', newline='', encoding='utf-8') as f:
#     fieldnames = ['原始網址', 'Facebook ID']
#     writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
#     writer.writeheader()
#     writer.writecolumn({"原始網址": target_url, "Facebook ID": convert_id})
