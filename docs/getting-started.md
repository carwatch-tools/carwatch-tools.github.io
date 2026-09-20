---
title: Get started
description: Prepare a CARWatch study, set up participant apps, and process sampling logs.
menu_title: Get started
menu_order: 1
full_width: true
---

# Get started with CARWatch

CARWatch connects study preparation, mobile recording of sampling events, and post-study data processing. This guide is for researchers setting up a saliva sampling study. Participants should use the QR code and sampling instructions supplied by their study team.

## What study personnel need

- A sampling protocol specifying study days, sample times, and participant instructions.
- A computer with a browser to configure the study and generate barcode labels and participant QR codes in the Study Manager.
- Saliva collection tubes, blank adhesive label sheets, and a printer to prepare the sampling materials. Print the CARWatch-generated labels and attach them to the corresponding tubes before distributing them.
- For post-study processing: a browser for the Study Manager, or an R or Python environment when using the analysis packages.

## What participants need

- An Android or iOS smartphone with the CARWatch app, either their own or a study phone.
- The prepared, barcode-labelled collection tubes supplied by the study team.
- Their study QR code and sampling instructions, also supplied by the study team.

Participants use these materials to set up the app and follow the sampling procedure; study personnel configure the protocol and prepare the materials beforehand.

CARWatch records app events and sampling timestamps. Laboratory measurements, such as cortisol concentrations, are obtained separately and can then be combined with those records.

## 1. Configure the study and prepare materials

Open the [Study Manager](https://carwatch-tools.github.io/study-manager/). Define the study settings and sampling schedule, generate and print barcode labels, and attach them to the corresponding tubes. Prepare participant QR codes for app setup. Keep participant materials and their assigned sample identifiers together.

## 2. Set up the participant app

Install CARWatch from [Google Play](https://play.google.com/store/apps/details?id=de.fau.cs.mad.carwatch) or the [App Store](https://apps.apple.com/de/app/carwatchapp/id6761441417). Scan the participant's QR code to load the study settings.

Before data collection, walk through the procedure with participants: reporting awakening where required, following reminders, and scanning the correct tube when collecting each sample. Check reminder and camera permissions and run a practice session. See [FAQ & Troubleshooting](/faq-troubleshooting/) for alarm settings and preparing study phones for reuse.

## 3. Collect and transfer the logs

During the study, participants use the app to record sampling events. Afterwards, they export their logs and transfer them to the study team using the method specified in the study instructions.

The standard workflow does not automatically upload logs to a CARWatch server. Specify the transfer procedure before the study starts, and retain the original exports for reproducible processing. See the [privacy information](/privacy/) for the framework's data handling and the distinction from study-specific responsibilities.

## 4. Process the data

Choose the tool that fits the next step:

| Tool | Use it for | Start here |
| --- | --- | --- |
| Study Manager | Browser-based study preparation and processing of exported sampling logs | [Open Study Manager](https://carwatch-tools.github.io/study-manager/) |
| R package | Scripted log processing, sampling-time compliance, and analysis with laboratory saliva measurements | [R documentation](https://carwatch-tools.github.io/carwatch-r/) |
| Python package | Scripted loading, conversion, validation, and analysis of logs and saliva data | [Python documentation](https://carwatch-python.readthedocs.io/en/latest/) |

The Study Manager processes study files locally in the browser. The R and Python packages run in your own analysis environment. Installation commands and links for all tools are on the [Components page](/components/#software-packages).

Review missing or inconsistent records and sampling-time deviations before downstream analysis. When laboratory measurements are available, use the sample identifiers to connect them with the sampling records.

## Cite CARWatch and get support

Use the [citation information](/publications/#citation) when reporting a study, and record the software components and versions used. For software problems, use the relevant [issue tracker](/components/#support-and-contributions). For project and research enquiries, contact [Robert Richer](mailto:robert.richer@fau.de).
