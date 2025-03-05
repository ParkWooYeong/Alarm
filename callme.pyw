import tkinter as tk
from tkinter import messagebox
import time
import threading
import datetime
import winsound

# 알람 소리 파일 
ALARM_SOUND = "alarmm.wav"

# 알람 설정 함수
def set_alarm():
    try:
        selected_hour = int(hour_listbox.get(tk.ACTIVE).strip())  
        selected_minute = int(minute_listbox.get(tk.ACTIVE).strip())  
        
        now = datetime.datetime.now()
        alarm_time = now.replace(hour=selected_hour, minute=selected_minute, second=0, microsecond=0)

        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)

        wait_time = (alarm_time - now).total_seconds()

        messagebox.showinfo("⏰ 알람 설정", f"{selected_hour}시 {selected_minute}분에 알람이 울립니다!")
        threading.Thread(target=alarm_countdown, args=(wait_time,), daemon=True).start()
    except ValueError:
        messagebox.showerror("오류", "시간과 분을 선택하세요!")

# 카운트다운 후 알람 실행
def alarm_countdown(wait_time):
    time.sleep(wait_time)
    winsound.PlaySound(ALARM_SOUND, winsound.SND_FILENAME)  # WAV 파일 재생

# Windows에서 마우스 휠 한 칸씩 이동
def on_mouse_wheel(event, listbox):
    direction = -1 if event.delta > 0 else 1  
    listbox.yview_scroll(direction, "units") 
# GUI 생성
root = tk.Tk()
root.title("Mero")
root.geometry("350x280")
root.configure(bg="#222831")  # 다크 모드 스타일 배경

tk.Label(root, text="⏰ 알람 시간 선택", font=("Arial", 12, "bold"), fg="white", bg="#222831").pack(pady=10)

# 프레임을 창 중앙에 배치
frame = tk.Frame(root, bg="#222831")
frame.place(relx=0.5, rely=0.45, anchor="center")  # 중앙 정렬

# 시간 선택
hour_listbox = tk.Listbox(frame, font=("Arial", 14), height=1, width=3, selectmode="browse",
    exportselection=False, bg="#222831", fg="white",
    selectbackground="#00ADB5", selectforeground="black",
    borderwidth=0, highlightthickness=0, justify="center")
hour_listbox.pack(side=tk.LEFT, padx=10, fill=tk.Y)

# 분 선택 Listbox
minute_listbox = tk.Listbox(frame, font=("Arial", 14), height=1, width=3, selectmode="browse",
    exportselection=False, bg="#222831", fg="white",
    selectbackground="#00ADB5", selectforeground="black",
    borderwidth=0, highlightthickness=0, justify="center")
minute_listbox.pack(side=tk.LEFT, padx=10, fill=tk.Y)

# 0~23시 추가 
for h in range(24):
    hour_listbox.insert(tk.END, f" {h:2d} ")

# 0~59분 추가
for m in range(60):
    minute_listbox.insert(tk.END, f" {m:2d} ")

# 기본 선택 (현재 시간 기준)
now = datetime.datetime.now()
hour_listbox.select_set(now.hour)
hour_listbox.activate(now.hour)
minute_listbox.select_set(now.minute)
minute_listbox.activate(now.minute)

# 마우스 휠 이벤트 바인딩 (휠 스크롤 한 칸씩 이동)
hour_listbox.bind("<MouseWheel>", lambda event: on_mouse_wheel(event, hour_listbox))
minute_listbox.bind("<MouseWheel>", lambda event: on_mouse_wheel(event, minute_listbox))

# 버튼을 창 중앙에 배치 (위치 유지)
button = tk.Button(root, text="🔔 알람 설정", font=("Arial", 12, "bold"), bg="#00ADB5", fg="white",
activebackground="#008C8C", activeforeground="white", padx=10, pady=5, command=set_alarm)
button.place(relx=0.5, rely=0.8, anchor="center")  # 버튼 위치 고정

root.mainloop()
