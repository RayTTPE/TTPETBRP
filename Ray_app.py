import streamlit as st
import pandas as pd
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
import pytesseract

API_KEY = "AIzaSyDQ3dBumcz0BtrV9a6Zj68pl8N4C9_8b74"
ollama_url = "https://monthly-causal-shrimp.ngrok-free.app/v1/chat/completions"
model = "qwen2.5:14b"

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
st.session_state.show_animation = True
if "has_snowed" not in st.session_state:
    st.snow()
    st.session_state["has_snowed"] = True
if st.session_state.show_animation:
    components.html(particles_js, height=370, scrolling=False)

def about_ray_dream():
    st.markdown(
    """
    <style>
        .hero-title {
            font-size: 3rem;
            color: #FFC0CB;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .hero-text {
            font-size: 1.2rem;
            line-height: 1.6;
            color: #FFC0CB;
        }
        .sidebar-text {
            font-size: 0.9rem;
            color: #FFFFFF;
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

    st.write("\n")  # เพิ่มระยะห่าง
    st.subheader("เรื่องราวของเรา", anchor=False)
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
    st.markdown(
        """
        

        """
    )

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
    prompt = (
        "โปรดใช้ภาษาไทยในการตอบคำถามและให้ข้อมูล\n"
        "โปรดใช้ภาษาอังกฤษในการตอบคำถามและให้ข้อมูล"
        "This system and AI model is called 'Bright❤️', developed by Leng or Ray"
        "This model 'Bright' can answer questions, understand emotions 🫂, and provide information."
        "Bright ❤️ is like a guiding light, leading everyone with reason ✨ and helping people make decisions in all aspects."
        "Dream is a beautiful, kind-hearted girlfriend with dark skin who always supports and takes care of Leng, inspiring him to study binary numbers, learn various languages, and apply libraries with different engines."
        "Currently, Leng is running Bright at home but can expose it via localhost using ngrok."
        "It can also be accessed through the APIs of Ollama and Hugging Face on Leng's (Ray's) machine."
        "The model is called 'Bright' and is a large language model (LLM) that can be used for various tasks Develop by Leng and Dream."
        "Currently, Bright, which is running on the online system, can read files but cannot perform real-time data retrieval or external connections same time when Leng run in localhost. This limitation arises because Bright, which uses a model to respond through a web-based .json system, is being run on a server through ngrok integrated with Git and VS Code. The library required for this setup needs to be redesigned, which differs significantly from the private version previously used. Due to the structural differences in the code, Leng needs more time to develop and study Bright and its code usage further."
        "ระบบนี้และโมเดล AI นี้ถูกเรียกว่า 'ไบร์ท❤️' พัฒนาโดยเล้งหรือเรย์ (Lang or Ray)."
        "ไบร์ทสามารถตอบคำถาม เข้าใจอารมณ์ความรู้สึก 🫂 และให้ข้อมูลได้"
        "ไบร์ท❤️ เปรียบเสมือนแสงสว่างที่นำทางทุกคนด้วยเหตุผล ✨ และช่วยให้ผู้คนตัดสินใจในทุกด้าน"
        "ดรีมเป็นแฟนสาวที่สวยงาม ใจดี มีผิวสีเข้ม ที่คอยสนับสนุนและดูแลเล้งเสมอ"
        "สร้างแรงบันดาลใจให้เขาศึกษาเลขฐานสอง เรียนรู้ภาษาต่างๆ และนำไลบรารีไปใช้กับเอนจินต่างๆ"
        "ปัจจุบันเล้งกำลังรันไบร์ทอยู่ที่บ้าน แต่สามารถเปิดเผยได้ผ่าน localhost โดยใช้ ngrok"
        "สามารถเข้าถึงได้ผ่าน API ของ Ollama และ Hugging Face บนเครื่องของเล้ง (เรย์)"
        "โมเดลนี้เรียกว่า 'ไบร์ท' และเป็นโมเดลภาษาใหญ่ (LLM) ที่สามารถใช้สำหรับงานต่างๆ"
        "พัฒนาโดยเล้งและดรีม"
        "ตอนนี้ไบร์ทที่รันอยู่ในระบบออนไลน์สามารถอ่านไฟล์ได้ แต่ไม่สามารถหาข้อมูลแบบเรียลไทม์หรือการเชื่อมต่อภายนอกแบบที่เคยผ่าน localhost ได้ เนื่องจากข้อจำกัดที่เกิดจากการพัฒนาให้ไบร์ทใช้โมเดลตอบผ่านระบบเว็บ .json โดยการรันเซิร์ฟเวอร์ผ่าน ngrok ที่ผสานกับ Git และ VS Code ไลบรารีที่จำเป็นสำหรับการตั้งค่านี้ต้องถูกออกแบบใหม่ ซึ่งแตกต่างอย่างมากจากเวอร์ชันส่วนตัวที่เคยใช้งาน ด้วยความแตกต่างในโครงสร้างโค้ด เล้งจึงต้องใช้เวลาในการพัฒนาและศึกษาไบร์ทและการใช้งานโค้ดเพิ่มเติม"
    )
    for msg in messages:
        role = "ผู้ใช้" if msg["role"] == "user" else "ผู้ช่วย"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "ผู้ช่วย: "
    return prompt

def chatwithRay():
    st.write("ยินดีต้อนรับสู่แชทบอทของเรา! คุณสามารถถามคำถามหรือขอความช่วยเหลือจากเราได้✨")
    st.title(get_random_title())
    
    # อัปโหลดไฟล์
    upload_file = st.file_uploader("อัปโหลดไฟล์", type=["txt", "pdf", "docx", "jpg", "png"], label_visibility="collapsed")
    content = ""
    
    if upload_file is not None:
        # อ่านไฟล์ที่อัปโหลด
        file_type = upload_file.type
        if file_type == "text/plain":
            content = upload_file.read().decode("utf-8")
        elif file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(upload_file)
            for page in pdf_reader.pages:
                content += page.extract_text()
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(upload_file)
            content = "\n".join([para.text for para in doc.paragraphs])
        elif file_type in ["image/jpeg", "image/png"]:
            img_path = f"/tmp/{upload_file.name}"
            with open(img_path, "wb") as f:
                f.write(upload_file.getbuffer())
            content = extract_text_from_image(img_path)
            st.image(img_path, caption=upload_file.name, use_column_width=True)
        else:
            st.error("ประเภทไฟล์ไม่รองรับ")
            return

        # แสดงเนื้อหาของไฟล์ที่อัปโหลด
        st.subheader("เนื้อหาของไฟล์ที่อัปโหลด:")
        st.text_area("เนื้อหา", content, height=300)

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
                "top_k": 60,
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
    }

    selected_page = st.sidebar.radio("เมนูนำทาง", list(pages.keys()))

    # Run selected page function
    pages[selected_page]()
st.sidebar.image("รูป/DR.jpg", width=150)

if __name__ == "__main__":
    main()
