import zipfile, os, hashlib

base = 'products'
out = f'{base}/bundle-all-10-packs.zip'

# Back up old zip, then rebuild with corrected content
if os.path.exists(out):
    os.replace(out, out + '.bak')

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for i in range(1, 11):
        d = f'prompt-pack-{i}'
        for fn in ['prompts.md', 'README.md']:
            path = f'{base}/{d}/{fn}'
            z.write(path, f'{d}/{fn}')

# Verify: list contents and byte-compare with disk
with zipfile.ZipFile(out) as z:
    names = z.namelist()
    print(f"Files in zip: {len(names)}")
    ok = True
    for n in names:
        disk = f'{base}/{n}'
        with open(disk, 'rb') as f:
            disk_hash = hashlib.sha256(f.read()).hexdigest()
        zbytes = z.read(n)
        zhash = hashlib.sha256(zbytes).hexdigest()
        match = disk_hash == zhash
        ok = ok and match
        if not match:
            print(f"MISMATCH: {n}")
    print("All files byte-identical to disk:", ok)
    prompts = [n for n in names if n.endswith('prompts.md')]
    print(f"prompts.md files in zip: {len(prompts)}")
    print("Size:", os.path.getsize(out), "bytes")
