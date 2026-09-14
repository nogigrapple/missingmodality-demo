from __future__ import annotations

import ast
import html
import json
import time
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------------------
# Server paths
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_ROOT = BASE_DIR / "data"

DATASETS = {
    "Baby": "Amazon Baby Dataset",
    "Beauty": "Amazon Beauty Dataset",
    "Office": "Amazon Office Products Dataset",
}


# ---------------------------------------------------------------------
# Page config + visual system
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="생성형 AI 기반 누락 모달리티 복원",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --bg: #f7f8fc;
        --text: #111827;
        --muted: #667085;
        --line: #e6e9f0;
        --accent: #4f46e5;
        --accent-soft: #eef2ff;
        --shadow: 0 18px 50px rgba(30, 41, 59, 0.08);
    }

    html, body, [class*="css"] {
        font-family: Inter, Pretendard, "Noto Sans KR", -apple-system, BlinkMacSystemFont,
                     "Segoe UI", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(99,102,241,0.10), transparent 28rem),
            radial-gradient(circle at 90% 8%, rgba(124,58,237,0.08), transparent 24rem),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
        max-width: 1480px;
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.1rem 2.2rem 1.9rem 2.2rem;
        border: 1px solid rgba(99,102,241,0.13);
        border-radius: 1.55rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.97), rgba(246,247,255,0.95));
        box-shadow: var(--shadow);
        margin-bottom: 1.1rem;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -90px;
        top: -120px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(99,102,241,.18), rgba(124,58,237,.06));
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .34rem .68rem;
        border-radius: 999px;
        background: var(--accent-soft);
        color: #4338ca;
        font-size: .77rem;
        font-weight: 800;
        letter-spacing: .04em;
        text-transform: uppercase;
        margin-bottom: .8rem;
    }

    .hero-title {
        margin: 0;
        font-size: clamp(2rem, 4vw, 3.35rem);
        line-height: 1.03;
        letter-spacing: -0.045em;
        font-weight: 850;
        color: #0f172a;
    }

    .hero-title .grad {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
    }

    .hero-sub {
        margin-top: .8rem;
        margin-bottom: 0;
        max-width: 900px;
        font-size: 1rem;
        line-height: 1.72;
        color: var(--muted);
    }

    .hero-chips {
        display: flex;
        gap: .55rem;
        flex-wrap: wrap;
        margin-top: 1.05rem;
    }

    .chip {
        display: inline-flex;
        align-items: center;
        padding: .42rem .72rem;
        border-radius: 999px;
        border: 1px solid #e4e7ec;
        background: rgba(255,255,255,.86);
        color: #475467;
        font-size: .8rem;
        font-weight: 700;
    }

    .section-title {
        font-size: .78rem;
        font-weight: 850;
        color: #475467;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin: 0 0 .15rem 0;
    }

    div[data-testid="stRadio"] > div { gap: .5rem; }
    div[data-testid="stSelectbox"] > div > div { border-radius: .8rem; }

    div[data-testid="stMetric"] {
        border: 1px solid var(--line);
        border-radius: 1rem;
        background: rgba(255,255,255,.90);
        padding: .7rem .9rem;
        box-shadow: 0 7px 22px rgba(30,41,59,.045);
    }

    div[data-testid="stMetricLabel"] {
        color: #667085;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 820;
        letter-spacing: -0.02em;
    }

    .stage-head { margin-bottom: .7rem; }

    .stage-index {
        display: inline-flex;
        width: 1.7rem;
        height: 1.7rem;
        border-radius: .55rem;
        align-items: center;
        justify-content: center;
        background: var(--accent-soft);
        color: #4f46e5;
        font-weight: 850;
        font-size: .82rem;
        margin-right: .42rem;
    }

    .stage-title {
        font-size: 1.02rem;
        font-weight: 850;
        color: #111827;
    }

    .stage-sub {
        margin-top: .28rem;
        color: #667085;
        line-height: 1.5;
        font-size: .82rem;
    }

    [data-testid="stImage"] img {
        border-radius: 1rem;
        border: 1px solid var(--line);
        box-shadow: 0 10px 28px rgba(30,41,59,.08);
        object-fit: contain;
        background: #ffffff;
    }

    textarea {
        border-radius: .95rem !important;
        border-color: #e4e7ec !important;
        background: #fbfcff !important;
        color: #344054 !important;
        line-height: 1.65 !important;
        font-size: .9rem !important;
    }

    textarea:disabled {
        opacity: 1 !important;
        -webkit-text-fill-color: #344054 !important;
    }

    div[data-testid="stButton"] > button[kind="primary"] {
        border: 0 !important;
        border-radius: .9rem !important;
        min-height: 3.05rem;
        font-weight: 850;
        letter-spacing: -.01em;
        background: linear-gradient(90deg, #4f46e5, #6d4df4) !important;
        box-shadow: 0 10px 24px rgba(79,70,229,.22);
        transition: all .18s ease;
    }

    div[data-testid="stButton"] > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 13px 28px rgba(79,70,229,.28);
    }

    .missing-box {
        min-height: 340px;
        border: 1.5px dashed #c7ccd6;
        border-radius: 1rem;
        background: linear-gradient(135deg, rgba(248,250,252,.98), rgba(245,247,255,.98));
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #667085;
        font-size: .93rem;
        font-weight: 700;
        padding: 1.3rem;
    }

    .missing-icon {
        font-size: 2rem;
        margin-bottom: .45rem;
        filter: grayscale(.25);
    }

    .mini-badge {
        display: inline-block;
        margin-bottom: .55rem;
        padding: .28rem .5rem;
        border-radius: .55rem;
        background: #f2f4f7;
        color: #475467;
        font-size: .7rem;
        font-weight: 850;
        letter-spacing: .06em;
        text-transform: uppercase;
    }

    .generated-badge { background: #eef2ff; color: #4f46e5; }
    .truth-badge { background: #f2f4f7; color: #475467; }
    .input-badge { background: #ecfdf3; color: #067647; }

    .item-title-box {
        padding: .85rem .95rem;
        border-radius: .9rem;
        border: 1px solid #e4e7ec;
        background: #ffffff;
        color: #101828;
        font-weight: 760;
        line-height: 1.48;
        margin-bottom: .75rem;
    }

    .notice {
        padding: .75rem .85rem;
        border-radius: .85rem;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412;
        font-weight: 760;
        font-size: .84rem;
        margin: .65rem 0 .8rem 0;
    }

    .success-note {
        padding: .75rem .9rem;
        border-radius: .85rem;
        background: #ecfdf3;
        border: 1px solid #abefc6;
        color: #067647;
        font-weight: 760;
        font-size: .84rem;
        margin-top: .65rem;
    }

    .status-card {
        margin-top: 1.65rem;
        padding: .72rem .9rem;
        border-radius: .9rem;
        border: 1px solid #e4e7ec;
        background: rgba(255,255,255,.88);
        color: #667085;
        font-size: .82rem;
        font-weight: 700;
    }

    .footline {
        text-align: center;
        color: #98a2b3;
        font-size: .76rem;
        margin-top: 1.6rem;
        padding-top: 1rem;
        border-top: 1px solid #eaecf0;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: .8rem;
            padding-right: .8rem;
        }
        .hero {
            padding: 1.35rem 1.2rem;
            border-radius: 1.2rem;
        }
        .hero-title { font-size: 2rem; }
        .hero-sub { font-size: .9rem; }
        .missing-box { min-height: 220px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------
def normalize_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = "\n".join(str(v) for v in value if str(v).strip())
    return html.unescape(str(value)).strip()


def parse_object(text: str):
    text = text.strip()
    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        pass

    try:
        return ast.literal_eval(text)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_records(path_string: str):
    path = Path(path_string)

    if not path.is_file():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    if not text:
        return []

    try:
        loaded = json.loads(text)

        if isinstance(loaded, list):
            return [row for row in loaded if isinstance(row, dict)]

        if isinstance(loaded, dict):
            for key in ("items", "data", "records"):
                if isinstance(loaded.get(key), list):
                    return [row for row in loaded[key] if isinstance(row, dict)]
            return [loaded]

    except json.JSONDecodeError:
        pass

    records = []
    for line in text.splitlines():
        row = parse_object(line)
        if isinstance(row, dict):
            records.append(row)

    return records

@st.cache_data(show_spinner=False)
def load_selected_asins(path_string: str):
    path = Path(path_string)
    if not path.is_file():
        raise FileNotFoundError(f"선택 샘플 파일을 찾을 수 없습니다: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    selected = []
    seen = set()

    for value in data:
        asin = str(value).strip()
        if asin and asin not in seen:
            selected.append(asin)
            seen.add(asin)

    return selected


@st.cache_data(show_spinner=False)
def load_metadata_map(path_string: str):
    mapping = {}
    for row in load_records(path_string):
        asin = normalize_text(row.get("asin"))
        if asin:
            mapping[asin] = row
    return mapping


@st.cache_data(show_spinner=False)
def load_selected_metadata_map(path_string: str, selected_asins: tuple[str, ...]):
    """선택된 ASIN만 읽는다. JSONL은 한 줄씩 읽고 모두 찾으면 즉시 중단한다."""
    path = Path(path_string)
    if not path.is_file():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

    selected_set = set(selected_asins)
    if not selected_set:
        return {}

    mapping = {}

    # 대용량 JSONL은 전체 파일을 메모리에 올리지 않고 필요한 행만 찾는다.
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                row = parse_object(line)
                if not isinstance(row, dict):
                    continue

                asin = normalize_text(row.get("asin"))
                if asin in selected_set:
                    mapping[asin] = row
                    if len(mapping) == len(selected_set):
                        break

        return mapping

    # 일반 JSON은 기존 로더를 사용하되 선택된 ASIN만 보관한다.
    for row in load_records(path_string):
        asin = normalize_text(row.get("asin"))
        if asin in selected_set:
            mapping[asin] = row
            if len(mapping) == len(selected_set):
                break

    return mapping


@st.cache_data(show_spinner=False)
def load_image_candidates(
    missing_meta_path_string: str,
    raw_image_dir_string: str,
    generated_image_dir_string: str,
    selected_asins: tuple[str, ...],
):
    raw_image_dir = Path(raw_image_dir_string)
    generated_image_dir = Path(generated_image_dir_string)
    selected_map = load_selected_metadata_map(missing_meta_path_string, selected_asins)

    candidates = []
    stats = {
        "selected_rows": len(selected_asins),
        "found_metadata_rows": len(selected_map),
        "missing_raw_image": 0,
        "missing_generated_image": 0,
    }

    for asin in selected_asins:
        row = selected_map.get(asin)
        if row is None or normalize_text(row.get("imUrl")):
            continue

        raw_image_path = raw_image_dir / f"{asin}.jpg"
        generated_image_path = generated_image_dir / f"{asin}.jpg"

        if not raw_image_path.is_file():
            stats["missing_raw_image"] += 1
            continue

        if not generated_image_path.is_file():
            stats["missing_generated_image"] += 1
            continue

        candidates.append(
            {
                "asin": asin,
                "title": normalize_text(row.get("title")) or "(no title)",
                "description": normalize_text(row.get("description")) or "(no description)",
                "raw_image_path": str(raw_image_path),
                "generated_image_path": str(generated_image_path),
            }
        )

    return candidates, stats


def extract_generated_text_from_augmented(row):
    if "description_generated" not in row:
        return "", ""

    generated_text = normalize_text(row.get("description_generated"))
    if not generated_text:
        return "", ""

    return generated_text, "description_generated"


@st.cache_data(show_spinner=False)
def load_text_candidates(
    missing_meta_path_string: str,
    augmented_meta_path_string: str,
    original_meta_path_string: str,
    raw_image_dir_string: str,
    selected_asins: tuple[str, ...],
):
    raw_image_dir = Path(raw_image_dir_string)

    # 세 메타데이터 파일 모두 whitelist에 포함된 ASIN만 읽는다.
    missing_map = load_selected_metadata_map(missing_meta_path_string, selected_asins)
    augmented_map = load_selected_metadata_map(augmented_meta_path_string, selected_asins)
    original_map = load_selected_metadata_map(original_meta_path_string, selected_asins)

    candidates = []
    generated_field_counts = {}
    stats = {
        "selected_rows": len(selected_asins),
        "found_missing_rows": len(missing_map),
        "found_augmented_rows": len(augmented_map),
        "found_original_rows": len(original_map),
        "missing_raw_image": 0,
        "missing_augmented_item": 0,
        "missing_description_generated_key": 0,
        "missing_generated_text": 0,
        "missing_original_item": 0,
        "missing_original_text": 0,
        "generated_field_counts": generated_field_counts,
    }

    for asin in selected_asins:
        missing_row = missing_map.get(asin)
        if missing_row is None or normalize_text(missing_row.get("description")):
            continue

        raw_image_path = raw_image_dir / f"{asin}.jpg"
        augmented_row = augmented_map.get(asin)
        original_row = original_map.get(asin)

        if not raw_image_path.is_file():
            stats["missing_raw_image"] += 1
            continue

        if augmented_row is None:
            stats["missing_augmented_item"] += 1
            continue

        if "description_generated" not in augmented_row:
            stats["missing_description_generated_key"] += 1
            continue

        generated_text, generated_field = extract_generated_text_from_augmented(augmented_row)
        if not generated_text:
            stats["missing_generated_text"] += 1
            continue

        generated_field_counts[generated_field] = generated_field_counts.get(generated_field, 0) + 1

        if original_row is None:
            stats["missing_original_item"] += 1
            continue

        original_text = normalize_text(original_row.get("description"))
        if not original_text:
            stats["missing_original_text"] += 1
            continue

        candidates.append(
            {
                "asin": asin,
                "title": (
                    normalize_text(missing_row.get("title"))
                    or normalize_text(augmented_row.get("title"))
                    or normalize_text(original_row.get("title"))
                    or "(no title)"
                ),
                "raw_image_path": str(raw_image_path),
                "generated_text": generated_text,
                "generated_text_field": generated_field,
                "original_text": original_text,
            }
        )

    return candidates, stats


# ---------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------
def format_candidate(item) -> str:
    title = " ".join(item["title"].split())
    if len(title) > 72:
        title = title[:72] + "..."
    return f'{item["asin"]} · {title}'


def run_generation_effect(missing_modality: str) -> None:
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0)

    if missing_modality == "Image":
        steps = [
            "상품 텍스트를 분석하는 중...",
            "상품의 시각적 특징을 추론하는 중...",
            "누락된 이미지를 복원하는 중...",
            "생성 결과를 준비하는 중...",
        ]
    else:
        steps = [
            "상품 이미지를 분석하는 중...",
            "이미지의 의미적 특징을 추출하는 중...",
            "누락된 상품 설명을 복원하는 중...",
            "생성 결과를 준비하는 중...",
        ]

    for index, step in enumerate(steps, start=1):
        status_placeholder.info(f"{index}/{len(steps)} · {step}")
        progress_bar.progress(int(index / len(steps) * 100))
        time.sleep(0.45)

    progress_placeholder.empty()
    status_placeholder.success("복원이 완료되었습니다.")


def reveal_key(mode: str, asin: str) -> str:
    key = f"revealed_{mode}_{asin}"
    if key not in st.session_state:
        st.session_state[key] = False
    return key


def render_stage_header(index: str, badge: str, title: str, subtitle: str, badge_class: str = ""):
    st.markdown(
        f"""
        <div class="stage-head">
            <div class="mini-badge {badge_class}">{badge}</div>
            <div>
                <span class="stage-index">{index}</span>
                <span class="stage-title">{title}</span>
            </div>
            <div class="stage-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_image_missing(item) -> None:
    key = reveal_key("image", item["asin"])

    original_col, input_col, generated_col = st.columns([1.0, 1.18, 1.0], gap="large")

    with original_col:
        render_stage_header(
            "01",
            "비교용 원본",
            "원본 이미지",
            "복원 결과를 비교하기 위한 참고 정보이며, 모델 입력에는 사용되지 않습니다.",
            "truth-badge",
        )
        st.image(item["raw_image_path"], use_container_width=True)

    with input_col:
        render_stage_header(
            "02",
            "사용 가능한 정보",
            "상품 텍스트",
            "모델은 남아 있는 상품 제목과 설명만을 활용합니다.",
            "input-badge",
        )

        st.markdown(
            f'<div class="item-title-box">{html.escape(item["title"])}</div>',
            unsafe_allow_html=True,
        )

        st.text_area(
            "available_description",
            value=item["description"],
            height=285,
            disabled=True,
            label_visibility="collapsed",
            key=f'image_description_{item["asin"]}',
        )

        if st.button(
            "✦ 누락 이미지 복원하기",
            type="primary",
            use_container_width=True,
            key=f'generate_image_{item["asin"]}',
        ):
            run_generation_effect("Image")
            st.session_state[key] = True

    with generated_col:
        render_stage_header(
            "03",
            "AI 복원 결과",
            "생성 이미지",
            "남아 있는 텍스트 정보를 바탕으로 생성형 AI가 복원한 이미지입니다.",
            "generated-badge",
        )

        if st.session_state[key]:
            st.image(item["generated_image_path"], use_container_width=True)
            st.markdown(
                '<div class="success-note">✓ 누락된 이미지 정보가 복원되었습니다.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="missing-box">
                    <div>
                        <div class="missing-icon">◫</div>
                        <div>이미지 정보가 누락되어 있습니다</div>
                        <div style="font-weight:500;font-size:.80rem;margin-top:.4rem;color:#98a2b3">
                            가운데의 ‘누락 이미지 복원하기’ 버튼을 눌러주세요.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_text_missing(item) -> None:
    key = reveal_key("text", item["asin"])

    original_col, input_col, generated_col = st.columns([1.06, 0.9, 1.06], gap="large")

    with original_col:
        render_stage_header(
            "01",
            "비교용 원본",
            "원본 상품 설명",
            "복원 결과를 비교하기 위한 참고 정보이며, 모델 입력에는 사용되지 않습니다.",
            "truth-badge",
        )
        st.text_area(
            "original_text",
            value=item["original_text"],
            height=390,
            disabled=True,
            label_visibility="collapsed",
            key=f'original_text_{item["asin"]}',
        )

    with input_col:
        render_stage_header(
            "02",
            "사용 가능한 정보",
            "상품 이미지",
            "모델은 남아 있는 상품 이미지만을 활용합니다.",
            "input-badge",
        )

        st.image(item["raw_image_path"], use_container_width=True)

        st.markdown(
            f'<div class="item-title-box">{html.escape(item["title"])}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="notice">현재 상품 설명 정보가 누락된 상태입니다.</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "✦ 누락 상품 설명 복원하기",
            type="primary",
            use_container_width=True,
            key=f'generate_text_{item["asin"]}',
        ):
            run_generation_effect("Text")
            st.session_state[key] = True

    with generated_col:
        render_stage_header(
            "03",
            "AI 복원 결과",
            "생성 상품 설명",
            "남아 있는 이미지 정보를 바탕으로 생성형 AI가 복원한 텍스트입니다.",
            "generated-badge",
        )

        if st.session_state[key]:
            st.text_area(
                "generated_text",
                value=item["generated_text"],
                height=390,
                disabled=True,
                label_visibility="collapsed",
                key=f'generated_text_{item["asin"]}',
            )
            st.markdown(
                '<div class="success-note">✓ 누락된 텍스트 정보가 복원되었습니다.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="missing-box" style="min-height:390px">
                    <div>
                        <div class="missing-icon">≡</div>
                        <div>상품 설명 정보가 누락되어 있습니다</div>
                        <div style="font-weight:500;font-size:.80rem;margin-top:.4rem;color:#98a2b3">
                            가운데의 ‘누락 상품 설명 복원하기’ 버튼을 눌러주세요.
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main() -> None:
    ratio = "10"

    dataset = st.selectbox(
        "데이터셋 선택",
        list(DATASETS.keys()),
        format_func=lambda x: DATASETS[x],
        key="dataset_selector",
    )

    dataset_dir = DATA_ROOT / dataset
    raw_image_dir_default = dataset_dir / "raw_images"
    generated_image_dir_default = dataset_dir / "generated_images"
    meta_dir_default = dataset_dir / "meta-data"
    original_meta_default = dataset_dir / f"{dataset}.json"
    image_selected_path = dataset_dir / "image_final_selected.json"
    text_selected_path = dataset_dir / "text_final_selected.json"

    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-kicker">✦ 생성형 AI 기반 멀티모달 복원 데모</div>
            <h1 class="hero-title">
                누락된 상품 정보를 <span class="grad">생성형 AI로 복원</span>합니다
            </h1>
            <p class="hero-sub">
                상품 이미지 또는 상품 설명이 제공되지 않는 상황에서도,
                남아 있는 다른 형태의 정보를 활용해 누락된 멀티모달 정보를 복원합니다.<br>
                원본 정보는 결과 비교를 위해서만 표시되며 모델 입력에는 사용되지 않습니다.
            </p>
            <div class="hero-chips">
                <span class="chip">{DATASETS[dataset]}</span>
                <span class="chip">이미지 ↔ 텍스트 복원</span>
                <span class="chip">생성형 AI 활용</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">어떤 정보를 복원할지 선택해보세요</div>',
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "복원할 정보",
        ["Image", "Text"],
        horizontal=True,
        format_func=lambda x: "이미지 복원" if x == "Image" else "텍스트 복원",
        label_visibility="collapsed",
        key="restore_mode",
    )

    missing_meta_default = meta_dir_default / f"{dataset}-missed-{mode.lower()}-{ratio}.jsonl"
    augmented_text_default = meta_dir_default / f"{dataset}-augmented-text-{ratio}.jsonl"

    # 서버 경로 점검용 설정. 일반 관람자는 사용할 필요가 없다.
    with st.sidebar:
        st.markdown("### 개발자 설정")
        st.caption("데이터 경로를 점검할 때만 사용합니다.")

        with st.expander("데이터 경로", expanded=False):
            missing_meta_path = st.text_input(
                "Missing metadata",
                str(missing_meta_default),
                key=f"missing_meta_{dataset}_{mode}",
            )
            raw_image_dir = st.text_input(
                "Raw image directory",
                str(raw_image_dir_default),
                key=f"raw_images_{dataset}_{mode}",
            )

            if mode == "Image":
                generated_image_dir = st.text_input(
                    "Generated image directory",
                    str(generated_image_dir_default),
                    key=f"generated_images_{dataset}_{mode}",
                )
                augmented_text_path = str(augmented_text_default)
                original_meta_path = str(original_meta_default)
            else:
                augmented_text_path = st.text_input(
                    "Augmented text metadata",
                    str(augmented_text_default),
                    key=f"augmented_text_{dataset}_{mode}",
                )
                original_meta_path = st.text_input(
                    f"Original metadata ({dataset}.json)",
                    str(original_meta_default),
                    key=f"original_meta_{dataset}_{mode}",
                )
                generated_image_dir = str(generated_image_dir_default)

    try:
        selected_path = image_selected_path if mode == "Image" else text_selected_path
        selected_asins = tuple(load_selected_asins(str(selected_path)))

        if mode == "Image":
            candidates, stats = load_image_candidates(
                missing_meta_path,
                raw_image_dir,
                generated_image_dir,
                selected_asins,
            )
        else:
            candidates, stats = load_text_candidates(
                missing_meta_path,
                augmented_text_path,
                original_meta_path,
                raw_image_dir,
                selected_asins,
            )
    except Exception as error:
        st.error(str(error))
        st.stop()

    if not candidates:
        st.warning(
            f"{DATASETS[dataset]}에서 현재 데모에 표시할 수 있는 검수 완료 사례가 없습니다."
        )
        st.stop()

    search_query = st.text_input(
        "상품명 검색",
        "",
        placeholder="상품 제목의 일부를 입력하세요",
        key=f"search_{dataset}_{mode}",
    ).strip().lower()

    filtered_candidates = [
        item
        for item in candidates
        if not search_query or search_query in item["title"].lower()
    ]

    if not filtered_candidates:
        st.warning("검색한 상품명과 일치하는 복원 사례가 없습니다.")
        st.stop()

    selected_index = st.selectbox(
        "복원 사례 선택",
        range(len(filtered_candidates)),
        format_func=lambda index: format_candidate(filtered_candidates[index]),
        key=f"case_{dataset}_{mode}",
    )
    selected = filtered_candidates[selected_index]

    st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)

    if mode == "Image":
        render_image_missing(selected)
    else:
        render_text_missing(selected)

    st.markdown(
        """
        <div class="footline">
            본 데모는 안정적인 시연을 위해 사전에 생성된 복원 결과를 사용합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
# from __future__ import annotations

# import ast
# import html
# import json
# import time
# from pathlib import Path

# import streamlit as st


# # ---------------------------------------------------------------------
# # Server paths
# # ---------------------------------------------------------------------
# # 향후 Baby / Beauty / Toys_Games 등 데이터셋 선택 기능으로 확장할 예정.
# # 현재 시연에서는 Baby만 사용한다.
# BASE_DIR = Path(__file__).resolve().parent
# DATASET = "Baby"
# DEMO_DATA_DIR = BASE_DIR / "data" / DATASET

# DEFAULT_RAW_IMAGE_DIR = DEMO_DATA_DIR / "raw_images"
# DEFAULT_GENERATED_IMAGE_DIR = DEMO_DATA_DIR / "generated_images"
# DEFAULT_META_DIR = DEMO_DATA_DIR / "meta-data"
# DEFAULT_ORIGINAL_META_PATH = DEMO_DATA_DIR / f"{DATASET}.json"

# IMAGE_SELECTED_PATH = DEMO_DATA_DIR / "image_final_selected.json"
# TEXT_SELECTED_PATH = DEMO_DATA_DIR / "text_final_selected.json"

# # ---------------------------------------------------------------------
# # Page config + visual system
# # ---------------------------------------------------------------------
# st.set_page_config(
#     page_title="생성형 AI 기반 누락 모달리티 복원",
#     page_icon="✦",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# st.markdown(
#     """
#     <style>
#     :root {
#         --bg: #f7f8fc;
#         --text: #111827;
#         --muted: #667085;
#         --line: #e6e9f0;
#         --accent: #4f46e5;
#         --accent-soft: #eef2ff;
#         --shadow: 0 18px 50px rgba(30, 41, 59, 0.08);
#     }

#     html, body, [class*="css"] {
#         font-family: Inter, Pretendard, "Noto Sans KR", -apple-system, BlinkMacSystemFont,
#                      "Segoe UI", sans-serif;
#     }

#     .stApp {
#         background:
#             radial-gradient(circle at 15% 0%, rgba(99,102,241,0.10), transparent 28rem),
#             radial-gradient(circle at 90% 8%, rgba(124,58,237,0.08), transparent 24rem),
#             var(--bg);
#         color: var(--text);
#     }

#     .block-container {
#         padding-top: 1.25rem;
#         padding-bottom: 2.5rem;
#         max-width: 1480px;
#     }

#     header[data-testid="stHeader"] { background: transparent; }
#     #MainMenu, footer { visibility: hidden; }

#     section[data-testid="stSidebar"] {
#         background: #ffffff;
#         border-right: 1px solid var(--line);
#     }

#     .hero {
#         position: relative;
#         overflow: hidden;
#         padding: 2.1rem 2.2rem 1.9rem 2.2rem;
#         border: 1px solid rgba(99,102,241,0.13);
#         border-radius: 1.55rem;
#         background: linear-gradient(135deg, rgba(255,255,255,0.97), rgba(246,247,255,0.95));
#         box-shadow: var(--shadow);
#         margin-bottom: 1.1rem;
#     }

#     .hero:after {
#         content: "";
#         position: absolute;
#         width: 280px;
#         height: 280px;
#         right: -90px;
#         top: -120px;
#         border-radius: 50%;
#         background: linear-gradient(135deg, rgba(99,102,241,.18), rgba(124,58,237,.06));
#     }

#     .hero-kicker {
#         display: inline-flex;
#         align-items: center;
#         gap: .45rem;
#         padding: .34rem .68rem;
#         border-radius: 999px;
#         background: var(--accent-soft);
#         color: #4338ca;
#         font-size: .77rem;
#         font-weight: 800;
#         letter-spacing: .04em;
#         text-transform: uppercase;
#         margin-bottom: .8rem;
#     }

#     .hero-title {
#         margin: 0;
#         font-size: clamp(2rem, 4vw, 3.35rem);
#         line-height: 1.03;
#         letter-spacing: -0.045em;
#         font-weight: 850;
#         color: #0f172a;
#     }

#     .hero-title .grad {
#         background: linear-gradient(90deg, #4f46e5, #7c3aed);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         color: transparent;
#     }

#     .hero-sub {
#         margin-top: .8rem;
#         margin-bottom: 0;
#         max-width: 900px;
#         font-size: 1rem;
#         line-height: 1.72;
#         color: var(--muted);
#     }

#     .hero-chips {
#         display: flex;
#         gap: .55rem;
#         flex-wrap: wrap;
#         margin-top: 1.05rem;
#     }

#     .chip {
#         display: inline-flex;
#         align-items: center;
#         padding: .42rem .72rem;
#         border-radius: 999px;
#         border: 1px solid #e4e7ec;
#         background: rgba(255,255,255,.86);
#         color: #475467;
#         font-size: .8rem;
#         font-weight: 700;
#     }

#     .section-title {
#         font-size: .78rem;
#         font-weight: 850;
#         color: #475467;
#         text-transform: uppercase;
#         letter-spacing: .08em;
#         margin: 0 0 .15rem 0;
#     }

#     div[data-testid="stRadio"] > div { gap: .5rem; }
#     div[data-testid="stSelectbox"] > div > div { border-radius: .8rem; }

#     div[data-testid="stMetric"] {
#         border: 1px solid var(--line);
#         border-radius: 1rem;
#         background: rgba(255,255,255,.90);
#         padding: .7rem .9rem;
#         box-shadow: 0 7px 22px rgba(30,41,59,.045);
#     }

#     div[data-testid="stMetricLabel"] {
#         color: #667085;
#         font-weight: 700;
#     }

#     div[data-testid="stMetricValue"] {
#         color: #111827;
#         font-weight: 820;
#         letter-spacing: -0.02em;
#     }

#     .stage-head { margin-bottom: .7rem; }

#     .stage-index {
#         display: inline-flex;
#         width: 1.7rem;
#         height: 1.7rem;
#         border-radius: .55rem;
#         align-items: center;
#         justify-content: center;
#         background: var(--accent-soft);
#         color: #4f46e5;
#         font-weight: 850;
#         font-size: .82rem;
#         margin-right: .42rem;
#     }

#     .stage-title {
#         font-size: 1.02rem;
#         font-weight: 850;
#         color: #111827;
#     }

#     .stage-sub {
#         margin-top: .28rem;
#         color: #667085;
#         line-height: 1.5;
#         font-size: .82rem;
#     }

#     [data-testid="stImage"] img {
#         border-radius: 1rem;
#         border: 1px solid var(--line);
#         box-shadow: 0 10px 28px rgba(30,41,59,.08);
#         object-fit: contain;
#         background: #ffffff;
#     }

#     textarea {
#         border-radius: .95rem !important;
#         border-color: #e4e7ec !important;
#         background: #fbfcff !important;
#         color: #344054 !important;
#         line-height: 1.65 !important;
#         font-size: .9rem !important;
#     }

#     textarea:disabled {
#         opacity: 1 !important;
#         -webkit-text-fill-color: #344054 !important;
#     }

#     div[data-testid="stButton"] > button[kind="primary"] {
#         border: 0 !important;
#         border-radius: .9rem !important;
#         min-height: 3.05rem;
#         font-weight: 850;
#         letter-spacing: -.01em;
#         background: linear-gradient(90deg, #4f46e5, #6d4df4) !important;
#         box-shadow: 0 10px 24px rgba(79,70,229,.22);
#         transition: all .18s ease;
#     }

#     div[data-testid="stButton"] > button[kind="primary"]:hover {
#         transform: translateY(-1px);
#         box-shadow: 0 13px 28px rgba(79,70,229,.28);
#     }

#     .missing-box {
#         min-height: 340px;
#         border: 1.5px dashed #c7ccd6;
#         border-radius: 1rem;
#         background: linear-gradient(135deg, rgba(248,250,252,.98), rgba(245,247,255,.98));
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         text-align: center;
#         color: #667085;
#         font-size: .93rem;
#         font-weight: 700;
#         padding: 1.3rem;
#     }

#     .missing-icon {
#         font-size: 2rem;
#         margin-bottom: .45rem;
#         filter: grayscale(.25);
#     }

#     .mini-badge {
#         display: inline-block;
#         margin-bottom: .55rem;
#         padding: .28rem .5rem;
#         border-radius: .55rem;
#         background: #f2f4f7;
#         color: #475467;
#         font-size: .7rem;
#         font-weight: 850;
#         letter-spacing: .06em;
#         text-transform: uppercase;
#     }

#     .generated-badge { background: #eef2ff; color: #4f46e5; }
#     .truth-badge { background: #f2f4f7; color: #475467; }
#     .input-badge { background: #ecfdf3; color: #067647; }

#     .item-title-box {
#         padding: .85rem .95rem;
#         border-radius: .9rem;
#         border: 1px solid #e4e7ec;
#         background: #ffffff;
#         color: #101828;
#         font-weight: 760;
#         line-height: 1.48;
#         margin-bottom: .75rem;
#     }

#     .notice {
#         padding: .75rem .85rem;
#         border-radius: .85rem;
#         background: #fff7ed;
#         border: 1px solid #fed7aa;
#         color: #9a3412;
#         font-weight: 760;
#         font-size: .84rem;
#         margin: .65rem 0 .8rem 0;
#     }

#     .success-note {
#         padding: .75rem .9rem;
#         border-radius: .85rem;
#         background: #ecfdf3;
#         border: 1px solid #abefc6;
#         color: #067647;
#         font-weight: 760;
#         font-size: .84rem;
#         margin-top: .65rem;
#     }

#     .status-card {
#         margin-top: 1.65rem;
#         padding: .72rem .9rem;
#         border-radius: .9rem;
#         border: 1px solid #e4e7ec;
#         background: rgba(255,255,255,.88);
#         color: #667085;
#         font-size: .82rem;
#         font-weight: 700;
#     }

#     .footline {
#         text-align: center;
#         color: #98a2b3;
#         font-size: .76rem;
#         margin-top: 1.6rem;
#         padding-top: 1rem;
#         border-top: 1px solid #eaecf0;
#     }

#     @media (max-width: 900px) {
#         .block-container {
#             padding-left: .8rem;
#             padding-right: .8rem;
#         }
#         .hero {
#             padding: 1.35rem 1.2rem;
#             border-radius: 1.2rem;
#         }
#         .hero-title { font-size: 2rem; }
#         .hero-sub { font-size: .9rem; }
#         .missing-box { min-height: 220px; }
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ---------------------------------------------------------------------
# # Data loading helpers
# # ---------------------------------------------------------------------
# def normalize_text(value) -> str:
#     if value is None:
#         return ""
#     if isinstance(value, list):
#         value = "\n".join(str(v) for v in value if str(v).strip())
#     return html.unescape(str(value)).strip()


# def parse_object(text: str):
#     text = text.strip()
#     if not text:
#         return None

#     try:
#         return json.loads(text)
#     except Exception:
#         pass

#     try:
#         return ast.literal_eval(text)
#     except Exception:
#         return None


# @st.cache_data(show_spinner=False)
# def load_records(path_string: str):
#     path = Path(path_string)

#     if not path.is_file():
#         raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")

#     text = path.read_text(encoding="utf-8", errors="ignore").strip()
#     if not text:
#         return []

#     try:
#         loaded = json.loads(text)

#         if isinstance(loaded, list):
#             return [row for row in loaded if isinstance(row, dict)]

#         if isinstance(loaded, dict):
#             for key in ("items", "data", "records"):
#                 if isinstance(loaded.get(key), list):
#                     return [row for row in loaded[key] if isinstance(row, dict)]
#             return [loaded]

#     except json.JSONDecodeError:
#         pass

#     records = []
#     for line in text.splitlines():
#         row = parse_object(line)
#         if isinstance(row, dict):
#             records.append(row)

#     return records

# @st.cache_data(show_spinner=False)
# def load_selected_asins(path_string: str):
#     path = Path(path_string)
#     if not path.is_file():
#         raise FileNotFoundError(f"선택 샘플 파일을 찾을 수 없습니다: {path}")
#     data = json.loads(path.read_text(encoding="utf-8"))
#     return set(str(x).strip() for x in data if str(x).strip())

# @st.cache_data(show_spinner=False)
# def load_metadata_map(path_string: str):
#     mapping = {}
#     for row in load_records(path_string):
#         asin = normalize_text(row.get("asin"))
#         if asin:
#             mapping[asin] = row
#     return mapping


# @st.cache_data(show_spinner=False)
# def load_image_candidates(
#     missing_meta_path_string: str,
#     raw_image_dir_string: str,
#     generated_image_dir_string: str,
# ):
#     raw_image_dir = Path(raw_image_dir_string)
#     generated_image_dir = Path(generated_image_dir_string)

#     candidates = []
#     stats = {
#         "metadata_rows": 0,
#         "missing_rows": 0,
#         "missing_raw_image": 0,
#         "missing_generated_image": 0,
#     }

#     for row in load_records(missing_meta_path_string):
#         stats["metadata_rows"] += 1

#         if normalize_text(row.get("imUrl")):
#             continue

#         stats["missing_rows"] += 1
#         asin = normalize_text(row.get("asin"))
#         if not asin:
#             continue

#         raw_image_path = raw_image_dir / f"{asin}.jpg"
#         generated_image_path = generated_image_dir / f"{asin}.jpg"

#         if not raw_image_path.is_file():
#             stats["missing_raw_image"] += 1
#             continue

#         if not generated_image_path.is_file():
#             stats["missing_generated_image"] += 1
#             continue

#         candidates.append(
#             {
#                 "asin": asin,
#                 "title": normalize_text(row.get("title")) or "(no title)",
#                 "description": normalize_text(row.get("description")) or "(no description)",
#                 "raw_image_path": str(raw_image_path),
#                 "generated_image_path": str(generated_image_path),
#             }
#         )

#     candidates.sort(key=lambda item: item["asin"])
#     return candidates, stats


# def extract_generated_text_from_augmented(row):
#     if "description_generated" not in row:
#         return "", ""

#     generated_text = normalize_text(row.get("description_generated"))
#     if not generated_text:
#         return "", ""

#     return generated_text, "description_generated"


# @st.cache_data(show_spinner=False)
# def load_text_candidates(
#     missing_meta_path_string: str,
#     augmented_meta_path_string: str,
#     original_meta_path_string: str,
#     raw_image_dir_string: str,
# ):
#     raw_image_dir = Path(raw_image_dir_string)
#     augmented_map = load_metadata_map(augmented_meta_path_string)
#     original_map = load_metadata_map(original_meta_path_string)

#     candidates = []
#     generated_field_counts = {}
#     stats = {
#         "metadata_rows": 0,
#         "missing_rows": 0,
#         "missing_raw_image": 0,
#         "missing_augmented_item": 0,
#         "missing_description_generated_key": 0,
#         "missing_generated_text": 0,
#         "missing_original_item": 0,
#         "missing_original_text": 0,
#         "generated_field_counts": generated_field_counts,
#         "sample_augmented_keys": [],
#     }

#     for missing_row in load_records(missing_meta_path_string):
#         stats["metadata_rows"] += 1

#         if normalize_text(missing_row.get("description")):
#             continue

#         stats["missing_rows"] += 1
#         asin = normalize_text(missing_row.get("asin"))
#         if not asin:
#             continue

#         raw_image_path = raw_image_dir / f"{asin}.jpg"
#         augmented_row = augmented_map.get(asin)
#         original_row = original_map.get(asin)

#         if not raw_image_path.is_file():
#             stats["missing_raw_image"] += 1
#             continue

#         if augmented_row is None:
#             stats["missing_augmented_item"] += 1
#             continue

#         if not stats["sample_augmented_keys"]:
#             stats["sample_augmented_keys"] = list(augmented_row.keys())

#         if "description_generated" not in augmented_row:
#             stats["missing_description_generated_key"] += 1
#             continue

#         generated_text, generated_field = extract_generated_text_from_augmented(augmented_row)
#         if not generated_text:
#             stats["missing_generated_text"] += 1
#             continue

#         generated_field_counts[generated_field] = generated_field_counts.get(generated_field, 0) + 1

#         if original_row is None:
#             stats["missing_original_item"] += 1
#             continue

#         original_text = normalize_text(original_row.get("description"))
#         if not original_text:
#             stats["missing_original_text"] += 1
#             continue

#         candidates.append(
#             {
#                 "asin": asin,
#                 "title": (
#                     normalize_text(missing_row.get("title"))
#                     or normalize_text(augmented_row.get("title"))
#                     or normalize_text(original_row.get("title"))
#                     or "(no title)"
#                 ),
#                 "raw_image_path": str(raw_image_path),
#                 "generated_text": generated_text,
#                 "generated_text_field": generated_field,
#                 "original_text": original_text,
#             }
#         )

#     candidates.sort(key=lambda item: item["asin"])
#     return candidates, stats


# # ---------------------------------------------------------------------
# # UI helpers
# # ---------------------------------------------------------------------
# def format_candidate(item) -> str:
#     title = " ".join(item["title"].split())
#     if len(title) > 72:
#         title = title[:72] + "..."
#     return f'{item["asin"]} · {title}'


# def run_generation_effect(missing_modality: str) -> None:
#     status_placeholder = st.empty()
#     progress_placeholder = st.empty()
#     progress_bar = progress_placeholder.progress(0)

#     if missing_modality == "Image":
#         steps = [
#             "상품 텍스트를 분석하는 중...",
#             "상품의 시각적 특징을 추론하는 중...",
#             "누락된 이미지를 복원하는 중...",
#             "생성 결과를 준비하는 중...",
#         ]
#     else:
#         steps = [
#             "상품 이미지를 분석하는 중...",
#             "이미지의 의미적 특징을 추출하는 중...",
#             "누락된 상품 설명을 복원하는 중...",
#             "생성 결과를 준비하는 중...",
#         ]

#     for index, step in enumerate(steps, start=1):
#         status_placeholder.info(f"{index}/{len(steps)} · {step}")
#         progress_bar.progress(int(index / len(steps) * 100))
#         time.sleep(0.45)

#     progress_placeholder.empty()
#     status_placeholder.success("복원이 완료되었습니다.")


# def reveal_key(mode: str, asin: str) -> str:
#     key = f"revealed_{mode}_{asin}"
#     if key not in st.session_state:
#         st.session_state[key] = False
#     return key


# def render_stage_header(index: str, badge: str, title: str, subtitle: str, badge_class: str = ""):
#     st.markdown(
#         f"""
#         <div class="stage-head">
#             <div class="mini-badge {badge_class}">{badge}</div>
#             <div>
#                 <span class="stage-index">{index}</span>
#                 <span class="stage-title">{title}</span>
#             </div>
#             <div class="stage-sub">{subtitle}</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# def render_image_missing(item) -> None:
#     key = reveal_key("image", item["asin"])

#     original_col, input_col, generated_col = st.columns([1.0, 1.18, 1.0], gap="large")

#     with original_col:
#         render_stage_header(
#             "01",
#             "비교용 원본",
#             "원본 이미지",
#             "복원 결과를 비교하기 위한 참고 정보이며, 모델 입력에는 사용되지 않습니다.",
#             "truth-badge",
#         )
#         st.image(item["raw_image_path"], use_container_width=True)

#     with input_col:
#         render_stage_header(
#             "02",
#             "사용 가능한 정보",
#             "상품 텍스트",
#             "모델은 남아 있는 상품 제목과 설명만을 활용합니다.",
#             "input-badge",
#         )

#         st.markdown(
#             f'<div class="item-title-box">{html.escape(item["title"])}</div>',
#             unsafe_allow_html=True,
#         )

#         st.text_area(
#             "available_description",
#             value=item["description"],
#             height=285,
#             disabled=True,
#             label_visibility="collapsed",
#             key=f'image_description_{item["asin"]}',
#         )

#         if st.button(
#             "✦ 누락 이미지 복원하기",
#             type="primary",
#             use_container_width=True,
#             key=f'generate_image_{item["asin"]}',
#         ):
#             run_generation_effect("Image")
#             st.session_state[key] = True

#     with generated_col:
#         render_stage_header(
#             "03",
#             "AI 복원 결과",
#             "생성 이미지",
#             "남아 있는 텍스트 정보를 바탕으로 생성형 AI가 복원한 이미지입니다.",
#             "generated-badge",
#         )

#         if st.session_state[key]:
#             st.image(item["generated_image_path"], use_container_width=True)
#             st.markdown(
#                 '<div class="success-note">✓ 누락된 이미지 정보가 복원되었습니다.</div>',
#                 unsafe_allow_html=True,
#             )
#         else:
#             st.markdown(
#                 """
#                 <div class="missing-box">
#                     <div>
#                         <div class="missing-icon">◫</div>
#                         <div>이미지 정보가 누락되어 있습니다</div>
#                         <div style="font-weight:500;font-size:.80rem;margin-top:.4rem;color:#98a2b3">
#                             가운데의 ‘누락 이미지 복원하기’ 버튼을 눌러주세요.
#                         </div>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )


# def render_text_missing(item) -> None:
#     key = reveal_key("text", item["asin"])

#     original_col, input_col, generated_col = st.columns([1.06, 0.9, 1.06], gap="large")

#     with original_col:
#         render_stage_header(
#             "01",
#             "비교용 원본",
#             "원본 상품 설명",
#             "복원 결과를 비교하기 위한 참고 정보이며, 모델 입력에는 사용되지 않습니다.",
#             "truth-badge",
#         )
#         st.text_area(
#             "original_text",
#             value=item["original_text"],
#             height=390,
#             disabled=True,
#             label_visibility="collapsed",
#             key=f'original_text_{item["asin"]}',
#         )

#     with input_col:
#         render_stage_header(
#             "02",
#             "사용 가능한 정보",
#             "상품 이미지",
#             "모델은 남아 있는 상품 이미지만을 활용합니다.",
#             "input-badge",
#         )

#         st.image(item["raw_image_path"], use_container_width=True)

#         st.markdown(
#             f'<div class="item-title-box">{html.escape(item["title"])}</div>',
#             unsafe_allow_html=True,
#         )

#         st.markdown(
#             '<div class="notice">현재 상품 설명 정보가 누락된 상태입니다.</div>',
#             unsafe_allow_html=True,
#         )

#         if st.button(
#             "✦ 누락 상품 설명 복원하기",
#             type="primary",
#             use_container_width=True,
#             key=f'generate_text_{item["asin"]}',
#         ):
#             run_generation_effect("Text")
#             st.session_state[key] = True

#     with generated_col:
#         render_stage_header(
#             "03",
#             "AI 복원 결과",
#             "생성 상품 설명",
#             "남아 있는 이미지 정보를 바탕으로 생성형 AI가 복원한 텍스트입니다.",
#             "generated-badge",
#         )

#         if st.session_state[key]:
#             st.text_area(
#                 "generated_text",
#                 value=item["generated_text"],
#                 height=390,
#                 disabled=True,
#                 label_visibility="collapsed",
#                 key=f'generated_text_{item["asin"]}',
#             )
#             st.markdown(
#                 '<div class="success-note">✓ 누락된 텍스트 정보가 복원되었습니다.</div>',
#                 unsafe_allow_html=True,
#             )
#         else:
#             st.markdown(
#                 """
#                 <div class="missing-box" style="min-height:390px">
#                     <div>
#                         <div class="missing-icon">≡</div>
#                         <div>상품 설명 정보가 누락되어 있습니다</div>
#                         <div style="font-weight:500;font-size:.80rem;margin-top:.4rem;color:#98a2b3">
#                             가운데의 ‘누락 상품 설명 복원하기’ 버튼을 눌러주세요.
#                         </div>
#                     </div>
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )


# # ---------------------------------------------------------------------
# # Main
# # ---------------------------------------------------------------------
# def main() -> None:
#     st.markdown(
#         """
#         <section class="hero">
#             <div class="hero-kicker">✦ 생성형 AI 기반 멀티모달 복원 데모</div>
#             <h1 class="hero-title">
#                 누락된 상품 정보를 <span class="grad">생성형 AI로 복원</span>합니다
#             </h1>
#             <p class="hero-sub">
#                 상품 이미지 또는 상품 설명이 제공되지 않는 상황에서도,
#                 남아 있는 다른 형태의 정보를 활용해 누락된 멀티모달 정보를 복원합니다.<br>
#                 원본 정보는 결과 비교를 위해서만 표시되며 모델 입력에는 사용되지 않습니다.
#             </p>
#             <div class="hero-chips">
#                 <span class="chip">Amazon Baby Dataset</span>
#                 <span class="chip">이미지 ↔ 텍스트 복원</span>
#                 <span class="chip">생성형 AI 활용</span>
#             </div>
#         </section>
#         """,
#         unsafe_allow_html=True,
#     )

#     # 전시용 데모에서는 missing ratio를 사용자에게 노출하지 않는다.
#     # 현재는 기존 10% 파일을 내부 데이터 소스로 사용한다.
#     ratio = "10"

#     st.markdown(
#         '<div class="section-title">어떤 정보를 복원할지 선택해보세요</div>',
#         unsafe_allow_html=True,
#     )

#     mode = st.radio(
#         "복원할 정보",
#         ["Image", "Text"],
#         horizontal=True,
#         format_func=lambda x: "이미지 복원" if x == "Image" else "텍스트 복원",
#         label_visibility="collapsed",
#     )

#     missing_meta_default = DEFAULT_META_DIR / f"Baby-missed-{mode.lower()}-{ratio}.jsonl"
#     augmented_text_default = DEFAULT_META_DIR / f"Baby-augmented-text-{ratio}.jsonl"

#     # 서버 경로 점검용 설정. 일반 관람자는 사용할 필요가 없다.
#     with st.sidebar:
#         st.markdown("### 개발자 설정")
#         st.caption("데이터 경로를 점검할 때만 사용합니다.")

#         with st.expander("데이터 경로", expanded=False):
#             missing_meta_path = st.text_input("Missing metadata", str(missing_meta_default))
#             raw_image_dir = st.text_input("Raw image directory", str(DEFAULT_RAW_IMAGE_DIR))

#             if mode == "Image":
#                 generated_image_dir = st.text_input(
#                     "Generated image directory",
#                     str(DEFAULT_GENERATED_IMAGE_DIR),
#                 )
#                 augmented_text_path = str(augmented_text_default)
#                 original_meta_path = str(DEFAULT_ORIGINAL_META_PATH)
#             else:
#                 augmented_text_path = st.text_input(
#                     "Augmented text metadata",
#                     str(augmented_text_default),
#                 )
#                 original_meta_path = st.text_input(
#                     "Original metadata (Baby.json)",
#                     str(DEFAULT_ORIGINAL_META_PATH),
#                 )
#                 generated_image_dir = str(DEFAULT_GENERATED_IMAGE_DIR)

#     try:
#         if mode == "Image":
#             candidates, stats = load_image_candidates(
#                 missing_meta_path,
#                 raw_image_dir,
#                 generated_image_dir,
#             )
#         else:
#             candidates, stats = load_text_candidates(
#                 missing_meta_path,
#                 augmented_text_path,
#                 original_meta_path,
#                 raw_image_dir,
#             )
#     except Exception as error:
#         st.error(str(error))
#         st.stop()

#     selected_path = IMAGE_SELECTED_PATH if mode == "Image" else TEXT_SELECTED_PATH
#     selected_asins = load_selected_asins(str(selected_path))
#     candidates = [item for item in candidates if item["asin"] in selected_asins]

#     if not candidates:
#         st.warning(
#             "현재 데모에 표시할 수 있는 사례가 없습니다. "
#             "왼쪽 개발자 설정에서 데이터 경로를 확인해주세요."
#         )
#         st.stop()

#     search_query = st.text_input(
#         "상품명 검색",
#         "",
#         placeholder="상품 제목의 일부를 입력하세요",
#     ).strip().lower()

#     filtered_candidates = [
#         item
#         for item in candidates
#         if not search_query or search_query in item["title"].lower()
#     ]

#     if not filtered_candidates:
#         st.warning("검색한 상품명과 일치하는 복원 사례가 없습니다.")
#         st.stop()

#     selected_index = st.selectbox(
#         "복원 사례 선택",
#         range(len(filtered_candidates)),
#         format_func=lambda index: format_candidate(filtered_candidates[index]),
#     )
#     selected = filtered_candidates[selected_index]

#     st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)

#     if mode == "Image":
#         render_image_missing(selected)
#     else:
#         render_text_missing(selected)

#     st.markdown(
#         """
#         <div class="footline">
#             본 데모는 안정적인 시연을 위해 사전에 생성된 복원 결과를 사용합니다.
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# if __name__ == "__main__":
#     main()
