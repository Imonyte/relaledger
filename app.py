import streamlit as st
import pandas as pd
import json
import uuid
import random
import re
from datetime import datetime
from math import pi
import plotly.graph_objects as go

# ✅ Import from core/loop_model.py
from core.loop_model import create_loop, compute_voltage, compute_semantic_current

LEDGER_PATH = "ledger/ledger.json"

# -----------------------
# 📁 Load / Save Ledger
# -----------------------
def load_ledger():
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_ledger(data):
    with open(LEDGER_PATH, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------
# 🌀 Spiral Plot
# -----------------------
def plot_spiral(ledger):
    if not ledger:
        st.warning("No loops to display.")
        return

    df = pd.DataFrame(ledger)
    df['angle'] = df.index * 0.25
    df['radius'] = df['distance'].astype(float)

    fig = go.Figure(go.Scatterpolar(
        r=df['radius'],
        theta=df['angle'] * 180 / pi,
        mode='markers+lines',
        marker=dict(size=8, color=df['modulus'], colorscale='Viridis', showscale=True),
        text=df['id'],
        name='Spiral Loops'
    ))

    fig.update_layout(
        title="RELA Spiral Map",
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 🚀 Streamlit App
# -----------------------
def main():
    st.set_page_config(layout="wide")
    st.title("🔁 RELAnalytics — Recursive Loop Engine")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Spiral Dashboard",
        "🧬 Validate Loop",
        "🔌 Live Input & Chat",
        "🪙 Token Rewards"
    ])

    # 📊 Tab 1: Spiral Dashboard
    with tab1:
        ledger = load_ledger()
        st.header("📊 Spiral Visualization")
        plot_spiral(ledger)

        st.subheader("📜 Ledger Viewer")
        df = pd.DataFrame(ledger)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.sort_values("timestamp", ascending=False)
        st.dataframe(df, use_container_width=True)

    # 🧬 Tab 2: Validate Loop
    with tab2:
        st.header("🧬 Validate a New Loop")
        with st.form("loop_form"):
            label = st.selectbox("Loop Label (Phase Node)", [f"node_{i}" for i in range(1, 9)])
            distance = st.number_input("Distance", value=1000.0, step=10.0)
            parent_id = st.text_input("Optional: Parent Loop ID")
            submitted = st.form_submit_button("✅ Submit")

        if submitted:
            loop = create_loop(label, distance, parent_id)
            msg = f"✅ Loop `{loop['id']}` saved.\n\nEntangled Pair: {loop['entangled_pair']}\nScore: {loop['spiral_score']}"
            st.success(msg)

    # 🔌 Tab 3: Live Input & Chat
    with tab3:
        st.header("🔌 Simulate Input or Chat")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📡 Simulate Sensor Input"):
                distance = round(random.uniform(900, 1300), 2)
                loop = create_loop("node_1", distance)
                st.success(f"✅ Sensor input loop added at {distance} (Score: {loop['spiral_score']})")

        with col2:
            chat_msg = st.chat_input("Ask RELAnalytics...")
            if chat_msg:
                st.chat_message("user").markdown(chat_msg)
                match = re.match(r"add (\d+(?:\.\d+)?) to (node_\d)", chat_msg.lower())
                if match:
                    dist = float(match.group(1))
                    label = match.group(2)
                    loop = create_loop(label, dist)
                    st.chat_message("assistant").markdown(
                        f"✅ Added to **{label}** at {dist}\nScore: **{loop['spiral_score']}**"
                    )
                elif "last harmonic" in chat_msg:
                    ledger = load_ledger()
                    for loop in reversed(ledger):
                        if loop.get("spiral_score") == "🟢 Harmonic":
                            st.chat_message("assistant").markdown(
                                f"🌟 Last harmonic: `{loop['id']}` — {loop['distance']} units"
                            )
                            break
                    else:
                        st.chat_message("assistant").markdown("No harmonic loops found.")
                else:
                    st.chat_message("assistant").markdown("❓ Try: `Add 1234 to node_2` or `last harmonic`")

    # 🪙 Tab 4: Token Rewards
    with tab4:
        st.header("🪙 Harmonic Token Rewards")
        ledger = load_ledger()
        total_tokens = 0
        log = []
        for loop in ledger:
            score = loop.get("harmonic_score", 0)
            reward = 10 if score == 100 else 5 if score >= 70 else 0
            total_tokens += reward
            log.append({
                "id": loop["id"],
                "label": loop["label"],
                "harmonic_score": score,
                "reward_token": reward,
                "timestamp": loop["timestamp"]
            })

        st.metric("💰 RELA Tokens Earned", total_tokens)
        df = pd.DataFrame(log)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.sort_values("timestamp", ascending=False)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
