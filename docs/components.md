---
title: Components
description: Overview of the main software components of the CARWatch framework.
menu_title: Components
menu_order: 2
full_width: true
---

# Components

## Android App

The Android application is the current production app within the CARWatch ecosystem.

It supports the mobile part of the sampling workflow, including reminders, awakening reports, barcode-based recording of sample events, and QR-code-based study setup.

The current public Android release is available on Google Play:

<https://play.google.com/store/apps/details?id=de.fau.cs.mad.carwatch>

The Android app source code is available on GitHub:

<https://github.com/carwatch-tools/carwatch-android>

## iOS App

The iOS application extends the same general workflow to Apple devices and is currently under development.

A public GitHub repository link will be added here once the iOS codebase is available publicly.

## Study Manager

The Study Manager is a web-based tool for study preparation and post-study log processing.

The public Study Manager is available here:

<https://carwatch-tools.github.io/study-manager/>

The Study Manager source code is available on GitHub:

<https://github.com/carwatch-tools/study-manager>

It can be used to:

- define study parameters
- generate barcodes and QR codes
- prepare study materials
- process exported CARWatch log files

This part of the workflow remains completely client-side in the browser, so exported study data is not uploaded to external servers for processing.
