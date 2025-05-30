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
ollama_url = "https://4655-171-7-211-183.ngrok-free.app/v1/chat/completions"
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
particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js</title>
  <style>
  #particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    z-index: -1; /* Send the animation to the back */
  }
  .content {
    position: relative;
    z-index: 1;
    color: white;
  }
  
</style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="content">
    <!-- Placeholder for Streamlit content -->
  </div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "image": {
            "src": "img/github.svg",
            "width": 100,
            "height": 100
          }
        },
        "opacity": {
          "value": 0.5,
          "random": false,
          "anim": {
            "enable": false,
            "speed": 1,
            "opacity_min": 0.2,
            "sync": false
          }
        },
        "size": {
          "value": 2,
          "random": true,
          "anim": {
            "enable": false,
            "speed": 40,
            "size_min": 0.1,
            "sync": false
          }
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": true,
          "attract": {
            "enable": false,
            "rotateX": 600,
            "rotateY": 1200
          }
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "bubble": {
            "distance": 400,
            "size": 2,
            "duration": 2,
            "opacity": 0.5,
            "speed": 1
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 2
          },
          "remove": {
            "particles_nb": 3
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""
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
if st.session_state.show_animation:
    components.html(particles_js, height=370, scrolling=True)

def about_ray_dream():
    st.markdown(
    """
    <style>
        .hero-title {
            font-size: 3rem;
            color: #FFC0CB;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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
    </style>
    """,
    unsafe_allow_html=True,
)
    st.markdown(
    """
    <style>
        .stApp {
            background: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDF8fGJsdXUlMjB3aGl0ZXxlbnwwfHx8fDE2OTY5NTQ1NzE&ixlib=rb-4.0.3&q=80&w=1080") no-repeat center center fixed;
            background-size: cover;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    with col1:
        st.image("./รูป/Love.jpg", width=300)  # เพิ่มขนาดภาพให้โดดเด่น

    with col2:
        st.markdown('<h1 class="hero-title">Dream & Ray</h1>', unsafe_allow_html=True)
        
        st.markdown(
            '<p class="hero-text">'
            "ความรักในช่วงเวลาแบบนี้เหมือนกับการที่โลกหยุดนิ่ง ให้ทั้งคู่สามารถมองเห็นกันและกันอย่างเต็มตา"
            "และเข้าใจว่าพวกเขาคือทุกสิ่งในโลกใบนี้ ความรักไม่ได้ต้องการสิ่งหรูหรา"
            "แต่ต้องการเพียงความเรียบง่ายที่เปี่ยมไปด้วยความจริงใจและความใส่ใจที่ไม่มีวันสิ้นสุด.."
            '</p>',
            unsafe_allow_html=True,
        )
        if st.button("✉️ ติดต่อเรา"):
            contact_form()

    st.write("\n")  # เพิ่มระยะห่างเพื่อไม่ให้หน้าดูอึดอัด
    st.subheader("ข้อมูลของพวกเรา", anchor=False)
    st.write(
        """
        - 🌟 ความรักของเราผสมผสานความเรียบง่ายกับความอบอุ่น
        - 🎨 เราชื่นชอบงานศิลปะและการเขียน
        - 🌍 การเดินทางคือแรงบันดาลใจของเรา
        - 💕 ความใส่ใจเล็กๆ เปลี่ยนแปลงโลกให้สดใสขึ้น
        """
    )
    #css style st.subheader
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
    #css animetion
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
    st.subheader("เรื่องราวของเรา", anchor=False)
    #css style หัวข้อ เรื่องราวของเรา
    
    st.write(
        """
        - 📍เรื่องราวของเราเริ่มจากวันที่ฝันกลายเป็นจริง 26/04/2022และทุกอย่างเปลี่ยนไปตั้งแต่วันนั้น
        - 🌟ความฝันของเราคือสร้างความสุขและกำลังใจให้กันและกันเพราะวันแรกของเราเต็มไปด้วยบทสนทนาเกี่ยวกับความฝันและความหวัง
        - 💼การเดินทางในโลกของเราเต็มไปด้วยบทเรียนชีวิตอันมีความหมายที่เต็มไปด้วยความอบอุ่นเเละเหน็บหนาวเพราะเราก็ต่างชอบสำรวจโลกผ่านมุมมองของกันและกัน
        - 💕เราเรียนรู้ที่จะเข้าใจความแตกต่าง และเปลี่ยนสิ่งเหล่านั้นให้เป็นพลังเราเชื่อว่าความรักสามารถเปลี่ยนโลกได้ด้วยความใส่ใจเล็กๆเราสนับสนุนกันและกันในทุกสถานการณ์
        """
    )

    # --- FOOTER ---
    st.write("\n")
    st.markdown(
        """
        <hr style="border: 1px solid #ddd; margin: 20px 0;">
        <p class="sidebar-text">สร้างโดยเล้ง ❤️ และดรีม</p>
        """,
        unsafe_allow_html=True,
    )

    st.write("\n")
#สร้าง dashboard
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

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
            background: url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGdhbGF4eXxlbnwwfHx8fDE2OTY5NTQ1NzE&ixlib=rb-4.0.3&q=80&w=1080") no-repeat center center fixed;
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
            "1 วัน": ("3d", "1h"),
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

        # คำนวณการเปลี่ยนแปลงราคา
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
        st.success(f"ราคาทองคำล่าสุด: ${price_now:,.2f} USD")
    except Exception as e:
        st.error(f"ไม่สามารถโหลดข้อมูลราคาทองคำได้: {e}")

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

def create_prompt(messages):
    """
    สร้าง prompt ความจำของระบบจากประวัติการสนทนา
    """
    prompt = get_prompt()
    for msg in messages:
        role = "ผู้ใช้" if msg["role"] == "user" else "ผู้ช่วย"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "ผู้ช่วย: "
    return prompt

def chatwithRay():
    #css style background
    st.markdown(
        """
        <style>
            .stApp {
                background: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGVhcnRoJTIwYW5kJTIwc3RhcnN8ZW58MHx8fHwxNjk2OTU0NTcx&ixlib=rb-4.0.3&q=80&w=1080") no-repeat center center fixed;
                background-size: cover;
                background-repeat: no-repeat;
                color: brown;
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
    
    
    # อัปโหลดไฟล์
    upload_file = st.file_uploader("อัปโหลดไฟล์", type=["txt", "pdf", "docx", "jpg", "png"], label_visibility="collapsed")
    content = ""

    # ตรวจสอบว่ามีการเก็บประวัติการสนทนาใน session_state หรือไม่
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # แสดงข้อความก่อนหน้า
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # รับข้อความจากผู้ใช้
    user_input = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")
    if user_input or content:
        #อ่านไฟล์ที่อัพโหลด
        if upload_file is not None:
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
            elif upload_file.type == "image/jpeg" or upload_file.type == "image/png":
                img_path = f"/tmp/{upload_file.name}"
                with open(img_path, "wb") as f:
                    f.write(upload_file.getbuffer())
                # ใช้ OCR API เพื่อดึงข้อความจากรูปภาพ
                content = extract_text_from_image(img_path)
                st.image(img_path, caption=upload_file.name, use_column_width=True)
                st.success("อัปโหลดไฟล์สำเร็จ!")
                st.write(content)
            else:
                st.write("ประเภทไฟล์ไม่รองรับ")
        # เพิ่มข้อความของผู้ใช้ในประวัติการสนทนา
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.write(user_input)

        # สร้าง prompt ความจำ
        prompt = create_prompt(st.session_state.messages)
        if content:
            prompt += f"\nเนื้อหาจากไฟล์:\n{content}\n"

        # เรียกใช้งาน API
        messages = [{"role": "user", "content": prompt}]
        response = chat(messages)

        # เพิ่มข้อความตอบกลับของผู้ช่วยในประวัติการสนทนา
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
                "temperature": 1.2,
                "top_p": 0.99,
                "top_k": 40,
                "repetition_penalty": 1.9,
            },
        )
        response.raise_for_status()
        output = response.json()
        return {"role": "assistant", "content": output["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"role": "assistant", "content": str(e)}

# ฟังก์ชันสำหรับดึงข้อความจากรูปภาพ
def extract_text_from_image(image_file):
    """ใช้ OCR API เพื่อดึงข้อความจากรูปภาพ"""
    api_url = "https://api.ocr.space/parse/image"
    api_key = "K88895368588957"  # สมัครใช้งาน OCR.Space API เพื่อรับ API Key
    
    with open(image_file, "rb") as file:
        response = requests.post(
            api_url,
            files={"filename": file},
            data={"apikey": api_key, "language": "eng", "language": "eng"},
        )
        result = response.json()
        return result.get("ParsedResults", [{}])[0].get("ParsedText", "ไม่พบข้อความ")

# ฟังก์ชันสำหรับเรียกใช้งานโมเดลของคุณ
def chat_with_model(prompt):
    """ส่งข้อความไปยังโมเดลของคุณและรับผลลัพธ์"""
    try:
        response = requests.post(
            ollama_url,
            json={
                "prompt": prompt,
                "model": model,
                "max_token": 2000,
                "temperature": 1.2,
                "top_p": 0.99,
                "top_k": 40,
                "repetition_penalty": 1.9,
            },
        )
        response.raise_for_status()
        output = response.json()
        return output["choices"][0]["message"]["content"]
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {e}"

# --- MAIN FUNCTION ---
def main():
    st.sidebar.title("D&R❤️")

    pages = {
        "About Ray & Dream": about_ray_dream, 
        "แชทกับเรา": chatwithRay,
        "Dashboard": dashboard,
    }

    selected_page = st.sidebar.radio("สำรวจ", list(pages.keys()))
    st.sidebar.markdown(
        """
        <style>
        /* เปลี่ยนสีพื้นหลังของ Sidebar */
        [data-testid="stSidebar"] {
            background-color: #2E4053;
            color: chocolate;
        }

        /* ปรับแต่งข้อความใน Sidebar */
        [data-testid="stSidebar"] .sidebar-text {
            font-size: 1rem;
            font-weight: bold;
            color: #F7DC6F;
        }

        /* ปรับแต่งปุ่ม Radio */
        [data-testid="stSidebar"] .stRadio > label {
            font-size: 5rem;
            color: #FFFF00;
        }

        /* ปรับแต่งรูปภาพใน Sidebar */
        [data-testid="stSidebar"] img {
            border-radius: 10px;
            margin-bottom: 10px;
        }
        /* ปรับแต่งข้อความใน Sidebar */
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
    st.sidebar.markdown(
        """

        """
    )
    # Run selected page function
    pages[selected_page]()
st.sidebar.image("รูป/DR.jpg", width=150)
#อัพโหลดรูปภาพพื้นหลัง sidebar
st.sidebar.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-image: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDF8fGZvcmVzdHxlbnwwfHx8fDE2OTY5NTQ1NzE&ixlib=rb-4.0.3&q=80&w=1080");
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
