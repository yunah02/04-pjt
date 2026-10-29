# 도서 인증 페이지 (Django)

Django의 **인증(Authentication) 시스템**과 **도서 CRUD**를 결합한 웹 서비스입니다.
회원가입·로그인 같은 계정 관리부터, 로그인한 사용자만 도서를 등록·수정·삭제할 수 있는 권한 처리,
그리고 **생성형 AI(Claude)를 이용한 작가 정보 자동 생성**까지 구현했습니다.

---

## 만든 사람

| 이름 | 담당 요구사항 | 주요 역할 |
| --- | --- | --- |
| **피윤아** | F401 ~ F411 | 프로젝트 세팅, accounts 앱(회원 모델·폼, 로그인/로그아웃/회원가입/정보수정/탈퇴/비밀번호 변경) |
| **최주희** | F412 ~ F419, NF401 ~ NF402 | books 앱(도서 CRUD), 심화(작가 정보 AI 생성, User 커스터마이징, 프로필 페이지), 메인 화면 디자인, 비기능 요구사항 점검 |

---

## 기술 스택

- **Language** : Python 3
- **Framework** : Django 5.2
- **Database** : SQLite3
- **Front** : Django Template, Bootstrap 5.3, Bootstrap Icons, Google Fonts(Noto Sans KR / Noto Serif KR)
- **AI** : Anthropic API (`anthropic` SDK, 모델 `claude-sonnet-5-5`)
- **기타** : `python-dotenv` (API 키 관리), Git 브랜치 협업

---

## 주요 기능

### 1. 회원 관리 (accounts) — 피윤아

| 요구사항 | 기능 | URL | 허용 Method | 설명 |
| --- | --- | --- | --- | --- |
| F401 | 프로젝트 세팅 | - | - | 프로젝트(`book_site`)·앱(`accounts`, `books`) 생성, 공용 템플릿 폴더, `AUTH_USER_MODEL` 설정 |
| F402 | User 모델 | - | - | `AbstractUser`를 상속한 커스텀 User 모델 |
| F403 | 인증 폼 | - | - | 회원가입·정보수정·로그인·비밀번호 변경 폼 커스터마이징 |
| F404 · F405 | Book 모델·폼 | - | - | 도서 모델과 `BookForm`(작성자는 뷰에서 지정) |
| F406 | 로그인 | `/accounts/login/` | GET, POST | 이미 로그인한 사용자는 메인으로 이동 |
| F407 | 로그아웃 | `/accounts/logout/` | POST | 로그인 상태에서만 가능 |
| F408 | 회원가입 | `/accounts/signup/` | GET, POST | 가입 직후 **자동 로그인** |
| F409 | 회원정보 수정 | `/accounts/update/` | GET, POST | 이메일·이름·성 수정 (비밀번호·권한 필드는 숨김) |
| F410 | 회원 탈퇴 | `/accounts/delete/` | POST | 탈퇴 전 확인창(`confirm`) 표시 |
| F411 | 비밀번호 변경 | `/accounts/password/` | GET, POST | 변경 후에도 로그인 상태 유지 |

### 2. 도서 관리 (books) — 최주희

| 요구사항 | 기능 | URL | 허용 Method | 설명 |
| --- | --- | --- | --- | --- |
| F412 ~ F416 | 도서 **목록 조회** | `/books/` | GET | 최신 등록순 카드 목록, 도서가 없으면 안내 문구 |
| | 도서 **등록** | `/books/create/` | GET, POST | 로그인 필수, 작성자는 로그인한 사용자로 자동 저장 |
| | 도서 **상세 조회** | `/books/<pk>` | GET | 제목·저자·작성자·설명·작성/수정 시각 표시 |
| | 도서 **수정** | `/books/<pk>/update/` | GET, POST | 로그인 필수 + **작성자 본인만** 수정 가능 |
| | 도서 **삭제** | `/books/<pk>/delete/` | POST | 로그인 필수 + **작성자 본인만** 삭제 가능 |

### 3. 심화 기능 — 최주희

| 요구사항 | 기능 | 설명 |
| --- | --- | --- |
| F417 | **AI 작가 정보 생성** | 도서 상세 페이지의 `작가 정보 생성` 버튼 → 서버가 Claude API 호출 → 응답을 `Book.author_info`에 **DB 저장** → 상세 페이지에 표시 |
| F418 | **User 모델 커스터마이징** | `introduction`(자기소개) 필드와 `followings`(팔로우용 자기 참조 M:N, `related_name='followers'`) 필드 추가 |
| F419 | **프로필 페이지** | `/accounts/<username>/` 에서 자기소개와 해당 회원이 작성한 도서 목록 확인. 도서 상세의 작성자 이름에서 바로 이동 가능 |

> `followings` 필드는 모델과 마이그레이션까지 준비되어 있으며, 팔로우/언팔로우 화면과 기능은 아직 구현하지 않았습니다. 이후 확장 포인트입니다.

### 4. 비기능 요구사항 — 최주희

| 요구사항 | 내용 | 적용 방법 |
| --- | --- | --- |
| NF401 | URL 유지보수성 | 모든 `urls.py`에 `app_name` 지정, 템플릿은 `{% url 'books:detail' book.pk %}`, 뷰는 `redirect('books:index')` 형태로만 이동 (하드코딩된 주소 없음) |
| NF402 | 허용된 HTTP Method만 | 조회 전용은 `@require_safe`, 폼 화면+처리는 `@require_http_methods(['GET', 'POST'])`, 삭제·로그아웃은 `@require_POST` |

### 접근 권한 정리

| 구분 | 비로그인 | 로그인 | 작성자 본인 |
| --- | :---: | :---: | :---: |
| 도서 목록·상세·프로필 조회 | ✅ | ✅ | ✅ |
| 도서 등록 · AI 작가 정보 생성 | ❌ (로그인 페이지로 이동) | ✅ | ✅ |
| 도서 수정·삭제 | ❌ | ❌ | ✅ |
| 회원정보 수정·비밀번호 변경·탈퇴 | ❌ | ✅ (본인 계정만) | ✅ |

---

## 프로젝트 구조

```
04-pjt/
├── book_site/                 # 프로젝트 설정 (settings, urls)
├── accounts/                  # 회원 앱
│   ├── models.py              #   커스텀 User (introduction, followings)
│   ├── forms.py               #   Bootstrap 적용 인증 폼들
│   ├── views.py               #   login / logout / signup / update / delete / change_password / profile
│   ├── urls.py
│   └── templates/accounts/    #   login, signup, update, change_password, profile, _auth_form(공통 폼)
├── books/                     # 도서 앱
│   ├── models.py              #   Book (user FK, title, author, description, author_info ...)
│   ├── forms.py               #   BookForm
│   ├── views.py               #   index / create / detail / update / delete / generate_author_info
│   ├── urls.py
│   ├── static/books/css/      #   style.css (메인 화면 디자인)
│   └── templates/books/       #   index, create, detail, update
├── templates/base.html        # 공통 레이아웃 (네비게이션)
├── .env.example               # 환경변수 예시
├── requirements.txt
└── manage.py
```

### 데이터 모델 (ERD)

```
┌──────────────────────────┐        ┌───────────────────────────────┐
│ User (AbstractUser 상속)  │ 1    N │ Book                          │
│ ─────────────────────────│────────│ ──────────────────────────────│
│ username / password ...  │        │ user (FK, CASCADE)            │
│ introduction (Text)      │        │ title (Char 100)              │
│ followings (M:N, self)   │        │ author (Char 50)              │
└──────────────────────────┘        │ description (Text)            │
                                    │ author_info (Text, blank)     │
                                    │ created_at / updated_at       │
                                    └───────────────────────────────┘
```

회원이 탈퇴하면 `on_delete=models.CASCADE`에 의해 그 회원이 등록한 도서도 함께 삭제됩니다.

---

## 실행 방법

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/Scripts/activate  #source venv/bin/activate        

# 2. 패키지 설치
pip install django
pip install -r requirements.txt
python -m pip install anthropic python-dotenv
python -m pip show anthropic
# (이 프로젝트에 꼭 필요한 패키지는 django, anthropic, python-dotenv 입니다)

# 3. 환경변수 설정 (AI 작가 정보 기능에 필요)
cp .env.example .env
# .env 파일을 열어 ANTHROPIC_API_KEY=발급받은_키 로 수정 ANTHROPIC_API_KEY=발급받은_키

# 4. 마이그레이션
python manage.py migrate

# 5. 서버 실행
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 로 접속하면 도서 목록 화면으로 이동합니다.

> `.env`는 API 키가 들어 있으므로 **절대 Git에 올리지 않습니다.** (`.gitignore`에 등록)
> API 키가 없거나 호출에 실패해도 서버가 죽지 않고 오류 안내 메시지를 처리하도록 `try/except`로 감쌌습니다.

---

## 학습 내용

### 인증(Authentication) 기능을 직접 구현하며 배운 점
- **`AUTH_USER_MODEL`은 첫 `migrate` 전에 설정해야 한다.** 나중에 바꾸면 DB를 지우고 마이그레이션을 다시 해야 합니다. 그래서 프로젝트 시작 단계(F401)에서 가장 먼저 `AbstractUser`를 상속한 커스텀 User를 잡아 두었습니다.
- **`User`를 직접 import하지 않고** `get_user_model()` / `settings.AUTH_USER_MODEL`을 사용해야 모델을 교체해도 코드가 깨지지 않습니다. (Book 모델의 FK, 각종 폼의 `Meta.model`)
- **`update_session_auth_hash`** : 비밀번호를 바꾸면 세션이 무효화되어 바로 로그아웃되는데, 이 함수를 호출해 로그인 상태를 유지합니다.
- **회원 탈퇴는 `delete()` → `logout()` 순서**로 처리해야 합니다. 로그아웃을 먼저 하면 `request.user`가 익명 사용자가 되어 삭제가 되지 않습니다.
- **`login_required`와 로그인 분기** : 이미 로그인한 사용자가 로그인/회원가입 화면에 접근하면 메인으로 돌려보내고, 로그인이 필요한 기능은 데코레이터로 보호했습니다.

### 폼과 템플릿
- `UserCreationForm`, `UserChangeForm`, `AuthenticationForm`, `PasswordChangeForm`을 **상속·커스터마이징**하는 방법 (회원정보 수정 폼에서 `password = None`으로 비밀번호 안내 숨기기, `fields`로 노출 항목 제한).
- **믹스인(`BootstrapFormMixin`)** 으로 모든 폼 입력칸에 Bootstrap 클래스를 한 번에 적용해 중복 코드를 줄였습니다.
- **`include`로 공통 템플릿(`_auth_form.html`) 재사용** : 로그인·회원가입·정보수정·비밀번호 변경이 하나의 카드형 폼 템플릿을 공유합니다.
- **템플릿 상속(`base.html`)** 으로 네비게이션을 한 곳에서 관리하고, 로그인 여부에 따라 메뉴를 다르게 보여줍니다.

### 모델 관계와 권한
- `ForeignKey(1:N)`로 도서와 작성자를 연결하고, `form.save(commit=False)` 후 `book.user = request.user`를 지정해 **폼에 없는 필드를 뷰에서 채우는** 방법.
- 수정·삭제 시 **작성자 본인인지 검사**해 다른 사람의 글을 건드리지 못하게 한 권한 처리.
- 역참조(`person.book_set.all`)로 프로필 페이지에서 작성한 도서 목록 출력.
- **자기 참조 M:N**(`ManyToManyField('self', symmetrical=False, related_name='followers')`)의 구조.

### 비기능 요구사항(URL·HTTP Method)
- URL에 `app_name`(네임스페이스)을 주고 `{% url %}` / `redirect(이름)`만 써서 **주소가 바뀌어도 수정할 곳이 없는** 구조 만들기.
- `@require_safe`, `@require_http_methods`, `@require_POST`로 **허용된 Method만 받도록** 제한. 삭제·로그아웃을 `<a>` 링크가 아닌 **POST 폼**으로 구현해야 하는 이유(주소창 접근 시 405).
- URL 패턴 순서 : `<str:username>/` 같은 가변 경로는 `login/`, `signup/` 같은 고정 경로 **아래**에 두어야 가려지지 않습니다.

### 생성형 AI 연동
- 서버에서 외부 API를 호출하고 **결과를 DB에 저장**한 뒤 화면에 보여주는 흐름 (버튼 → POST 뷰 → API 호출 → 저장 → 상세 페이지 redirect).
- API 키는 코드에 직접 쓰지 않고 **`.env` + `python-dotenv`** 로 읽고, `.gitignore`로 보호.
- 키 누락·네트워크 오류에 대비한 **예외 처리**, 그리고 *"확실하지 않은 내용은 지어내지 말고 모르면 모른다고 말해줘"* 처럼 **환각(hallucination)을 줄이는 프롬프트** 작성.

### 협업(Git)
- 담당 기능을 나눠 브랜치(`yunah`, `back`)에서 각자 작업한 뒤 **merge** 하는 흐름과, 같은 파일(`base.html`, `views.py` 등)을 함께 다룰 때 생기는 충돌을 해결하는 경험.

---

## 느낀 점

### 피윤아
그동안 수업 시간에 배운 내용을 기반으로 프로젝트를 진행하면서, **배웠던 것들을 다시 한번 차근차근 정리할 수 있었던 좋은 기회**였습니다. 수업 때는 "이렇게 하면 된다"고 따라 쳤던 코드가 많았는데, 직접 만들어 보니 *왜 이 순서로 써야 하는지*(예: 회원 탈퇴에서 삭제 후 로그아웃, 비밀번호 변경 후 세션 유지)를 몸으로 이해하게 되었습니다.
특히 **스켈레톤 코드 없이 처음부터 직접 구현**해 보니 신기하기도 했고, 모델 → 폼 → 뷰 → URL → 템플릿으로 이어지는 Django의 흐름이 머릿속에서 하나로 연결되는 느낌이었습니다. 에러 메시지를 읽고 원인을 찾아가는 과정에서 많이 배웠고, 앞으로 더 큰 프로젝트도 해낼 수 있겠다는 자신감이 생겼습니다.

### 최주희
뒷부분을 맡아서 처음엔 **살짝 어렵게 느껴지는 부분**도 있었지만, 도서 CRUD의 권한 처리부터 **심화 기능(User 커스터마이징, 프로필 페이지, AI 작가 정보 생성)** 까지 직접 구현해 볼 수 있어서 의미 있었습니다. 특히 외부 AI API를 서버에서 호출해 결과를 DB에 저장하고 화면에 보여주는 과정은 "내가 만든 서비스에 AI가 들어갔다"는 느낌이 들어서 가장 재미있었습니다.
화면 모양과 배치도 더 다듬어 마음에 드는 기능 구현과 디자인을 함께 하고 싶어, 메인 화면처럼 도서 상세·프로필·폼 화면도 통일감 있게 꾸며 보았습니다. 완성본이 생각보다 통일감있고 깔끔하게 생각보다 더 잘 나와서 프론트엔드와 같이 화면을 꾸미는 것이 즐겁다는 것을 새롭게 알게 되었고 흥미를 찾은 것 같습니다. 


