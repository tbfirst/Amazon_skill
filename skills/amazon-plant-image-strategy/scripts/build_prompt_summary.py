"""Compile exact per-image prompt text into Markdown and UTF-8 TXT; never PDF."""
import argparse
import json
import re
from pathlib import Path

ASSETS = ['DIM01', 'DETAIL01', *[f'SCENE{i:02}' for i in range(1, 5)],
          *[f'APLUS{i:02}' for i in range(1, 6)]]


def target_assets(manifest):
    mode = manifest.get('campaignMode', 'new-set')
    if mode == 'new-set':
        if 'targetAssetIds' in manifest and manifest['targetAssetIds'] != ASSETS:
            raise ValueError('new-set uses the fixed 11 asset IDs; use set-refresh for an explicit update scope')
        return ASSETS
    if mode != 'set-refresh':
        raise ValueError('Unknown campaignMode')
    selected = manifest.get('targetAssetIds')
    pattern = r'(?:MAIN01|(?:DIM|DETAIL|SCENE|APLUS)(?:0[1-9]|[1-9][0-9]))'
    if (not isinstance(selected, list) or not selected
            or not all(isinstance(v, str) and re.fullmatch(pattern, v) for v in selected)
            or len(selected) != len(set(selected))):
        raise ValueError('set-refresh requires an explicit ordered list of unique valid targetAssetIds')
    return selected


def compile_summary(project):
    project = Path(project).resolve()
    manifest = json.loads((project / 'prompt-manifest.json').read_text(encoding='utf-8-sig'))
    entries = manifest['assets']
    selected = target_assets(manifest)
    if len(entries) != len(selected) or {e['id'] for e in entries} != set(selected):
        raise ValueError('Manifest must contain exactly the selected unique asset IDs (11 for new-set)')
    by_id = {e['id']: e for e in entries}
    ready, blocked = [], []
    for asset in selected:
        entry = by_id[asset]
        status = entry['status']
        if status not in {'READY', 'PROVISIONAL', 'BLOCKED'}:
            raise ValueError(f'{asset}: invalid status')
        relative = f"prompts/{'blocked/' if status == 'BLOCKED' else ''}{asset}.txt"
        if entry['prompt'] != relative:
            raise ValueError(f'{asset}: expected prompt path {relative}')
        path = (project / relative).resolve()
        if not path.is_relative_to(project):
            raise ValueError(f'{asset}: prompt escapes project')
        body = path.read_text(encoding='utf-8-sig')
        if not body.strip():
            raise ValueError(f'{asset}: empty prompt')
        conditional = body.lstrip().startswith('CONDITIONAL DRAFT')
        if (status == 'BLOCKED') != conditional:
            raise ValueError(f'{asset}: conditional draft/status mismatch')
        if status != 'READY' and not entry.get('condition', '').strip():
            raise ValueError(f'{asset}: missing remaining condition')
        refs = entry.get('references')
        if not isinstance(refs, list) or not all(isinstance(r, str) and r.strip() for r in refs):
            raise ValueError(f'{asset}: references must be an ordered list of upload filenames/roles')
        item = (entry, relative, body)
        (blocked if status == 'BLOCKED' else ready).append(item)
    md = ['# 总提示词汇总\n\n按资产逐条复制；每次生成一张图。先按列出的顺序上传本张参考文件，再复制完整代码块。PROVISIONAL 的限制见该条说明；BLOCKED 不在可执行正文内。\n\n']
    txt = ['总提示词汇总\n按资产逐条复制，每次生成一张图；按每条参考文件顺序上传。BLOCKED 正文不进入可执行合集。\n\n']
    for entry, relative, body in ready:
        asset, status = entry['id'], entry['status']
        refs = '\n'.join(f'{i}. {r}' for i, r in enumerate(entry['references'], 1)) or '无需附件'
        note = entry.get('condition') or '无阻塞条件；成图和平台上传仍需核验。'
        fence = '`' * max(3, max((len(run) for run in re.findall(r'`+', body)), default=0) + 1)
        md.append(f'## {asset} — {status}\n\n参考文件（上传顺序）：\n\n{refs}\n\n条件：{note}\n\n[单张提示词]({relative})\n\n{fence}text\n{body}')
        md.append(('' if body.endswith('\n') else '\n') + fence + '\n\n')
        txt.append(f'===== {asset} | {status} =====\n参考文件（上传顺序）：\n{refs}\n条件：{note}\nBEGIN PROMPT\n{body}')
        txt.append(('' if body.endswith('\n') else '\n') + 'END PROMPT\n\n')
    md.append('## BLOCKED — 待补资料\n\n')
    txt.append('===== BLOCKED — 待补资料；不含可执行正文 =====\n')
    for entry, relative, _ in blocked:
        md.append(f"- {entry['id']}：{entry['condition']}；[条件草案]({relative})\n")
        txt.append(f"{entry['id']}: {entry['condition']} | {relative}\n")
    if not blocked:
        md.append('无。\n')
        txt.append('无。\n')
    # Validate all entries before replacing either summary.
    (project / 'all-prompts.md').write_text(''.join(md), encoding='utf-8')
    (project / 'all-prompts.txt').write_text(''.join(txt), encoding='utf-8')
    return {'executable': len(ready), 'blocked': len(blocked), 'total': len(entries)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(compile_summary(args.project), ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    main()
