---
title: Overview
description: Background and general purpose of the CARWatch framework.
menu_title: Overview
menu_order: 1
full_width: true
---

# Overview

CARWatch was first introduced as a smartphone application to improve the accuracy of cortisol awakening response sampling. The central idea was to support saliva sampling with automated reminders and to document sample events objectively through barcode scans.

This is important because CAR assessment is highly time-critical. Even short delays between awakening and sampling can systematically distort CAR estimates, yet such deviations are difficult to detect in unsupervised field studies when studies rely on self-reported timestamps alone.

Since then, CARWatch has developed into a broader framework. In addition to the original mobile application, the project now includes tools for:

- study configuration
- preparation of sampling materials
- processing of CARWatch log files after data collection

The framework was originally motivated by cortisol awakening response research, but it is not limited to this use case. CARWatch can also support more flexible saliva sampling protocols, including multiple sampling days, different numbers of samples per day, and combinations of relative and absolute alarms.

## Why CARWatch

Field-based saliva sampling studies often rely on procedures that are difficult to supervise directly. Delays, missed samples, or inaccurate time notes can introduce systematic bias and are regarded as a major source of inconsistent findings in CAR research.

CARWatch is intended to make these workflows easier to implement while improving documentation of when samples were actually taken. Barcode scans objectively record sample events, automated reminders support adherence, and QR-code-based setup allows predefined study settings to be transferred to the mobile app.

## Scope

CARWatch is designed as an open-source research framework. It combines software tools for study preparation, mobile support during data collection, and processing of the resulting study logs. The aim is to lower the practical barrier for more objective saliva sampling studies in everyday environments.

In the web interface, processing of exported log files can remain client-side in the browser.
