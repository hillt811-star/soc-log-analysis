#!/usr/bin/env python3
"""
Generate synthetic authentication logs.

Usage:
    python data/generate_auth_logs.py --rows 1000 --out data/auth_logs_expanded.csv
"""

import csv
import random
from datetime import datetime, timedelta
import argparse

USERS = ['alice','bob','charlie','david','eve','frank','george','henry','ivan','jane','kate','liam','maria','nina']
# A few attacker-like IPs we will amplify
ATTACKER_IPS = ['198.51.100.10', '203.0.113.5']
NORMAL_IP_POOL = [f'198.51.100.{i}' for i in range(20,120)] + [f'192.0.2.{i}' for i in range(2,80)] + [f'203.0.113.{i}' for i in range(20,120)]

def random_ip():
    # bias towards attacker IPs sometimes
    if random.random() < 0.02:
        return random.choice(ATTACKER_IPS)
    return random.choice(NORMAL_IP_POOL)

def generate_rows(start_time, rows):
    rows_out = []
    t = start_time
    for i in range(rows):
        # step time forward by random seconds (to simulate logs)
        t += timedelta(seconds=random.randint(5, 300))
        user = random.choice(USERS)
        # make attacker IP create many failed attempts against 'alice' sometimes
        if random.random() < 0.06:
            ip = ATTACKER_IPS[0]
            action = 'failed' if random.random() < 0.95 else 'success'
            user = 'alice' if random.random() < 0.7 else user
        else:
            ip = random_ip()
            action = 'success' if random.random() < 0.90 else 'failed'
        message = 'Accepted password' if action == 'success' else 'Invalid password'
        rows_out.append({
            'timestamp': t.isoformat() + 'Z',
            'user': user,
            'src_ip': ip,
            'action': action,
            'message': message
        })
    return rows_out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=1000)
    parser.add_argument('--out', type=str, default='data/auth_logs_expanded.csv')
    args = parser.parse_args()
    start = datetime.utcnow() - timedelta(days=2)
    rows = generate_rows(start, args.rows)
    with open(args.out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp','user','src_ip','action','message'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {args.out} ({args.rows} rows)')

if __name__ == '__main__':
    main()
