import streamlit as st
from PIL import Image
import requests
import PyPDF2
import docx
import sqlite3
import json
import streamlit.components.v1 as components
import re
from ติดต่อ.contact import contact_form
import random
import os
from memory import get_prompt

API_KEY = "AIzaSyDQ3dBumcz0BtrV9a6Zj68pl8N4C9_8b74"
ollama_url = "https://4de7-171-7-34-62.ngrok-free.app/v1/chat/completions"
model = "gemma3:12b"

config = {
    "primaryColor": "#d33682",
    "backgroundColor": "#002b36",
    "secondaryBackgroundColor": "#586e75",
    "textColor": "#fff",
    "toolbarMode": "minimal",
    "toImageButtonOptions": {
        "format": "jpg",
        "filename": "custom_image",
        "height": 720,
        "width": 480,
        "scale": 6
    }
}

st.markdown(
    """
    <style>
        .snowflake {
            position: absolute;
            top: 0;
            z-index: 9999;
            pointer-events: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# --- SNOW ANIMATION ---
st.markdown(
    """
    <script>
        var snowflakes = [];
        for (var i = 0; i < 100; i++) {
            var snowflake = document.createElement("div");
            snowflake.className = "snowflake";
            snowflake.innerHTML = "&#10052;";
            snowflake.style.left = Math.random() * window.innerWidth + "px";
            snowflake.style.animationDuration = Math.random() * 3 + 2 + "s";
            document.body.appendChild(snowflake);
            snowflakes.push(snowflake);
        }
    </script>
    """,
    unsafe_allow_html=True,
)
# --- SNOW ANIMATION ---
st.markdown(
    """
    <style>
        .snowflake {
            position: absolute;
            top: 0;
            z-index: 9999;
            pointer-events: none;
        }
        .snowflake:nth-child(1) { left: 10%; animation-delay: 0s; }
        .snowflake:nth-child(2) { left: 20%; animation-delay: 0.5s; }
        .snowflake:nth-child(3) { left: 30%; animation-delay: 1s; }
        .snowflake:nth-child(4) { left: 40%; animation-delay: 1.5s; }
        .snowflake:nth-child(5) { left: 50%; animation-delay: 2s; }
        .snowflake:nth-child(6) { left: 60%; animation-delay: 2.5s; }
        .snowflake:nth-child(7) { left: 70%; animation-delay: 3s; }
        .snowflake:nth-child(8) { left: 80%; animation-delay: 3.5s; }
        .snowflake:nth-child(9) { left: 90%; animation-delay: 4s; }
        .snowflake:nth-child(10) { left: 100%; animation-delay: 4.5s; }
        @keyframes snow {
            0% { transform: translateY(0); }
            100% { transform: translateY(100vh); }
        }
        .snowflake {
            animation: snow linear infinite;
            font-size: 2rem;
            color: #ffffff;
            opacity: 0.8;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
            animation-name: snow;
            animation-duration: 10s;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
            animation-fill-mode: forwards;
            animation-delay: 0s;
            animation-direction: normal;
            animation-play-state: running;
            transform: translateY(0);
            transform-origin: center;
            transform-style: preserve-3d;
            will-change: transform;
            transition: transform 0.5s ease-in-out;
        }
        .snowflake:hover {
            transform: scale(1.2) rotate(360deg);
            transition: transform 0.5s ease-in-out;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            animation-duration: 5s;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
            animation-fill-mode: forwards;
            animation-delay: 0s;
            animation-direction: normal;
            animation-play-state: running;
            transform: translateY(0);
            transform-origin: center;
            transform-style: preserve-3d;
            will-change: transform;
            transition: transform 0.5s ease-in-out;
            animation-name: snow;
            animation-duration: 10s;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
            animation-fill-mode: forwards;
            animation-delay: 0s;
            animation-direction: normal;
            animation-play-state: running;
            transform: translateY(0);
            transform-origin: center;
            transform-style: preserve-3d;
            will-change: transform;
            transition: transform 0.5s ease-in-out;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.show_animation = True
if "has_snowed" not in st.session_state:
    st.snow()
    st.session_state["has_snowed"] = True

def about_ray_dream():
    st.markdown(
    """
    <style>
        .hero-title {
            font-size: 3rem;
            color: #FF1493;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            font-family: 'Courier New', Courier, monospace;
            text-transform: uppercase;
            letter-spacing: 2px;
            background: linear-gradient(to right, #FF69B4, #FF1493);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 2s ease-in-out;
        }
        .hero-text {
            font-size: 1.2rem;
            line-height: 1.6;
            color: pink;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            margin-top: 20px;
            text-align: center;
        }
        .sidebar-text {
            font-size: 0.9rem;
            color: pink;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }
        .sidebar-title {
            font-size: 2rem;
            color: #FFC0CB;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }
        .sidebar-pages {
            font-size: 1.5rem;
            color: #FFC0CB;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
        }
        .sidebar-text {
            font-size: 1rem;
            color: #FFC0CB;
            text-align: left;
            font-weight: bold;
            margin-top: 20px;
        }
        .hero-button {
            background-color: #FF69B4;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1rem;
            font-weight: bold;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .hero-button:hover {
            background-color: #FF1493;
            color: white;
            text-decoration: none;
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .hero-image {
            width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        .hero-image:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease; 
        }
        .hero-image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 20px;
        }
        .resume-section {
            font-size: 1.3rem;
            font-weight: bold;
            color: #DAA520;
            margin-top: 20px;
        }
        @keyframes fadeIn {
            0% {
                opacity: 0;
                transform: translateY(-20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

    </style>
    """,
    unsafe_allow_html=True,
)
    st.markdown(
    """
    <style>
        .stApp {
            background: url("") no-repeat center center fixed;
            background-size: cover;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    with col1:
        st.image("./รูป/Ray.jpg", width=300)

    with col2:
        st.markdown('<h1 class="hero-title">Leng(เล้ง)</h1>', unsafe_allow_html=True)
        
        st.markdown("""
            <style>
                .resume-section {
                    background: linear-gradient(135deg, rgba(138, 43, 226, 0.7), rgba(30, 144, 255, 0.6));
                    padding: 15px;
                    border-radius: 15px;
                    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.4);
                    font-size: 2rem;
                    font-weight: bold;
                    color: White;
                    margin-top: 20px;
                    text-align: center;
                }
                .resume-box {
                    background-color: rgba(255, 255, 255, 5);
                    padding: 15px;
                    border-radius: 20px;
                    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.5);
                    color: #333333;
                    font-size: 1rem;
                    line-height: 1.6;
                }
                .resume-sectionA {
                    background: linear-gradient(135deg, rgba(0, 0, 139, 0.8), rgba(135, 206, 250, 0.6));
                    padding: 15px;
                    border-radius: 15px;
                    box-shadow: 0px 6px 15px rgba(0, 0, 0, 1);
                    font-size: 2rem;
                    font-weight: bold;
                    color: #FFFFFF;
                    margin-top: 20px;
                    text-align: Left;
                }
                .resume-text {
                    background: rgba(255, 255, 255, 5);
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.9);
                    color: #333;
                    font-size: 1rem;
                    line-height: 1.6;
                }

                .resume-textB { 
                    background-color: rgba(255, 255, 255, 0.9);
                    border-radius: 10px;
                    padding: 15px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
                    color: #333;
                    font-size: 1rem;
                    line-height: 1.6;
                }

                .resume-sectionB {
                    background: linear-gradient(135deg, rgba(135, 206, 250, 0.8), rgba(0, 255, 127, 0.6));
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 6px 12px rgba(255, 215, 0, 0.9);
                    color: white;
                    font-size: 1.2rem;
                    line-height: 1.6;
                }
            </style>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="resume-section">📌 ข้อมูลส่วนตัว</div>
            <div class="resume-box">
                <b>ชื่อ:</b> กันตภณ ม้าสุวรรณ<br>
                <b>การศึกษา:</b> นักศึกษาชั้นปีที่ 4 มหาวิทยาลัยกรุงเทพ สาขาการแสดง<br>
                <b>ความสามารถเฉพาะทาง:</b> พัฒนาและปรับปรุง AI Chatbot ที่สามารถวิเคราะห์ข้อมูลแบบเรียลไทม์รวมถึงระบบที่มีการโต้ตอบด้วยเสียงและความสามารถในการจดจำบริบทการพูดคุยทั้งหมด
                    
            </div>
            """, unsafe_allow_html=True)


        if st.button("✉️ ติดต่อเรา"):
            contact_form()

    st.write("\n")
    st.markdown("""
    <div class="resume-sectionA">💡 ทักษะและประสบการณ์</div>
    <div class="resume-text">
    ✔️ พัฒนา UI สำหรับ AI โต้ตอบผ่านเว็บ ด้วยpython เป็นหลักในการดึงapiและสร้างฟังชั้นการใช้งานต่างๆ และนำ css มาตบแต่งหน้าUIรวมถึงการสร้าง dashboard รวมถึงดึงข้อมูลหรือข่าวต่างๆมาใช้งาน<br>
    ✔️ โมเดลที่รันแบบ local Host มีระบบโต้ตอบด้วยเสียง สามารถค้นหาข้อมูลผ่านอินเทอร์เน็ต มีการรับรู้เหมือนเอไอคอยอ่านข่าวล่าสุดอยู่ตลอดเวลา และยังคงให้ความช่วยเหลือพูดคุยเรื่องต่างๆได้ รวมถึงระบบควบคุมการเปิดเพลง, เปิดเกม, และคำทักทายหรืออำลาแบบสุ่ม เพื่อเพิ่มความสามารถในการโต้ตอบ<br>
    ✔️ เริ่มแรกของระบบผมเคยทดลองใช้โมเดล Typhoon-7B และศึกษาวิธีแปลงคอลัมน์ข้อมูลจาก Huggingface เพื่อให้พร้อมสำหรับ fine-tuning แม้พบอุปสรรคทางเทคนิค แต่ใช้การเรียนรู้ผ่าน YouTube, GitHub และ GPT มาช่วยแก้ปัญหาและต่อยอดได้จากopen-soureอื่นแทน<br>
    ✔️ ศึกษาและปรับปรุงโค้ดจาก YouTube GitHub และ GPT เพื่อให้ AI มีความสามารถที่ก้าวหน้า<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            .stMarkdown {
                font-size: 1.2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
            }
            .stSubheader {
                font-size: 2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
            .stSubheader {
                font-size: 2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
                animation: fadeIn 3s ease-in-out;
            }
            @keyframes fadeIn {
                0% {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .stMarkdown {
                font-size: 1.2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
                animation: fadeIn 5s ease-in-out;
            }
            @keyframes fadeIn {
                0% {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .stSubheader {
                font-size: 2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
                animation: fadeIn 5s ease-in-out;
            }
            @keyframes fadeIn {
                0% {
                    opacity: 0;
                    transform: translateY(-50px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .stMarkdown {
                font-size: 1.2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
                animation: fadeIn 10s ease-in-out;
            }
            @keyframes fadeIn {
                0% {
                    opacity: 0;
                    transform: translateY(-60px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .stSubheader {
                font-size: 2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
                animation: fadeIn 10s ease-in-out;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.write("\n")  # เพิ่มระยะห่าง
    st.markdown("""
    <div class="resume-sectionB">🚀 เป้าหมายในอนาคต</div>
    <div class="resume-textB">
    🔥 พัฒนา AI ที่สามารถ ใช้กล้องในการเรียนรู้พฤติกรรมผู้ใช้แบบเรียลไทม์ และวิเคราะห์ข้อความต่อเนื่องของบริบทการสนทนา เพื่ออัปเดตเนื้อหาและตอบสนองอย่างชาญฉลาด<br>
    🔥 ออกแบบระบบที่ช่วยให้ AI สามารถ แทรกความเห็นหรือโต้แย้งอย่างมีเหตุผล โดยยังคงรักษาแนวคิดหลักของการสนทนาไว้ เพื่อเลียนแบบการโต้ตอบของมนุษย์ได้อย่างเป็นธรรมชาติยิ่งขึ้น<br>
    🔥 ผสมผสาน AI เข้ากับการทำงานหรือฟังชั้นต่างๆที่พอหาได้ให้โมเดลมีเครื่องมือที่ครบที่สุด
    </div>
    """, unsafe_allow_html=True)

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import pytz
from datetime import datetime
import feedparser

def dashboard():
    st.markdown("""
    <style>
        .stMarkdown {
            font-size: 1.4rem;
            color: #FFD700; /* สีทอง */
            text-align: left;
            font-weight: bold;
        }
        .stSubheader {
            font-size: 2.2rem;
            color: #FFD700;
            text-align: left;
            font-weight: bold;
        }
        .stApp {
            background: url("https://images.unsplash.com/photo-1519810755548-39cd217da494?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center fixed;
            background-size: cover;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Real-Time Gold Spot Dashboard")
    st_autorefresh(interval=60000, key="refresh_gold")

    st.subheader("📈 กราฟราคาทองคำ Spot (XAU/USD)", anchor=False)

    try:
        range_options = {
            "1 นาที": ("1d", "1m"),
            "5 นาที": ("1d", "5m"),
            "15 นาที": ("1d", "15m"),
            "30 นาที": ("1d", "30m"),
            "1 ชั่วโมง": ("1d", "1h"),
            "1 วัน": ("1d", "4h"),
            "3 วัน": ("3d", "4h"),
            "7 วัน": ("7d", "4h"),
            "30 วัน": ("30d", "4h"),
            "90 วัน": ("90d", "4h"),
            "180 วัน": ("180d", "4h"),
            "1 ปี": ("1y", "4h"),
            "2 ปี": ("2y", "4h"),
        }

        selected_range = st.selectbox("เลือกช่วงเวลาย้อนหลัง:", list(range_options.keys()))
        period, interval = range_options[selected_range]

        chart_type = st.selectbox("เลือกประเภทกราฟ:", ["เส้น", "แท่งเทียน"])

        gold = yf.Ticker("GC=F")
        hist = gold.history(period=period, interval=interval)
        hist = hist.reset_index()

        if hist['Datetime'].dt.tz is None:
            hist['Datetime'] = hist['Datetime'].dt.tz_localize('UTC')
        hist['Datetime'] = hist['Datetime'].dt.tz_convert('Asia/Bangkok')

        price_now = hist['Close'].iloc[-1]
        price_prev = hist['Close'].iloc[0]
        price_diff = price_now - price_prev
        price_pct = (price_diff / price_prev) * 100
        fig = go.Figure()

        change_color = "#00FF00" if price_pct >= 0 else "#FF6347"
        st.markdown(f"""
        <div style="
            background-color: rgba(0, 0, 0, 0.6);
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.4rem;
            color: {change_color};
            font-weight: bold;
            box-shadow: 0 0 10px #000000;
        ">
            การเปลี่ยนแปลงในช่วง <span style='color:#FFD700;'>{selected_range}</span>: {price_pct:+.2f}%
        </div>
        """, unsafe_allow_html=True)


        if chart_type == "แท่งเทียน":
            fig.add_trace(go.Candlestick(
                x=hist['Datetime'],
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name="Gold Spot"
            ))
        else:
            fig.add_trace(go.Scatter(x=hist['Datetime'], y=hist['Close'], mode='lines', name='Gold Spot'))

        fig.update_layout(
            title=f"ราคาทองคำ Spot ({selected_range})",
            xaxis_title="ตามเวลา(ประเทศไทย)",
            yaxis_title="USD",
            template="plotly_dark",
            font=dict(size=14, color="#FFD700")
        )

        st.plotly_chart(fig, use_container_width=True)

        particles_js = """
        <div style="position: relative; width: 100%; height: 370px;">
            <div id="particles-js" style="position: absolute; width: 100%; height: 100%;"></div>
            
            <!-- กล่องข้อความราคาทองคำ -->
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                        text-align: center; font-size: 18px; font-weight: bold; color: #FFFFFF;
                        background-color: rgba(0, 160, 0, 0.4); padding: 8px; border-radius: 5px;
                        box-shadow: 0px 0px 8px rgba(0, 255, 0, 0.3);">
                {price_text}
            </div>
            
            <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
            <script>
                particlesJS("particles-js", {
                    "particles": {
                        "number": {"value": 300, "density": {"enable": true, "value_area": 800}},
                        "color": {"value": "#ffffff"},
                        "shape": {"type": "circle"},
                        "opacity": {"value": 0.5},
                        "size": {"value": 2, "random": true},
                        "line_linked": {"enable": true, "distance": 100, "color": "#ffffff", "opacity": 0.22, "width": 1},
                        "move": {"enable": true, "speed": 0.2, "direction": "none"}
                    },
                    "interactivity": {"detect_on": "canvas", "events": {"onhover": {"enable": true, "mode": "grab"}, "onclick": {"enable": true, "mode": "repulse"}}}
                });
            </script>
        </div>
        """.replace("{price_text}", f"ราคาทองคำล่าสุด: ${price_now:,.2f} USD")

        components.html(particles_js, height=370, scrolling=False)

    except Exception as e:
        st.error(f"ตลาดปิดทำการในวันหยุด: กรุณาดูย้อนหลัง 3 วัน")

def หน้าที่4():
    st.markdown("""
        <style>
            .stApp {
                background: url("https://images.unsplash.com/photo-1635868355594-a297d37b3494?q=80&w=3987&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center fixed;
                background-size: cover;
                color: White
            }
            .subheader {
                font-size: 2rem;
                color: #FFD700;
                text-align: center;
                font-weight: bold;
                text-shadow: 3px 3px 7px rgba(0,0,0,0.3);
            }
            .ข่าวในแทบ {
                padding: 20px;
                border-radius: 15px;
                background: rgba(0, 0, 0, 0.7);
                box-shadow: 0px 6px 12px rgba(0,0,0,0.2);
                border: 2px solid rgba(255, 215, 0, 0.6);
                color: #FFF;
                margin-bottom: 20px;
            }
            .หัวข้อข่าว {
                font-size: 1.6rem;
                font-weight: bold;
                color: #FFD700;
            }
            .news-content {
                font-size: 1.2rem;
                line-height: 1.8;
            }
            .ลิ้งข่าว {
                font-size: 1rem;
                font-weight: bold;
                color: #87CEEB;
                text-decoration: underline;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-size: 1.4rem;
        color: #FFD700;
        font-weight: bold;
        box-shadow: 0 0 10px #000000;
    ">
        📰ข่าวล่าสุด🛑LIVE <span style='color:#FFD700;
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            .stApp {
                background: url("https://images.unsplash.com/photo-1635868355594-a297d37b3494?q=80&w=3987&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") no-repeat center center fixed;
                background-size: cover;
                color: White;
            }
        </style>
    """, unsafe_allow_html=True)

    # -- สร้างแท็บด้านบนภายในหน้า --
    tabs = st.tabs(["🪙 เศรษฐกิจ", "🏛️ ข่าวการเมือง","SPORT⚽", "📰ทั่วไป", "TECHNOLOGY🚀" ,"✈️ท่องเที่ยว"])

    with tabs[0]:  # ข่าวเศรษฐกิจ
        st.markdown("<h2 class='subheader'>📈 ข่าวเศรษฐกิจ</h2>", unsafe_allow_html=True)
        feed_urls = [
            "https://www.ryt9.com/stock/rss.xml",
            "https://www.ryt9.com/economy/rss.xml"
        ]
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                full_content = entry.content[0].value if "content" in entry else entry.summary
                with st.expander(f"🔍 {entry.title}"):
                    st.markdown(f"""
                        <div class="ข่าวในแทบ">
                            <div class="หัวข้อข่าว">{entry.title}</div>
                            <div>{full_content}</div>
                            <a class="ลิ้งข่าว" href="{entry.link}" target="_blank">🔗 อ่านเพิ่มเติม</a>
                        </div>
                    """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("<h2 class='subheader'>🌍 ข่าวการเมือง 🇹🇭</h2>", unsafe_allow_html=True)
        feed_urls = [
            "https://www.ryt9.com/politics-latest/rss.xml"
        ]
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                full_content = entry.content[0].value if "content" in entry else entry.summary
                with st.expander(f"🔍 {entry.title}"):
                    st.markdown(f"""
                        <div class="ข่าวในแทบ">
                            <div class="หัวข้อข่าว">{entry.title}</div>
                            <div>{full_content}</div>
                            <a class="ลิ้งข่าว" href="{entry.link}" target="_blank">🔗 อ่านเพิ่มเติม</a>
                        </div>
                    """, unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("<h2 class='subheader'>ข่าวกีฬา🏆</h2>", unsafe_allow_html=True)
        feed_urls = [
            "https://www.ryt9.com/sports/rss.xml/rss.xml"
        ]
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                full_content = entry.content[0].value if "content" in entry else entry.summary
                with st.expander(f"🔍 {entry.title}"):
                    st.markdown(f"""
                    <div class="ข่าวในแทบ">
                            <div class="หัวข้อข่าว">{entry.title}</div>
                            <div>{full_content}</div>
                            <a class="ลิ้งข่าว" href="{entry.link}" target="_blank">🔗 อ่านเพิ่มเติม</a>
                        </div>
                    """, unsafe_allow_html=True)
    with tabs[3]:
        st.markdown("<h2 class='subheader'>📢ข่าวทั่วไป</h2>", unsafe_allow_html=True)
        feed_urls = [
            "https://www.ryt9.com/general/rss.xml"
        ]
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                full_content = entry.content[0].value if "content" in entry else entry.summary
                with st.expander(f"🔍 {entry.title}"):
                    st.markdown(f"""
                    <div class="ข่าวในแทบ">
                            <div class="หัวข้อข่าว">{entry.title}</div>
                            <div>{full_content}</div>
                            <a class="ลิ้งข่าว" href="{entry.link}" target="_blank">🔗 อ่านเพิ่มเติม</a>
                        </div>
                    """, unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("<h2 class='subheader'>💻เทคโนโลยีและยานยนต์</h2>", unsafe_allow_html=True)
        feed_urls = [
            "https://www.ryt9.com/technology/rss.xml",
            "https://www.ryt9.com/motor/rss.xml"
        ]
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                full_content = entry.content[0].value if "content" in entry else entry.summary
                with st.expander(f"🔍 {entry.title}"):
                    st.markdown(f"""
                    <div class="ข่าวในแทบ">
                            <div class="หัวข้อข่าว">{entry.title}</div>
                            <div>{full_content}</div>
                            <a class="ลิ้งข่าว" href="{entry.link}" target="_blank">🔗 อ่านเพิ่มเติม</a>
                        </div>
                    """, unsafe_allow_html=True)

    with tabs[5]:
        st.markdown("<h2 class='subheader'>🥥🌴🌺🌅🌊</h2>", unsafe_allow_html=True)
        feed_urls = [
            "https://www.ryt9.com/travel/rss.xml"
        ]
        for url in feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                full_content = entry.content[0].value if "content" in entry else entry.summary
                with st.expander(f"🔍 {entry.title}"):
                    st.markdown(f"""
                    <div class="ข่าวในแทบ">
                            <div class="หัวข้อข่าว">{entry.title}</div>
                            <div>{full_content}</div>
                            <a class="ลิ้งข่าว" href="{entry.link}" target="_blank">🔗 อ่านเพิ่มเติม</a>
                        </div>
                    """, unsafe_allow_html=True)
                    

def get_random_title():
    """ฟังก์ชันสำหรับสุ่มข้อความหัวข้อ"""
    titles = [
        "แชทกับเรา💬",
        "พูดคุยกับไบร์ทของเรย์และดรีม✨",
        "ยินดีต้อนรับสู่แชทของเรา😊",
        "ถามเราได้เลย! 🚀",
        "มาเริ่มพูดคุยกัน! 💡"
    ]
    return random.choice(titles)

def ข่าวล่าสุด():
    ข่าว_urls = [
        "https://www.ryt9.com/stock/rss.xml",
        "https://www.ryt9.com/economy/rss.xml"
        "https://www.ryt9.com/politics/rss.xml"
    ]
    เก็บหัวข้อข่าว = []
    for url in ข่าว_urls:
        ข่าว = feedparser.parse(url)
        for entry in ข่าว.entries[:3]:
            เก็บหัวข้อข่าว.append(f"- {entry.title.strip()}")
    return "\n".join(เก็บหัวข้อข่าว)

def ราคาทอง():
    try:
        # ดึงราคาทอง Spot
        ทอง = yf.Ticker("GC=F")
        data = ทอง.history(period="3d", interval="1h")
        if data.empty or data["Close"].isnull().all():
            return "❌ ไม่สามารถดึงข้อมูลราคาทองคำได้ในขณะนี้"

        ราคาต่อUSD = data["Close"].dropna().iloc[-1]

        # ดึงค่าเงินบาท
        บาท = yf.Ticker("THB=X")
        U_data = บาท.history(period="3d", interval="1h")
        if U_data.empty or U_data["Close"].isnull().all():
            return f"💰 ราคาทอง Spot: ${ราคาต่อUSD:.2f} USD\n⚠️ ไม่สามารถดึงค่าเงินบาทได้"

        U = U_data["Close"].dropna().iloc[-1]

        ราคาต่อบาท = ราคาต่อUSD * 0.473 * U
        return (
            f"📈 ราคาทองคำ Spot: ${ราคาต่อUSD:,.2f} USD\n"
            f"💴 คิดเป็นราคาทองบาท: {ราคาต่อบาท:,.2f} บาท\n"
            f"💱 ค่าเงินบาทล่าสุด: 1 USD ≈ {U:.2f} THB"
        )
    
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดในการดึงข้อมูลราคาทอง: {e}"

import datetime
import pytz

def GDT():
    tz = pytz.timezone('Asia/Bangkok')
    N = datetime.datetime.now(tz)

    WDS = ['วันจันทร์', 'วันอังคาร', 'วันพุธ', 'วันพฤหัสบดี', 'วันศุกร์', 'วันเสาร์', 'วันอาทิตย์']
    MS = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
          'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']

    WD = WDS[N.weekday()]
    D = N.day
    M = MS[N.month - 1]
    year = N.year + 543

    return f"{WD}ที่ {D} {M} พ.ศ. {year}"

def create_prompt(messages):
    """
    สร้าง prompt ความจำของระบบจากประวัติการสนทนาของไบร์ทกับผู้สร้าง เล้ง
    """
    prompt = get_prompt()

    ข่าว = ข่าวล่าสุด()
    ทอง = ราคาทอง()
    วันเวลา = GDT()
    Bitcoin = ราคาบิทคอย()

    prompt += f"📅 วันที่ปัจจุบัน: {วันเวลา}\n\n"
    prompt += f"📰 ข้อมูลข่าวล่าสุด:\n{ข่าว}\n\n"
    prompt += f"ราคาทองล่าสุด:\n{ทอง}\n\n"
    prompt += f"ราคาบิทคอยล่าสุด:\n{Bitcoin}\n\n"

    for msg in messages:
        role = "ผู้ใช้" if msg["role"] == "user" else "ผู้ช่วย"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "ผู้ช่วย: "
    return prompt


def ราคาบิทคอย():
    try:
        BTC = yf.Ticker("BTC-USD")
        data = BTC.history(period="3d", interval="1h")
        if data.empty or data["Close"].isnull().all():
            return "❌ วันนี้วันหยุดฉันไม่สามารถดึงข้อมูลราคาทองคำได้ในขณะนี้"

        ราคาต่อUSD = data["Close"].dropna().iloc[-1]
        return (
            f"📈 ราคาBTC: ${ราคาต่อUSD:,.2f} USD\n"
        )

    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดในการดึงข้อมูลราคาทอง: {e}"

def chatwithRay():
    st.markdown(
        """
        <style>
            .stApp {
                background: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGVhcnRoJTIwYW5kJTIwc3RhcnN8ZW58MHx8fHwxNjk2OTU0NTcx&ixlib=rb-4.0.3&q=80&w=1080") no-repeat center center fixed;
                background-size: cover;
                background-repeat: no-repeat;
                color: black;
            }
            .stMarkdown {
                font-size: 1.2rem;
                color: dark;
                text-align: left;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(1,1,0,1.5);
                margin-top: 0px;
                text-align: left;
            }
            .stSubheader {
                font-size: 2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
            }
            .stChatMessage {
                font-size: 1.2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
            }
            .stChatInput {
                font-size: 1.2rem;
                color: black;
                text-align: left;
                font-weight: bold;
            }
            .stButton {
                font-size: 1.2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
            }
            .stFileUploader {
                font-size: 1.2rem;
                color: #FFC0CB;
                text-align: left;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.write("ยินดีต้อนรับสู่แชทบอทของเรา! คุณสามารถถามคำถามหรือขอความช่วยเหลือจากเราได้✨")
    st.title(get_random_title())
    
    upload_file = st.file_uploader("อัปโหลดไฟล์", type=["txt", "pdf", "docx", "jpg", "png", "py"], label_visibility="collapsed")
    content = ""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # แสดงข้อความแบบ bubble พร้อมระบบ chat_message
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):  # ไม่มี avatar
            st.markdown(f"""
                <div style='
                    background-color: {"rgba(255, 215, 0, 0.1)" if msg["role"] == "user" else "rgba(135, 206, 235, 0.15)"};
                    color: {"#FFD700" if msg["role"] == "user" else "#87CEEB"};
                    padding: 14px 18px;
                    border-radius: 12px;
                    font-size: 1.1rem;
                    font-weight: bold;
                    line-height: 1.6;
                    box-shadow: 0px 2px 6px rgba(0,0,0,0.3);
                '>
                    {msg["content"]}
                </div>
            """, unsafe_allow_html=True)

    
    user_input = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")
    if user_input or content:

        if upload_file is not None:
            file_type = upload_file.type
            if upload_file.type == "text/plain":
                content = upload_file.read().decode("utf-8")

            elif upload_file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(upload_file)
                for page in pdf_reader.pages:
                    content += page.extract_text()

            elif upload_file.type == "application/pdf":
                with open(upload_file, "rb") as f:
                    for page in reader.pages:
                        reader = PyPDF2.PdfReader(f)
                        content += page.extract_text()

            elif upload_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(upload_file)
                content = "\n".join([para.text for para in doc.paragraphs])

            elif file_type in ["image/jpeg", "image/png"]:
                img_path = f"/tmp/{upload_file.name}"
                with open(img_path, "wb") as f:
                    f.write(upload_file.getbuffer())

            elif upload_file is not None:
                if upload_file.type in ["text/plain", "text/x-python"]:
                    lines = upload_file.read().decode("utf-8").split("\n")
                    content = "\n".join(lines[:2000])

                content = extract_text_from_image(img_path)
                st.image(img_path, caption=upload_file.name, use_column_width=True)
                st.success("อัปโหลดไฟล์สำเร็จ!")
                st.write(content)
            else:
                st.write("ประเภทไฟล์ไม่รองรับ")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

        prompt = create_prompt(st.session_state.messages)
        if content:
            prompt += f"\nเนื้อหาจากไฟล์:\n{content}\n"

        messages = [{"role": "user", "content": prompt}]
        response = chat(messages)

        st.session_state.messages.append({"role": "assistant", "content": response["content"]})
        with st.chat_message("assistant"):
            placeholder = st.empty()
            current_content = ""
            for chunk in response_generator(response["content"]):
                current_content += chunk
                placeholder.markdown(current_content)
    

def response_generator(msg_content):
    """สตรีมข้อความทีละคำเพื่อสร้างเอฟเฟกต์ตอบกลับแบบเรียลไทม์"""
    words = msg_content.split()
    for word in words:
        yield word + " "
    yield "\n"

def chat(messages):
    """ส่งข้อความไปยัง API และรับผลลัพธ์"""
    try:
        response = requests.post(
            ollama_url,
            json={
                "messages": messages,
                "model": model,
                "max_token": 2000,
                "temperature": 0.8,
                "top_p": 0.98,
                "top_k": 40,
                "repetition_penalty": 1.9,
            },
        )
        response.raise_for_status()
        output = response.json()
        return {"role": "assistant", "content": output["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"role": "assistant", "content": str(e)}

def extract_text_from_image(image_file):
    """ใช้ OCR API เพื่อดึงข้อความจากรูปภาพ"""
    api_url = "https://api.ocr.space/parse/image"
    api_key = "K88895368588957"
    
    with open(image_file, "rb") as file:
        response = requests.post(
            api_url,
            files={"filename": file},
            data={"apikey": api_key, "language": "eng", "language": "eng"},
        )
        result = response.json()
        return result.get("ParsedResults", [{}])[0].get("ParsedText", "ไม่พบข้อความ")

def chat_with_model(prompt):
    """ส่งข้อความไปยังโมเดลของคุณและรับผลลัพธ์"""
    try:
        response = requests.post(
            ollama_url,
            json={
                "prompt": prompt,
                "model": model,
                "max_token": 2000,
                "temperature": 2,
                "top_p": 0.85,
                "top_k": 25,
                "repetition_penalty": 1.9,
            },
        )
        response.raise_for_status()
        output = response.json()
        return output["choices"][0]["message"]["content"]
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {e}"
def main():
    st.sidebar.title("D&R❤️")

    pages = {
        "โปรไฟล์": about_ray_dream, 
        "แชทกับเรา": chatwithRay,
        "Dashboard": dashboard,
        "ข่าวล่าสุด": หน้าที่4,
    }

    selected_page = st.sidebar.radio("สำรวจ", list(pages.keys()))
    st.sidebar.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #2E4053;
            color: chocolate;
        }

        [data-testid="stSidebar"] .sidebar-text {
            font-size: 1rem;
            font-weight: bold;
            color: #F7DC6F;
        }

        [data-testid="stSidebar"] .stRadio > label {
            font-size: 5rem;
            color: #FFFF00;
        }

        [data-testid="stSidebar"] img {
            border-radius: 10px;
            margin-bottom: 10px;
        }
        [data-testid="stSidebar"] .sidebar-title {
            font-size: 2rem;
            font-weight: bold;
            color: white;
        }
        [data-testid="stSidebar"] > div:first-child {{
        background-image: ("รูป/DR.jpg);
        background-color: #2E4053;
        background-position: center; 
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
        }}

    </style>
    """,
        unsafe_allow_html=True,
        
    )

    st.sidebar.markdown(
        """
        <p class="sidebar-text">สร้างโดยเล้ง ❤️ และดรีม</p>
        """,
        unsafe_allow_html=True,
    )
    particles_js = """
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        setTimeout(function() {
            particlesJS("particles-js", {
                "particles": {
                    "number": {"value": 300, "density": {"enable": true, "value_area": 800}},
                    "color": {"value": "#ffffff"},
                    "shape": {"type": "circle"},
                    "opacity": {"value": 0.5},
                    "size": {"value": 2, "random": true},
                    "line_linked": {"enable": true, "distance": 100, "color": "#ffffff", "opacity": 0.22, "width": 1},
                    "move": {"enable": true, "speed": 0.2, "direction": "none"}
                },
                "interactivity": {"detect_on": "canvas", "events": {"onhover": {"enable": true, "mode": "grab"}, "onclick": {"enable": true, "mode": "repulse"}}}
            });
        }, 1000);  // หน่วงเวลา 1 วินาทีก่อนเริ่มทำงาน
    </script>
    """
    with st.sidebar:
        components.html(particles_js, height=370, scrolling=False) 

    pages[selected_page]()
st.sidebar.image("รูป/DR.jpg", width=150)
st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-image: url("https://images.pexels.com/photos/1175136/pexels-photo-1175136.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            color: White;

        }
    </style>
    """,
    unsafe_allow_html=True,
)

if __name__ == "__main__":
    main()
