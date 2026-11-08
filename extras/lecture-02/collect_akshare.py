"""Optional network example: immutable raw A-share data snapshot (no mock fallback)."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import akshare as ak


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--symbol', default='601318', help='Six-digit A-share code')
    parser.add_argument('--start', default='20250620', help='YYYYMMDD')
    parser.add_argument('--end', default='20250704', help='YYYYMMDD')
    parser.add_argument('--output', required=True, type=Path, help='New snapshot directory; must not exist')
    args = parser.parse_args()
    if len(args.symbol) != 6 or not args.symbol.isdigit():
        parser.error('--symbol must contain six digits')
    start = datetime.strptime(args.start, '%Y%m%d')
    end = datetime.strptime(args.end, '%Y%m%d')
    if start > end:
        parser.error('--start must not be after --end')
    if args.output.exists():
        parser.error('--output already exists; use a new snapshot directory')
    # Fetch all datasets before creating the snapshot. Errors are not converted to fake data.
    frames = {}
    for adjustment in ('', 'hfq'):
        frame = ak.stock_zh_a_hist(symbol=args.symbol, period='daily',
                                 start_date=args.start, end_date=args.end,
                                 adjust=adjustment)
        required = {'日期', '开盘', '最高', '最低', '收盘', '成交量', '成交额'}
        if frame.empty or not required.issubset(frame.columns):
            raise RuntimeError(f'Empty data or changed schema: adjust={adjustment!r}')
        if frame['日期'].duplicated().any():
            raise RuntimeError('Duplicate dates; inspect upstream before use')
        frames[adjustment or 'raw'] = frame
    if set(frames['raw']['日期']) != set(frames['hfq']['日期']):
        raise RuntimeError('raw/hfq date coverage differs; inspect the source before comparing')
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = {'source': 'AkShare / Eastmoney stock_zh_a_hist',
                'symbol': args.symbol, 'start': args.start, 'end': args.end,
                'period': 'daily', 'volume_unit': 'lot (手)', 'amount_unit': 'CNY',
                'fetched_at_utc': datetime.now(timezone.utc).isoformat(),
                'python': platform.python_version(), 'akshare': version('akshare'),
                'pandas': version('pandas'), 'files': {}}
    for adjustment, frame in frames.items():
        path = args.output / f'{args.symbol}_{adjustment}.csv'
        frame.to_csv(path, index=False, encoding='utf-8-sig')
        manifest['files'][path.name] = {'adjust': '' if adjustment == 'raw' else adjustment,
                                      'rows': len(frame),
                                      'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Saved observed market data snapshot: {args.output.resolve()}')


if __name__ == '__main__':
    main()
