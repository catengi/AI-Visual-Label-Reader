![pmub](https://github.com/user-attachments/assets/b6a7560d-ae8e-4409-8ba0-9e086fdaa5d5)

**ระบบอ่านฉลากของชิ้นส่วนของงานประกอบด้วยปัญญาประดิษฐ์
(AI Visual Label Reader)**

**วิธีการติดตั้งใช้งาน**
1. Download File ทั้งหมดเข้าสู่ computer / server
2. ติดตั้ง n8n ใน command prompt ด้วยคำสั่ง npm install -g n8n หรือใช้ n8n บน cloud ก็ได้โดยดูรายละเอียดที่นี่: https://n8n.io/
3. Import ไฟล์ My Workflow เข้าสู่ n8n แล้วตั้งค่าให้มีการ active ระบบแบบ production
4. ติดตั้งโปรแกรม Ollama จาก https://ollama.com/
5. ติดตั้งโมเดล Gemma3:4B ที่แนบมาพร้อมไฟล์ โดยเพิ่มเข้าไปใน environment ของ Ollama
6. รันไฟล์ main.py ด้วย Python Runner หรือ Python IDE
7. ทดสอบการใช้งานระบบได้เลยที่หน้าเว็บ: http://localhost:5000/

<img width="1269" height="849" alt="image" src="https://github.com/user-attachments/assets/ef2690f0-6477-4731-8619-0502018c5cb4" />
 

