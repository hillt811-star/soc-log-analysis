#!/usr/bin/env python3
"""
Simple auth log parser & detector
Usage: python src/parse_logs.py data/auth_logs_sample.csv
"""

import sys
import pandas as pd
from datetime import datetime

def load_csv(path):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    # normalize columns
    df.columns = [c.strip() for c in df.columns]
    return df

def summarize(df):
    total = len(df)
    by_action = df['action'].str.lower().value_counts()
    print(f"Total events: {total}")
    print("Counts by action:")
    print(by_action.to_string())
    print()

def failed_ips(df, threshold=10):
    failed = df[df['action'].str.lower() == 'failed']
    counts = failed.groupby('src_ip').size().reset_index(name='failed_count')
    counts = counts.sort_values('failed_count', ascending=False)
    suspicious = counts[counts['failed_count'] > threshold]
    return counts, suspicious

def recent_failures(df, minutes=15):
    # find bursts of failures per IP within a sliding window (simple approach)
    failed = df[df['action'].str.lower() == 'failed'].sort_values('timestamp')
    # naive detection: failed attempts within the last X minutes per IP
    now = failed['timestamp'].max()
    window_start = now - pd.Timedelta(minutes=minutes)
    recent = failed[failed['timestamp'] >= window_start]
    return recent.groupby('src_ip').size().reset_index(name='recent_failed')

def main(path):
    df = load_csv(path)
    summarize(df)
    counts, suspicious = failed_ips(df, threshold=10)
    print("Top failed-login IPs:")
    print(counts.head(20).to_string(index=False))
    print()
    if not suspicious.empty:
        print("Suspicious IPs (failed > 10):")
        print(suspicious.to_string(index=False))
    else:
        print("No IPs exceeded the failure threshold.")
    print()
    recent = recent_failures(df, minutes=15)
    if not recent.empty:
        print("Recent failures (last 15 minutes) by IP:")
        print(recent.to_string(index=False))
    print()
    # Example triage hint output
    if not suspicious.empty:
        print("Triage suggestion: Investigate IPs above; check associated usernames, timestamps, and corresponding successful logins.")
    else:
        print("Triage suggestion: Monitor for increased failure rates and correlate with other telemetry (VPN logs, firewall).")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/auth_logs_sample.csv"
    main(path)
