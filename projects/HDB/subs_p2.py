"""Betulkan subtitle Part 2 & kumpul jadi frasa. Guna: python3 -I subs_p2.py words.json out.js"""
import json, sys
w = json.load(open(sys.argv[1]))
fix = {0:"Dia",3:"rundingan",8:"peperangan.",9:"Baginda",16:"berunding",18:"kaum",19:"Quraisy",23:"di",24:"Makkah.",
       25:"Pada",29:"Saidina",32:"Saidina",36:"Saidina",39:"Ya",40:"Rasulullah,",48:"rundingan",53:"peperangan.",
       67:"Uthman.",69:"Sebab",70:"Saidina",71:"Uthman",80:"Diplomatik,",81:"Saidina",82:"Uthman",105:"bas."}
merge = {(10,11):"SAW", (65,66):"Saidina", (78,79):"negotiate."}
drop = {20, 68}
out, i = [], 0
while i < len(w):
    m = next(((a,b) for (a,b) in merge if a == i), None)
    if m:
        a, b = m; out.append({"w": merge[m], "s": w[a]["s"], "e": w[b]["e"]}); i = b + 1; continue
    if i not in drop:
        out.append({"w": fix.get(i, w[i]["w"].strip()), "s": w[i]["s"], "e": w[i]["e"]})
    i += 1
key = {"rundingan","peperangan.","Quraisy","Makkah.","Umar","Umar.","Uthman","Uthman.","negotiate.","Diplomatik,","pandai.","pandai"}
groups, cur = [], []
for x in out:
    if cur and (len(" ".join(c["w"] for c in cur + [x])) > 26 or x["s"] - cur[-1]["e"] > 0.35 or cur[-1]["w"][-1] in ",.?"):
        groups.append(cur); cur = []
    cur.append(x)
groups.append(cur)
for j in range(len(groups)-1, 0, -1):
    if len(groups[j]) == 1 and groups[j][0]["s"] - groups[j-1][-1]["e"] < 0.35:
        groups[j-1] += groups.pop(j)
G = [{"s": g[0]["s"], "e": g[-1]["e"], "w": [[x["w"], x["s"], int(x["w"] in key)] for x in g]} for g in groups]
open(sys.argv[2], "w").write("window.SUBS = " + json.dumps(G, ensure_ascii=False) + ";\n")
print(len(G), "frasa"); print(" / ".join(" ".join(x[0] for x in g["w"]) for g in G))
