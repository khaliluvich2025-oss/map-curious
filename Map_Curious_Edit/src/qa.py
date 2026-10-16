"""Post-export QA on the actual MP4 files.

Checks: container/stream specs, duration vs MP3, last-word-to-end gap, black
frames, frozen stretches, silences, loudness, caption bounds/ text vs script,
max gap between visual beats, full re-transcription of the exported audio
(Whisper, local) compared to the script, and contact sheets extracted from the
MP4 itself.  Writes qa/qa_report.json and qa/<ep>_mp4_sheet.jpg.
"""
import sys, os, json, re, subprocess, difflib, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import EDIT, VO, CAP_X0, CAP_X1, CAP_Y0, CAP_Y1
from render import EPISODES, load_ep

OUT = EDIT / 'output'; QA = EDIT / 'qa'


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(p):
    r = run(['ffprobe', '-v', 'error', '-show_entries',
             'format=duration,bit_rate:stream=codec_type,codec_name,profile,width,height,r_frame_rate,nb_frames,pix_fmt,sample_rate,channels,duration',
             '-of', 'json', str(p)])
    return json.loads(r.stdout)


def detect(p, vf=None, af=None):
    cmd = ['ffmpeg', '-hide_banner', '-nostats', '-i', str(p)]
    cmd += (['-vf', vf, '-an'] if vf else ['-af', af, '-vn']) + ['-f', 'null', '-']
    return run(cmd).stderr


def audio(p, sr=16000):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-f', 's16le', '-ac', '1', '-ar', str(sr), '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def norm(w):
    return re.sub(r"[^a-z0-9]", '', w.lower())


def sheet(p, key, every=1.0, cols=8, w=200):
    tmp = QA / f'_frames_{key}'; tmp.mkdir(exist_ok=True)
    for f in tmp.glob('*.jpg'):
        f.unlink()
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(p), '-vf', f'fps=1/{every},scale={w}:-1', str(tmp / 'f%03d.jpg')], check=True)
    fr = sorted(tmp.glob('*.jpg'))
    ims = [Image.open(f) for f in fr]
    h = ims[0].height
    rows = math.ceil(len(ims) / cols)
    S = Image.new('RGB', (cols * w, rows * (h + 18)), (25, 25, 25)); d = ImageDraw.Draw(S)
    for i, im in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * (h + 18)
        S.paste(im, (x, y + 18)); d.text((x + 4, y + 3), f'{i * every:.0f}s', fill=(255, 255, 255))
    out = QA / f'{key}_mp4_sheet.jpg'; S.save(out, quality=85)
    return out


def main(keys):
    from faster_whisper import WhisperModel
    model = WhisperModel(__import__('os').environ.get('MC_WHISPER', 'medium.en'), device='cpu', compute_type='int8')
    report = {}
    for key in keys:
        ep = load_ep(key)
        p = OUT / ep.out
        R = {'file': ep.out}
        info = probe(p)
        v = [s for s in info['streams'] if s['codec_type'] == 'video'][0]
        a = [s for s in info['streams'] if s['codec_type'] == 'audio'][0]
        R['video'] = f"{v['codec_name']} {v.get('profile')} {v['width']}x{v['height']} {v['r_frame_rate']} {v['pix_fmt']} frames={v.get('nb_frames')}"
        R['audio'] = f"{a['codec_name']} {a['sample_rate']}Hz ch={a['channels']}"
        R['duration'] = round(float(info['format']['duration']), 3)
        R['mp3_duration'] = round(ep.dur, 3)
        R['last_word_end'] = ep.words[-1]['end']
        R['end_after_last_word'] = round(R['duration'] - ep.words[-1]['end'], 3)
        # black / freeze / silence
        bl = detect(p, vf='blackdetect=d=0.1:pix_th=0.10')
        R['black_segments'] = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', bl)
        fz = detect(p, vf='freezedetect=n=0.0008:d=1.5')
        R['frozen_segments_over_1.5s'] = re.findall(r'freeze_start: ([\d.]+)', fz)
        si = detect(p, af='silencedetect=n=-45dB:d=0.7')
        R['silences_over_0.7s'] = re.findall(r'silence_start: ([\d.]+)', si)
        ln = detect(p, af='loudnorm=print_format=json')
        j = json.loads(ln[ln.rindex('{'):ln.rindex('}') + 1])
        R['loudness_LUFS'] = float(j['input_i']); R['true_peak_dBTP'] = float(j['input_tp'])
        # narration retained: correlation with source MP3 in 1 s windows
        src = audio(ep.vo / f'{ep.slug}.mp3'); dst = audio(p)
        n = min(len(src), len(dst))
        win = 16000; cors = []
        for i in range(0, n - win, win):
            x, y = src[i:i + win], dst[i:i + win]
            if np.sqrt((x ** 2).mean()) < 1e-3:
                continue
            cors.append(float(np.corrcoef(x, y)[0, 1]))
        R['narration_corr_min'] = round(min(cors), 3); R['narration_corr_mean'] = round(float(np.mean(cors)), 3)
        R['narration_samples_src_vs_out'] = [len(src), len(dst)]
        # re-transcribe exported audio
        segs, _ = model.transcribe(dst, word_timestamps=False, condition_on_previous_text=False, beam_size=5, language='en')
        hyp = ' '.join(s.text.strip() for s in segs)
        script = re.sub(r'\[[^\]]*\]', ' ', (ep.vo / f'{ep.slug}_script.txt').read_text(encoding='utf-8'))
        A = [norm(w) for w in script.split() if norm(w)]; B = [norm(w) for w in hyp.split() if norm(w)]
        sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
        R['transcript_match'] = round(sm.ratio(), 3)
        R['transcript_diffs'] = [(t, ' '.join(A[i1:i2]), ' '.join(B[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
        R['transcript_tail'] = hyp[-90:]
        # captions
        bounds = ep.caps.bounds()
        R['caption_groups'] = len(bounds)
        R['caption_out_of_bounds'] = [b[0] for b in bounds if b[1] < CAP_X0 or b[3] > CAP_X1 or b[2] < CAP_Y0 or b[4] > CAP_Y1]
        R['caption_widest_px'] = round(max(b[3] - b[1] for b in bounds))
        R['caption_words_per_group'] = sorted({len(g['words']) for g in ep.caps.groups})
        srt = (EDIT / 'srt' / ep.out.replace('.mp4', '.srt')).read_text(encoding='utf-8')
        R['srt_has_brackets'] = bool(re.search(r'\[|\]', srt))
        srt_words = [norm(w) for ln_ in srt.splitlines() if ln_ and not ln_.isdigit() and '-->' not in ln_ for w in ln_.split()]
        R['srt_equals_script'] = srt_words == A
        # visual beats
        bt = sorted(b[0] for b in ep.beats)
        gaps = np.diff([0.0] + bt + [ep.dur])
        R['visual_beats'] = len(bt); R['max_gap_between_beats_s'] = round(float(gaps.max()), 2)
        R['sheet'] = str(sheet(p, key).name)
        report[key] = R
        print(json.dumps(R, indent=1))
    old = {}
    rp = QA / 'qa_report.json'
    if rp.exists():
        old = json.loads(rp.read_text())
    old.update(report)
    rp.write_text(json.dumps(old, indent=1))


if __name__ == '__main__':
    k = sys.argv[1] if len(sys.argv) > 1 else 'all'
    main(list(EPISODES) if k == 'all' else k.split(','))
