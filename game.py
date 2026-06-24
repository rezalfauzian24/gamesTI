import pygame
import sys
import os
import math
import random
import threading
import time
import cv2
import mediapipe as mp
import numpy as np

# ─── CONFIG ──────────────────────────────────────────────────────────────────
SCREEN_W, SCREEN_H = 1000, 650
FPS = 60
GRAVITY = 0.55
JUMP_FORCE = -14
MOVE_SPEED = 5
PLATFORM_Y = SCREEN_H - 100
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── ALL QUESTIONS POOL ───────────────────────────────────────────────────────
ALL_QUESTIONS = [
    # === SOAL LAMA (HMTI Formal) ===
    {
        "q": "Kapan HMTI Universitas Nusa Putra resmi terbentuk secara terpisah?",
        "options": {"A": "25 September 2011", "B": "25 September 2012",
                    "C": "25 September 2013", "D": "25 September 2014"},
        "answer": "C"
    },
    {
        "q": "Apa nilai utama yang terkandung dalam Moto HMTI?",
        "options": {"A": "Kompetisi dan kemandirian", "B": "Loyalitas dan solidaritas",
                    "C": "Kebebasan dan kreativitas", "D": "Keadilan dan ketegasan"},
        "answer": "B"
    },
    {
        "q": 'Pada logo HMTI, simbol "Globe" memiliki makna sebagai wadah pengetahuan untuk mendukung...',
        "options": {"A": "Kemajuan perkembangan zaman", "B": "Keberhasilan ekonomi digital",
                    "C": "Hubungan internasional mahasiswa", "D": "Kelestarian lingkungan hidup"},
        "answer": "A"
    },
    {
        "q": 'Apa arti simbol "Core" pada logo HMTI?',
        "options": {"A": "Puncak prestasi mahasiswa", "B": "Pusat dari segala bentuk dasar",
                    "C": "Pusat pembelajaran Mahasiswa Teknik Informatika", "D": "Dasar kekuatan organisasi"},
        "answer": "C"
    },
    {
        "q": 'Kata "HMTI" pada logo merupakan kependekan dari...',
        "options": {"A": "Himpunan Mahasiswa Teknologi Informasi", "B": "Himpunan Mahasiswa Teknik Informatika",
                    "C": "Hubungan Mahasiswa Teknik Informatika", "D": "Himpunan Masyarakat Teknokrat Indonesia"},
        "answer": "B"
    },
    {
        "q": "Warna biru pada logo HMTI mengandung arti...",
        "options": {"A": "Terang atau cerdas", "B": "Pencapaian tujuan",
                    "C": "Panutan", "D": "Kekuatan finansial"},
        "answer": "C"
    },
    {
        "q": "Berdasarkan peran HMTI, organisasi ini bergerak di bidang...",
        "options": {"A": "Ekonomi dan bisnis", "B": "Pendidikan dan sosial budaya",
                    "C": "Politik dan hukum", "D": "Olahraga dan seni"},
        "answer": "B"
    },
    {
        "q": "Salah satu fungsi HMTI adalah menampung dan menyalurkan aspirasi mahasiswa program studi...",
        "options": {"A": "Sistem Informasi", "B": "Teknik Informatika",
                    "C": "Desain Komunikasi Visual", "D": "Teknik Sipil"},
        "answer": "B"
    },
    {
        "q": "Manakah yang termasuk ke dalam salah satu tujuan HMTI?",
        "options": {"A": "Memonopoli industri perangkat lunak",
                    "B": "Melaksanakan penelitian dan pengabdian untuk melestarikan kearifan lokal",
                    "C": "Mengurangi jam kuliah mahasiswa",
                    "D": "Membatasi ruang gerak organisasi lain"},
        "answer": "B"
    },
    {
        "q": "Berikut ini yang bukan merupakan bagian dari divisi struktural kepengurusan HMTI adalah...",
        "options": {"A": "Divisi Kaderisasi", "B": "Divisi Hubungan Masyarakat",
                    "C": "Divisi Hukum dan Keamanan", "D": "Divisi Logistik dan Perlengkapan"},
        "answer": "D"
    },

    # === SOAL BARU (COMPILE 2026 - Lucu & Menjebak) ===
    {
        "q": "Apa nama Instagram HMTI?",
        "options": {"A": "hmti_nusaputra", "B": "teknikinformatika_unsp",
                    "C": "hmti_unsp", "D": "hmti.sukabumi"},
        "answer": "C"
    },
    {
        "q": "Berapa jumlah postingan Instagram HMTI? (Hati-hati, jangan asal tebak! 👀)",
        "options": {"A": "614", "B": "500",
                    "C": "725", "D": "999"},
        "answer": "A"
    },
    {
        "q": 'HMTI, huruf "M" berarti?',
        "options": {"A": "Mancing", "B": "Main Game",
                    "C": "Menyala", "D": "Mahasiswa"},
        "answer": "D"
    },
    {
        "q": "Ruang Kaprodi Teknik Informatika berada di lantai berapa?",
        "options": {"A": "Lantai 1", "B": "Lantai 2",
                    "C": "Lantai 4", "D": "Lantai 7"},
        "answer": "C"
    },
    {
        "q": "HMTI identik dengan?",
        "options": {"A": "Motor RX King", "B": "Laptop",
                    "C": "Wibu", "D": "Pancingan Ikan"},
        "answer": "B"
    },
    {
        "q": "Apa moto HMTI?",
        "options": {"A": "Coding Sampai Subuh", "B": "Kerja Kelompok Selamanya",
                    "C": "Informatika Menyala", "D": "Together Be Better"},
        "answer": "D"
    },
    {
        "q": "Berapa jumlah menu pada website COMPILE?",
        "options": {"A": "7", "B": "5",
                    "C": "10", "D": "12"},
        "answer": "A"
    },
    {
        "q": "Apa nama Instagram Ketua Angkatan 2025?",
        "options": {"A": "ilhamti25", "B": "hmti_ilham",
                    "C": "moilham_", "D": "ilhamcompile"},
        "answer": "C"
    },
    {
        "q": "Hewan yang paling identik dengan TI Angkatan 2025?",
        "options": {"A": "Elang", "B": "Harimau",
                    "C": "Panda", "D": "Kucing"},
        "answer": "D"
    },
    {
        "q": '"Aku dan kamu adalah kita, dan kita adalah ..."',
        "options": {"A": "Keluarga Cemara", "B": "HMTI",
                    "C": "Avengers", "D": "Tim Esport"},
        "answer": "B"
    },

    # === BONUS SOAL RANDOM (Santai & Menjebak) ===
    {
        "q": "Saat deadline mepet, mahasiswa TI biasanya?",
        "options": {"A": "Tidur nyenyak", "B": "Main bola",
                    "C": "Begadang coding", "D": "Pergi mancing"},
        "answer": "C"
    },
    {
        "q": "Bahasa pemrograman yang sering dipelajari mahasiswa TI?",
        "options": {"A": "Bahasa Jawa", "B": "Bahasa Sunda",
                    "C": "Python", "D": "Bahasa Alien"},
        "answer": "C"
    },
    {
        "q": "Ketika error muncul 100 kali, mahasiswa TI biasanya?",
        "options": {"A": "Menangis", "B": "Install ulang laptop",
                    "C": "Cari solusi di Google/ChatGPT", "D": "Ganti jurusan"},
        "answer": "C"
    },
    {
        "q": "Teman terbaik anak TI adalah?",
        "options": {"A": "Kalkulator", "B": "Sepeda",
                    "C": "Laptop", "D": "Sendal Jepit"},
        "answer": "C"
    },
    {
        "q": 'Saat dosen berkata "mudah kok", biasanya artinya?',
        "options": {"A": "Benar-benar mudah", "B": "Sangat mudah",
                    "C": "Bisa selesai 5 menit", "D": "Tidak semudah yang dibayangkan"},
        "answer": "D"
    },
    {
        "q": "Jika WiFi kampus mati saat presentasi maka?",
        "options": {"A": "Pulang", "B": "Menyerah",
                    "C": "Hotspot teman", "D": "Ganti kampus"},
        "answer": "C"
    },
    {
        "q": "Anak TI paling takut ketika melihat?",
        "options": {"A": "Kucing", "B": "Hujan",
                    "C": "Error sebelum deadline", "D": "Semut"},
        "answer": "C"
    },
    {
        "q": "Jika ada bug yang tiba-tiba hilang sendiri maka itu disebut?",
        "options": {"A": "Keajaiban", "B": "Mukjizat Teknologi",
                    "C": "Gangguan Dimensi", "D": "Semua jawaban benar"},
        "answer": "D"
    },
    {
        "q": "Minuman favorit saat mengerjakan tugas besar?",
        "options": {"A": "Air putih", "B": "Susu",
                    "C": "Kopi", "D": "Semua jawaban benar"},
        "answer": "D"
    },
    {
        "q": "COMPILE 2026 adalah?",
        "options": {"A": "Event futsal", "B": "Event memasak",
                    "C": "Event memancing", "D": "Program pengenalan dan eksplorasi HMTI"},
        "answer": "D"
    },
]


def get_random_questions(n=10):
    """Ambil n soal secara random dari pool, tanpa pengulangan."""
    return random.sample(ALL_QUESTIONS, min(n, len(ALL_QUESTIONS)))


# ─── GESTURE CONTROLLER ───────────────────────────────────────────────────────
class GestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.5
        )
        self.move_left = False
        self.move_right = False
        self.jump = False
        self.running = False
        self.cap = None
        self.frame = None
        self.lock = threading.Lock()

    def start(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Kamera tidak tersedia, gunakan kontrol keyboard.")
            return False
        self.running = True
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()
        return True

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def _get_index_tilt(self, hand_landmarks):
        tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        dx = tip.x - wrist.x
        return dx

    def _is_pinching(self, hand_landmarks):
        thumb = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        dist = math.hypot(thumb.x - index.x, thumb.y - index.y)
        return dist < 0.06

    def _loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            ml = mr = jmp = False

            if results.multi_hand_landmarks and results.multi_handedness:
                for hand_lm, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                    label = hand_info.classification[0].label
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, hand_lm, self.mp_hands.HAND_CONNECTIONS)

                    if label == "Left":
                        dx = self._get_index_tilt(hand_lm)
                        if dx < -0.05:
                            ml = True
                        elif dx > 0.05:
                            mr = True
                    elif label == "Right":
                        if self._is_pinching(hand_lm):
                            jmp = True

            with self.lock:
                self.move_left = ml
                self.move_right = mr
                self.jump = jmp
                self.frame = frame.copy()

    def get_state(self):
        with self.lock:
            return self.move_left, self.move_right, self.jump

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None


# ─── FALLING ANSWER ───────────────────────────────────────────────────────────
class FallingAnswer:
    def __init__(self, label, text, x, speed, font_sm):
        self.label = label
        self.text = text
        self.x = x
        self.y = -80
        self.speed = speed
        self.font = font_sm
        self.collected = False
        colors = {"A": (255, 200, 60), "B": (80, 200, 120),
                  "C": (80, 180, 255), "D": (255, 100, 100)}
        self.color = colors.get(label, (200, 200, 200))

        self.lines = self._wrap(f"{label}. {text}", 200)
        self.width = 220
        self.height = max(60, len(self.lines) * 22 + 20)

    def _wrap(self, text, max_px):
        font = self.font
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_px:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def update(self):
        self.y += self.speed

    def draw(self, surf):
        if self.collected:
            return
        rect = pygame.Rect(self.x - self.width // 2, int(self.y), self.width, self.height)
        pygame.draw.rect(surf, self.color, rect, border_radius=10)
        pygame.draw.rect(surf, (255, 255, 255), rect, 2, border_radius=10)
        total_h = len(self.lines) * 22
        start_y = int(self.y) + (self.height - total_h) // 2
        for i, ln in enumerate(self.lines):
            ls = self.font.render(ln, True, (20, 20, 40))
            surf.blit(ls, ls.get_rect(centerx=self.x, y=start_y + i * 22))

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, int(self.y), self.width, self.height)

    def off_screen(self):
        return self.y > SCREEN_H


# ─── PARTICLE ─────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -1)
        self.life = random.randint(20, 40)
        self.color = color
        self.size = random.randint(3, 7)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1

    def draw(self, surf):
        alpha = max(0, self.life * 6)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        surf.blit(s, (int(self.x - self.size), int(self.y - self.size)))


# ─── GAME ─────────────────────────────────────────────────────────────────────
class HMTIGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("HMTI Bisa!")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("arialrounded", 36, bold=True)
        self.font_q = pygame.font.SysFont("arial", 22, bold=True)
        self.font_sm = pygame.font.SysFont("arial", 16, bold=True)
        self.font_score = pygame.font.SysFont("arialrounded", 28, bold=True)
        self.font_big = pygame.font.SysFont("arialrounded", 52, bold=True)

        self._load_assets()
        self.gesture = GestureController()
        self.cam_available = self.gesture.start()

        # Session questions: randomized fresh each game
        self.session_questions = []
        self._reset()

    def _load_assets(self):
        bg_path = os.path.join(ASSETS_DIR, "latarbelakanggames.webp")
        if os.path.exists(bg_path):
            bg = pygame.image.load(bg_path).convert()
            self.bg = pygame.transform.scale(bg, (SCREEN_W, SCREEN_H))
        else:
            self.bg = None

        mask_path = os.path.join(ASSETS_DIR, "maskotgames.png")
        if os.path.exists(mask_path):
            img = pygame.image.load(mask_path).convert_alpha()
            self.mascot_img = pygame.transform.scale(img, (120, 170))
        else:
            self.mascot_img = None

    def _reset(self):
        # Pick 10 random questions fresh every game
        self.session_questions = get_random_questions(10)
        self.q_index = 0
        self.score = 0
        self.state = "playing"
        self.feedback_msg = ""
        self.feedback_color = (255, 255, 255)
        self.feedback_timer = 0
        self._init_question()

    def _current_q(self):
        return self.session_questions[self.q_index]

    def _init_question(self):
        self.player_x = SCREEN_W // 2
        self.player_y = float(PLATFORM_Y - 100)
        self.vel_y = 0.0
        self.on_ground = False
        self.facing = 1
        self.answers = []
        self.particles = []
        self.jump_pressed_last = False
        self._spawn_answers()
        self.answered = False

    def _spawn_answers(self):
        q = self._current_q()
        labels = list(q["options"].keys())
        random.shuffle(labels)
        xs = [150, 350, 650, 850]
        speeds = [random.uniform(0.7, 1.2) for _ in labels]
        offsets = [random.uniform(0, 300) for _ in labels]
        self.answers = []
        for i, lbl in enumerate(labels):
            fa = FallingAnswer(lbl, q["options"][lbl], xs[i], speeds[i], self.font_sm)
            fa.y = -60 - offsets[i]
            self.answers.append(fa)

    def _wrap_text(self, text, font, max_w):
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def _draw_bg(self):
        if self.bg:
            self.screen.blit(self.bg, (0, 0))
        else:
            self.screen.fill((20, 30, 60))
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 100))
        self.screen.blit(overlay, (0, 0))

    def _draw_platform(self):
        pygame.draw.rect(self.screen, (60, 40, 20),
                         (0, PLATFORM_Y, SCREEN_W, SCREEN_H - PLATFORM_Y))
        pygame.draw.rect(self.screen, (100, 200, 100),
                         (0, PLATFORM_Y, SCREEN_W, 10))
        for gx in range(20, SCREEN_W, 60):
            pygame.draw.polygon(self.screen, (60, 180, 60), [
                (gx, PLATFORM_Y), (gx + 8, PLATFORM_Y - 12), (gx + 16, PLATFORM_Y)])

    def _draw_question(self):
        q_text = self._current_q()["q"]
        lines = self._wrap_text(q_text, self.font_q, SCREEN_W - 40)
        panel_h = len(lines) * 30 + 20
        panel = pygame.Surface((SCREEN_W - 20, panel_h), pygame.SRCALPHA)
        panel.fill((10, 20, 50, 200))
        self.screen.blit(panel, (10, 8))

        badge = self.font_sm.render(f"SOAL {self.q_index + 1}/10", True, (255, 220, 50))
        self.screen.blit(badge, (20, 10))

        for i, ln in enumerate(lines):
            surf = self.font_q.render(ln, True, (255, 255, 255))
            self.screen.blit(surf, (20, 10 + (i + 0.8) * 28))

    def _draw_score(self):
        sc = self.font_score.render(f"Nilai: {self.score}", True, (255, 220, 50))
        self.screen.blit(sc, (SCREEN_W - sc.get_width() - 15, 8))

    def _draw_player(self):
        px, py = int(self.player_x), int(self.player_y)
        if self.mascot_img:
            img = self.mascot_img if self.facing >= 0 else pygame.transform.flip(self.mascot_img, True, False)
            self.screen.blit(img, (px - 60, py - 170))
        else:
            pygame.draw.ellipse(self.screen, (255, 220, 150), (px - 18, py - 95, 36, 36))
            body_color = (30, 80, 200)
            pygame.draw.rect(self.screen, body_color, (px - 16, py - 60, 32, 40), border_radius=6)
            leg_y = py - 20
            pygame.draw.rect(self.screen, (30, 30, 100), (px - 16, leg_y, 14, 20), border_radius=4)
            pygame.draw.rect(self.screen, (30, 30, 100), (px + 2, leg_y, 14, 20), border_radius=4)

    def _draw_feedback(self):
        if self.feedback_timer > 0:
            alpha = min(255, self.feedback_timer * 8)
            surf = self.font_big.render(self.feedback_msg, True, self.feedback_color)
            s2 = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            s2.blit(surf, (0, 0))
            s2.set_alpha(alpha)
            x = SCREEN_W // 2 - surf.get_width() // 2
            self.screen.blit(s2, (x, SCREEN_H // 2 - 60))
            self.feedback_timer -= 1

    def _draw_next_button(self):
        is_last = self.q_index >= len(self.session_questions) - 1
        label = "LIHAT NILAI 🏆" if is_last else "NEXT ▶"
        bw = 220 if is_last else 180
        bx = SCREEN_W // 2 - bw // 2
        by, bh = SCREEN_H // 2 + 20, 55
        color = (255, 160, 30) if is_last else (30, 150, 255)
        pygame.draw.rect(self.screen, color, (bx, by, bw, bh), border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255), (bx, by, bw, bh), 2, border_radius=12)
        t = self.font_score.render(label, True, (255, 255, 255))
        self.screen.blit(t, t.get_rect(center=(SCREEN_W // 2, by + bh // 2)))
        return pygame.Rect(bx, by, bw, bh)

    def _draw_finished(self):
        self._draw_bg()
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 40, 200))
        self.screen.blit(overlay, (0, 0))

        title = self.font_big.render("🎉 SELESAI! 🎉", True, (255, 220, 50))
        self.screen.blit(title, title.get_rect(center=(SCREEN_W // 2, 150)))

        sc = self.font_big.render(f"Nilai Kamu: {self.score} / 100", True, (100, 255, 150))
        self.screen.blit(sc, sc.get_rect(center=(SCREEN_W // 2, 240)))

        correct = self.score // 10
        info = self.font_score.render(f"Benar: {correct}/10 Soal", True, (200, 200, 255))
        self.screen.blit(info, info.get_rect(center=(SCREEN_W // 2, 305)))

        if self.score == 100:
            grade = "SEMPURNA! HMTI BISA! 💙"
        elif self.score >= 80:
            grade = "LUAR BIASA! 🌟"
        elif self.score >= 60:
            grade = "BAGUS! TERUS BELAJAR! 📚"
        else:
            grade = "SEMANGAT! COBA LAGI! 💪"

        gs = self.font_score.render(grade, True, (255, 200, 80))
        self.screen.blit(gs, gs.get_rect(center=(SCREEN_W // 2, 365)))

        # Info soal sudah diacak
        info2 = self.font_sm.render("✨ Soal berikutnya akan diacak ulang secara otomatis!", True, (160, 200, 255))
        self.screen.blit(info2, info2.get_rect(center=(SCREEN_W // 2, 415)))

        # Restart button
        bx, by = SCREEN_W // 2 - 120, 455
        pygame.draw.rect(self.screen, (255, 80, 80), (bx, by, 240, 55), border_radius=14)
        rb = self.font_score.render("🔄 MAIN LAGI", True, (255, 255, 255))
        self.screen.blit(rb, rb.get_rect(center=(bx + 120, by + 27)))
        return pygame.Rect(bx, by, 240, 55)

    def _draw_cam_preview(self):
        frame = self.gesture.get_frame()
        if frame is None:
            return
        small = cv2.resize(frame, (200, 150))
        small_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        surf = pygame.surfarray.make_surface(small_rgb.swapaxes(0, 1))
        self.screen.blit(surf, (10, SCREEN_H - 165))
        pygame.draw.rect(self.screen, (100, 200, 255), (10, SCREEN_H - 165, 200, 150), 2)
        cam_label = self.font_sm.render("📷 Gestur Tangan", True, (100, 220, 255))
        self.screen.blit(cam_label, (10, SCREEN_H - 175))

    def _draw_controls_hint(self):
        if not self.cam_available:
            hint = self.font_sm.render("⌨  A/D: Gerak  |  SPASI: Lompat", True, (180, 180, 255))
        else:
            hint = self.font_sm.render("👋 Tangan Kiri: Tilt Telunjuk  |  Tangan Kanan: Cubit=Lompat  |  A/D/SPASI juga bisa", True, (180, 180, 255))
        self.screen.blit(hint, (220, SCREEN_H - 22))

    def run(self):
        next_btn_rect = None
        restart_btn_rect = None

        while True:
            dt = self.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.gesture.stop()
                    pygame.quit()
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mouse_click = True
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r and self.state == "finished":
                    self._reset()

            # ── FINISHED STATE ────────────────────────────────────────────────
            if self.state == "finished":
                restart_btn_rect = self._draw_finished()
                if mouse_click and restart_btn_rect and restart_btn_rect.collidepoint(mouse_pos):
                    self._reset()
                pygame.display.flip()
                continue

            # ── DRAW BG & PLATFORM ────────────────────────────────────────────
            self._draw_bg()
            self._draw_platform()

            # ── INPUT ─────────────────────────────────────────────────────────
            keys = pygame.key.get_pressed()
            g_left, g_right, g_jump = self.gesture.get_state()

            move_left = keys[pygame.K_a] or g_left
            move_right = keys[pygame.K_d] or g_right
            do_jump = keys[pygame.K_SPACE] or g_jump

            # ── PLAYER PHYSICS ────────────────────────────────────────────────
            if self.state == "playing":
                if move_left:
                    self.player_x -= MOVE_SPEED
                    self.facing = -1
                if move_right:
                    self.player_x += MOVE_SPEED
                    self.facing = 1

                if do_jump and self.on_ground and not self.jump_pressed_last:
                    self.vel_y = JUMP_FORCE
                    self.on_ground = False
                self.jump_pressed_last = do_jump

                self.vel_y += GRAVITY
                self.player_y += self.vel_y

                if self.player_y >= PLATFORM_Y:
                    self.player_y = float(PLATFORM_Y)
                    self.vel_y = 0
                    self.on_ground = True

                self.player_x = max(35, min(SCREEN_W - 35, self.player_x))

                for fa in self.answers:
                    fa.update()
                    fa.draw(self.screen)

                if not self.answered:
                    player_rect = pygame.Rect(int(self.player_x) - 25, int(self.player_y) - 90, 50, 90)
                    for fa in self.answers:
                        if not fa.collected and fa.get_rect().colliderect(player_rect):
                            fa.collected = True
                            correct = self._current_q()["answer"]
                            self.answered = True
                            if fa.label == correct:
                                self.score += 10
                                self.feedback_msg = "✅ BENAR! +10"
                                self.feedback_color = (80, 255, 130)
                                for _ in range(30):
                                    self.particles.append(Particle(fa.x, fa.y, (80, 255, 130)))
                            else:
                                self.feedback_msg = f"❌ Salah! Jwb: {correct}"
                                self.feedback_color = (255, 80, 80)
                                for _ in range(20):
                                    self.particles.append(Particle(fa.x, fa.y, (255, 80, 80)))
                            self.feedback_timer = 90
                            self.state = "next"
                            break

                active = [fa for fa in self.answers if not fa.collected and not fa.off_screen()]
                if not active and not self.answered:
                    self.answers = []
                    self._spawn_answers()
                else:
                    self.answers = [fa for fa in self.answers if not fa.off_screen() or fa.collected]

            elif self.state == "next":
                for fa in self.answers:
                    fa.draw(self.screen)
                next_btn_rect = self._draw_next_button()
                if mouse_click and next_btn_rect.collidepoint(mouse_pos):
                    if self.q_index >= len(self.session_questions) - 1:
                        self.state = "finished"
                    else:
                        self.q_index += 1
                        self.state = "playing"
                        self._init_question()

            for p in self.particles:
                p.update()
                p.draw(self.screen)
            self.particles = [p for p in self.particles if p.life > 0]

            self._draw_player()
            self._draw_question()
            self._draw_score()
            self._draw_feedback()
            if self.cam_available:
                self._draw_cam_preview()
            self._draw_controls_hint()

            title_surf = self.font_title.render("HMTI BISA!", True, (255, 220, 50))
            shadow = self.font_title.render("HMTI BISA!", True, (0, 0, 0))
            self.screen.blit(shadow, (SCREEN_W // 2 - title_surf.get_width() // 2 + 2, SCREEN_H - 42))
            self.screen.blit(title_surf, (SCREEN_W // 2 - title_surf.get_width() // 2, SCREEN_H - 44))

            pygame.display.flip()

        self.gesture.stop()


if __name__ == "__main__":
    game = HMTIGame()
    game.run()