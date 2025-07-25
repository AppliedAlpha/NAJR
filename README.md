# NAJR: "Nareum Invitational Festival" 공연 좌석 예약 서비스

![Service Logo](static/logos/cluster-logo.svg)

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [주요 기능](#주요-기능)
3. [기술 스택](#기술-스택)
4. [프로젝트 구조](#프로젝트-구조)
5. [배포 현황](#배포-현황)
6. [기여](#기여)
6. [라이선스](#라이선스)

## 프로젝트 개요

이 프로젝트는 `2025 Nareum Invitation Festival` 공연 좌석을 웹에서 간편하게 예약할 수 있도록 만든 예매 시스템입니다.

프로젝트는 **Flask + SQLite** 기반 환경에서 구현되었으며, **Synology NAS Web Station** 호스팅을 활용해 배포되었습니다.

관람객은 회원가입 없이 이름과 연락처, 이메일 인증만으로 손쉽게 좌석을 예약할 수 있고, 예약을 확인하거나 취소할 수 있습니다.

## 주요 기능
* **좌석 보기 & 예약**: 남은 좌석 확인, 예약 폼 제출
* **이메일 인증**: 이메일 유효성 검사를 위한 랜덤 코드 전송 & 확인 시스템 *(pseudo-implementation)*
* **예약 확인/취소**: 이름·전화번호로 본인 예약 조회 및 취소
* **공지사항/시간표 확인**: 서비스 내부 팝업 창을 통한 공지사항 및 공연 시간표 확인

## 기술 스택

| 분야       | 기술/라이브러리                          |
| -------- | --------------------------------- |
| 백엔드      | Python, Flask                     |
| 메일 전송    | Flask-Mail, Gmail SMTP (SSL)      |
| DB       | SQLite             |
| 프론트엔드    | Jinja2 Templates, Bootstrap (CSS) |

## 프로젝트 구조

```plaintext
.
├── app.py                 # Flask 애플리케이션 진입점
├── models.py              # SQLAlchemy DB 모델 정의
├── instance/              # DB 저장 폴더 (Git 제외)
│   └── seats.db           # SQLite 데이터베이스 파일
├── templates/             # Jinja2 HTML 템플릿
│   ├── title.html             # 홈(타이틀) 페이지
│   ├── reservation.html       # 좌석 예약 페이지
│   ├── reservation_email.html # 예약 확인 이메일 템플릿
│   ├── check_cancel.html      # 예약 확인/취소 페이지
│   └── rev_list.html          # 관리자용 예약 목록 페이지
├── static/                # CSS, JS, 이미지 등 정적 파일
└── README.md              # 프로젝트 설명
```

## 배포 현황
현재 이 사이트는 나름청소년활동센터 홈페이지의 서브 도메인(https://2025festival.nareum.life) 에 배포되어 있습니다.

## 기여
이 프로젝트에 기여를 원하신다면, 다음과 같은 방식을 활용해주세요.
- 이 저장소를 Fork한 후 > 새로운 Branch를 만들어 Commit/Push > Pull Request 생성
- 사이트 담당자 이메일 주소 ([clusterfriends@gmail.com](mailto:clusterfriends@gmail.com)) 로 수정사항 요청

## 라이선스
Copyright 2025. Team Cluster (최원서, 김지훈) All Rights Reserved.
