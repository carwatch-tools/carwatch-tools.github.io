---
title: Components
description: Overview of the main software components of the CARWatch framework.
menu_title: Components
menu_order: 2
full_width: true
---

# Components

For your first study, follow the [getting-started guide](/getting-started/) from study preparation to data analysis.

## Study Manager

The Study Manager is a web-based tool for study configuration, study material preparation, and post-study log processing. It's available [here](https://carwatch-tools.github.io/study-manager/).

![Overview screenshot of the CARWatch Study Manager interface](/img/img_study_manager.png)

It can be used to:

- define study parameters
- generate barcodes and QR codes
- prepare study materials
- process exported CARWatch log files

This part of the workflow remains completely client-side in the browser, so exported study data is not uploaded to external servers for processing.

The source code for the Study Manager is available on [GitHub](https://github.com/carwatch-tools/study-manager).

## Software Packages

CARWatch provides language-specific software packages for processing CARWatch logs and saliva data after collection.

### Python Package

The [CARWatch Python package](https://github.com/carwatch-tools/carwatch-python) provides tools for loading, converting, validating, and analysing CARWatch logs and saliva data. The current version is available on [PyPi](https://pypi.org/project/carwatch/).

Install it with Python 3.10 or newer:

```bash
pip install carwatch
```

See the [package documentation](https://carwatch-python.readthedocs.io/en/latest/) for tutorials and the function reference.

### R Package

The [CARWatch R package](https://github.com/carwatch-tools/carwatch-r) is available on [CRAN](https://CRAN.R-project.org/package=carwatch).

Install it from CRAN with R 4.3 or newer:

```r
install.packages("carwatch")
library(carwatch)
```

See the [package documentation](https://carwatch-tools.github.io/carwatch-r/) for tutorials and the function reference.


## Smartphone Apps

CARWatch includes smartphone applications for Android and iOS that support the mobile part of the sampling workflow, including reminders, awakening reports, barcode-based recording of sample events, and QR-code-based study setup.

<p class="store-badges">
  <a class="store-badge store-badge-google" href="https://play.google.com/store/apps/details?id=de.fau.cs.mad.carwatch" aria-label="Get CARWatch on Google Play">
    <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" alt="Get it on Google Play">
  </a>
  <a class="store-badge store-badge-apple" href="https://apps.apple.com/de/app/carwatchapp/id6761441417" aria-label="Download CARWatch on the App Store">
    <img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us?size=250x83" alt="Download on the App Store">
  </a>
</p>

### Android App
The current Android app release is available on [Google Play](https://play.google.com/store/apps/details?id=de.fau.cs.mad.carwatch).

![CARWatch Android App](/img/img_android_app.png)

The source code is available on [GitHub](https://github.com/carwatch-tools/carwatch-android).

### iOS App

The current iOS app release is available on the [App Store](https://apps.apple.com/de/app/carwatchapp/id6761441417).

![CARWatch iOS App](/img/img_ios_app.png)

The source code is available on [GitHub](https://github.com/carwatch-tools/carwatch-ios).

## Support and contributions

CARWatch is developed across the repositories in the [CARWatch GitHub organisation](https://github.com/carwatch-tools). Use the issue tracker for the component concerned to report a bug or discuss a contribution:

- [Study Manager issues](https://github.com/carwatch-tools/study-manager/issues)
- [Android app issues](https://github.com/carwatch-tools/carwatch-android/issues)
- [iOS app issues](https://github.com/carwatch-tools/carwatch-ios/issues)
- [R package issues](https://github.com/carwatch-tools/carwatch-r/issues)
- [Python package issues](https://github.com/carwatch-tools/carwatch-python/issues)

Include the component version, relevant device or operating system, and steps to reproduce the problem. Use a minimal example without participant data in public reports.
