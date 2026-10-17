'use client';
import { useState } from 'react';
import { CheckCircle2, FileText, RotateCcw, XCircle, Search } from 'lucide-react';

/* Case #001 is entirely fictional: the islands, people and events are invented. */
const SITES = [
  { id: 'mill', name: 'Old Mill', x: 382, y: 186 },
  { id: 'hut', name: 'Shepherd’s Hut', x: 205, y: 330 },
  { id: 'chapel', name: 'Chapel', x: 540, y: 196 },
  { id: 'beach', name: 'North Beach Hut', x: 545, y: 150 },
  { id: 'boathouse', name: 'South Boathouse', x: 540, y: 300 },
  { id: 'landing', name: 'West Landing', x: 490, y: 248 },
];

interface Step { title: string; evidence: string[]; question: string; options: { id: string; label: string }[]; answer: string; why: string }
const STEPS: Step[] = [
  {
    title: 'Evidence 1 · The postcard',
    evidence: ['Postcard found in her flat, postmarked the morning she vanished:', '“Writing this from my sketching spot. The lighthouse stands due north of me, and the Twin Peaks are due west.”'],
    question: 'Which grid square was she sketching in?',
    options: [{ id: 'B2', label: 'B2' }, { id: 'D2', label: 'D2' }, { id: 'D4', label: 'D4' }, { id: 'F3', label: 'F3' }],
    answer: 'D2',
    why: 'The lighthouse is in column D, and the Twin Peaks sit on row 2. Due north of her = same column; due west of her = same row. That puts her in D2, right next to the Old Mill.',
  },
  {
    title: 'Evidence 2 · Tide table and a mill ledger',
    evidence: ['Harbor tide table: “Low tide 14:10. The sandbar is passable for one hour either side of low tide (13:10–15:10).”', 'Old Mill visitor ledger: “Signed out 13:20.” The walk from the mill to the sandbar takes about 40 minutes.'],
    question: 'Could she have crossed the sandbar to Little Corran?',
    options: [{ id: 'yes', label: 'Yes, she reached it inside the safe window' }, { id: 'no', label: 'No, the tide was already too high' }, { id: 'boat', label: 'She must have taken a boat to the lighthouse' }],
    answer: 'yes',
    why: 'Leaving at 13:20 and walking 40 minutes puts her at the sandbar at 14:00, comfortably inside the 13:10–15:10 window. She crossed to Little Corran.',
  },
  {
    title: 'Evidence 3 · The last journal page',
    evidence: ['Page torn from her journal, found at the West Landing:', '“Rested at the chapel. Then I set off again with the setting sun on my right-hand side, until I reached the water.”'],
    question: 'Which direction was she walking from the chapel?',
    options: [{ id: 'north', label: 'North' }, { id: 'south', label: 'South' }, { id: 'east', label: 'East' }, { id: 'west', label: 'West' }],
    answer: 'south',
    why: 'The sun sets in the west. If the west is on your right-hand side, you are facing south.',
  },
  {
    title: 'Final deduction',
    evidence: ['You know she crossed to Little Corran, rested at the chapel, then walked south until she reached the water.'],
    question: 'Where should the search team go? Pick on the map or below.',
    options: SITES.map((s) => ({ id: s.id, label: s.name })),
    answer: 'boathouse',
    why: 'Due south of the chapel, at the water’s edge, is the South Boathouse. That’s where the search team found her, safe, waiting out the tide with a finished map of Little Corran.',
  },
];

function CaseMap({ highlight, onPick, pickable }: { highlight?: string; onPick?: (id: string) => void; pickable: boolean }) {
  const cols = 'ABCDEF';
  return (
    <svg viewBox="0 0 600 400" className="h-auto w-full rounded-lg border border-line bg-[#0e3b52]" role="img" aria-label="Fictional map of Halvard Island and Little Corran with a lettered grid">
      <defs><pattern id="w" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 6h12" stroke="#16506b" strokeWidth="1" /></pattern></defs>
      <rect width="600" height="400" fill="url(#w)" />
      {/* Halvard Island */}
      <path d="M40 140 Q60 90 140 100 Q240 80 300 110 Q380 95 430 150 Q445 220 430 260 Q420 330 360 360 Q260 385 160 365 Q70 350 50 290 Q25 220 40 140Z" fill="#5d7a45" stroke="#d9e3b5" strokeWidth="2" />
      {/* Little Corran */}
      <path d="M485 150 Q520 125 565 140 Q590 190 580 250 Q575 305 540 318 Q500 320 487 285 Q478 220 485 150Z" fill="#6d8a50" stroke="#d9e3b5" strokeWidth="2" />
      {/* sandbar */}
      <path d="M428 246 Q458 238 488 248" stroke="#e8d7a0" strokeWidth="9" fill="none" strokeLinecap="round" strokeDasharray="2 4" />
      <text x="440" y="232" fill="#f5e7b8" fontSize="10" fontWeight="700">SANDBAR</text>
      {/* lighthouse rock */}
      <circle cx="350" cy="38" r="12" fill="#6b6b6b" stroke="#d9e3b5" strokeWidth="2" />
      <path d="M346 42 L350 22 L354 42Z" fill="#fff" /><circle cx="350" cy="22" r="3" fill="#C8F34B" />
      <text x="368" y="42" fill="#fff" fontSize="11" fontWeight="700">LIGHTHOUSE</text>
      {/* twin peaks */}
      <path d="M105 200 L125 160 L140 185 L155 158 L178 200Z" fill="#8a7a62" stroke="#f0e6d0" strokeWidth="1.5" />
      <text x="100" y="152" fill="#fff" fontSize="11" fontWeight="700">TWIN PEAKS</text>
      {/* river */}
      <path d="M150 200 Q220 240 300 255 Q340 230 382 192 M300 255 Q330 300 362 350" stroke="#7fc4ff" strokeWidth="4" fill="none" />
      {/* grid */}
      {Array.from({ length: 6 }).map((_, i) => <line key={`v${i}`} x1={i * 100} y1="0" x2={i * 100} y2="400" stroke="#ffffff" strokeOpacity=".18" />)}
      {Array.from({ length: 4 }).map((_, i) => <line key={`h${i}`} x1="0" y1={i * 100} x2="600" y2={i * 100} stroke="#ffffff" strokeOpacity=".18" />)}
      {cols.split('').map((c, i) => <text key={c} x={i * 100 + 6} y="14" fill="#C8F34B" fontSize="12" fontWeight="800">{c}</text>)}
      {[1, 2, 3, 4].map((r) => <text key={r} x="4" y={(r - 1) * 100 + 30} fill="#C8F34B" fontSize="12" fontWeight="800">{r}</text>)}
      {/* compass */}
      <g transform="translate(560 365)"><circle r="22" fill="#081521" opacity=".7" /><path d="M0 -17 L5 0 L0 17 L-5 0Z" fill="#fff" /><path d="M0 -17 L5 0 L-5 0Z" fill="#C8F34B" /><text y="-25" textAnchor="middle" fill="#fff" fontSize="11" fontWeight="800">N</text></g>
      <text x="300" y="392" textAnchor="middle" fill="#fff" fontSize="10" opacity=".8">HALVARD ISLAND · LITTLE CORRAN — FICTIONAL MAP</text>
      {SITES.map((s) => (
        <g key={s.id} onClick={() => pickable && onPick?.(s.id)} className={pickable ? 'cursor-pointer' : ''} role={pickable ? 'button' : undefined}
          tabIndex={pickable ? 0 : undefined} aria-label={pickable ? `Choose ${s.name}` : undefined}
          onKeyDown={(e) => pickable && (e.key === 'Enter' || e.key === ' ') && onPick?.(s.id)}>
          <circle cx={s.x} cy={s.y} r={highlight === s.id ? 10 : 7} fill={highlight === s.id ? '#F28B42' : '#081521'} stroke="#C8F34B" strokeWidth="2.5" />
          <text x={s.x > 520 ? s.x - 11 : s.x + 11} y={s.y + 4} textAnchor={s.x > 520 ? 'end' : 'start'} fill="#fff" fontSize="10" fontWeight="700" stroke="#081521" strokeWidth="3" paintOrder="stroke">{s.name}</text>
        </g>
      ))}
    </svg>
  );
}

export default function MapDetective() {
  const [started, setStarted] = useState(false);
  const [step, setStep] = useState(0);
  const [tries, setTries] = useState<number[]>([0, 0, 0, 0]);
  const [picked, setPicked] = useState<string | null>(null);
  const [solved, setSolved] = useState(false);
  const finished = step >= STEPS.length;
  const s = STEPS[Math.min(step, STEPS.length - 1)];
  const points = tries.reduce((sum, t, i) => sum + (i < step || (i === step && solved) ? Math.max(5, 25 - (t - 1) * 10) : 0), 0);

  const choose = (id: string) => {
    if (solved) return;
    setPicked(id);
    setTries((t) => t.map((v, i) => (i === step ? v + 1 : v)));
    if (id === s.answer) setSolved(true);
  };
  const next = () => { setStep((x) => x + 1); setPicked(null); setSolved(false); };
  const reset = () => { setStarted(false); setStep(0); setTries([0, 0, 0, 0]); setPicked(null); setSolved(false); };

  if (!started)
    return (
      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_1.2fr]">
        <div className="card p-6">
          <p className="chip !text-fire">FICTIONAL CASE · all places and people are invented</p>
          <h2 className="mt-4 font-display text-2xl font-extrabold">Case #001: The Vanishing Cartographer</h2>
          <p className="mt-3 text-mist">Mapmaker Ida Varga set out to survey two small islands and did not come home. She left behind a postcard, a ledger signature and a torn journal page. Use the map, the compass and the clues to work out where she went.</p>
          <ul className="mt-4 space-y-1 text-sm text-mist"><li>• 4 investigation steps</li><li>• 25 points per step on the first try</li><li>• Grid squares: column letter + row number</li></ul>
          <button onClick={() => setStarted(true)} className="btn-primary mt-6"><Search className="h-4 w-4" aria-hidden />Open the case file</button>
        </div>
        <CaseMap pickable={false} />
      </div>
    );

  if (finished)
    return (
      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_1.2fr]">
        <div className="card p-6" aria-live="polite">
          <p className="eyebrow">Case closed</p>
          <p className="mt-2 font-display text-4xl font-extrabold">{points} <span className="text-base text-mist">/ 100</span></p>
          <p className="mt-1 text-mist">{points >= 90 ? 'Chief Detective: flawless map reading.' : points >= 60 ? 'Senior Investigator: solid deductions.' : 'Field Agent: you got there in the end.'}</p>
          <p className="mt-4 text-sm text-mist">{STEPS[3].why}</p>
          <button onClick={reset} className="btn-primary mt-6"><RotateCcw className="h-4 w-4" aria-hidden />Play again</button>
        </div>
        <CaseMap highlight="boathouse" pickable={false} />
      </div>
    );

  return (
    <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_1.2fr]">
      <div className="card flex flex-col p-6">
        <div className="flex items-center justify-between text-sm text-mist"><span>Step {step + 1} / {STEPS.length}</span><span className="font-display font-extrabold text-lime">{points} pts</span></div>
        <h2 className="mt-4 flex items-center gap-2 font-display text-xl font-extrabold"><FileText className="h-5 w-5 text-lime" aria-hidden />{s.title}</h2>
        <div className="mt-3 space-y-2 rounded-md border border-line bg-navy p-4 text-sm leading-relaxed">{s.evidence.map((e, i) => <p key={i} className={i ? 'italic text-white' : 'text-mist'}>{e}</p>)}</div>
        <p className="mt-5 font-semibold">{s.question}</p>
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          {s.options.map((o) => {
            const st = picked === o.id ? (o.id === s.answer ? 'border-lime bg-lime/15' : 'border-red-400 bg-red-400/10') : 'border-line hover:border-lime';
            return <button key={o.id} onClick={() => choose(o.id)} disabled={solved} className={`rounded-md border px-3 py-2.5 text-left text-sm transition ${st}`}>{o.label}</button>;
          })}
        </div>
        <div aria-live="polite">
          {picked && !solved && <p className="mt-3 flex items-center gap-1.5 text-sm text-red-300"><XCircle className="h-4 w-4" aria-hidden />Not quite. Look at the map again.</p>}
          {solved && (
            <div className="mt-4 rounded-md border border-lime/50 bg-lime/10 p-4 text-sm">
              <p className="flex items-center gap-1.5 font-bold text-lime"><CheckCircle2 className="h-4 w-4" aria-hidden />Correct</p>
              <p className="mt-1 text-mist">{s.why}</p>
              <button onClick={next} className="btn-primary mt-4">{step === STEPS.length - 1 ? 'Close the case' : 'Next clue'}</button>
            </div>
          )}
        </div>
      </div>
      <CaseMap pickable={step === STEPS.length - 1 && !solved} onPick={choose} highlight={step === STEPS.length - 1 ? picked ?? undefined : undefined} />
    </div>
  );
}
