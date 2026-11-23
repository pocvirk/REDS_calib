"""2026-11-20: FB-strength campaign (KB reds_feedback_sf.md 'Calibration levers'): do we recover the MEGATRON trend
(stronger FB -> lower M* but f_esc rising faster than 1/M* -> higher x_HII)?

usage: python -I fbtrend.py --a 0.100 --out DIR rundir:label:series ...
Per run, at the analysed snapshot closest to a (|da| < 2e-3, <rundir>/dashboard/halos_iterN.txt from run_dashboard.py):
M* in halos, intrinsic Ndot, photon-weighted global f_esc (ray-traced col 15, M1 col 10, NaN-safe), escaping rate
Ndot_esc = sum f_esc Ndot (ray-traced), and x_HII (volume) at that a from <rundir>/averages.txt (runtime, dyablo
[run] dump_averages) or <rundir>/dashboard/averages.txt. Within each series (runs ordered by M*): slope
d log f_esc / d log M* between neighbours; the MEGATRON trend is 'x_HII decreases as M* increases' (slope < -1).
Writes DIR/fbtrend_a<a>.png and DIR/fbtrend_a<a>.txt."""
import argparse, glob, os, re
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

p = argparse.ArgumentParser()
p.add_argument("runs", nargs="+")
p.add_argument("--a", type=float, required=True)
p.add_argument("--out", required=True)
A = p.parse_args()
os.makedirs(A.out, exist_ok=True)
# series key -> description on the figures (2026-11-23, PO: name the series and the closest MEGATRON recipe)
SERIES = {"A": "series A: smooth SF (closest MEGATRON recipe: smooth): eps0.03 (n/n_th)^0.5 <= 0.1, mech, t_SNII 10 Myr, SN x2/4/10, M_max 300",
          "B": "series B: bursty SF (closest MEGATRON recipe: bursty; also high eps): eps 0.3, n_th 10, mech, t_SNII 3 Myr, SN x2/5/10, M_max 300",
          "M": "pair M: smooth SF (closest MEGATRON recipe: smooth), mech SN x4, t_SNII 10 Myr: BPASS M_max 100 vs 300"}


def history(d):
    """(aexp, x_HII volume) arrays, runtime file first"""
    f = os.path.join(d, "averages.txt")
    if os.path.exists(f) and open(f).readline().startswith("# aexp one nH x"):
        t = np.loadtxt(f, ndmin=2)
        it = t[:, -1]
        keep = np.r_[it[1:] > it[:-1], True] if len(it) > 1 else np.array([True])   # monotonic (restarts truncate anyway)
        return t[keep, 0], t[keep, 3]
    f = os.path.join(d, "dashboard", "averages.txt")
    if os.path.exists(f):
        t = np.loadtxt(f, ndmin=2)
        return 1 / (1 + t[:, 2]), t[:, 3]
    return None, None


rows = []
for spec in A.runs:
    d, lab, ser = (spec.split(":") + ["", ""])[:3]
    lab = lab or os.path.basename(d)
    best = None
    for f in glob.glob(os.path.join(d, "dashboard", "halos_iter*.txt")):
        m = re.search(r"z=([0-9.]+)", open(f).readline())
        if m:
            a = 1 / (1 + float(m.group(1)))
            if abs(a - A.a) < 2e-3 and (best is None or abs(a - A.a) < abs(best[0] - A.a)):
                best = (a, f)
    aa, xx = history(d)
    if best is None:
        print(f"{lab}: no analysed snapshot near a = {A.a}")
        continue
    H = np.loadtxt(best[1], ndmin=2)
    Ms, Nd, fm1, frt = H[:, 7], H[:, 9], H[:, 10], H[:, 15]
    ok, okr = np.isfinite(fm1) & (Nd > 0), np.isfinite(frt) & (Nd > 0)
    f_m1 = (np.clip(fm1, 0, 1) * Nd)[ok].sum() / Nd[ok].sum() if ok.any() else np.nan
    f_rt = (frt * Nd)[okr].sum() / Nd[okr].sum() if okr.any() else np.nan
    if aa is not None:
        o = np.argsort(aa); aa, xx = aa[o], xx[o]
    xh = np.interp(best[0], aa, xx) if aa is not None and aa[0] - 2e-3 <= best[0] <= aa[-1] + 2e-3 else np.nan
    rows.append(dict(d=d, lab=lab, ser=ser, a=best[0], Ms=Ms.sum(), Nd=Nd[ok | okr].sum(), f_rt=f_rt, f_m1=f_m1,
                     esc=(frt * Nd)[okr].sum(), x=xh, aa=aa, xx=xx))

out = [f"a = {A.a} (z = {1 / A.a - 1:.2f})",
       f"{'series':8s} {'run':42s} {'a':>7s} {'M*[Msun]':>9s} {'Ndot':>9s} {'f_RT':>6s} {'f_M1':>6s} {'Ndot_esc':>9s} {'x_HII':>7s}"]
for r in rows:
    out.append(f"{r['ser']:8s} {r['lab']:42s} {r['a']:7.4f} {r['Ms']:9.3g} {r['Nd']:9.3g} {r['f_rt']:6.3f} {r['f_m1']:6.3f} "
               f"{r['esc']:9.3g} {r['x']:7.4f}")
out.append("\n".join([""] + [SERIES[s] for s in sorted({r["ser"] for r in rows}) if s in SERIES]))
out.append("\nper series, neighbours ordered by M*: slope s = dlog f_esc/dlog M* (RT, M1); partial MEGATRON trend if s < 0 "
           "(f_esc anticorrelated with M*), full if also x_HII rises as M* falls (needs s < ~-1)")
for ser in sorted({r["ser"] for r in rows}):
    S = sorted([r for r in rows if r["ser"] == ser], key=lambda r: r["Ms"])
    for lo, hi in zip(S[:-1], S[1:]):
        dl = np.log10(hi["Ms"] / lo["Ms"])
        s_rt = np.log10(hi["f_rt"] / lo["f_rt"]) / dl if dl else np.nan
        s_m1 = np.log10(hi["f_m1"] / lo["f_m1"]) / dl if dl else np.nan
        anti = lo["f_rt"] > hi["f_rt"]     # f_esc anticorrelated with M* (lower-M* run escapes more)
        verdict = ("x_HII n/a" if not (np.isfinite(lo["x"]) and np.isfinite(hi["x"])) else
                   "full MEGATRON trend (lower-M* run has higher f_esc and higher x_HII)" if anti and lo["x"] > hi["x"] else
                   "partial: f_esc anticorrelated with M*, but too shallow, more stars win on x_HII" if anti else
                   "lower-M* run ionizes more, f_esc not anticorrelated" if lo["x"] > hi["x"] else
                   "no trend: f_esc not anticorrelated, more stars win")
        out.append(f"  {ser}: {lo['lab']} (M* {lo['Ms']:.2g}, x {lo['x']:.4f}) vs {hi['lab']} (M* {hi['Ms']:.2g}, x {hi['x']:.4f}): "
                   f"s_RT {s_rt:+.2f} s_M1 {s_m1:+.2f} -> {verdict}")
txt = "\n".join(out)
print(txt)
open(os.path.join(A.out, f"fbtrend_a{A.a:.3f}.txt"), "w").write(txt + "\n")

fig, ax = plt.subplots(1, 4, figsize=(22, 5.2), constrained_layout=True)
mk = {s: m for s, m in zip(sorted({r["ser"] for r in rows}), "osD^v<>")}
for i, r in enumerate(rows):
    c = f"C{i % 10}"
    if r["aa"] is not None:
        ax[0].semilogy(1 / r["aa"] - 1, r["xx"], color=c, label=f"{r['ser']}: {r['lab']}")
    for k, (key, yl) in enumerate([("f_rt", "global f_esc (ray-traced; open: M1)"), ("x", "x_HII (volume)"), ("esc", "escaping photons/s (ray-traced)")]):
        ax[k + 1].loglog(r["Ms"], r[key], mk[r["ser"]], color=c, ms=9, label=f"{r['ser']}: {r['lab']}" if k == 0 else None)
        ax[k + 1].set(xlabel="M* in halos [Msun]", ylabel=yl)
    ax[1].loglog(r["Ms"], r["f_m1"], mk[r["ser"]], color=c, ms=9, mfc="none")
ms = np.array([r["Ms"] for r in rows])
if len(ms):
    g = np.geomspace(ms.min() / 1.5, ms.max() * 1.5, 10)
    f0 = np.nanmedian([r["f_rt"] for r in rows]); m0 = np.median(ms)
    ax[1].loglog(g, f0 * (g / m0)**-1, "k:", label="f_esc ~ 1/M* (equal photon output)")
ax[0].axvline(1 / A.a - 1, color="k", lw=.5)
ax[0].set(xlabel="z", ylabel="x_HII (volume)", title="reionization history", xlim=(16, 1 / A.a - 1 - 1.5))
ax[1].set_title(f"f_esc vs M*, z = {1 / A.a - 1:.2f}"); ax[2].set_title("x_HII vs M*"); ax[3].set_title("escaping photon rate vs M*")
for a in ax:
    a.grid(alpha=.3, which="both")
ax[0].legend(fontsize=7); ax[1].legend(fontsize=7)
fig.text(0.005, 0.005, "\n".join(SERIES[s] for s in sorted({r["ser"] for r in rows}) if s in SERIES), ha="left", va="bottom",
         fontsize=9, color="0.25")
fig.get_layout_engine().set(rect=(0, 0.13, 1, 0.87))
plt.savefig(os.path.join(A.out, f"fbtrend_a{A.a:.3f}.png"), dpi=80)
print("wrote", os.path.join(A.out, f"fbtrend_a{A.a:.3f}.png"))
