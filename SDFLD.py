def search_news(input_search, lately_day):
    '''
    최근 몇일간의 검색 데이터 추출
    args:
        input_search : 원하는 검색어 '' 작성 / dtype == str 
        lately_day : 당일 기준 이전 몇일 전부터의 사이트를 추출할 것 인지 작성 / dtype == int
    return:
        'input_search'에 대한 당일 기준 lately_day일 전부터의 뉴스 데이터를 DataFrame으로 변환
            이때, 해당 table의 key = ['date' 'category', 'press', 'title', 'dicument','link']
    '''
    
    
    # default value
    if input_search == '':
        input_search = '딥러닝'
    if lately_day == '':
        lately_day = 3
    
    # date formatting
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=int(lately_day))
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')



    # list 생성    
    title_list = []
    date_list = []
    category_list = []
    press_list = []
    document_list = []
    urls_list = []

    current_news_page=1
    while current_news_page:
        print('\n{}번째 기사글부터 크롤링을 시작합니다.'.format(current_news_page))
        web_url = 'https://search.naver.com/search.naver?where=news&query={0}&sort=1&nso=so:dd,p:from{1}to{2},a:all&start={3}'.format(input_search,start_date,end_date,current_news_page)

        # 네이버 페이지 자체 크롤링 오류 확인
        try:
            web = requests.get(web_url).content
            soup = BeautifulSoup(web, 'html.parser')

            # 해당 페이지의 naver news url parsing
            url_list = []
            for a_tag in soup.find_all('a', {'class': 'info'}):
                if a_tag['href'].startswith('https://n.news.naver.com/'):
                    url_list.append(a_tag['href'])
                    
        except:
            print('네이버 뉴스 링크를 모으는 중 에러가 발생, 에러 링크 : ', url)

        print('{}개 사이트 크롤링 중..................'.format(len(url_list)))
        
        
        # 마지막 페이지 까지만 크롤링
        if [soup.find('div', {'class':'not_found02'})] == [None]:     

        # 네이버 뉴스 링크 접근 오류 확인 & 해당 바퀴에 네이버 페이지가 없다면 pass
          if url_list != []:
              for url in url_list:
                  try :
                      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                      web_news = requests.get(url, headers=headers).content
                      source = BeautifulSoup(web_news, 'html.parser')


                      # title
                      title = source.find('h2', {'id':'title_area'}).get_text() 
                      print('Processing article : {}'.format(title))

                      # date
                      date=source.find_all('div',{'class': 'media_end_head_info_datestamp_bunch'})[0].find('span')['data-date-time']

                        
                      # category
                      category = source.find('em',{'class': 'media_end_categorize_item'}).get_text()

                      # press
                      press = source.find('em',{'class': 'media_end_linked_more_point'}).get_text()

                      #document
                      document = source.find('article',{'id':'dic_area'}).get_text()
                      document = document.replace("\n", "")
                      document = document.replace("\\", "")
                      document = document.replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", "")
                      document = document.replace("동영상 뉴스       ", "")
                      document = document.replace("동영상 뉴스", "")
                      document = document.strip()


                    
                      # 붙여넣기
                      title_list.append(title)
                      category_list.append(category)
                      press_list.append(press)
                      document_list.append(document)
                      urls_list.append(url)
                      date_list.append(date)

                  except:
                      print('*** 에러 발생 링크 : {}'.format(url))

          else:
              pass

        else:
             break

        time.sleep(5)
        current_news_page += 10

    print('크롤링을 마무리했습니다.') 

    article_df = pd.DataFrame({'date':date_list,
                               'category' : category_list,
                               'press' : press_list,
                               'title':title_list,
                               'dicument': document_list, 
                               'link':urls_list})
    
    article_df.to_excel('{0}_{1}.xlsx'.format(input_search,datetime.now().strftime('%y%m%d)), index=False, encoding='utf-8')
