import re
from collections import Counter

base = 'products'
files = {}
for i in range(1, 11):
    files[f'prompt-pack-{i}'] = f'{base}/prompt-pack-{i}/prompts.md'
for n in ['ai-finance-prompt-pack', 'ai-legal-prompt-pack', 'ai-real-estate-prompt-pack']:
    files[n] = f'{base}/feature-packs/{n}/prompts.md'

PLACEHOLDER = re.compile(r'customiz?e and use the above', re.I)
results = []
all_prompts = []

for name, path in files.items():
    with open(path, encoding='utf-8') as f:
        text = f.read()
    lines = text.splitlines()
    numbered = [l for l in lines if re.match(r'^\d+\.\s', l)]
    for l in numbered:
        core = re.sub(r'^\d+\.\s*', '', l).strip().strip('"')
        norm = re.sub(r'\s+', ' ', core.lower())
        norm = re.sub(r'\[[^\]]*\]', 'X', norm)
        norm = re.sub(r'[^a-z0-9 ]', '', norm)
        all_prompts.append((name, norm))
    ph_count = sum(1 for l in lines if PLACEHOLDER.search(l))
    heads = sum(1 for l in lines if re.match(r'^##\s', l))
    word_counts = [len(re.sub(r'^\d+\.\s*', '', l).split()) for l in numbered]
    avg_w = sum(word_counts) / len(word_counts) if word_counts else 0
    thin = sum(1 for w in word_counts if w < 15)
    results.append((name, len(numbered), len(lines), heads, ph_count, round(avg_w), thin))

print(f"{'PACK':34} {'PROMPTS':>7} {'LINES':>6} {'SECTS':>5} {'PLACE':>5} {'AVGWD':>5} {'THIN':>4}")
for r in results:
    print(f"{r[0]:34} {r[1]:>7} {r[2]:>6} {r[3]:>5} {r[4]:>5} {r[5]:>5} {r[6]:>4}")

c = Counter(p[1] for p in all_prompts)
dups = {k: v for k, v in c.items() if v > 1}
print(f"\nDuplicate prompt texts (normalized, within+across): {len(dups)}")
for d, n in list(dups.items())[:10]:
    where = sorted(set(p[0] for p in all_prompts if p[1] == d))
    print(f"  x{n} in {where}: {d[:70]}")

print("\nPlaceholder lines remaining:", sum(r[4] for r in results))
print("Total prompts:", sum(r[1] for r in results))
