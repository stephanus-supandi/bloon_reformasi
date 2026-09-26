import pygame
import sys
from dataclasses import dataclass

pygame.init()

W, H = 1280, 720
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("BLOON_REFORMASI — 1997 → 2026")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 22)
SMALL = pygame.font.SysFont("consolas", 16)
BIG = pygame.font.SysFont("consolas", 42, bold=True)
TITLE = pygame.font.SysFont("consolas", 30, bold=True)

# BLOON_REFORMASI
# "BLOON — Bangsa, Lembaga, Organisasi, Opini, Nalar"
# "REFORMASI — Rekonstruksi Evolusi Fondasi, Organisasi, Regulasi,
#               Masyarakat, Administrasi, Sistem, Institusi"
#
# This is a fictionalized educational timeline/simulation.
# It is not an electoral recommendation or a ranking of political actors.

@dataclass
class Era:
    year: int
    title: str
    acronym: str
    description: str
    event_color: tuple
    effects: dict

ERAS = [
    Era(1997, "KRISMON ASIA", "KRISMON",
        "Guncangan moneter Asia. Rupiah, perbankan, dan ekonomi masuk mode DAMAGE.",
        (170, 80, 80), {"economy": -25, "institutions": -5, "society": -10}),
    Era(1998, "REFORMASI", "REFORMASI",
        "Pergantian politik besar pada 1998 membuka fase transisi baru.",
        (210, 150, 70), {"economy": -5, "institutions": 8, "society": 12}),
    Era(1999, "PEMILU", "PEMILU",
        "Pemilu 1999 menjadi salah satu tonggak awal sistem politik pasca-Reformasi.",
        (80, 150, 210), {"participation": 15, "institutions": 5}),
    Era(2000, "AMENDEMEN", "UUD-REF",
        "Perubahan konstitusi berlangsung bertahap pada 1999–2002.",
        (100, 170, 120), {"institutions": 15, "participation": 5}),
    Era(2004, "PILPRES LANGSUNG", "PILPRES",
        "Pemilihan presiden secara langsung masuk ke sistem permainan.",
        (90, 140, 220), {"participation": 12, "institutions": 8}),
    Era(2009, "PEMILU 2009", "PEMILU09",
        "Siklus pemilu nasional berikutnya: mesin demokrasi makin kompleks.",
        (90, 150, 200), {"participation": 7, "digital": 4}),
    Era(2014, "DIGITAL RISE", "DIGITAL",
        "Media sosial dan platform digital makin memengaruhi ruang publik.",
        (130, 100, 190), {"digital": 18, "society": 5}),
    Era(2019, "5-KOTAK", "SERENTAK",
        "Pemilu serentak mempertemukan banyak jenis pemilihan dalam satu hari.",
        (100, 110, 190), {"participation": 8, "digital": 10, "institutions": -2}),
    Era(2020, "PANDEMI", "COVID",
        "Pandemi menguji kapasitas administrasi, ekonomi, dan koordinasi sosial.",
        (120, 120, 120), {"economy": -12, "institutions": -4, "society": -8}),
    Era(2024, "PEMILU 2024", "PEMILU24",
        "Pemilu nasional serentak kembali menjadi milestone besar.",
        (80, 160, 210), {"participation": 10, "digital": 8, "institutions": 4}),
    Era(2026, "NOW", "2026",
        "Checkpoint: bukan ending. Reformasi diperlakukan sebagai proses yang terus bergerak.",
        (190, 120, 210), {"digital": 5, "society": 5}),
]

events = {
    1997: "BANKING.EXE: WARNING",
    1998: "SYSTEM REBOOT",
    1999: "ELECTION_ENGINE: ONLINE",
    2000: "CONSTITUTION_PATCH",
    2004: "DIRECT_ELECTION_MODE",
    2009: "ELECTION_CYCLE",
    2014: "SOCIAL_MEDIA.EXE",
    2019: "5-BALLOT MODE",
    2020: "PANDEMIC.EXCEPTION",
    2024: "NATIONAL_ELECTION",
    2026: "CURRENT_CHECKPOINT",
}

state = {
    "economy": 55,
    "institutions": 45,
    "participation": 40,
    "digital": 10,
    "society": 50,
}
year_index = 0
paused = False
auto = True
last_advance = pygame.time.get_ticks()
advance_ms = 2800

def clamp(v):
    return max(0, min(100, v))

def apply_era(era):
    for k, v in era.effects.items():
        state[k] = clamp(state.get(k, 50) + v)

# Start at 1997 with baseline; each transition applies the next era's effects.
apply_era(ERAS[0])

def reset():
    global state, year_index, paused, auto, last_advance
    state = {"economy": 55, "institutions": 45, "participation": 40, "digital": 10, "society": 50}
    year_index = 0
    paused = False
    auto = True
    apply_era(ERAS[0])
    last_advance = pygame.time.get_ticks()

def next_era():
    global year_index, last_advance
    if year_index < len(ERAS) - 1:
        year_index += 1
        apply_era(ERAS[year_index])
        last_advance = pygame.time.get_ticks()

def draw_text(txt, x, y, font=FONT, center=False):
    surf = font.render(txt, True, (235, 235, 235))
    rect = surf.get_rect()
    rect.center = (x, y) if center else rect.center
    if not center:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

def draw_bar(label, value, x, y, width=330):
    draw_text(f"{label:<14} {value:3d}", x, y, SMALL)
    pygame.draw.rect(screen, (35, 35, 42), (x, y + 24, width, 18), border_radius=4)
    pygame.draw.rect(screen, (210, 210, 220), (x, y + 24, int(width * value / 100), 18), border_radius=4)

def draw_timeline():
    y = 650
    x0, x1 = 70, 1210
    pygame.draw.line(screen, (80, 80, 90), (x0, y), (x1, y), 3)
    for i, era in enumerate(ERAS):
        x = x0 + (x1-x0) * i/(len(ERAS)-1)
        col = (240, 220, 90) if i == year_index else (130, 130, 140)
        pygame.draw.circle(screen, col, (int(x), y), 8 if i == year_index else 5)
        draw_text(str(era.year), int(x)-22, y+14, SMALL)

def draw():
    screen.fill((14, 15, 20))
    era = ERAS[year_index]

    draw_text("BLOON_REFORMASI", 50, 30, BIG)
    draw_text("BLOON = Bangsa • Lembaga • Organisasi • Opini • Nalar", 53, 82, SMALL)
    draw_text("REFORMASI = Rekonstruksi Evolusi Fondasi • Organisasi • Regulasi • Masyarakat • Administrasi • Sistem • Institusi",
              53, 105, SMALL)

    pygame.draw.rect(screen, (24, 25, 33), (45, 145, 750, 430), border_radius=14)
    draw_text(f"{era.year}  |  {era.title}", 75, 170, TITLE)
    draw_text(f"[ {era.acronym} ]", 75, 215, FONT)

    # wrapped description
    words = era.description.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if FONT.size(test)[0] > 650:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)
    for j, ln in enumerate(lines):
        draw_text(ln, 75, 260 + j*30, FONT)

    draw_text("EVENT LOG", 75, 375, TITLE)
    draw_text(events[era.year], 75, 420, FONT)
    draw_text("← / →  timeline     SPACE pause     A auto     R reset", 75, 485, SMALL)
    draw_text("ESC quit", 75, 515, SMALL)

    pygame.draw.rect(screen, (24, 25, 33), (820, 145, 415, 430), border_radius=14)
    draw_text("SYSTEM STATE", 850, 170, TITLE)
    draw_bar("ECONOMY", state["economy"], 850, 225)
    draw_bar("INSTITUTIONS", state["institutions"], 850, 300)
    draw_bar("PARTICIPATION", state["participation"], 850, 375)
    draw_bar("DIGITAL", state["digital"], 850, 450)
    draw_bar("SOCIETY", state["society"], 850, 525)

    draw_timeline()
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RIGHT:
                next_era()
            elif event.key == pygame.K_LEFT:
                if year_index > 0:
                    year_index -= 1
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_a:
                auto = not auto
            elif event.key == pygame.K_r:
                reset()

    if auto and not paused and pygame.time.get_ticks() - last_advance > advance_ms:
        next_era()

    draw()
    clock.tick(60)
