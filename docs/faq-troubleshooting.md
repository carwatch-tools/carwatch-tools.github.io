---
title: FAQ & Troubleshooting
description: Common questions, known issues, and troubleshooting guidance for CARWatch.
menu_title: FAQ & Troubleshooting
menu_order: 4
full_width: true
---

# FAQ & Troubleshooting

This page summarizes common support topics for CARWatch based on the current onboarding and troubleshooting slides.

## FAQ

### How can I demonstrate the CARWatch app to participants?

If you want to walk participants through the app again, use the in-app option to re-show the tutorial from the beginning.

<img class="faq-screenshot" src="/img/faq/img_carwatch_faq-001.png" alt="FAQ-Part1">

### I am using study phones and want to prepare a phone for the next participant

Before handing a study phone to the next participant:

1. delete the logs from the previous participant
2. register the CARWatch app again with the QR code for the next participant

<img class="faq-screenshot" src="/img/faq/img_carwatch_faq-002.png" alt="FAQ-Part2">

### Help, the alarms are stuck and cannot be turned off

CARWatch includes a kill switch for this case:

1. press `Kill Alarms` five times
2. this disables all alarms

This action cannot be undone, so it should only be used when alarms are stuck.

<img class="faq-screenshot" src="/img/faq/img_carwatch_faq-003.png" alt="FAQ-Part3">

## Known Issues & Troubleshooting

### The alarms do not ring, or they ring inconsistently

On some Android devices, manufacturer-specific settings can interfere with reminders and alarms even when the normal Android settings look correct.

Possible fixes:

- Turn off battery optimization for CARWatch, including manufacturer-specific battery-saving features, as described [here](https://support.alfred.camera/hc/en-us/articles/900004435343-How-do-I-turn-off-battery-optimization-to-reduce-connection-issues-Android)
- Add CARWatch to the device auto-start whitelist, as described in [this video](https://www.youtube.com/watch?v=a3SSF-e7OgI)
- Check whether the manufacturer adds extra lock-screen notification restrictions on top of standard Android settings, as described [here](https://stackoverflow.com/a/75662780)
- On Xiaomi or Redmi devices, try disabling MIUI optimization, as described in [this video](https://www.youtube.com/watch?v=uXtsiMbNwYI)

These settings differ by manufacturer and Android variant, so the exact wording of the menus may vary from device to device.

## Need More Help?

If the issue is not covered above, please open an issue in one of the [CARWatch GitHub](https://github.com/orgs/carwatch-tools/repositories) repositories or contact us directly by email.