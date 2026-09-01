# Splunk Detection & Dashboard — Guide

This document contains example Splunk searches, a Sigma rule, and a Simple XML dashboard layout you can import into Splunk for screenshots.

Example Splunk search (detect repeated failed logins by IP):
```
index=auth sourcetype=linux_secure action=failed
| stats count AS failed_count BY src_ip, user
| where failed_count > 10
| sort - failed_count
```

Example enrichment (add recent success for same user):
```
index=auth (action=failed OR action=success)
| stats latest(action) AS last_action latest(_time) AS last_time BY src_ip, user
| where last_action="failed"
```

Simple Sigma rule (YAML, conceptual)
```yaml
title: Multiple Failed Logins by Source IP
id: 123e4567-e89b-12d3-a456-426614174000
status: experimental
description: Detects source IPs with more than 10 failed authentication attempts.
author: Your Name
logsource:
  product: linux
detection:
  selection:
    EventID: Failed
  condition: selection | count by src_ip > 10
fields:
  - src_ip
  - user
level: medium
```

Splunk dashboard (Simple XML) — minimal panels
```xml
<dashboard>
  <label>Auth Triage</label>
  <row>
    <panel>
      <title>Top Failed IPs</title>
      <chart>
        <search>
          <query>index=auth sourcetype=linux_secure action=failed | stats count BY src_ip | sort - count | head 10</query>
        </search>
      </chart>
    </panel>
    <panel>
      <title>Failed Attempts Over Time</title>
      <chart>
        <search>
          <query>index=auth sourcetype=linux_secure action=failed | timechart span=5m count</query>
        </search>
      </chart>
    </panel>
  </row>
  <row>
    <panel>
      <title>Recent Suspicious Alerts</title>
      <table>
        <search>
          <query>index=auth sourcetype=linux_secure action=failed | stats count BY src_ip,user | where count > 5</query>
        </search>
      </table>
    </panel>
  </row>
</dashboard>
```

How to create screenshots
1. Import the dashboard XML into Splunk (Dashboards > Create New > Paste XML).
2. Run the searches (adjust index/sourcetype for your environment or upload the sample CSV to the Splunk _internal or a test index).
3. Use your OS screenshot tool or a browser extension (e.g., Full Page Screen Capture) to capture panels.
4. Save screenshots to `demo/` and link them in your project README.

Tuning notes
- Adjust thresholds by noise levels (make threshold a function of normal failing rate).
- Add whitelists for known services (e.g., monitoring checkers).
- Correlate with geolocation and ASN data for prioritization.
