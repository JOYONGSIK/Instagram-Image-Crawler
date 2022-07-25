# Instagram Image Crawler 

- 인스타그램 계정, 해시태그 이미지 크롤러.
    - Instagram account, hashtag image crawler.

- MTCNN을 사용하여 사람 검출 후 이미지 저장.
    - Use MTCNN to detect people and save images.

--- 

- API 필요없이 Selenium XPATH 상대 경로 지정하여 사용. 
    - (Class 이름이 변경되어도, 상대 경로로 전체 잡아놓았기에 문제 X)

- 계정이 잠길 수 있으니 부계정으로 사용하세요. 

--- 

> How to Use? 

```python
insta_driver = login_insta(user_id, passwd)
user_extract(insta_driver, '...')
hashtag_extract(insta_driver, '...')
```

--- 
### requirements?

- Chrome Version : 103.0.5060.134, Mac Os
- selenium == 3.14.1
- Pillow == 9.0.1
- Numpy == 1.19.5
