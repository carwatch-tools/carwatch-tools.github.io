---
title: Components
description: Description of the main parts of the CARWatch framework.
menu_title: Components
menu_order: 3
full_width: true
---

# Components

## Mobile Apps

The mobile applications are used during data collection. They support reminder-based sampling workflows, barcode-based logging of saliva samples, and study setup through QR codes generated in advance.

The Android version is already part of the CARWatch ecosystem. An iOS version is under development.

## Web Interface

The web interface supports study preparation and data processing. Researchers can use it to define study parameters such as:

- number of sampling days
- number of samples per day
- sampling schedules
- study-specific configuration settings

The same interface can also be used to process exported CARWatch log files after data collection.

## Study Materials

CARWatch supports generation of barcodes for saliva sampling tubes and QR codes for app setup.

- Barcodes can encode study-specific information such as participant identifiers, study days, or sample numbers.
- QR codes can encode the study configuration and application behavior so that participants can initialize the mobile app with predefined settings.

## Log Processing

After data collection, CARWatch log files can be processed into structured datasets containing relevant timing information, including awakening and saliva sampling times where available.

In the web interface, this processing can be performed client-side in the browser.
