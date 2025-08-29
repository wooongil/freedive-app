import streamlit as st
from datetime import time, date, timedelta

st.set_page_config(page_title="교육 안내문 생성기", page_icon=":mailbox_with_mail:", layout="centered")

# ---- 데이터 (필요하면 여기만 수정) -----------------------------------------
COURSES = {
    "AIDA1": {"구성": "이론1+풀장1일", "유효기간_일": 30},
    "입문 프리다이버": {"구성": "이론1+풀장3일", "유효기간_일": 90},
    "AIDA2": {"구성": "이론1+풀장3일", "유효기간_일": 90},
    "AIDA3": {"구성": "이론+풀장4일", "유효기간_일": 120},
    "AIDA4": {"구성": "이론+풀장4일", "유효기간_일": 180},
    "2+3 패키지": {"구성": "이론2+풀장6일", "유효기간_일": 180},
    "3+4 패키지": {"구성": "이론2+풀장7일", "유효기간_일": 240},
    "4+강사 패키지": {"구성": "마스터4일+강사7일", "유효기간_일": 540},
}

LOCATIONS = {
    "올림픽수영장 잠수풀": {
        "주소": "서울 송파구 올림픽로 25",
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
        "입장료_주말": 5000,
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
with col2:
    loc_name = st.selectbox("교육 장소", options=list(LOCATIONS.keys()))
    dt_date = st.date_input("교육 날짜", value=date.today())
    
    # 시간을 AM/PM으로 선택
    col3, col4 = st.columns(2)
    with col3:
        time_hour = st.selectbox("시간", options=list(range(1, 13)), index=2)  # 3시 = index 2
    with col4:
        time_minute = st.selectbox("분", options=[0, 15, 30, 45])
    
    # AM/PM 선택
    time_ampm = st.selectbox("AM/PM", options=["PM", "AM"], index=0)

# 이론수업 선택 및 일정
theory_class = st.checkbox("이론수업 포함", value=False)

# 이론수업 일정 설정 (이론수업 선택 시에만 표시)
if theory_class:
    col5, col6 = st.columns(2)
    with col5:
        theory_date = st.date_input("이론수업 날짜", value=dt_date)
        theory_hour = st.selectbox("이론수업 시간", options=list(range(1, 13)), index=6)  # 7시 = index 6
        theory_minute = st.selectbox("이론수업 분", options=[0, 15, 30, 45])
    with col6:
        theory_ampm = st.selectbox("이론수업 AM/PM", options=["PM", "AM"], index=0)
        theory_weekday = weekday_kr[theory_date.weekday()]
        theory_date_kr = f"{theory_date.month}월 {theory_date.day}일"

name = st.text_input("교육생 이름(선택)", placeholder="예) 홍길동")

# ---- 데이터 계산 ------------------------------------------------------------
loc = LOCATIONS.get(loc_name, {})
course_meta = COURSES.get(course, {})

# 한국 형식 날짜/시간 (Windows 호환)
weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
dow = weekday_kr[dt_date.weekday()]

# 시간 계산 (AM/PM 기반)
def convert_to_24hr(hour, ampm):
    if ampm == "PM" and hour != 12:
        return hour + 12
    elif ampm == "AM" and hour == 12:
        return 0
    else:
        return hour

# 10분 전 시간 계산
def calculate_arrival_time(hour, minute, ampm):
    arrival_hour = hour
    arrival_minute = minute - 10
    
    # 분이 음수가 되는 경우 처리
    if arrival_minute < 0:
        arrival_hour -= 1
        arrival_minute += 60
    
    # 시간이 0이 되는 경우 처리
    if arrival_hour <= 0:
        arrival_hour = 12
        ampm = "AM" if ampm == "PM" else "PM"
    
    return f"{arrival_hour:02d}:{arrival_minute:02d} {ampm}"

# 잠수풀 수업 시간
pool_hour = convert_to_24hr(time_hour, time_ampm)
time_str = f"{time_hour:02d}:{time_minute:02d} {time_ampm}"
end_hour = (pool_hour + 3) % 24
end_time_str = f"{end_hour:02d}:{time_minute:02d}"

# 이론수업 시간 (이론수업 선택 시)
if theory_class:
    theory_hour_24 = convert_to_24hr(theory_hour, theory_ampm)
    theory_time_str = f"{theory_hour:02d}:{theory_minute:02d} {theory_ampm}"
    theory_end_hour = (theory_hour_24 + 2) % 24
    theory_end_time_str = f"{theory_end_hour:02d}:{theory_minute:02d}"

date_kr = f"{dt_date.month}월 {dt_date.day}일"

# 유효기간 자동 계산 (일수 기반) - 종료일만 표시
유효기간_일 = course_meta.get("유효기간_일", 0)
if 유효기간_일 > 0:
    만료일 = dt_date + timedelta(days=유효기간_일)
    만료일_str = f"{만료일.month}월 {만료일.day}일"
    유효기간_표시 = f"교육소진유효기간: {만료일_str}"  # 시작일 제거, 종료일만
else:
    유효기간_표시 = ""

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
    parts = []
    if g:
        parts.append(f"{g}")
    if 유효기간_표시:
        parts.append(유효기간_표시)
    if parts:
        course_line = f"({', '.join(parts)})"

# 금액/빈값 안전 처리
fee_str = f"{fee:,}원 ({fee_type})" if isinstance(fee, (int, float)) and fee > 0 else "현장 안내"

# 수강생 이름 라인
name_line = f"수강생: {name}" if name.strip() else ""

# 교육 스케줄 생성
schedule_lines = []
if theory_class:
    schedule_lines.append(f"- 이론수업 {theory_date_kr}({theory_weekday}) {theory_time_str}~{theory_end_time_str} (자택/Zoom)")

schedule_lines.append(f"- 잠수풀 수업 {date_kr}({dow}) {time_str}~{end_time_str}")

schedule_text = "\n".join(schedule_lines)

# 도착 시간 계산 (10분 전)
arrival_time = calculate_arrival_time(time_hour, time_minute, time_ampm)

# ---- 안내문 생성 ------------------------------------------------------------
message = f"""▶ 신청레벨
- {course}
{course_line}

▶ 교육스케줄
- {date_kr}({dow})
{schedule_text}"""

# 이론수업이 아닌 경우에만 교육장소 표시
if not theory_class:
    message += f"""

▶ 교육장소
{loc_name} ({loc.get('주소','')})
오시는 방법 {loc.get('링크','')}"""

# 올림픽수영장 잠수풀만 주의사항 추가
if loc_name == "올림픽수영장 잠수풀" and not theory_class:
    message += f"""
주의사항: {loc.get('주의','')}"""

message += f"""

▶ 준비물
- {custom_items}"""

# 이론수업이 아닌 경우에만 입장료 표시
if not theory_class:
    message += f"""
- 입장료 {fee_str} (수업 후 안내)"""

message += f"""

▶ 강사 연락처
교육강사 연락처는 교육 전 안내드립니다.
대표번호 블루페블 02-6278-7787
{name_line}

📍 안내멘트
{date_kr}({dow}) {arrival_time}까지 {loc.get('멘트','')}
궁금하신 점은 언제든 문의주세요😃"""

if add_extra.strip():
    message += f"\n\n추가 안내: {add_extra.strip()}"

# ---- 출력 UI ---------------------------------------------------------------
st.subheader("생성된 안내문")

# 수정 가능한 text_area
edited_message = st.text_area("아래 내용을 수정하거나 복사해서 사용하세요:", value=message, height=360)

# 수정된 내용으로 다운로드
st.download_button(
    label="안내문 .txt 다운로드",
    data=edited_message.encode("utf-8"),
    file_name=f"안내문_{dt_date.isoformat()}_{loc_name}.txt",
    mime="text/plain"
)

# 수정된 내용으로 코드 블록 표시
st.code(edited_message, language="")

# 미리보기 카드
with st.expander("장소 상세 미리보기"):
    st.markdown(f"**주소**: {loc.get('주소','')}")
    st.markdown(f"**링크**: {loc.get('링크','')}")
    st.markdown(f"**입장료**: {fee_str}")
    st.markdown(f"**주의사항**: {loc.get('주의','')}")
