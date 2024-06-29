def search_news_count(input_search, category, count):
    """
    네이버 뉴스를 크롤링하여 특정 카테고리의 기사들을 수집하고 엑셀 파일로 저장합니다.

    Args:
        input_search (str): 검색어. 빈 문자열인 경우 기본값 '딥러닝'이 사용됩니다.
        category (str): 검색할 뉴스의 카테고리 (예: 'IT/과학', '생활/문화').
        count (int): 수집할 뉴스 기사 수. 빈 문자열인 경우 기본값 70이 사용됩니다.

    Returns:
        None: 함수는 파일을 생성하며 반환값은 없습니다.
    
    Raises:
        Exception: 네이버 뉴스 페이지 접근 중 에러가 발생할 경우 예외를 출력합니다.
    """
    if input_search == '':
        input_search = '딥러닝'
    if count == '':
        count = 70  # count를 정수로 설정

    title_list = []
    date_list = []
    category_list = []
    press_list = []
    document_list = []
    urls_list = []

    current_news_page = 1
    while len(title_list) < int(count):
        print('\n{}번째 기사글부터 크롤링을 시작합니다.'.format(current_news_page))
        web_url = f'https://search.naver.com/search.naver?where=news&query={input_search}&sort=1&start={current_news_page}'

        try:
            web = requests.get(web_url).content
            soup = BeautifulSoup(web, 'html.parser')

            url_list = [a_tag['href'] for a_tag in soup.find_all('a', {'class': 'info'}) if a_tag['href'].startswith('https://n.news.naver.com/')]
            print(f'> {len(url_list)}개 사이트 크롤링 중..................')

            for url in url_list:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                    web_news = requests.get(url, headers=headers).content
                    source = BeautifulSoup(web_news, 'html.parser')

                    current_category = source.find('em', {'class': 'media_end_categorize_item'}).get_text()

                    if current_category in ['IT', '과학']:
                        current_category = 'IT/과학'
                    elif current_category in ['생활', '문화']:
                        current_category = '생활/문화'

                    if current_category == category:
                        title = source.find('h2', {'id': 'title_area'}).get_text()
                        print('Processing article:', title)

                        date = source.find('span', {'class': 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'}).get_text()
                        press = source.find('em', {'class': 'media_end_linked_more_point'}).get_text()
                        document = source.find('article', {'id': 'dic_area'}).get_text().replace("\n", "").replace("\\", "").replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", "").replace("동영상 뉴스       ", "").replace("동영상 뉴스", "").strip()

                        title_list.append(title)
                        category_list.append(current_category)
                        press_list.append(press)
                        document_list.append(document)
                        urls_list.append(url)
                        date_list.append(date)

                except Exception as e:
                    print('네이버 뉴스 링크를 모으거나 기사를 처리하는 중 에러가 발생:', e)
                    print('**에러 발생 링크 : {}'.format(url))

            time.sleep(5)
            current_news_page += 10

        except Exception as e:
            print('네이버 뉴스 페이지 접근 중 에러가 발생:', e)
            print('**에러 발생 링크 : {}'.format(url))

    print('크롤링을 마무리했습니다.') 

    article_df = pd.DataFrame({
        'date': date_list,
        'category': category_list,
        'press': press_list,
        'title': title_list,
        'document': document_list,
        'link': urls_list
    })

    print(f'총 {len(article_df)}개의 사이트를 정리하였습니다.')

    # 파일 이름 생성
    file_category = category.replace('/', '_')

    article_df.to_excel(f'{input_search}({file_category})_{datetime.now().strftime("%y%m%d")}.xlsx', index=False, encoding='utf-8')
