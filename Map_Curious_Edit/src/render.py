"""Render / export Map Curious episodes.

  python render.py 01                 full render of episode 01 -> output/01_..._Final.mp4
  python render.py 01 --stills 0.5,2  QA stills (with captions) -> qa/
  python render.py all                all four episodes
Also writes SRT, cover, beat log and audio mix.
"""
import sys, os, json, math, subprocess, importlib, time, shutil
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import EDIT, VO, W, H, FPS, SR, sfx, SFX_LEVEL

EPISODES = {'01': 'ep01_fort_jefferson', '02': 'ep02_db_cooper', '03': 'ep03_centralia', '04': 'ep04_underwater_waterfall',
            '05': 'ep05_mount_st_helens', '06': 'ep06_niagara_falls', '07': 'ep07_iceland_rift', '08': 'ep08_overseas_highway',
            '09': 'ep09_chicxulub_crater', '10': 'ep10_crater_lake', '11': 'ep11_erie_canal', '12': 'ep12_hudson_river',
            '13': 'ep13_mount_rainier', '14': 'ep14_greenland_ice', '15': 'ep15_everglades', '16': 'ep16_surtsey'}
NARRATION_GAIN_DB = 8.0
TMP = EDIT / '_render_tmp'


def load_ep(key):
    return importlib.import_module(EPISODES[key]).EP()


_EP = None


def _init_worker(key):
    global _EP
    _EP = load_ep(key)


def _frame_bytes(f):
    return _EP.frame(f / FPS).tobytes()


def _segment(args):
    key, f0, f1, path = args
    ep = load_ep(key)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
           '-pix_fmt', 'yuv420p', '-g', str(FPS * 2), '-bf', '2', '-colorspace', 'bt709', '-color_primaries', 'bt709',
           '-color_trc', 'bt709', '-x264-params', 'keyint=48:min-keyint=48:scenecut=0', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for f in range(f0, f1):
        p.stdin.write(ep.frame(f / FPS).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode:
        raise RuntimeError(f'ffmpeg failed on {path}')
    return f1 - f0, time.time() - t0


def build_audio(ep, path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ep.vo / f'{ep.slug}.mp3'), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    nar = np.frombuffer(raw, np.float32).copy()
    total = int(round(ep.nframes / FPS * SR))
    mix = np.zeros((total, 2), np.float32)
    g = 10 ** (NARRATION_GAIN_DB / 20)
    mix[:len(nar), 0] += nar[:total] * g
    mix[:len(nar), 1] += nar[:total] * g
    for t, kind, off in ep.sfx_events:
        s = sfx(kind) * 10 ** ((SFX_LEVEL[kind] + off) / 20)
        i = int(t * SR)
        if i >= total:
            continue
        s = s[:total - i]
        pan = 0.5
        mix[i:i + len(s), 0] += s * math.sqrt(1 - pan) * 1.41
        mix[i:i + len(s), 1] += s * math.sqrt(pan) * 1.41
    wavfile.write(path, SR, mix)


def render(key, workers=int(os.environ.get('MC_WORKERS', 4))):
    t_start = time.time()
    ep = load_ep(key)
    name = ep.out
    TMP.mkdir(exist_ok=True)
    (EDIT / 'output').mkdir(exist_ok=True); (EDIT / 'srt').mkdir(exist_ok=True); (EDIT / 'covers').mkdir(exist_ok=True)
    # captions / logs
    srt_path = EDIT / 'srt' / name.replace('.mp4', '.srt')
    srt_path.write_text(ep.caps.srt(), encoding='utf-8')
    (EDIT / 'timing' / f'{ep.slug}.beats.json').write_text(json.dumps({'beats': sorted(ep.beats), 'sfx': sorted(ep.sfx_events),
        'captions': ep.caps.groups and [{'start': round(g['start'], 3), 'end': round(g['end'], 3), 'text': g['text']} for g in ep.caps.groups],
        'caption_bounds': ep.caps.bounds()}, indent=1), encoding='utf-8')
    ep.cover().save(EDIT / 'covers' / name.replace('_Final.mp4', '_Cover.jpg'), quality=93)
    # audio
    wav = TMP / f'{key}_mix.wav'; build_audio(ep, wav)
    # frames rendered by worker processes (in order) -> ONE x264 encoder (low memory)
    video = TMP / f'{key}_video.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
           '-pix_fmt', 'yuv420p', '-g', str(FPS * 2), '-colorspace', 'bt709', '-color_primaries', 'bt709',
           '-color_trc', 'bt709', '-x264-params', 'rc-lookahead=20', str(video)]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with ProcessPoolExecutor(workers, initializer=_init_worker, initargs=(key,)) as ex:
        for i, buf in enumerate(ex.map(_frame_bytes, range(ep.nframes), chunksize=6)):
            enc.stdin.write(buf)
            if i % 240 == 0:
                print(f'  {name}: frame {i}/{ep.nframes}', flush=True)
    enc.stdin.close(); enc.wait()
    if enc.returncode:
        raise RuntimeError('x264 encode failed')
    stats = [(ep.nframes, 0)]
    out = EDIT / 'output' / name
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-i', str(wav),
                    '-filter:a', 'alimiter=limit=0.85:attack=4:release=60:level=disabled',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    '-movflags', '+faststart', '-metadata', f'title={ep.title}', str(out)], check=True)
    fr = sum(s[0] for s in stats)
    print(f'{name}: {fr} frames, {ep.dur:.2f}s audio, rendered in {time.time() - t_start:.0f}s')
    return out


def stills(key, times, captions=True):
    ep = load_ep(key)
    (EDIT / 'qa').mkdir(exist_ok=True)
    paths = []
    for t in times:
        p = EDIT / 'qa' / f'{key}_t{t:05.2f}.jpg'
        ep.frame(t, captions).save(p, quality=88); paths.append(p)
    return paths


def contact(key, times, cols=6, scale=.25, captions=True):
    from PIL import Image, ImageDraw
    ep = load_ep(key)
    w, h = int(W * scale), int(H * scale)
    rows = math.ceil(len(times) / cols)
    sheet = Image.new('RGB', (cols * w, rows * (h + 26)), (30, 30, 30))
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(times):
        im = ep.frame(t, captions).resize((w, h), Image.LANCZOS)
        x, y = (i % cols) * w, (i // cols) * (h + 26)
        sheet.paste(im, (x, y + 26)); d.text((x + 6, y + 4), f'{t:.2f}s', fill=(255, 255, 255))
    (EDIT / 'qa').mkdir(exist_ok=True)
    p = EDIT / 'qa' / f'{key}_contact_{times[0]:.0f}-{times[-1]:.0f}.jpg'
    sheet.save(p, quality=85)
    return p


if __name__ == '__main__':
    key = sys.argv[1]
    keys = list(EPISODES) if key == 'all' else [key]
    if '--stills' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]
        for k in keys:
            print(stills(k, ts))
    elif '--contact' in sys.argv:
        a, b, step = [float(x) for x in sys.argv[sys.argv.index('--contact') + 1].split(',')]
        for k in keys:
            print(contact(k, list(np.arange(a, b, step))))
    else:
        for k in [k for k in keys if k != '--skip']:
            render(k)
