import math
import os
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from pydub import AudioSegment


ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)


@dataclass
class Segment:
    key: str
    headline_hi: str
    bullet_hi: str
    narration_hi: str
    color_bg: str
    accent: str
    icon_type: str


SEGMENTS = [
    Segment(
        key="overview",
        headline_hi="कार्यक्रम के बारे में",
        bullet_hi="राष्ट्रीय आवास सहायता योजना सुरक्षित घर दिलाने में मदद करती है।",
        narration_hi=(
            "नमस्कार। यह राष्ट्रीय आवास सहायता कार्यक्रम कम और मध्यम "
            "आय वाले परिवारों को सुरक्षित और किफायती घर उपलब्ध कराने में मदद करता है। "
            "उद्देश्य है हर नागरिक तक स्थायी छत पहुँचाना, बिना किसी जटिल प्रक्रिया के।"
        ),
        color_bg="#f4f7fb",
        accent="#0f5fa6",
        icon_type="document",
    ),
    Segment(
        key="eligibility",
        headline_hi="कौन आवेदन कर सकता है",
        bullet_hi="भारतीय नागरिक, जिनकी आय योजना की सीमा में है और जिनका अपना घर नहीं है।",
        narration_hi=(
            "इस योजना का लाभ वे नागरिक उठा सकते हैं जिनकी आय निर्धारित सीमा के भीतर है, "
            "जिनके पास स्थायी घर नहीं है, और जो सरकारी आवास मदद के पिछले लाभार्थी नहीं रहे हैं।"
        ),
        color_bg="#f8f5f0",
        accent="#c47a0f",
        icon_type="people",
    ),
    Segment(
        key="apply",
        headline_hi="ऑनलाइन आवेदन कैसे करें",
        bullet_hi="आधिकारिक पोर्टल पर जाएं, आधार और आय संबंधी विवरण भरें, दस्तावेज़ अपलोड करें।",
        narration_hi=(
            "ऑनलाइन आवेदन के लिए आधिकारिक पोर्टल पर जाएं, अपना आधार विवरण, आय और परिवार की जानकारी "
            "भरें, आवश्यक दस्तावेज़ अपलोड करें और आवेदन जमा करने से पहले सभी जानकारी की पुष्टि करें।"
        ),
        color_bg="#eef7f2",
        accent="#1f7a52",
        icon_type="laptop",
    ),
    Segment(
        key="benefits",
        headline_hi="मुख्य लाभ",
        bullet_hi="घर खरीद या निर्माण के लिए आर्थिक सहायता, सरल प्रक्रिया और समय पर सहायता।",
        narration_hi=(
            "स्वीकृति के बाद समय पर आर्थिक सहायता सीधे आपके खाते में आती है। "
            "योजना घर खरीदने, बनाने या सुधारने में सहायता देती है, और पूरी प्रक्रिया पारदर्शी तथा सरल है।"
        ),
        color_bg="#f4f0f6",
        accent="#6b2fa3",
        icon_type="home",
    ),
]

IMAGE_SIZE = (1280, 720)
TITLE_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def ensure_fonts():
    if not Path(TITLE_FONT_PATH).exists() or not Path(BODY_FONT_PATH).exists():
        raise FileNotFoundError("Required fonts not found on system.")


def draw_icon(draw: ImageDraw.ImageDraw, icon_type: str, accent: str):
    cx = IMAGE_SIZE[0] // 2
    cy = IMAGE_SIZE[1] // 2 + 40
    accent_rgb = tuple(int(accent[i : i + 2], 16) for i in (1, 3, 5))
    neutral = (245, 245, 245)
    if icon_type == "document":
        w, h = 260, 340
        draw.rounded_rectangle(
            [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
            radius=28,
            fill=neutral,
            outline=accent_rgb,
            width=6,
        )
        line_y = cy - h // 2 + 80
        for i in range(4):
            draw.line(
                [cx - w // 2 + 40, line_y + i * 55, cx + w // 2 - 40, line_y + i * 55],
                fill=accent_rgb,
                width=8,
            )
        draw.rectangle(
            [cx - w // 2 + 40, cy - h // 2 + 35, cx - w // 2 + 120, cy - h // 2 + 55],
            fill=accent_rgb,
        )
    elif icon_type == "people":
        for offset in (-120, 0, 120):
            head_radius = 65 if offset == 0 else 55
            body_width = 140 if offset == 0 else 120
            body_height = 190 if offset == 0 else 170
            head_center = (cx + offset, cy - 80)
            body_top = cy - 20
            body_bounds = [
                head_center[0] - body_width // 2,
                body_top,
                head_center[0] + body_width // 2,
                body_top + body_height,
            ]
            draw.ellipse(
                [
                    head_center[0] - head_radius,
                    head_center[1] - head_radius,
                    head_center[0] + head_radius,
                    head_center[1] + head_radius,
                ],
                fill=accent_rgb,
            )
            draw.rounded_rectangle(body_bounds, radius=60, fill=neutral)
    elif icon_type == "laptop":
        base_w, base_h = 420, 110
        screen_w, screen_h = 420, 260
        draw.rounded_rectangle(
            [cx - screen_w // 2, cy - screen_h // 2 - 60, cx + screen_w // 2, cy + screen_h // 2 - 60],
            radius=24,
            outline=accent_rgb,
            width=10,
            fill=neutral,
        )
        draw.rectangle(
            [cx - base_w // 2, cy + screen_h // 2 - 50, cx + base_w // 2, cy + screen_h // 2 + base_h - 50],
            fill=accent_rgb,
        )
        draw.polygon(
            [
                (cx - base_w // 2, cy + screen_h // 2 + base_h - 50),
                (cx + base_w // 2, cy + screen_h // 2 + base_h - 50),
                (cx + base_w // 2 + 20, cy + screen_h // 2 + base_h + 10),
                (cx - base_w // 2 - 20, cy + screen_h // 2 + base_h + 10),
            ],
            fill=accent_rgb,
        )
    elif icon_type == "home":
        house_w, house_h = 420, 280
        roof_height = 200
        draw.rectangle(
            [cx - house_w // 2, cy - house_h // 2 + 40, cx + house_w // 2, cy + house_h // 2 + 40],
            fill=neutral,
            outline=accent_rgb,
            width=8,
        )
        draw.polygon(
            [
                (cx, cy - house_h // 2 - roof_height // 2),
                (cx - house_w // 2 - 40, cy - house_h // 2 + 40),
                (cx + house_w // 2 + 40, cy - house_h // 2 + 40),
            ],
            fill=accent_rgb,
        )
        door_w = 100
        draw.rectangle(
            [cx - door_w // 2, cy + house_h // 2 - 60, cx + door_w // 2, cy + house_h // 2 + 40],
            fill=accent_rgb,
        )
        window_size = 90
        for offset in (-130, 130):
            draw.rectangle(
                [
                    cx + offset - window_size // 2,
                    cy - 20 - window_size // 2,
                    cx + offset + window_size // 2,
                    cy - 20 + window_size // 2,
                ],
                fill=accent_rgb,
            )
            draw.line(
                [
                    cx + offset - window_size // 2,
                    cy - 20,
                    cx + offset + window_size // 2,
                    cy - 20,
                ],
                fill=neutral,
                width=6,
            )
            draw.line(
                [
                    cx + offset,
                    cy - 20 - window_size // 2,
                    cx + offset,
                    cy - 20 + window_size // 2,
                ],
                fill=neutral,
                width=6,
            )


def create_slide_image(segment: Segment):
    image = Image.new("RGB", IMAGE_SIZE, segment.color_bg)
    draw = ImageDraw.Draw(image)
    ensure_fonts()
    title_font = ImageFont.truetype(TITLE_FONT_PATH, 72)
    body_font = ImageFont.truetype(BODY_FONT_PATH, 46)
    accent_rgb = tuple(int(segment.accent[i : i + 2], 16) for i in (1, 3, 5))

    heading_x, heading_y = 120, 120
    draw.text((heading_x, heading_y), segment.headline_hi, font=title_font, fill=accent_rgb)

    wrapped = textwrap.fill(segment.bullet_hi, width=24)
    draw.text((heading_x, heading_y + 140), wrapped, font=body_font, fill="#1f2933")

    draw_icon(draw, segment.icon_type, segment.accent)

    path = ASSETS_DIR / f"{segment.key}.png"
    image.save(path)
    return path


def generate_voice_segments():
    audio_paths = []
    for idx, segment in enumerate(SEGMENTS, start=1):
        tts = gTTS(text=segment.narration_hi, lang="hi", slow=False)
        path = ASSETS_DIR / f"{idx:02d}_{segment.key}.mp3"
        tts.save(path.as_posix())
        audio_paths.append(path)
    return audio_paths


def combine_voice(audio_paths):
    pre_roll = 500
    inter_gap = 400
    post_roll = 600
    combined = AudioSegment.silent(duration=pre_roll)
    durations = []
    for idx, path in enumerate(audio_paths):
        clip = AudioSegment.from_file(path)
        combined += clip
        is_last = idx == len(audio_paths) - 1
        gap = post_roll if is_last else inter_gap
        combined += AudioSegment.silent(duration=gap)
        seg_duration = (
            (pre_roll / 1000 if idx == 0 else 0)
            + clip.duration_seconds
            + (post_roll / 1000 if is_last else inter_gap / 1000)
        )
        durations.append(seg_duration)
    combined = combined.set_frame_rate(44100).set_channels(2)
    narration_path = ASSETS_DIR / "narration.wav"
    combined.export(narration_path, format="wav")
    return narration_path, durations


def render_music(duration=65):
    music_path = ASSETS_DIR / "music.wav"
    if music_path.exists():
        return music_path
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=432:duration={duration}:sample_rate=44100",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=528:duration={duration}:sample_rate=44100",
        "-filter_complex",
        "[0:a]volume=0.25[a0];[1:a]volume=0.18[a1];[a0][a1]amix=inputs=2:duration=shortest:normalize=0",
        music_path.as_posix(),
    ]
    subprocess.run(cmd, check=True)
    return music_path


def mix_audio(narration_path: Path, music_path: Path):
    final_audio = ASSETS_DIR / "final_audio.wav"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        narration_path.as_posix(),
        "-i",
        music_path.as_posix(),
        "-filter_complex",
        "[0:a]volume=1[a0];[1:a]volume=0.22[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=2",
        "-ac",
        "2",
        "-ar",
        "44100",
        final_audio.as_posix(),
    ]
    subprocess.run(cmd, check=True)
    return final_audio


def create_video_segments(durations):
    video_paths = []
    for idx, (segment, duration) in enumerate(zip(SEGMENTS, durations), start=1):
        slide_path = create_slide_image(segment)
        segment_video = ASSETS_DIR / f"{idx:02d}_{segment.key}.mp4"
        cmd = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            slide_path.as_posix(),
            "-c:v",
            "libx264",
            "-t",
            f"{duration:.2f}",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "scale=1280:720",
            segment_video.as_posix(),
        ]
        subprocess.run(cmd, check=True)
        video_paths.append(segment_video)
    return video_paths


def concat_video(video_paths, audio_path):
    list_file = ASSETS_DIR / "segments.txt"
    with list_file.open("w") as fp:
        for video in video_paths:
            fp.write(f"file '{video.as_posix()}'\n")
    output_video = ASSETS_DIR / "housing_support.mp4"
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        list_file.as_posix(),
        "-i",
        audio_path.as_posix(),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-pix_fmt",
        "yuv420p",
        output_video.as_posix(),
    ]
    subprocess.run(cmd, check=True)
    return output_video


def main():
    audio_segments = generate_voice_segments()
    narration_path, durations = combine_voice(audio_segments)
    music_path = render_music(duration=math.ceil(sum(durations)) + 5)
    final_audio = mix_audio(narration_path, music_path)
    video_paths = create_video_segments(durations)
    video_path = concat_video(video_paths, final_audio)
    print(f"Video created at {video_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
