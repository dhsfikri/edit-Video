"""Betulkan subtitle Part 1 (nama/istilah) & kumpul jadi frasa. Guna: python3 -I subs_p1.py words.json out.js"""
import json, sys
w = json.load(open(sys.argv[1]))
fix = {0:"Saidina",6:"tebang",17:"sepohon",23:"Allahu",24:"a'lam",25:"bissawab.",34:"Khalifah",37:"Umar",
       54:"kesyirikan.",55:"Iaitu",66:"amalan",67:"pemujaan",77:"Saidina",82:"Maka",83:"Saidina",89:"tebang",96:"Saidina"}
merge = {(10,12):"Baiatur Ridwan,", (35,36):"Saidina", (38,40):"al-Khattab,", (79,81):"al-Khattab,"}
out, i = [], 0
while i < len(w):
    m = next(((a,b) for (a,b) in merge if a == i), None)
    if m:
        a, b = m; out.append({"w": merge[m], "s": w[a]["s"], "e": w[b]["e"]}); i = b + 1; continue
    out.append({"w": fix.get(i, w[i]["w"].strip()), "s": w[i]["s"], "e": w[i]["e"]}); i += 1
# 'peristiwa' hilang dari timestamp (jeda panjang) — sisip manual
k = next(j for j,x in enumerate(out) if x["w"]=="Adakah")
out.insert(k+1, {"w":"peristiwa","s":3.08,"e":3.6})
key = {"tebang","Baiatur","Ridwan,","sepohon","pokok.","kesyirikan.","pemujaan","tegas.","a'lam","Umar","al-Khattab,"}
# kumpul frasa: maks ~26 aksara / pecah pada tanda baca / jeda > .35s
groups, cur = [], []
for x in out:
    if cur and (len(" ".join(c["w"] for c in cur + [x])) > 26 or x["s"] - cur[-1]["e"] > 0.35 or cur[-1]["w"][-1] in ",.?"):
        groups.append(cur); cur = []
    cur.append(x)
groups.append(cur)
# cantum yatim 1 perkataan ke frasa sebelum
for j in range(len(groups)-1, 0, -1):
    if len(groups[j]) == 1 and groups[j][0]["s"] - groups[j-1][-1]["e"] < 0.35:
        groups[j-1] += groups.pop(j)
G = [{"s": g[0]["s"], "e": g[-1]["e"], "w": [[x["w"], x["s"], int(any(t in x["w"] for t in key))] for x in g]} for g in groups]
open(sys.argv[2], "w").write("window.SUBS = " + json.dumps(G, ensure_ascii=False) + ";\n")
print(len(G), "frasa"); print(" / ".join(" ".join(x[0] for x in g["w"]) for g in G))
