#引入selenium库中的 webdriver 模块
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
import time as origin_time
#import datetime
from datetime import datetime, time

import xml.etree.ElementTree as ET


from selenium.webdriver.edge.options import Options# 实现无可视化界面的操作,

f=open('log.txt', 'a', encoding='utf-8')
# 重定向stdout到文件
sys.stdout = f



# 读取 XML 文件
tree = ET.parse("configuration.xml")
root = tree.getroot()

# 提取数据
data = {
    'target_time': root.find('target_time').text,
    'fresh_interval': float(root.find('fresh_interval').text),
    'position_kind': root.find('position_kind').text,
    'username': root.find('username').text,
    'password': root.find('password').text,
    'car_id': root.find('car_id').text,
    'debug': root.find('debug').text,
    'URL': root.find('URL').text
}

# print(data)

TARGET_TIME=data.get('target_time')
#TARGET_TIME="12:11:00"
FRESH_INTERVAL =data.get('fresh_interval')
# 一般车位 充电车位
POSITION_KIND=data.get('position_kind')
USERNAME=data.get('username')
PASSWORD=data.get('password')
CAR_ID=data.get('car_id')
DEBUG=data.get('debug')
URL=data.get('URL')

print("data==",TARGET_TIME,FRESH_INTERVAL,POSITION_KIND,USERNAME,PASSWORD,CAR_ID,DEBUG,URL)



original_stdout = sys.stdout



#定义浏览器对象
#实现无可视化界面的操作,无可视化界面（无头浏览器）
options = Options()#定义一个option对象
# options.add_argument("headless")

# 指定 WebDriver 路径
service = Service("msedgedriver.exe")
# service = Service("D:\script\msedgedriver.exe")
driver = webdriver.Edge(service=service , options=options)
# driver = webdriver.Edge()

#网页打开
driver.get(URL)

# 输入账号和密码
wait = WebDriverWait(driver, 100, 0.1)#等待网页刷新出来，最多100秒

while True:
    try:
        user_input = wait.until(EC.presence_of_element_located((By.ID, "loginid"))).send_keys(USERNAME)
        pw_input = wait.until(EC.presence_of_element_located((By.ID, "userpassword"))).send_keys(PASSWORD)
        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        #点击登录
        origin_time.sleep(1)
        login_btn.click()
        break
    except Exception as e:
        print(f"登入失败,重新登入: {e}")
        driver.refresh()
        origin_time.sleep(1)
        continue
    # driver.save_screenshot(r"login_error_screenshot.png")

while True:
    try:
        # 刷新页面
        refresh_xpath = f"//button[@class='ant-btn ant-btn-primary' and @ecid='undefined_Button@mrj0h4_button@xq1ea3']"
        refresh_btn = wait.until(EC.element_to_be_clickable((By.XPATH, refresh_xpath)))
        refresh_btn.click()
        # origin_time.sleep(3)
        # driver.refresh()
        print(f"登入完成于 {origin_time.strftime("%H:%M:%S", origin_time.localtime())} 预计于{TARGET_TIME} 开始执行")
        break
    except Exception as e:
        print(f"刷新失败,重新点击刷新: {e}")
        origin_time.sleep(1)
        continue

# origin_time.sleep(2)  # 等待页面加载完成
# result = driver.execute_script("document.querySelector('.linkage_hide').classList.remove('linkage_hide');")
# origin_time.sleep(2)  # 等待页面加载完成
# result = driver.execute_script("document.querySelector('.linkage_hide').classList.remove('linkage_hide');")
# input("按任意键关闭浏览器...")
# driver.quit() # 用户输入后关闭浏览器
# sys.exit(0)


stayon_interval = 29
count=0
# 将字符串分割为时、分、秒
h, m, s = map(int, TARGET_TIME.split(':'))
target_time = time(h, m, s)

#trigger at specific time
while True:
    current_time=datetime.now().time()
    print("current_time=",current_time)
    # 每60秒刷新一次页面
    count += 1
    if count % stayon_interval == 0:
        driver.refresh()
        print(f"每 {stayon_interval}s刷新页面,防止超时登出，第 {count // stayon_interval } 次刷新")
    if current_time > target_time:
        print(f"代码在 {current_time} 执行")
        break
    origin_time.sleep(1)

wait1 = WebDriverWait(driver, 1, 0.1)#等待网页刷新出来，最多100秒

while True:
    # 等待抢车位开始，并输入车牌
    while True:
        try:
            car_id = wait1.until(EC.presence_of_element_located((By.ID, "field521776")))
            # origin_time.sleep(0.5)  # 等待元素稳定
            # 找到元素后。且元素可见，执行操作
            if car_id.is_displayed():
                try:
                    car_id.send_keys(CAR_ID)
                    print("成功")
                except Exception as e:
                    print(f"车牌输入失败: {e}")
                    continue
                print("开始时间 ",datetime.now().time())
                break  # 成功找到则跳出循环
            else:
                print("元素是隐藏的",datetime.now().time())
                driver.refresh()
                origin_time.sleep(FRESH_INTERVAL)
        except Exception as e:
            print(f"等待车牌输入框失败: {e}")
            driver.refresh()
            origin_time.sleep(FRESH_INTERVAL)
            continue
            

        #选择车位种类 打开下拉框
    try:
        WebDriverWait(driver, 1).until(
            #EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-select-selection.ant-select-selection--single"))
             EC.element_to_be_clickable((By.CSS_SELECTOR, "div.ant-select-selection"))
             ).click()
    except Exception as e:
        print(f"打开下拉框失败: {e}")
        continue

    try:
        # 2. 等待下拉菜单可见（注意移除hidden类）
        WebDriverWait(driver, 1).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.ant-select-dropdown-hidden"))
        )

        # 3. 定位目标选项（使用title属性更可靠）
        # 一般车位 充电车位
        option_xpath = f"//li[contains(@class, 'ant-select-dropdown-menu-item') and @title='{POSITION_KIND}']"
        option = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )

        # 4. 滚动到视图并点击
        # driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", option)
        # origin_time.sleep(0.5)  # 小延迟确保滚动完成
        option.click()
    except Exception as e:
        print(f"点击下拉框失败: {e}")
        continue  

    # 提交申请
    # origin_time.sleep(0.5)
    if DEBUG == 'debug':
        print("debug模式,跳过提交申请",datetime.now().time())
    else:
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "wf-req-top-button"))).click()
            print("提交时间 ",datetime.now().time())
            # break
        except Exception as e:
            print(f"点击提交失败: {e}")
            continue 

    looptime=0
    while True:
        try:
            if '检测中…' in driver.page_source:
                print("正在检测")
                looptime=0
                # elements = driver.find_elements(By.XPATH, "//*[contains(text(), '检测中…')]")
                continue
            if '申请时间范围在12：00~13：00' in driver.page_source:
                driver.refresh()
                print("不在时间内，重新申请")
                break
            if '校验通过' in driver.page_source:
                print("申请成功，完成时间 ",datetime.now().time())
                input("按任意键关闭浏览器...")
                driver.quit() # 用户输入后关闭浏览器
                sys.exit(0)
            looptime+=1
            if looptime>100:
                driver.refresh()
                print("等待超时")
                break
            origin_time.sleep(0.1)
            print("等待检测页面")
        except Exception as e:
            print(f"等待完毕失败: {e}")
            continue  
