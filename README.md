# Naver News Crawler

네이버 뉴스 기사 크롤러 생성

## 개요

이 프로젝트는 네이버 뉴스를 크롤링하는 몇 가지의 파이썬 기반의 크롤러를 제공합니다.

## 파일 설명

- `SDFLD.py` : 최근 며칠 동안의 검색 데이터를 추출하는 스크립트입니다.
- `SDFSCC.py` : 특정 카테고리와 개수에 대한 검색 데이터를 추출하는 스크립트입니다.

## 사용 방법

### 환경 설정

1. 필요한 패키지를 설치합니다:
    ```bash
    pip install -r requirements.txt
    ```

2. `SDFLD.py` 또는 `SDFSCC.py` 파일을 실행하여 데이터를 수집합니다.

### 예제

```python
# SDFSCC.py 예제
from SDFSCC import search_news_count

# 검색어: '인공지능', 카테고리: 'IT/과학', 개수: 100
search_news_count('인공지능', 'IT/과학', 100)
