import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ROOT = ROOT / 'sample_data'
DB = Path(os.getenv('WORKBENCH_DB', str(ROOT/'state/ledger.sqlite3')))
TITLE = '代收款划拨账'
SLUG = 'courier-cod'
KEY = '划拨单'
FIELDS = ('账务流水', '营业日', '营业截止小时')
ROLE = '同城配送资金对账员'
UNIT = '分'
SIGNATURE = '收付借贷条'
RULE_VERSION = 'courier-cod-1.0'
TABS = {'intake': '来源采信', 'contract': '字段解释', 'quality': '隔离裁决', 'domain': '归属结算', 'reconcile': '独立对账', 'runs': '批次复算', 'review': '交付复核'}
