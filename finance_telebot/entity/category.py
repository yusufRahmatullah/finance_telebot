categories = {
    'Arisan+iuran': ['arisan+iuran', 'arisan iuran', 'arisan_iuran', 'arisan'],
    'Bensin': ['bensin'],
    'Bulanan': ['bulanan'],
    'Bulanan Dede': ['bulanan dede', 'bulanan-dede', 'bulanan_dede'],
    'Darurat': ['darurat'],
    'Gas+Galon': [
        'gas+galon', 'gas galon', 'gas-galon', 'gas_galon', 'gas', 'galon'
    ],
    'Internet+Pulsa': [
        'internet', 'inet', 'internet_pulsa', 'internet+pulsa', 'pulsa',
        'internet-pulsa', 'indosat', 'byu', 'by u'
    ],
    'Kontrakan': ['kontrakan'],
    'Listrik dan air': [
        'listrik', 'air', 'listrik+air', 'listrik_air', 'listrik-air',
        'listrik air'
    ],
    'Makan': ['makan'],
    'Orang Tua': ['ortu', 'orang+tua', 'orang-tua', 'orang_tua', 'orang tua'],
    'Service': ['service'],
    'Sisa': ['sisa'],
    'Skincare': ['skincare'],
    'Tabungan': ['tabungan'],
    'Tabungan Dede': [
        'tabungan dede', 'tabungan-dede', 'tabungan+dede', 'tabungan_dede'
    ],
    'Transport': ['transport'],
    'Zakat': ['zakat']
}

wallets = {
    'Amplop': ['amplop'],
    'BSM': ['bsm'],
    'Dana Sari': ['dana+sari', 'dana-sari', 'dana_sari', 'dana sari'],
    'Dana Ucup': ['dana+ucup', 'dana-ucup', 'dana_ucup', 'dana ucup'],
    'Dompet Sari': [
        'dompet+sari', 'dompet-sari', 'dompet_sari', 'dompet sari'
    ],
    'Dompet Ucup': [
        'dompet+ucup', 'dompet-ucup', 'dompet_ucup', 'dompet ucup'
    ],
    'Gopay Sari': [
        'gopay+sari', 'gopay-sari', 'gopay_sari', 'gopay sari'
    ],
    'Gopay Ucup': [
        'gopay+ucup', 'gopay-ucup', 'gopay_ucup', 'gopay ucup'
    ],
    'Jenius': ['jenius'],
    'Salary': ['salary'],
    'Shopee Pay': [
        'shopee+pay', 'shopee_pay', 'shopee-pay', 'shopee pay'
    ]
}

_reverse_categories = {}
_reverse_wallets = {}


def _generate_gategories():
    global _reverse_categories
    for cat, syns in categories.items():
        for syn in syns:
            _reverse_categories[syn] = cat


def _generate_wallets():
    global _reverse_wallets
    for wal, syns in wallets.items():
        for syn in syns:
            _reverse_wallets[syn] = wal


def find_category(category: str) -> str:
    if not _reverse_categories:
        _generate_gategories()
    return _reverse_categories[category]


def find_wallet(wallet: str) -> str:
    if not _reverse_wallets:
        _generate_wallets()
    return _reverse_wallets[wallet]
