import streamlit as st
from datetime import time, date, timedelta, datetime  # datetime 추가

st.set_page_config(page_title="교육 안내문 생성기", page_icon=":mailbox_with_mail:", layout="centered")

# ---- 데이터 (필요하면 여기만 수정) -----------------------------------------
COURSES = {
    "AIDA1": {"구성": "이론1+풀장1일", "유효기간_일": 30},
    "입문 2일 과정": {"구성": "이론1+풀장3일", "유효기간_일": 90},
    "입문 3일 과정": {"구성": "이론1+풀장3일", "유효기간_일": 90},
    "AIDA3(어드밴스) 3일 과정": {"구성": "이론+풀장4일", "유효기간_일": 120},
    "AIDA3(어드밴스) 4일 과정": {"구성": "이론+풀장4일", "유효기간_일": 120},
    "AIDA4(마스터)": {"구성": "이론+풀장4일", "유효기간_일": 180},
    "1+2+3 어드밴스 패키지": {"구성": "이론2+풀장6일", "유효기간_일": 180},
    "3+4 패키지": {"구성": "이론2+풀장7일", "유효기간_일": 240},
    "1+2+3+4 마스터 패키지": {"구성": "마스터4일+강사7일", "유효기간_일": 540},
    "4+ 강사 패키지": {"구성": "마스터4일+강사7일", "유효기간_일": 540},
}

LOCATIONS = {
    "올림픽수영장 잠수풀": {
        "주소": "서울 송파구 올림픽로 25",
        "링크": "https://cafe.naver.com/bluepebble/620",
        "입장료_평일": 18000,
        "입장료_주말": 22000,
        "주의": "매우 크고 복잡합니다. 꼭! 오시기 전에 링크 확인해주세요.",
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
        "주의": "신분증 또는 맡기실 거 가지고 오세요!",
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
st.subheader("잠수풀 수업 설정")
col1, col2 = st.columns(2)
with col1:
    course = st.selectbox("신청 레벨(과정)", options=list(COURSES.keys()))
    loc_name = st.selectbox("교육 장소", options=list(LOCATIONS.keys()))
with col2:
    dt_date = st.date_input("교육 날짜", value=date.today())
    
    # 잠수풀 수업 시간 설정
    col3, col4, col5 = st.columns(3)
    with col3:
        time_hour = st.selectbox("시각", options=list(range(1, 13)), index=2, key="pool_hour")
    with col4:
        time_minute = st.selectbox("분", options=[0, 15, 30, 45], key="pool_minute")
    with col5:
        time_ampm = st.selectbox("AM/PM", options=["PM", "AM"], index=0, key="pool_ampm")
        
# 온라인 이론수업 설정 (항시 열림)
st.subheader("온라인 이론수업 설정")
theory_class = st.checkbox("이론수업 포함", value=False)

# 이론수업 일정 설정 (항시 표시)
col6, col7, col8, col9 = st.columns(4)
with col6:
    theory_date = st.date_input("이론수업 날짜", value=dt_date)
with col7:
    theory_hour = st.selectbox("이론수업 시각", options=list(range(1, 13)), index=6, key="theory_hour")
with col8:
    theory_minute = st.selectbox("이론수업 분", options=[0, 15, 30, 45], key="theory_minute")
with col9:
    theory_ampm = st.selectbox("이론수업 AM/PM", options=["PM", "AM"], index=0, key="theory_ampm")

# ---- 데이터 계산 ------------------------------------------------------------
loc = LOCATIONS.get(loc_name, {})
course_meta = COURSES.get(course, {})

weekday_kr = ["월", "화", "수", "목", "금", "토", "일"]
dow = weekday_kr[dt_date.weekday()]

# 시간 계산 함수들
def convert_to_24hr(hour, ampm):
    if ampm == "PM" and hour != 12:
        return hour + 12
    elif ampm == "AM" and hour == 12:
        return 0
    else:
        return hour

def calculate_arrival_time(hour, minute, ampm):
    arrival_hour = hour
    arrival_minute = minute - 10
    if arrival_minute < 0:
        arrival_hour -= 1
        arrival_minute += 60
    if arrival_hour <= 0:
        arrival_hour = 12
        ampm = "AM" if ampm == "PM" else "PM"
    return f"{arrival_hour:02d}:{arrival_minute:02d} {ampm}"

def format_time_range(hour, minute, ampm, end_hour, end_minute, end_ampm):
    return f"{ampm} {hour:02d}:{minute:02d} ~ {end_ampm} {end_hour:02d}:{end_minute:02d}"

# 잠수풀 시간 계산
pool_hour = convert_to_24hr(time_hour, time_ampm)
end_hour_24 = (pool_hour + 3) % 24
if end_hour_24 == 0:
    end_hour, end_ampm = 12, "AM"
elif end_hour_24 > 12:
    end_hour, end_ampm = end_hour_24 - 12, "PM"
else:
    end_hour, end_ampm = end_hour_24, "AM"

# 이론수업 시간 계산
theory_hour_24 = convert_to_24hr(theory_hour, theory_ampm)
theory_end_hour_24 = (theory_hour_24 + 2) % 24
if theory_end_hour_24 == 0:
    theory_end_hour, theory_end_ampm = 12, "AM"
elif theory_end_hour_24 > 12:
    theory_end_hour, theory_end_ampm = theory_end_hour_24 - 12, "PM"
else:
    theory_end_hour, theory_end_ampm = theory_end_hour_24, "AM"

date_kr = f"{dt_date.month}월 {dt_date.day}일"

# 유효기간
유효기간_일 = course_meta.get("유효기간_일", 0)
if 유효기간_일 > 0:
    만료일 = dt_date + timedelta(days=유효기간_일)
    유효기간_표시 = f"교육소진 유효기간: {만료일.month}월 {만료일.day}일"
else:
    유효기간_표시 = ""

# 평일/주말 입장료
is_weekend = dow in ["토", "일"]
fee = loc.get("입장료_주말" if is_weekend else "입장료_평일", 0)
fee_type = "주말" if is_weekend else "평일"
fee_str = f"{fee:,}원 ({fee_type})" if fee else "현장 안내"

# 과정 상세
course_line = ""
if show_details:
    g = course_meta.get("구성", "")
    parts = [p for p in [g, 유효기간_표시] if p]
    if parts:
        course_line = f"({', '.join(parts)})"

# ---- 교육 스케줄 생성 (시간순 + 2줄 형식) ------------------------
events = []
pool_start_dt = datetime(dt_date.year, dt_date.month, dt_date.day, pool_hour, time_minute)
pool_item = f"- 잠수풀 수업\n{date_kr}({dow}) {format_time_range(time_hour, time_minute, time_ampm, end_hour, time_minute, end_ampm)}"
events.append((pool_start_dt, pool_item))

if theory_class:
    theory_weekday = weekday_kr[theory_date.weekday()]
    theory_date_kr = f"{theory_date.month}월 {theory_date.day}일"
    theory_start_dt = datetime(theory_date.year, theory_date.month, theory_date.day, theory_hour_24, theory_minute)
    theory_item = f"- 온라인 이론수업\n{theory_date_kr}({theory_weekday}) {format_time_range(theory_hour, theory_minute, theory_ampm, theory_end_hour, theory_minute, theory_end_ampm)}"
    events.append((theory_start_dt, theory_item))

events.sort(key=lambda x: x[0])
schedule_text = "\n\n".join(item for _, item in events)

# 도착 시간
arrival_time = calculate_arrival_time(time_hour, time_minute, time_ampm)

# ---- 안내문 생성 ------------------------------------------------------------
message = f"""▶ 신청레벨
- {course}
{course_line}

▶ 교육스케줄
{schedule_text}

▶ 교육장소
{loc_name} ({loc.get('주소','')})
오시는 방법 {loc.get('링크','')}"""

if loc_name == "올림픽수영장 잠수풀":
    message += f"""
주의사항: {loc.get('주의','')}"""

elif loc_name == "송도풀":
    message += f"""
주의사항: {loc.get('주의','')}"""

message += f"""

▶ 준비물
- {custom_items}"""

if not theory_class:
    message += f"""
- 입장료 {fee_str}"""

message += f"""

▶ 강사 연락처
교육강사 연락처는 교육 전 안내드립니다.
대표번호 블루페블 02-6278-7787

{date_kr}({dow}) {arrival_time}까지 {loc.get('멘트','')}
궁금하신 점은 언제든 문의주세요😃"""

if add_extra.strip():
    message += f"""

▶ 추가 안내
{add_extra.strip()}"""

# ---- 출력 UI ---------------------------------------------------------------
st.subheader("생성된 안내문")
edited_message = st.text_area("아래 내용을 수정하거나 복사해서 사용하세요:", value=message, height=360)
st.code(edited_message, language="")














