from __future__ import annotations
import html
import secrets
from pathlib import Path
import streamlit as st
from data.cases import CASE_01, ClinicalCase, MedicationRule
from data.id_quiz import ID_QUIZ_01, LEARNING_SEQUENCE, QUESTIONS_BY_ID, display_choices, display_questions, questions_for_stage
from scoring import score_case, xp_earned

st.set_page_config(page_title="PharmReview", page_icon="💊", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=Newsreader:opsz,wght@6..72,600&display=swap');
:root{--navy:#031f42;--teal:#0964e8;--mint:#edf4ff;--ink:#0c1930;--muted:#5f6c82;--line:#dbe3ee;--cream:#f8faff}
.stApp{background:var(--cream);color:var(--ink);font-family:'DM Sans',sans-serif}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#031f42,#062b55)}
[data-testid="stSidebar"] *{color:#eef9f7}
[data-testid="stSidebar"] .stButton button{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.15)}
h1,h2,h3{font-family:'Newsreader',serif;color:var(--navy)} .block-container{max-width:1280px;padding-top:1.8rem}
.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-weight:700;color:var(--teal);font-size:.72rem}
.patient-card,.clinical-card,.med-card,.result-card{background:#fff;border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 30px rgba(18,48,71,.06)}
.patient-card{padding:1rem 1.2rem;margin:.5rem 0 1rem;display:grid;grid-template-columns:1.35fr .9fr .8fr .95fr;align-items:center;gap:0}
.patient-identity{display:flex;align-items:center;gap:1rem;padding-right:1.1rem}.patient-avatar{position:static;text-align:center;color:#0964e8;font-size:.64rem;font-weight:700;flex:none}.avatar-icon{width:84px;height:84px;border-radius:50%;background:linear-gradient(145deg,#e8ebef,#cfd7df);border:4px solid white;box-shadow:0 4px 14px rgba(18,48,71,.14);display:grid;place-items:center;font-size:2.6rem;margin:auto}.patient-cell{min-height:82px;border-left:1px solid var(--line);padding:.45rem 1.05rem}.patient-cell-title{font-weight:800;font-size:.82rem;margin-bottom:.35rem}.patient-cell-title b{color:#0964e8;margin-right:.35rem}.patient-cell-copy{font-size:.8rem;line-height:1.5;color:var(--ink)}
.patient-name{font-family:'Newsreader',serif;font-size:2.1rem;font-weight:600;color:var(--navy)}
.patient-meta,.small-muted{color:var(--muted)}.clinical-card{padding:1rem 1.15rem;height:100%}
.metric-label{color:var(--muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}.metric-value{color:var(--navy);font-size:1.1rem;font-weight:700}
.visit-note{background:#f3f8f7;border-left:4px solid var(--teal);padding:.85rem 1rem;border-radius:4px 10px 10px 4px;color:#415864;margin:.35rem 0 1rem}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:.5rem 0 1rem}.chart-panel{background:white;border:1px solid var(--line);border-radius:14px;padding:1rem 1.15rem;box-shadow:0 5px 18px rgba(18,48,71,.04)}.chart-panel-title{display:flex;align-items:center;gap:.45rem;color:var(--navy);font-weight:800;font-size:.92rem;margin-bottom:.55rem;text-transform:uppercase;letter-spacing:.06em}.chart-row{display:flex;align-items:center;justify-content:space-between;border-top:1px solid #edf2f1;padding:.57rem 0}.chart-row:first-of-type{border-top:0}.chart-row span{color:var(--muted);font-size:.86rem}.chart-row strong{color:var(--navy);font-size:.96rem}.history-pills{display:flex;gap:.45rem;flex-wrap:wrap;margin:.4rem 0}.history-pill{background:#edf6f4;color:#176c65;border:1px solid #cee5df;border-radius:999px;padding:.33rem .65rem;font-size:.78rem;font-weight:700}
.chart-grid.compact{grid-template-columns:1fr}
.lab-list{background:#fff;border:1px solid var(--line);border-radius:12px;padding:.2rem .9rem}
.lab-list .chart-row{min-width:0;gap:1rem}
.lab-list .chart-row span{flex:0 0 auto;white-space:nowrap}
.lab-list .chart-row strong{min-width:0;text-align:right;white-space:nowrap;overflow-wrap:normal;word-break:normal}
@media(max-width:900px){.chart-grid{grid-template-columns:1fr}.patient-card{grid-template-columns:1fr}.patient-cell{border-left:0;border-top:1px solid var(--line);min-height:auto}}
.med-card{padding:1.35rem;border-top:0;margin-bottom:.75rem}.med-name{font-family:'DM Sans',sans-serif;color:var(--navy);font-size:1.35rem;font-weight:700}
.pill{display:inline-block;padding:.3rem .65rem;border-radius:999px;background:var(--mint);color:var(--teal);font-size:.75rem;font-weight:700;margin-right:.35rem}
.progress-label{display:flex;justify-content:space-between;color:var(--muted);font-size:.82rem}
.result-card{padding:1.15rem 1.3rem;margin:.8rem 0;border-left:5px solid #98a8ad}.result-correct{border-left-color:#079669}.result-partial{border-left-color:#d69022}.result-wrong{border-left-color:#c44848}
.pearl{background:#eff8f6;border-radius:10px;padding:.8rem 1rem;margin-top:.7rem}
.score-hero{background:linear-gradient(125deg,#123047,#087f73);color:#fff;padding:1.5rem;border-radius:18px}.score-hero h2{color:#fff;margin:0}.score-number{font-family:'Newsreader',serif;font-size:3rem;font-weight:600}
.case-banner{background:linear-gradient(120deg,#123047 0%,#164a59 62%,#087f73 100%);color:white;border-radius:18px;padding:1.4rem 1.6rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center}
.case-banner h2{color:white;margin:.15rem 0}.case-banner .signal{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:12px;padding:.75rem 1rem;font-size:.86rem}
.review-row{background:white;border:1px solid var(--line);border-radius:12px;padding:.85rem 1rem;margin:.45rem 0}
.decision-keep{color:#087f73}.decision-modify{color:#b36b00}.decision-remove{color:#b63838}
.action-guide{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0}.action-chip{border-radius:10px;padding:1rem .75rem;text-align:center;font-weight:800;font-size:.9rem;border:1px solid;background:#fff}.action-chip small{font-weight:500;color:#263a59}.keep-chip{color:#29a957;border-color:#53c873}.modify-chip{color:#bd7900;border-color:#ffb82f}.remove-chip{color:#df3e47;border-color:#ff6470}
[class*="st-key-keep_action_"] button,[class*="st-key-modify_action_"] button,[class*="st-key-remove_action_"] button{min-height:108px!important;background:#fff!important;font-size:.84rem!important;white-space:pre-line!important}
[class*="st-key-keep_action_"] button{border:1px solid #53c873!important;color:#269b4c!important}[class*="st-key-modify_action_"] button{border:1px solid #ffb82f!important;color:#b87800!important}[class*="st-key-remove_action_"] button{border:1px solid #ff6470!important;color:#db3944!important}
[class*="st-key-keep_action_"][class*="_selected"] button{background:#dff6e7!important;border:2px solid #35b75f!important;color:#147b36!important;box-shadow:0 0 0 3px rgba(53,183,95,.13)!important;transform:translateY(-2px)}
[class*="st-key-modify_action_"][class*="_selected"] button{background:#fff0cf!important;border:2px solid #f4a914!important;color:#9b6100!important;box-shadow:0 0 0 3px rgba(244,169,20,.14)!important;transform:translateY(-2px)}
[class*="st-key-remove_action_"][class*="_selected"] button{background:#ffe1e3!important;border:2px solid #ed4c58!important;color:#b9212c!important;box-shadow:0 0 0 3px rgba(237,76,88,.13)!important;transform:translateY(-2px)}
.med-progress{text-align:center;background:#fff;border:1px solid var(--line);border-radius:10px;padding:.8rem 1rem;margin-bottom:.9rem}.step-track{display:flex;align-items:center;justify-content:center;margin:.5rem auto 0;max-width:420px}.step{width:29px;height:29px;border-radius:50%;border:1px solid #b9c5d5;background:#fff;display:grid;place-items:center;font-size:.75rem;color:#31405b}.step.active{background:#0964e8;color:#fff;border-color:#0964e8}.step-line{height:3px;background:#d7deea;width:56px}
.med-summary{display:grid;grid-template-columns:1.15fr 1.15fr .85fr;align-items:center;gap:1rem;border-bottom:1px solid #e5ebf3;padding-bottom:1rem;margin-bottom:1rem}.drug-identity{display:flex;align-items:center;gap:.8rem}.drug-icon{width:52px;height:52px;border-radius:50%;display:grid;place-items:center;background:#52bf6d;color:#fff;font-size:1.45rem}.med-meta{border-left:1px solid var(--line);padding-left:1rem}.indication-tag{display:inline-block;background:#edf4ff;color:#075ee5;border-radius:7px;padding:.38rem .55rem;font-size:.78rem}.class-tag{background:#edf9f0;border-radius:9px;padding:.65rem;color:#24472f;font-size:.78rem}.workspace-head{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.7rem}.workspace-head h2{font-family:'DM Sans',sans-serif;font-size:1.25rem;margin:0}.workspace-head p{font-size:.82rem;color:var(--muted);margin:.25rem 0}
.decision-badge{display:inline-block;border-radius:999px;padding:.32rem .7rem;font-size:.78rem;font-weight:800}.badge-keep{background:#e6f6ef;color:#087a58}.badge-modify{background:#fff3dc;color:#a45d00}.badge-remove{background:#fdeaea;color:#b63838}
.case-top{display:flex;justify-content:space-between;align-items:center;margin:0 0 1rem;padding:.65rem .15rem;font-weight:800;font-size:1.02rem;min-height:42px}.case-top-left{display:flex;align-items:center;gap:.1rem}.beginner-badge{background:#dff5e5;color:#178342;border-radius:999px;padding:.3rem .7rem;font-size:.75rem;margin-left:.5rem}
.overview-grid{display:grid;grid-template-columns:1fr 1fr 1.18fr;gap:1rem}.overview-stack{display:grid;gap:1rem}.overview-box{background:#fff;border:1px solid var(--line);border-radius:10px;padding:1rem 1.1rem}.box-title{font-weight:800;font-size:.88rem;margin-bottom:.55rem}.med-list-row{display:grid;grid-template-columns:32px 1fr auto;align-items:center;gap:.55rem;border-top:1px solid #e9edf3;padding:.55rem 0}.med-list-row:first-of-type{border-top:0}.med-dot{width:28px;height:28px;border-radius:50%;display:grid;place-items:center;color:#fff;background:#5ebf77}.med-list-row small{color:var(--muted)}.task-band{display:grid;grid-template-columns:1.6fr .8fr;align-items:center;gap:1rem;background:#edf4ff;border-radius:12px;padding:1.15rem 1.35rem;margin-top:1rem}.task-band h3{font-family:'DM Sans',sans-serif;color:#0959ce;margin:0 0 .25rem}
.result-layout{display:grid;grid-template-columns:2.1fr .95fr;gap:1rem}.result-main,.patient-summary{background:#fff;border:1px solid var(--line);border-radius:10px;padding:1rem}.result-head{display:flex;justify-content:space-between;align-items:center}.result-score{display:flex;align-items:center;gap:1.5rem;background:#f3faf5;border:1px solid #d8eadc;border-radius:9px;padding:.65rem 1rem}.result-score strong{font-size:2rem;color:#168a4a}.result-stats{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:9px;margin:.8rem 0}.result-stat{padding:.65rem .8rem;border-left:1px solid var(--line);font-size:.76rem}.result-stat:first-child{border-left:0}.result-stat b{display:block;font-size:1rem;margin-top:.2rem}.decision-table{border:1px solid var(--line);border-radius:9px;overflow:hidden}.decision-row{display:grid;grid-template-columns:1.35fr 1fr 1fr .75fr;align-items:center;gap:.5rem;padding:.62rem .8rem;border-top:1px solid var(--line);font-size:.8rem}.decision-row:first-child{border-top:0;background:#f8faff;font-size:.68rem;font-weight:800}.decision-name{font-weight:700}.decision-name small{display:block;color:var(--muted);font-weight:400}.feedback-grid{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-top:.6rem}.feedback-cell{padding:.8rem;border-left:1px solid var(--line);font-size:.76rem;line-height:1.45}.feedback-cell:first-child{border-left:0}.feedback-cell b{display:block;color:#0959ce;margin-bottom:.35rem}.correct-tag{background:#e8f7ee;color:#087b3c;border:1px solid #bce0ca;border-radius:6px;padding:.25rem .55rem;font-weight:700}.partial-tag{background:#fff2dc;color:#a25e00;border:1px solid #efd09a;border-radius:6px;padding:.25rem .55rem;font-weight:700}.wrong-tag{background:#fdeaea;color:#c82f38;border:1px solid #efb9bd;border-radius:6px;padding:.25rem .55rem;font-weight:700}
@media(max-width:1000px){.overview-grid,.result-layout{grid-template-columns:1fr}.task-band{grid-template-columns:1fr}.result-stats{grid-template-columns:1fr 1fr}.feedback-grid{grid-template-columns:1fr}}
.score-strip{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.75rem;margin-top:1rem}.score-stat{background:rgba(255,255,255,.1);border-radius:10px;padding:.65rem .8rem}.score-stat small{display:block;opacity:.72}.score-stat b{font-size:1.1rem}
.battle-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem}.battle-top h1{font-family:'DM Sans',sans-serif;font-size:1.65rem;margin:0}.learning-badge{display:inline-block;background:#e5f7e9;color:#167c3c;border:1px solid #9bd6aa;border-radius:8px;padding:.3rem .65rem;font-size:.72rem;font-weight:800;margin-left:.55rem}.battle-progress{background:#f2f7ff;border:1px solid #ccdaed;border-radius:10px;padding:.7rem 1rem;margin-bottom:1rem}.battle-progress-label{display:flex;justify-content:space-between;font-size:.82rem;margin-bottom:.45rem}.battle-progress-track{height:8px;background:#d8dee8;border-radius:99px;overflow:hidden}.battle-progress-fill{height:100%;background:#1262d6;border-radius:99px}.battle-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:1.15rem;box-shadow:0 6px 24px rgba(18,48,71,.05)}.enemy-panel{height:100%;display:flex;flex-direction:column;justify-content:center;border-right:1px solid var(--line);padding:1rem 1.25rem 1rem .4rem}.enemy-art{width:150px;height:150px;margin:0 auto 1rem;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle,#dff8f5,#eaf3ff 62%,#fff 63%);font-size:5.5rem;filter:drop-shadow(0 8px 14px rgba(9,100,232,.14))}.enemy-health-label{display:flex;justify-content:space-between;font-size:.75rem;font-weight:800;margin-bottom:.35rem}.enemy-health{height:10px;background:#dce2eb;border-radius:99px;overflow:hidden}.enemy-health>div{height:100%;background:linear-gradient(90deg,#22a65a,#58c77c);border-radius:99px}.battle-question{font-family:'DM Sans',sans-serif;font-size:1.3rem;font-weight:800;line-height:1.35;color:var(--navy);margin:.3rem 0 .7rem}.clue-row{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:.85rem}.clue{background:#edf4ff;color:#075cce;border:1px solid #d6e3f8;border-radius:7px;padding:.3rem .55rem;font-size:.74rem;font-weight:700}
[class*="st-key-enemy_panel_"]{border-right:1px solid var(--line);padding:1rem 1.25rem 1rem .4rem}[class*="st-key-enemy_panel_"] [data-testid="stImage"]{display:flex;justify-content:center}[class*="st-key-enemy_panel_"] img{border-radius:50%;box-shadow:0 8px 22px rgba(9,100,232,.12)}
[class*="st-key-id_choice_"] button{min-height:78px!important;justify-content:flex-start!important;text-align:left!important;padding:.75rem 1rem!important;background:#fff!important;border:1.5px solid #80aaf0!important;color:var(--navy)!important;font-size:.9rem!important}
[class*="st-key-id_choice_"][class*="_correct"] button{background:#e8f8ed!important;border:2px solid #299d4c!important;color:#126d32!important;opacity:1!important}
[class*="st-key-id_choice_"][class*="_wrong"] button{background:#fdebec!important;border:2px solid #df4c56!important;color:#aa2530!important;opacity:1!important}
[class*="st-key-id_choice_"][class*="_dim"] button{background:#f7f9fc!important;border-color:#d9e1ec!important;color:#778195!important;opacity:.78!important}
.battle-feedback{border-radius:12px;padding:1rem 1.15rem;margin-top:1rem}.battle-feedback.correct{background:#eaf8ee;border:1px solid #69bd7d}.battle-feedback.wrong{background:#fff2f2;border:1px solid #e99da3}.battle-feedback-title{font-weight:900;font-size:.9rem;margin-bottom:.3rem}.battle-feedback-copy{font-size:.78rem;line-height:1.45}.battle-feedback-grid{display:grid;grid-template-columns:1.35fr 1fr;gap:1.25rem;border-top:1px solid rgba(30,80,50,.15);margin-top:.7rem;padding-top:.7rem}.battle-feedback-section b{display:block;font-size:.7rem;letter-spacing:.04em;margin-bottom:.3rem}.battle-feedback-option{font-size:.74rem;line-height:1.4;margin:.3rem 0}.battle-feedback-option b{display:inline!important;margin:0 .2rem 0 0!important}.battle-feedback-source{color:#5f6c82;font-size:.66rem;line-height:1.35;margin-top:.65rem}.battle-footer{display:flex;align-items:center;justify-content:space-between;gap:1rem;margin-top:1rem}.battle-stats{display:flex;align-items:center;gap:1rem;font-weight:800}.xp-chip{background:#fff1d8;color:#ac6700;border:1px solid #efbd62;border-radius:8px;padding:.45rem .7rem}.quiz-complete{background:linear-gradient(125deg,#062c59,#0964e8);color:white;border-radius:16px;padding:2rem;text-align:center}.quiz-complete h1{color:white}.quiz-score{font-size:3rem;font-weight:800}
@media(max-width:800px){.enemy-panel{border-right:0;border-bottom:1px solid var(--line)}.battle-feedback-grid{grid-template-columns:1fr}.battle-footer{align-items:stretch;flex-direction:column}}
div.stButton>button{border-radius:10px;font-weight:700;min-height:46px}div.stButton>button[kind="primary"]{background:var(--teal);border-color:var(--teal)}
[data-testid="stProgressBar"]>div>div{background-color:#4ed2b6}
</style>""", unsafe_allow_html=True)

def init_state():
    defaults = {"app_mode":"case", "screen":"overview", "med_index":0, "answers":{}, "submitted":False,
                "id_index":0, "id_answers":{}, "id_selected":None, "id_revealed":False,
                "id_streak":0, "id_best_streak":0, "id_xp":0}
    for key, value in defaults.items():
        if key not in st.session_state: st.session_state[key] = value
    # One seed keeps both question and choice shuffles stable during an attempt.
    if "id_choice_seed" not in st.session_state:
        st.session_state.id_choice_seed = secrets.randbits(64)

def reset():
    for key in ("screen","med_index","answers","submitted"): st.session_state.pop(key, None)
    st.rerun()

def reset_id_quiz():
    for key in ("id_index", "id_answers", "id_selected", "id_revealed", "id_streak", "id_best_streak", "id_xp"):
        st.session_state.pop(key, None)
    st.session_state.id_choice_seed = secrets.randbits(64)
    st.session_state.app_mode = "id"
    st.rerun()

def sidebar(case: ClinicalCase):
    with st.sidebar:
        st.markdown("## ⚕ PharmReview")
        st.caption("Clinical Decisions. Better Outcomes.")
        st.divider()
        if st.button("Dashboard", icon=":material/home:", width="stretch"):
            st.session_state.app_mode = "case"; st.rerun()
        st.markdown(":material/inventory_2: Case Library")
        if st.button("ID Quiz Prep", icon=":material/biotech:", width="stretch"):
            st.session_state.app_mode = "id"; st.rerun()
        st.markdown(":material/trending_up: My Progress")
        st.markdown(":material/bookmark: Saved Topics")
        st.markdown(":material/menu_book: References")
        st.markdown(":material/settings: Settings")
        st.divider()
        st.caption("CURRENT LEVEL")
        st.markdown("**Student Pharmacist**")
        earned = st.session_state.id_xp if st.session_state.app_mode == "id" else (xp_earned(case, st.session_state.answers) if st.session_state.submitted else 0)
        st.caption("XP to next level")
        st.progress(min((650+earned) / 1000, 1.0)); st.caption(f"{650+earned} / 1000 XP")
        if st.session_state.app_mode == "id":
            if st.button("Restart ID quiz", icon=":material/restart_alt:", width="stretch"): reset_id_quiz()
        elif st.button("Reset case", icon=":material/restart_alt:", width="stretch"): reset()

def patient_header(case: ClinicalCase):
    p = case.patient
    st.markdown(f"""<div class="patient-card">
    <div class="patient-identity"><div class="patient-avatar"><div class="avatar-icon">👨🏽‍🦳</div></div><div><div class="patient-name">{p['name']}</div><div>{p['age']} · {p['sex']}</div><div style="color:#0964e8;font-weight:700;margin-top:.35rem">{p['reason']}</div></div></div>
    <div class="patient-cell"><div class="patient-cell-title"><b>▣</b> Today's Visit</div><div class="patient-cell-copy">Routine follow-up. Patient reports doing well overall. No new complaints.</div></div>
    <div class="patient-cell"><div class="patient-cell-title"><b>▤</b> Allergies</div><div class="patient-cell-copy">No known drug allergies</div></div>
    <div class="patient-cell"><div class="patient-cell-title"><b>♢</b> Risk Factors</div><div class="patient-cell-copy">Age, HTN, T2DM, Hyperlipidemia</div></div>
    </div>""", unsafe_allow_html=True)

def case_top():
    st.markdown('<div class="case-top"><div class="case-top-left">CASE 01 <span class="beginner-badge">BEGINNER</span></div><div>ⓘ How to Play &nbsp; ☼</div></div>', unsafe_allow_html=True)

def metric_grid(values):
    for col, (label, value) in zip(st.columns(len(values)), values.items()):
        col.markdown(f'<div class="clinical-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

def chart_rows(values):
    return "".join(f'<div class="chart-row"><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>' for label, value in values.items())

def chart(case: ClinicalCase, compact: bool = False):
    tabs = st.tabs(["Summary","Labs","Conditions","Medications","Notes"])
    with tabs[0]:
        st.markdown("#### Today’s visit")
        st.markdown('<div class="visit-note">Routine medication review. James reports good adherence, no new complaints, and no medication-related adverse effects.</div>', unsafe_allow_html=True)
        grid_class="chart-grid compact" if compact else "chart-grid"
        st.markdown(f'''<div class="{grid_class}">
        <div class="chart-panel"><div class="chart-panel-title">◉ Vitals</div>{chart_rows(case.vitals)}</div>
        <div class="chart-panel"><div class="chart-panel-title">▦ Key labs</div>{chart_rows(case.labs)}</div>
        </div>''', unsafe_allow_html=True)
        st.markdown("#### Medical history")
        st.markdown('<div class="history-pills">'+"".join(f'<span class="history-pill">{html.escape(item)}</span>' for item in case.conditions)+'</div>', unsafe_allow_html=True)
        st.markdown("#### Risk factors")
        st.caption(" · ".join(case.risk_factors))
    with tabs[1]:
        if compact:
            st.markdown(f'<div class="lab-list">{chart_rows(case.labs)}</div>', unsafe_allow_html=True)
        else:
            metric_grid(case.labs)
    with tabs[2]:
        for item in case.conditions: st.markdown(f"- {item}")
    with tabs[3]:
        for med in case.medications: st.markdown(f"**{med.name}**  \n{med.dose} · {med.indication}")
    with tabs[4]:
        for note in case.notes: st.markdown(f"- {note}")

def overview(case):
    case_top()
    patient_header(case)
    tabs=st.tabs(["⌂  OVERVIEW","⚗  LABS","♡  CONDITIONS","◒  MEDICATIONS","▤  NOTES"])
    with tabs[0]:
        med_rows="".join(f'<div class="med-list-row"><div class="med-dot">◐</div><div>{med.name}</div><small>{med.dose}</small></div>' for med in case.medications)
        st.markdown(f'''<div class="overview-grid">
        <div class="overview-stack"><div class="overview-box"><div class="box-title">♡ &nbsp; VITAL SIGNS</div>{chart_rows(case.vitals)}</div>
        <div class="overview-box"><div class="box-title">▤ &nbsp; MEDICAL HISTORY</div><div class="history-pills">{"".join(f'<span class="history-pill">{item}</span>' for item in case.conditions)}</div></div></div>
        <div class="overview-stack"><div class="overview-box"><div class="box-title">⚗ &nbsp; KEY LABS</div>{chart_rows(case.labs)}</div>
        <div class="overview-box"><div class="box-title">♙ &nbsp; SOCIAL HISTORY</div>{chart_rows({"Tobacco":"Never smoker","Alcohol":"Occasional","Exercise":"Walks ~20 min, 3x/week","Diet":"Trying to reduce carbs"})}</div></div>
        <div class="overview-box"><div class="box-title">CURRENT MEDICATIONS (5)</div>{med_rows}</div></div>''', unsafe_allow_html=True)
    with tabs[1]: metric_grid(case.labs)
    with tabs[2]:
        for item in case.conditions: st.markdown(f"- {item}")
    with tabs[3]:
        for med in case.medications: st.markdown(f"**{med.name}** — {med.dose}")
    with tabs[4]:
        for note in case.notes: st.markdown(f"- {note}")
    st.markdown('<div class="task-band"><div><h3>▣ &nbsp; Your Task</h3><div>Review the patient’s information in each tab above. Then evaluate each medication for appropriateness.</div></div><div>Patient information remains available throughout the review.</div></div>', unsafe_allow_html=True)
    if st.button("Begin medication review", icon=":material/arrow_forward:", type="primary", width="stretch"):
        st.session_state.screen="review"; st.session_state.med_index=0; st.rerun()

def save_choice(med: MedicationRule, decision):
    old = st.session_state.answers.get(med.id, {})
    st.session_state.answers[med.id] = {"decision":decision,"modification":old.get("modification") if decision == "MODIFY" else None}

def review(case):
    index = st.session_state.med_index; med = case.medications[index]
    case_top()
    patient_header(case)
    left, right = st.columns([2.1,.95], gap="small")
    with left:
        st.markdown('<div class="workspace-head"><div><h2>MEDICATION REVIEW</h2><p>Review each medication and determine whether intervention is necessary.</p></div><div class="indication-tag">▣ View Patient Chart</div></div>', unsafe_allow_html=True)
        steps=""
        for number in range(1,len(case.medications)+1):
            if number>1: steps+='<div class="step-line"></div>'
            steps+=f'<div class="step {"active" if number==index+1 else ""}">{number}</div>'
        st.markdown(f'<div class="med-progress">Medication {index+1} of {len(case.medications)}<div class="step-track">{steps}</div></div>', unsafe_allow_html=True)
        med_class={"metformin":"Biguanide","atorvastatin":"HMG-CoA reductase inhibitor","amlodipine":"Calcium channel blocker","omeprazole":"Proton pump inhibitor","levothyroxine":"Thyroid hormone"}[med.id]
        st.markdown(f'''<div class="med-card"><div class="med-summary">
        <div class="drug-identity"><div class="drug-icon">◐</div><div><div class="med-name">{med.name}</div><div>{med.dose}</div></div></div>
        <div class="med-meta"><small>Indication on chart</small><br><span class="indication-tag">{html.escape(med.indication)}</span></div>
        <div class="class-tag"><small>Class</small><br>{med_class}</div></div>
        <b>What is your decision for this medication?</b></div>''', unsafe_allow_html=True)
        choice = st.session_state.answers.get(med.id, {}).get("decision")
        labels={"KEEP":"KEEP  \nContinue as prescribed","MODIFY":"MODIFY  \nChange dose, frequency, or medication","REMOVE":"REMOVE  \nDiscontinue medication"}
        icons={"KEEP":":material/check_circle:","MODIFY":":material/edit:","REMOVE":":material/cancel:"}
        for col, decision in zip(st.columns(3),("KEEP","MODIFY","REMOVE")):
            selected_suffix="_selected" if choice==decision else ""
            with col.container(key=f"{decision.lower()}_action_{med.id}{selected_suffix}"):
                if st.button(labels[decision], icon=icons[decision], key=f"{med.id}-{decision}", width="stretch"):
                    save_choice(med, decision); st.rerun()
        if choice == "MODIFY" and med.modification_options:
            existing = st.session_state.answers[med.id].get("modification")
            selected = st.selectbox("Select the specific modification", med.modification_options, index=med.modification_options.index(existing) if existing in med.modification_options else None, placeholder="Choose one…")
            st.session_state.answers[med.id]["modification"] = selected
        st.info("Consider the patient’s conditions, labs, risk factors, and all available information.", icon=":material/info:")
        back, onward = st.columns([1,2])
        if back.button("Back", icon=":material/arrow_back:", disabled=index == 0, width="stretch"):
            st.session_state.med_index -= 1; st.rerun()
        complete = choice is not None and (choice != "MODIFY" or not med.modification_options or st.session_state.answers[med.id].get("modification"))
        label = "Review decisions →" if index == len(case.medications)-1 else "Save & continue →"
        if onward.button(label, type="primary", disabled=not complete, width="stretch"):
            if index == len(case.medications)-1: st.session_state.screen = "confirm"
            else: st.session_state.med_index += 1
            st.rerun()
    with right:
        with st.container(border=True):
            chart(case, compact=True)

def confirm(case):
    case_top()
    st.markdown('<div class="eyebrow">Final check</div>', unsafe_allow_html=True)
    st.title("Review your decisions"); patient_header(case)
    for index, med in enumerate(case.medications):
        answer = st.session_state.answers.get(med.id,{})
        left, middle, right = st.columns([3,2,1], vertical_alignment="center"); left.markdown(f"**{med.name}**  \n{med.dose}")
        detail = answer.get("decision","Not answered") + (f" — {answer['modification']}" if answer.get("modification") else "")
        badge_class={"KEEP":"badge-keep","MODIFY":"badge-modify","REMOVE":"badge-remove"}.get(answer.get("decision"),"")
        middle.markdown(f'<span class="decision-badge {badge_class}">{html.escape(detail)}</span>', unsafe_allow_html=True)
        if right.button("Edit", key=f"edit-{med.id}", icon=":material/edit:", width="stretch"):
            st.session_state.med_index=index; st.session_state.screen="review"; st.rerun()
        st.divider()
    left,right=st.columns([1,2])
    if left.button("Return to review", icon=":material/arrow_back:", width="stretch"):
        st.session_state.med_index=len(case.medications)-1; st.session_state.screen="review"; st.rerun()
    if right.button("Submit medication review", icon=":material/task_alt:", type="primary", width="stretch"):
        st.session_state.submitted=True; st.session_state.screen="results"; st.rerun()

def results(case):
    score, details = score_case(case, st.session_state.answers); xp=xp_earned(case, st.session_state.answers)
    correct_count=sum(item.total==20 for item in details); by_id={item.medication_id:item for item in details}
    case_top()
    patient_header(case)
    main,side=st.columns([2.1,.95],gap="small")
    with main:
        st.markdown(f'''<div class="result-main"><div class="result-head"><div><b>MEDICATION REVIEW COMPLETE 🎉</b><br><small>Great work! You’ve completed the medication review.</small></div><div class="result-score"><span><b>{correct_count}</b> / 5 Correct</span><strong>{score}%</strong></div></div>
        <div class="result-stats"><div class="result-stat">You earned<b>+{xp} XP</b></div><div class="result-stat">Correct decisions<b>{correct_count}</b></div><div class="result-stat">Medication problems<b>{len(case.medications)-correct_count} identified</b></div><div class="result-stat">Case status<b>Complete</b></div></div></div>''', unsafe_allow_html=True)
        rows='<div class="decision-row"><div>MEDICATION</div><div>YOUR DECISION</div><div>RECOMMENDED</div><div>RESULT</div></div>'
        for med in case.medications:
            answer=st.session_state.answers[med.id]; points=by_id[med.id].total
            selected=answer["decision"]; recommended=med.accepted_decision
            css,label=("correct-tag","CORRECT") if points==20 else (("partial-tag","PARTIAL") if points else ("wrong-tag","INCORRECT"))
            rows+=f'<div class="decision-row"><div class="decision-name">{med.name}<small>{med.dose}</small></div><div class="badge-{selected.lower()}">● {selected}</div><div class="badge-{recommended.lower()}">● {recommended}</div><div><span class="{css}">{label}</span></div></div>'
        st.markdown(f'<div class="decision-table">{rows}</div>',unsafe_allow_html=True)
        st.markdown("#### Detailed feedback")
        for med in case.medications:
            points=by_id[med.id].total
            with st.expander(f'{"✓" if points==20 else "!"}  {med.name} · {points}/20'):
                st.markdown(f'''<div class="feedback-grid"><div class="feedback-cell"><b>WHY?</b>{html.escape(med.rationale)}</div><div class="feedback-cell"><b>CLINICAL PEARL</b>{html.escape(med.clinical_pearl)}</div><div class="feedback-cell"><b>EVIDENCE & GUIDELINES</b>{html.escape(med.reference.title)}<br><a href="{med.reference.url}" target="_blank">View full guideline ↗</a></div></div>''',unsafe_allow_html=True)
    with side:
        with st.container(border=True):
            st.markdown("**PATIENT SUMMARY**")
            chart(case,compact=True)
    if st.button("Restart Case 01", icon=":material/replay:", width="stretch"): reset()
    st.caption("Educational prototype only. It does not provide patient-specific medical advice or replace clinical judgment.")

def record_id_answer(question_id: str, choice_id: str):
    if st.session_state.id_revealed:
        return
    question = QUESTIONS_BY_ID[question_id]
    correct = choice_id == question.correct_choice_id
    st.session_state.id_answers[question_id] = choice_id
    st.session_state.id_selected = choice_id
    st.session_state.id_revealed = True
    if correct:
        st.session_state.id_streak += 1
        st.session_state.id_xp += 20
        st.session_state.id_best_streak = max(st.session_state.id_best_streak, st.session_state.id_streak)
    else:
        st.session_state.id_streak = 0

def advance_id_battle():
    st.session_state.id_index += 1
    st.session_state.id_selected = None
    st.session_state.id_revealed = False
    st.rerun()

def id_quiz_complete():
    question_order = display_questions(st.session_state.id_choice_seed)
    correct = sum(
        selected == QUESTIONS_BY_ID[question_id].correct_choice_id
        for question_id, selected in st.session_state.id_answers.items()
    )
    total = len(ID_QUIZ_01)
    score = round(correct / total * 100)
    st.markdown(f'''<div class="quiz-complete"><div class="eyebrow" style="color:#a9d4ff">MOST V · ID QUIZ PREP</div>
    <h1>Learning module complete</h1><div class="quiz-score">{correct} / {total}</div><p>{score}% correct · +{st.session_state.id_xp} XP</p>
    <p>Best memory streak: {st.session_state.id_best_streak}</p></div>''', unsafe_allow_html=True)
    missed = [q for q in question_order if st.session_state.id_answers.get(q.id) != q.correct_choice_id]
    if missed:
        st.markdown("### Concepts to revisit")
        for question in missed:
            st.markdown(f"- **{question.topic}:** {question.memory_hook}")
    else:
        st.success("Perfect run — every enemy was defeated.", icon=":material/trophy:")
    if st.button("Restart learning mode", icon=":material/replay:", type="primary", width="stretch"):
        reset_id_quiz()

ENEMY_ASSETS = tuple(Path(__file__).parent / "assets" / "enemies" / name for name in (
    "cocci-cluster.png", "cocci-chain.png", "bacillus.png", "spiral.png"
))


def enemy_asset_for(question):
    tags = set(question.tags)
    if "clusters" in tags:
        return ENEMY_ASSETS[0]
    if "chains" in tags:
        return ENEMY_ASSETS[1]
    if "rods" in tags or "gram-negative" in tags:
        return ENEMY_ASSETS[2]
    return ENEMY_ASSETS[sum(map(ord, question.id)) % len(ENEMY_ASSETS)]


def render_enemy(question, is_correct: bool):
    health = 60 if is_correct else 100
    enemy_label = "Enemy weakened" if is_correct else "Enemy health"
    with st.container(key=f"enemy_panel_{question.id}"):
        st.image(enemy_asset_for(question), width=180)
        st.markdown(f'''
    <div class="enemy-health-label"><span>{enemy_label.upper()}</span><span>{health}%</span></div>
    <div class="enemy-health"><div style="width:{health}%"></div></div>''', unsafe_allow_html=True)

def render_id_choices(question, ordered_choices, display_letters, revealed: bool, selected_id: str | None):
    for row_start in (0, 2):
        columns = st.columns(2)
        for column, choice in zip(columns, ordered_choices[row_start:row_start + 2]):
            status = "neutral"
            if revealed:
                if choice.id == question.correct_choice_id:
                    status = "correct"
                elif choice.id == selected_id:
                    status = "wrong"
                else:
                    status = "dim"
            with column.container(key=f"id_choice_{question.id}_{choice.id}_{status}"):
                icon = ":material/check_circle:" if status == "correct" else (":material/cancel:" if status == "wrong" else None)
                if st.button(f"{display_letters[choice.id]}.  {choice.text}", key=f"answer-{question.id}-{choice.id}", icon=icon, disabled=revealed, width="stretch"):
                    record_id_answer(question.id, choice.id)
                    st.rerun()

def render_id_feedback(question, ordered_choices, display_letters, selected_id: str, is_correct: bool):
    selected = next(choice for choice in question.choices if choice.id == selected_id)
    other_feedback = "".join(
        f'<div class="battle-feedback-option"><b style="display:inline">{display_letters[choice.id]}.</b> {html.escape(choice.feedback)}</div>'
        for choice in ordered_choices if choice.id not in (question.correct_choice_id, selected_id)
    )
    feedback_class = "correct" if is_correct else "wrong"
    feedback_title = "CORRECT — EFFECTIVE HIT!" if is_correct else "NOT QUITE — REVIEW THE CLUES"
    st.markdown(f'''<div class="battle-feedback {feedback_class}"><div class="battle-feedback-title">{feedback_title}</div>
    <div class="battle-feedback-copy">{html.escape(selected.feedback)}</div>
    <div class="battle-feedback-grid"><div class="battle-feedback-section"><b>WHY THE OPTIONS FIT OR MISS</b>{other_feedback}</div>
    <div class="battle-feedback-section"><b>MEMORY HOOK</b><div class="battle-feedback-copy">{html.escape(question.memory_hook)}</div>
    <div class="battle-feedback-source">Source: {html.escape(question.source_title)} · {html.escape(question.source_section)}</div></div></div></div>''', unsafe_allow_html=True)

def id_quiz():
    question_order = display_questions(st.session_state.id_choice_seed)
    if st.session_state.id_index >= len(question_order):
        id_quiz_complete()
        return

    question = question_order[st.session_state.id_index]
    stage = next(item for item in LEARNING_SEQUENCE if item.id == question.stage)
    stage_questions = questions_for_stage(question.stage)
    stage_position = next(index for index, item in enumerate(stage_questions, start=1) if item.id == question.id)
    global_position = st.session_state.id_index + 1
    stage_percent = round(stage_position / len(stage_questions) * 100)
    revealed = st.session_state.id_revealed
    selected_id = st.session_state.id_selected
    is_correct = revealed and selected_id == question.correct_choice_id
    ordered_choices = display_choices(question, st.session_state.id_choice_seed)
    display_letters = {choice.id: chr(65 + index) for index, choice in enumerate(ordered_choices)}

    st.markdown(f'''<div class="battle-top"><div><h1>ID QUIZ PREP <span class="learning-badge">LEARNING MODE</span></h1></div>
    <div><b>Question {global_position} of {len(ID_QUIZ_01)}</b> &nbsp; ⓘ How to Play</div></div>
    <div class="battle-progress"><div class="battle-progress-label"><b>{html.escape(stage.title)}</b><span>{stage_position} of {len(stage_questions)}</span></div>
    <div class="battle-progress-track"><div class="battle-progress-fill" style="width:{stage_percent}%"></div></div></div>''', unsafe_allow_html=True)

    with st.container(border=True):
        enemy, answers = st.columns([.72, 2], gap="medium", vertical_alignment="center")
        with enemy:
            render_enemy(question, is_correct)
        with answers:
            st.caption(f"{question.topic.upper()} · {question.difficulty.upper()}")
            st.markdown(f'<div class="battle-question">{html.escape(question.prompt)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="clue-row">' + "".join(f'<span class="clue">{html.escape(tag.replace("-", " ").title())}</span>' for tag in question.tags[:3]) + '</div>', unsafe_allow_html=True)
            render_id_choices(question, ordered_choices, display_letters, revealed, selected_id)

    if revealed:
        render_id_feedback(question, ordered_choices, display_letters, selected_id, is_correct)

    st.markdown(f'''<div class="battle-footer"><div class="battle-stats"><span>🔥 Streak {st.session_state.id_streak}</span>
    <span class="xp-chip">+{st.session_state.id_xp} XP</span></div><small>Learn the distinction, then continue to the next battle.</small></div>''', unsafe_allow_html=True)
    if st.button("Next battle", icon=":material/arrow_forward:", type="primary", disabled=not revealed, width="stretch"):
        advance_id_battle()

init_state(); sidebar(CASE_01)
if st.session_state.app_mode == "id":
    id_quiz()
else:
    {"overview":overview,"review":review,"confirm":confirm,"results":results}[st.session_state.screen](CASE_01)
