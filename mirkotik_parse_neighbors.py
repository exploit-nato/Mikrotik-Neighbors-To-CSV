#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, csv, sys

def parse_file(input_path, output_path):
    # Regex to match key="quoted value" or key=unquotedValue
    pattern = re.compile(r'(\b[\w-]+)=(?:"([^"]*)"|(\S+))')
    blocks = []
    current = []

    # Read and group lines into neighbor blocks
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            # Skip comment lines
            if stripped.startswith('#'):
                continue
            # Blank line = end of a block
            if stripped == '':
                if current:
                    blocks.append(' '.join(current))
                    current = []
            else:
                current.append(stripped)
        # Add last block if file doesn't end with blank line
        if current:
            blocks.append(' '.join(current))

    records = []
    keys = set()

    # Parse each block
    for block in blocks:
        # Split off the leading index
        parts = block.split(' ', 1)
        idx = parts[0]
        rec = {'index': idx}
        # Find all key=value pairs
        for m in pattern.finditer(block):
            key = m.group(1)
            val = m.group(2) if m.group(2) is not None else m.group(3)
            rec[key] = val
            keys.add(key)
        records.append(rec)

    # Prepare header: index first, then sorted keys
    header = ['index'] + sorted(keys)

    # Write CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as out:
        writer = csv.DictWriter(out, fieldnames=header)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)

    print(f'Wrote {len(records)} records to {output_path}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} INPUT_FILE OUTPUT_CSV')
        sys.exit(1)
    parse_file(sys.argv[1], sys.argv[2])
