from selenium import webdriver as wd
from detection.utils.image import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from detection.face_detector import FaceDetector

import os 
import time
import random


def login_insta(user_id, user_passwd):    
    driver = wd.Chrome('./chromedriver')
    driver.set_window_size(520, 920) # 사이즈 축소. 사이즈에 따라서도 Tag가 바뀜.
    driver.get('https://www.instagram.com/accounts/login/')
    
    # Interval
    time.sleep(5)
    
    # Login Part
    try:
        instagram_id_form = driver.find_element(by=By.XPATH, value='//input[@aria-label="전화번호, 사용자 이름 또는 이메일"]')
        instagram_id_form.click()
        time.sleep(1)
        
        instagram_id_form.send_keys(user_id)
        time.sleep(1)
        
        instagram_pw_form = driver.find_element(by=By.XPATH, value='//input[@aria-label="비밀번호"]')
        instagram_pw_form.click()
        time.sleep(1)
        
        instagram_pw_form.send_keys(user_passwd)
        time.sleep(random.randrange(5, 10))
        instagram_pw_form.send_keys(Keys.ENTER)
        
        print(f"현재 접속한 아이디는 : {user_id} 입니다.")
        return driver
        
    except:
        print('로그인에 실패했습니다.')
        
        
def user_extract(driver, target_user):
    print(f"{target_user} 계정의 사진 추출을 시작합니다.")
    
    time.sleep(5)
    url = f"https://www.instagram.com/{target_user}/"
    driver.get(url)
    
    # Interval 
    time.sleep(10)
    
    # 첫 게시물 보기
    first_feed = driver.find_element(by=By.XPATH, value='//article//img //ancestor :: div[2]')
    first_feed.click()
    time.sleep(5)
    
    feed_count = 0 # 게시물 개수
    
    while True:
        try:
            time.sleep(10)
            feed_img_list = driver.find_elements(by=By.XPATH, value="//article/div/div[2]/div/div[2]/div")

            if len(feed_img_list) == 0:
                download_img(feed_count, 0, driver, target_user)
                time.sleep(random.randrange(3, 5))
                next_post_btn(driver)
                feed_count += 1 

            else:
                for img_count in range(len(feed_img_list)):
                    try:
                        # 마지막 사진은 다음 사진 클릭 불가. 바로 저장 후 다음 게시글로 이동.
                        next_img_btn = driver.find_element(by=By.XPATH, value='//button[@aria-label="다음"]')  # 다음 이미지
                        download_various_imgs(feed_count, img_count, driver, target_user)
                        next_img_btn.click()
                        time.sleep(random.randrange(3, 5))
                    except:
                        download_various_imgs(feed_count, img_count, driver, target_user)
                        next_post_btn(driver)
                        feed_count += 1

        except:
            try:
                time.sleep(random.randrange(3, 5))
                next_img_btn.click()
                
            except:
                try:
                    next_post_btn(driver)
                    feed_count += 1 
                except:
                    print(f"게시물 크롤링이 끝났습니다.")
                    break
                        
                        
def download_various_imgs(feed_count # 게시물 개수
                         ,img_count # 게시물에 있는 사진 개수 
                        ,driver, target_user):
    try:
        src_range_list = [2, 3, 3, 3, 3, 3, 3, 3, 3, 3] 
        # 왜 인덱스 0 은 2 인가? : Html Value에서 첫 게시물의 value가 2로 들어감.
        src_range = src_range_list[img_count]
    
        src_img_path = driver.find_element(by=By.XPATH, value=f'//article //li[{src_range}] //img')
        url = src_img_path.get_attribute('src')        
        img = Image.url_load(url) # url 에서 가져온 이미지
        bboxes, conf = FaceDetector.detect(img=img)
        annotated_img = Image.annotate_green_bboxes(img=img, bboxes=[bboxes[0]])
        
        bboxes = bboxes[0] # [[1, 1, 100, 100]] 이런식으로 출력.
        conf = conf[0]['confidence']
        
        try:
            if len(bboxes) >= 1:
                create_folder(f'result/{target_user}/label/')
                with open(f'result/{target_user}/label/{target_user}_{feed_count+1}_{img_count+1}_conf{round(conf, 5)}.txt', 'w', encoding='UTF-8') as f:
                    f.write(f'{url}\n{bboxes} {conf} \n')
                
                # 원본 이미지
                create_folder(f'result/{target_user}/detect/')
                path = f'result/{target_user}/detect/{target_user}_{feed_count+1}_{img_count+1}_conf{round(conf, 5)}.jpg'
                Image.save(img, path=path)
                
                # bboxes 이미지 
                create_folder(f'result/{target_user}/detect_bboxes/')
                path = f'result/{target_user}/detect_bboxes/{target_user}_{feed_count+1}_{img_count+1}_conf{round(conf, 5)}.jpg'
                Image.save(annotated_img, path=path)
                
        except:     
            time.sleep(3)
        
    except Exception as e:
        create_folder(f'result/{target_user}/none_bboxes/')
        path = f'result/{target_user}/none_bboxes/{target_user}_{feed_count+1}_{img_count+1}.jpg'
        Image.save(img, path=path)
        time.sleep(3)
         
            
def download_img(feed_count # 게시물 개수
                 ,img_count # 게시물에 있는 사진 개수 카운트
                ,driver, target_user):
    try:
        src_img_path = driver.find_element(by=By.XPATH, value='//article[@role="presentation"] //div /img')
        url = src_img_path.get_attribute('src')
        
        img = Image.url_load(url) # url 에서 가져온 이미지
        bboxes, conf = FaceDetector.detect(img=img)
        annotated_img = Image.annotate_green_bboxes(img=img, bboxes=[bboxes[0]])
        
        bboxes = bboxes[0] # [[1, 1, 100, 100]] 이런식으로 출력.
        conf = conf[0]['confidence']
        
        try:
            if len(bboxes) >= 1:
                create_folder(f'result/{target_user}/label/')
                with open(f'result/{target_user}/label/{target_user}_{feed_count+1}_{img_count+1}_conf{round(conf, 5)}.txt', 'w', encoding='UTF-8') as f:
                    f.write(f'{url}\n{bboxes} {conf} \n')
                
                # 원본 이미지
                create_folder(f'result/{target_user}/detect/')
                path = f'result/{target_user}/detect/{target_user}_{feed_count+1}_{img_count+1}_conf{round(conf, 5)}.jpg'
                Image.save(img, path=path)
                
                # bboxes 이미지 
                create_folder(f'result/{target_user}/detect_bboxes/')
                path = f'result/{target_user}/detect_bboxes/{target_user}_{feed_count+1}_{img_count+1}_conf{round(conf, 5)}.jpg'
                Image.save(annotated_img, path=path)
                
        except:     
            time.sleep(3)
        
    except Exception as e:
        create_folder(f'result/{target_user}/none_bboxes/')
        path = f'result/{target_user}/none_bboxes/{target_user}_{feed_count+1}_{img_count+1}.jpg'
        Image.save(img, path=path)
        time.sleep(3)
    

def create_folder(folder_name):
    return os.makedirs(folder_name, exist_ok=True)


def next_post_btn(driver):
    return driver.find_element(By.XPATH, '//*[@aria-label="다음" and @height="16"] //ancestor :: button').click()