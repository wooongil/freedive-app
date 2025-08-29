import streamlit as st
from datetime import time, date

st.set_page_config(page_title="교육 안내문 생성기", page_icon=":mailbox_with_mail:", layout="centered")

# ---- 데이터 (필요하면 여기만 수정) -----------------------------------------
COURSES = {
    "AIDA1": {"구성": "이론1+풀장1일", "유효기간": "1개월"},
    "입문 프리다이버": {"구성": "이론1+풀장3일", "유효기간": "3개월"},
    "AIDA2": {"구성": "이론1+풀장3일", "유효기간": "3개월"},
    "AIDA3": {"구성": "이론+풀장4일", "유효기간": "4개월"},
    "AIDA4": {"구성": "이론+풀장4일", "유효기간": "6개월"},
    "2+3 패키지": {"구성": "이론2+풀장6일", "유효기간": "6개월"},
    "3+4 패키지": {"구성": "이론2+풀장7일", "유효기간": "8개월"},
    "4+강사 패키지": {"구성": "마스터4일+강사7일", "유효기간": "1년6개월"},
}

LOCATIONS = {
    "올팍": {
        "주소": "서울 송파구 올림픽로 424",
        "링크": "https://cafe.naver.com/bluepebble/620",
        "입장료_평일": 18000,
        "입장료_주말": 22000,
        "주의": "매우 크고 복잡합니다 꼭! 오시기 전에 링크 확인해주세요",
        "멘트": "올림픽공원 수영장 잠수풀 입구에서 뵙겠습니다."
    },
    "잠실풀": {
        "주소": "서울 송파구 올림픽로 25",
        "링크": "https://cafe.naver.com/bluepebble/259",
        "입장료_평일": 15000,
        "입장료_주말": 15000,
        "주의": "예약후 취소가 어렵습니다.",
        "멘트": "잠실 종합운동장 제2수영장 입구에서 뵙겠습니다."
    },
    "송도풀": {
        "주소": "인천 연수구 인천신항대로892번길 40 인천환경공단 송도스포츠파크",
        "링크": "https://ssp.eco-i.or.kr/sub/contents/default_page.asp?mNo=MA070000000",
        "입장료_평일": 5000,
        "입장료_주말": 18000,
        "주의": "국립 운영(주말 수업 어려움), 동시입장 필요",
        "멘트": "송도 잠수풀 로비에서 강사님을 만나시면 됩니다."
    },
    "수원풀": {
        "주소": "경기 수원시 팔달구 창룡대로210번길 41 (수원 스포츠아일랜드)",
        "링크": "https://www.worldcupdivingpool.com/Map",
        "입장료_평일": 18000,
        "입장료_주말": 18000,
        "주의": "입장 시 주차 3시간 할인 등록",
        "멘트": "수영장 입구가 아닌 스쿠버풀 입구에서 뵙겠습니다."
    },
    "성남풀": {
        "주소": "경기 성남시 중원구 제일로 60 성남종합스포츠센터 B동 지하2층",
        "링크": "https://cafe.naver.com/bluepebble/633",
        "입장료_평일": 15000,
        "입장료_주말": 20000,
        "주의": "지하2층 잠수풀 입구에서 뵙겠습니다.",
        "멘트": "성남 아쿠아라인 잠수풀 입구에서 뵙겠습니다."
    },
    "K26": {
        "주소": "경기 가평군 청평면 고재길 262-57",
        "링크": "https://k-26.com/intro/index3.php",
        "입장료_평일": 33000,
        "입장료_주말": 55000,
        "주의": "지각 시 결석 처리될 수 있습니다.",
        "멘트": "가평 K26 1층 로비에서 뵙겠습니다."
    },
    "딥스테이션": {
        "주소": "경기 용인시 처인구 포곡읍 성산로 523 딥스테이션",
        "링크": "https://deepstation.kr/theme/basic/sub/location.php",
        "입장료_평일": 48000,
        "입장료_주말": 66000,
        "주의": "현장 규정 준수",
        "멘트": "딥스테이션 2층에서 뵙겠습니다."
    },
    "파라다이브": {
        "주소": "경기도 시흥시 거북섬중앙로 1 1동3층 303호",
        "링크": "https://paradive.co.kr/About/location.php",
        "입장료_평일": 45000,
        "입장료_주말": 67000,
        "주의": "평일 5m존만 가능",
        "멘트": "파라다이브 3층 로비에서 뵙겠습니다."
    },
}

INSTRUCTORS = [
    "김혜진", "함현석", "이주희", "신가은", "박주흠",
    "노진아", "선동진", "이동규", "차진명", "김민현",
    "조아라", "육소영", "노진아", "주선형", "김동희",
    "표정승"
]

DEFAULT_ITEMS = "수영복, 수영모, 수건, 세면도구"

# ---- 사이드바 --------------------------------------------------------------
with st.sidebar:
    st.header("옵션")
    show_details = st.checkbox("과정 구성/유효기간 문구 포함", value=True)
    custom_items = st.text_input("기본 준비물(수정 가능)", value=DEFAULT_ITEMS)
    add_extra = st.text_area("추가 안내문(선택)", placeholder="예) 신분증 지참, 동시입장 필요 등")

st.title("교육 안내문 생성기")
st.caption("드롭다운 선택 → 자동으로 안내문 완성 → 복사/다운로드")

# ---- 입력 영역 --------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    course = st.selectbox("신청 레벨(과정)", options=list(COURSES.keys()))
    instr = st.selectbox("강사명", options=INSTRUCTORS)
with col2:
    loc_name = st.selectbox("교육 장소", options=list(LOCATIONS.keys()))
    dt_date = st.date_input("교육 날짜", value=date.today())
    dt_time = st.time_input("교육 시간", value=time(15, 0))

name = st.text_input("교육생 이름(선택)", placeholder="예) 홍길동")

# ---- 데이터 계산 ------------------------------------------------------------
loc = LOCATIONS.get(loc_name, {})
course_meta = COURSES.get(course, {})

# 한국 형식 날짜/시간 (Windows 호환)
weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
dow = weekday_kr[dt_date.weekday()]
time_str = dt_time.strftime("%H:%M")
date_kr = f"{dt_date.month}월 {dt_date.day}일"

# 평일/주말 구분
is_weekend = dow in ["토", "일"]
if is_weekend:
    fee = loc.get("입장료_주말", 0)
    fee_type = "주말"
else:
    fee = loc.get("입장료_평일", 0)
    fee_type = "평일"

# 보기용 구성/유효기간
course_line = ""
if show_details:
    g = course_meta.get("구성", "")
    v = course_meta.get("유효기간", "")
    parts = []
    if g:
        parts.append(f"{g}")
    if v:
        parts.append(f"교육소진유효기간: {v}")
    if parts:
        course_line = f"({', '.join(parts)})"

# 금액/빈값 안전 처리
fee_str = f"{fee:,}원 ({fee_type})" if isinstance(fee, (int, float)) and fee > 0 else "현장 안내"

# 수강생 이름 라인
name_line = f"수강생: {name}" if name.strip() else ""

# ---- 안내문 생성 ------------------------------------------------------------
message = f"""▶ 신청레벨
- {course}
{course_line}

▶ 교육스케줄
- {date_kr}({dow})
잠수풀/이론 수업 {time_str}

▶ 교육장소
{loc_name} ({loc.get('주소','')})
오시는 방법 {loc.get('링크','')}

▶ 준비물
- {custom_items}
- 입장료 {fee_str} (수업 후 안내)

▶ 강사 연락처
교육강사: {instr}
대표번호 블루페블 02-6278-7787
{name_line}

📍 안내멘트
{date_kr}({dow}) {time_str}에 {loc.get('멘트','')}
주의사항: {loc.get('주의','')}
"""

if add_extra.strip():
    message += f"\n추가 안내: {add_extra.strip()}\n"

# ---- 출력 UI ---------------------------------------------------------------
st.subheader("생성된 안내문")
st.text_area("아래 내용 통째로 복사해서 보내면 됩니다.", value=message, height=360)
st.code(message, language="")  # 복사 버튼 제공

# 다운로드 버튼 (txt)
st.download_button(
    label="안내문 .txt 다운로드",
    data=message.encode("utf-8"),
    file_name=f"안내문_{dt_date.isoformat()}_{loc_name}.txt",
    file_name=f"안내문_{dt_date.isoformat()}_{loc_name}.txt",
    mime="text/plain"
)

# 미리보기 카드
with st.expander("장소 상세 미리보기"):
    st.markdown(f"**주소**: {loc.get('주소','')}")
    st.markdown(f"**링크**: {loc.get('링크','')}")
    st.markdown(f"**입장료**: {fee_str}")
    st.markdown(f"**주의사항**: {loc.get('주의','')}")
