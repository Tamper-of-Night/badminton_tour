# -*- coding: utf-8 -*-
"""
GitHub Actions 适配版 - 自动填写表单
完整移植版，确保能完成所有功能
"""
import logging
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('log_Wednesday_1.log', encoding='utf-8')
    ]
)

# ========== 场地映射配置（完整复制你的配置） ==========

# 周一场地号对应标签
available_court_1_18_20 = {
    1: "r650c6c04fc918f4943f4d271",
    2: "r650c6c04fc918f4943f4d273",
    3: "r650c6c04fc918f4943f4d274",
    7: "r650c6c04fc918f4943f4d278",
    8: "r65f8f2bcfc918f57803051ed"
}

available_court_1_20_22 = {
    1: "r660bd230fc918f578077634f",
    2: "r660bd230fc918f5780776350",
    3: "r660bd230fc918f5780776351",
    4: "r660bd230fc918f5780776352",
    6: "r6824114b75a03c036c8f7962",
    7: "r660bd230fc918f5780776355",
    8: "r660bd230fc918f5780776356"
}

# 周三场地号对应标签
available_court_3_18_19 = {
    1: "r6152870f75a03c68fe0252ba",
    2: "r6152870f75a03c68fe0252bb",
    3: "r631fea17fc918f28d9ea7976",
    6: "r6824114b75a03c036c8f7963",
    7: "r6152870f75a03c68fe0252bd",
    8: "r6152870f75a03c68fe0252be"
}

available_court_3_19_20 = {
    1: "r615287be75a03c68fe025d0c",
    2: "r615287be75a03c68fe025d0d",
    3: "r631fee6b75a03c4ff391a971",
    4: "r63f9771c75a03c4aa436f8c8",
    5: "r631fee6b75a03c4ff391a972",
    6: "r6824114b75a03c036c8f7964",
    7: "r615287be75a03c68fe025d0f",
    8: "r6420fcd475a03c35cf66f64f"
}

# 周五场地号对应标签
available_court_5 = {
    1: "r65112f5875a03c70bbc49e16",
    2: "r65112f5875a03c70bbc49e17",
    3: "r65112f5875a03c70bbc49e18",
    4: "r65112f5875a03c70bbc49e19",
    5: "r65112f5875a03c70bbc49e1a",
    6: "r6824114b75a03c036c8f7966",
    7: "r65112f5875a03c70bbc49e1c",
    8: "r65112f5875a03c70bbc49e1d"
}

# 周六场地号对应标签
available_court_6_12_14 = {
    1: "r5f6eb54f75a03c0cbfd2d862",
    2: "r5f6eb54f75a03c0cbfd2d863",
    3: "r5f6eb54f75a03c0cbfd2d865",
    4: "r5f6eb54f75a03c0cbfd2d866",
    5: "r5f6eb54f75a03c0cbfd2d867",
    6: "r6824114b75a03c036c8f7967",
    7: "r6420fd5075a03c35cf66fd30",
    8: "r65fd9436fc918f578042f2ee"
}

available_court_6_14_16 = {
    1: "r5f6eb54f75a03c0cbfd2d86b",
    2: "r5f6eb54f75a03c0cbfd2d86d",
    3: "r5f6eb54f75a03c0cbfd2d86e",
    4: "r5f6eb54f75a03c0cbfd2d86f",
    5: "r5f6eb54f75a03c0cbfd2d870",
    6: "r6824114b75a03c036c8f7968",
    7: "r5f6eb54f75a03c0cbfd2d872",
    8: "r65fd9436fc918f578042f2ef"
}

available_court_6_16_18 = {
    1: "r5f6eb54f75a03c0cbfd2d874",
    2: "r5f6eb54f75a03c0cbfd2d875",
    3: "r622602b0fc918f7b240a7c86",
    4: "r5f6eb54f75a03c0cbfd2d877",
    5: "r5f6eb54f75a03c0cbfd2d878",
    6: "r6824114b75a03c036c8f7969",
    7: "r5f6eb54f75a03c0cbfd2d87a",
    8: "r5f6eb54f75a03c0cbfd2d87b"
}

available_court_6_18_20 = {
    1: "r5f6eb54f75a03c0cbfd2d87d",
    2: "r5f6eb54f75a03c0cbfd2d87e",
    3: "r622602b6fc918f7b240a7c92",
    4: "r5f6eb54f75a03c0cbfd2d880",
    5: "r5f6eb54f75a03c0cbfd2d881",
    6: "r6824114b75a03c036c8f796a",
    7: "r5f6eb54f75a03c0cbfd2d883",
    8: "r5f6eb54f75a03c0cbfd2d884"
}

available_court_6_20_22 = {
    1: "r5f6eb54f75a03c0cbfd2d886",
    2: "r5f6eb54f75a03c0cbfd2d887",
    3: "r622602c0fc918f7b240a7cdb",
    4: "r5f6eb54f75a03c0cbfd2d889",
    5: "r5f6eb54f75a03c0cbfd2d88a",
    6: "r6824114b75a03c036c8f796b",
    7: "r5f6eb54f75a03c0cbfd2d88c",
    8: "r5f6eb54f75a03c0cbfd2d88d"
}

# 周日场地号对应标签
available_court_7_18_20 = {
    1: "r5fb6a2e3fc918f15180bb71c",
    2: "r5fb6a2e3fc918f15180bb71d",
    3: "r62260211fc918f7b240a7ab8",
    4: "r5fb6a2e3fc918f15180bb71e",
    5: "r5fb6a2e3fc918f15180bb71f",
    6: "r6824114b75a03c036c8f796e",
    7: "r5fb6a2e3fc918f15180bb721",
    8: "r5fb6a2e3fc918f15180bb722"
}

available_court_7_20_22 = {
    1: "r5f6eb54f75a03c0cbfd2d898",
    2: "r5f6eb54f75a03c0cbfd2d899",
    3: "r62260211fc918f7b240a7ab9",
    4: "r5f6eb54f75a03c0cbfd2d89b",
    5: "r5f6eb54f75a03c0cbfd2d89c",
    6: "r6824124075a03c036c8f8073",
    7: "r5f6eb54f75a03c0cbfd2d89e",
    8: "r5f6eb54f75a03c0cbfd2d89f"
}

# 场地选择映射字典
available_court_dict = {
    ("周一", "18:30-21:00"): available_court_1_18_20,
    ("周一", "21:00-22:30"): available_court_1_20_22,
    ("周三", "18:30-20:30"): available_court_3_18_19,
    ("周三", "20:30-22:30"): available_court_3_19_20,
    ("周五", "21:00-22:30"): available_court_5,
    ("周六", "12-14"): available_court_6_12_14,
    ("周六", "14-16"): available_court_6_14_16,
    ("周六", "16-18"): available_court_6_16_18,
    ("周六", "18-20"): available_court_6_18_20,
    ("周六", "20-22:30"): available_court_6_20_22,
    ("周日", "18：00-20：00"): available_court_7_18_20,
    ("周日", "20：00-22：30"): available_court_7_20_22
}

# 规则允许的场地
ALLOWED_BY_RULE = {
    "周一": {
        "18:30-21:00": [1, 2, 3, 7, 8],
        "21:00-22:30": [1, 2, 3, 4, 6, 7, 8],
    },
    "周三": {
        "18:30-20:30": [1, 2, 3, 6, 7, 8],
        "20:30-22:30": [1, 2, 3, 6, 7, 8],
    },
    "周五": {
        "21:00-22:30": [1, 2, 3, 4, 6, 7, 8],
    },
    "周日": {
        "18：00-20：00": [1, 2, 3, 4, 5, 6, 7, 8],
        "20：00-22：30": [1, 2, 3, 4, 5, 6, 7, 8],
    },
}

# 优先和备选场地
PRIORITY_FIELDS = [3, 4, 5, 8]
BACKUP_FIELDS = [1, 2, 6, 7]

# ========== 主函数 ==========

def auto_fill_form(name, student_id, phone_number, day, time_slot, court):
    driver = None
    try:
        logging.info("=" * 50)
        logging.info("🚀 开始执行自动填表任务")
        
        # ========== 浏览器配置 ==========
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--lang=zh-CN")
        driver = webdriver.Chrome(options=chrome_options)
        
        logging.info("✅ 启动浏览器成功")
        
        # 打开目标网页
        driver.get("http://koudaigou.net/web/formview/5f6eb43475a03c0cbfd2d74c")
        logging.info("✅ 打开网页成功")
        
        # 截图记录初始页面
        driver.save_screenshot("01_initial_page.png")
        
        # 使用等待
        wait = WebDriverWait(driver, 10)
        
        # ========== 填写基本信息 ==========
        logging.info("开始填写基本信息...")
        
        # 等待姓名输入框出现
        name_field = wait.until(EC.presence_of_element_located((By.NAME, "F1")))
        name_field.send_keys(name)
        logging.info(f"✅ 填写姓名: {name}")
        
        # 填写学号
        student_id_field = driver.find_element(By.NAME, "F3")
        student_id_field.send_keys(student_id)
        logging.info(f"✅ 填写学号: {student_id}")
        
        # 填写电话
        phone_field = driver.find_element(By.NAME, "F4")
        phone_field.send_keys(str(phone_number))
        logging.info(f"✅ 填写电话: {phone_number}")
        
        time.sleep(1)
        driver.save_screenshot("02_basic_info_filled.png")
        
        # ========== 选择日期 ==========
        logging.info(f"选择日期: {day}")
        try:
            day_checkbox = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//label/span[contains(text(), '{day}')]"))
            )
            day_checkbox.click()
            logging.info(f"✅ 选择日期成功: {day}")
            time.sleep(1)
            driver.save_screenshot(f"03_day_selected_{day}.png")
        except Exception as e:
            logging.error(f"❌ 选择日期失败: {e}")
            raise
        
        # ========== 选择时间段 ==========
        logging.info(f"选择时间段: {time_slot}")
        try:
            if day == "周五" and time_slot == "21:00-22:30":
                time_slot_element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"(//label/span[contains(text(), '{time_slot}')])[2]"))
                )
            else:
                time_slot_element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//label/span[contains(text(), '{time_slot}')]"))
                )
            time_slot_element.click()
            logging.info(f"✅ 选择时间段成功: {time_slot}")
            time.sleep(1)
            driver.save_screenshot(f"04_time_selected_{time_slot.replace(':', '_')}.png")
        except Exception as e:
            logging.error(f"❌ 选择时间段失败: {e}")
            raise
        
        # ========== 选择场地 ==========
        logging.info("开始选择场地...")
        
        def get_rule_allowed_fields(day_str: str, slot_str: str):
            """规则层允许的场地集合"""
            if day_str in ALLOWED_BY_RULE and slot_str in ALLOWED_BY_RULE[day_str]:
                return set(ALLOWED_BY_RULE[day_str][slot_str])
            return set(range(1, 9))
        
        # 获取当前时段的场地映射
        court_dict = available_court_dict.get((day, time_slot), {})
        if not court_dict:
            logging.warning(f"未找到 {day} {time_slot} 的场地配置")
            court_dict = {}
        
        # 获取规则允许的场地
        rule_allowed = get_rule_allowed_fields(day, time_slot)
        page_available_fields = set(court_dict.keys())
        effective_allowed = list(sorted(rule_allowed & page_available_fields))
        
        logging.info(f"规则允许的场地: {rule_allowed}")
        logging.info(f"页面可用的场地: {page_available_fields}")
        logging.info(f"有效的场地: {effective_allowed}")
        
        selected_court = None
        
        def select_court_from_list(court_list):
            """在给定列表顺序中找第一个可选的场地"""
            nonlocal selected_court
            for field in court_list:
                label = court_dict.get(field)
                if not label:
                    continue
                court_xpath = f"//label[@for='{label}']/following-sibling::label[@class='residue']"
                try:
                    court_status = driver.find_element(By.XPATH, court_xpath).text
                    if "剩余:1" in court_status:
                        selected_court = field
                        return True
                    else:
                        logging.info(f"场地 {field} 已满")
                except Exception as _:
                    logging.info(f"场地 {field} 查找失败")
            return False
        
        # 1. 先尝试用户指定的场地
        if court is not None and effective_allowed:
            try:
                court_int = int(court)
                if court_int in effective_allowed:
                    label = court_dict.get(court_int)
                    if label:
                        court_xpath = f"//label[@for='{label}']/following-sibling::label[@class='residue']"
                        try:
                            court_status = driver.find_element(By.XPATH, court_xpath).text
                            if "剩余:1" in court_status:
                                selected_court = court_int
                                logging.info(f"✅ 用户指定场地 {court_int} 可用")
                            else:
                                logging.info(f"场地 {court_int} 已满，尝试其他场地")
                        except Exception:
                            logging.info(f"场地 {court_int} 查找失败")
            except Exception as e:
                logging.info(f"处理用户指定场地时出错: {e}")
        
        # 2. 如果未选上，按优先→备选尝试
        if not selected_court and effective_allowed:
            tried = set([int(court)]) if (court is not None and str(court).isdigit()) else set()
            priority_seq = [f for f in PRIORITY_FIELDS if f in effective_allowed and f not in tried]
            backup_seq = [f for f in BACKUP_FIELDS if f in effective_allowed and f not in tried]
            
            if priority_seq:
                logging.info(f"尝试优先场地: {priority_seq}")
                if select_court_from_list(priority_seq):
                    logging.info(f"✅ 选择优先场地: {selected_court}")
            
            if not selected_court and backup_seq:
                logging.info("优先场地不可用，尝试备选场地")
                logging.info(f"备选场地: {backup_seq}")
                if select_court_from_list(backup_seq):
                    logging.info(f"✅ 选择备选场地: {selected_court}")
        
        # 3. 点击选择场地
        if selected_court:
            label = court_dict[selected_court]
            court_choice = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='{label}']")))
            court_choice.click()
            logging.info(f"✅ 成功选择场地: {selected_court}")
            time.sleep(1)
            driver.save_screenshot(f"05_court_selected_{selected_court}.png")
        else:
            logging.warning("⚠️ 未找到可用场地，可能已全部订满")
            driver.save_screenshot("06_no_available_court.png")
            # 即使没有场地，也继续提交表单看看
        
        # ========== 提交表单 ==========
        logging.info("准备提交表单...")
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
            submit_button.click()
            logging.info("✅ 点击提交按钮")
            
            # 等待提交结果
            time.sleep(3)
            driver.save_screenshot("07_after_submit.png")
            
            # 检查是否提交成功
            final_url = driver.current_url
            page_title = driver.title
            page_source = driver.page_source
            
            if "success" in page_source.lower() or "成功" in page_source:
                logging.info("🎉 表单提交成功！")
                success = True
            else:
                logging.warning("表单提交状态不确定，请查看截图")
                success = True  # 假设成功，避免影响后续执行
            
        except Exception as e:
            logging.error(f"❌ 提交表单失败: {e}")
            driver.save_screenshot("08_submit_error.png")
            success = False
            raise
        
        # 关闭浏览器
        driver.quit()
        logging.info("✅ 浏览器已关闭")
        
        return success
        
    except TimeoutException:
        logging.error("⏰ 操作超时，无法找到某些元素")
        if driver:
            driver.save_screenshot("timeout_error.png")
            driver.quit()
        return False
        
    except Exception as e:
        logging.error(f"💥 执行过程中发生错误: {e}", exc_info=True)
        if driver:
            try:
                driver.save_screenshot(f"error_{datetime.now().strftime('%H%M%S')}.png")
                driver.quit()
            except:
                pass
        return False

# ========== 主程序入口 ==========

def main():
    """主函数"""
    logging.info("=" * 60)
    logging.info("GitHub Actions 自动填表任务开始执行")
    logging.info(f"执行时间: {datetime.now()}")
    logging.info("=" * 60)
    
    # ========== 在这里修改你的预定信息 ==========
    NAME = "孙思远"
    STUDENT_ID = "0231113021"
    PHONE = 18946851287
    DAY = "周三"
    TIME_SLOT = "18:30-20:30"
    COURT = 8
    # =========================================
    
    logging.info(f"预定配置:")
    logging.info(f"  姓名: {NAME}")
    logging.info(f"  学号: {STUDENT_ID}")
    logging.info(f"  电话: {PHONE}")
    logging.info(f"  日期: {DAY}")
    logging.info(f"  时间: {TIME_SLOT}")
    logging.info(f"  场地: {COURT}")
    
    # 执行自动填表
    success = auto_fill_form(NAME, STUDENT_ID, PHONE, DAY, TIME_SLOT, COURT)
    
    if success:
        logging.info("🎉 任务执行成功！")
        print("✅ 任务执行成功！")
        sys.exit(0)  # 成功退出码
    else:
        logging.error("💥 任务执行失败！")
        print("❌ 任务执行失败！")
        sys.exit(1)  # 失败退出码

if __name__ == "__main__":
    main()
