---
title: Components
description: Description of the main parts of the CARWatch framework.
menu_title: Components
menu_order: 3
full_width: true
---

# Components

## Mobile Apps

The mobile applications are used during data collection. They support reminder-based sampling workflows, barcode-based recording of sample events, and study setup through QR codes generated in advance. This allows study parameters to be prepared centrally and transferred to participants with minimal manual setup.

The Android version is already part of the CARWatch ecosystem. An iOS version is under development.

## Web Interface

The web interface supports study preparation and data processing. Researchers can use it to define study parameters such as:

- number of sampling days
- number of samples per day
- sampling schedules
- study-specific configuration settings

The same interface can also be used to process exported CARWatch log files after data collection. This supports a single workflow from study preparation to structured output.

## Study Materials

CARWatch supports generation of barcodes for saliva sampling tubes and QR codes for app setup.

- Barcodes can encode study-specific information such as participant identifiers, study days, or sample numbers.
- QR codes can encode the study configuration and application behavior so that participants can initialize the mobile app with predefined settings.

## Log Processing

After data collection, CARWatch log files can be processed into structured datasets containing relevant timing information, including awakening and saliva sampling times where available. This helps turn raw event logs into data that can be used more directly in downstream analyses.

In the web interface, this processing can be performed client-side in the browser, so exported study data does not need to be uploaded to an external server for these steps.
