<div align="center" markdown>
<img src=""/>

# Import Images Groups

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a>
</p>
  
[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-pascal-voc)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-images-groups)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-groups&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-groups&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-groups&counter=runs&label=runs&123)](https://supervise.ly)

</div>

## Overview
Import images groups in [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi) and creates a new project in the current `Team` -> `Workspace`.

Application key points:
* Define group tag name in modal window when starting the application
* Grouped images will be tagged with a user defined tag (tag value type: `ANY_STRING`). e.g. tag: group_name value: car_id_105

### Project structure have to be the following:

### Archive:
**(`zip`, `tar`, `gztar`, `bztar`, or `xztar` or any other registered unpacking format)**
```text
.
└── project.zip
    └── project
        └── dataset_1
            ├── img
            │   ├── car_id_105
            │   │   ├── car_105_front.jpg
            │   │   └── car_105_top.jpg
            │   ├── car_id_202
            │   │   ├── car_202_front.jpg
            │   │   └── car_202_top.jpg
            │   ├── car_id_357
            │   │   ├── car_357_front.jpg
            │   │   └── car_357_top.jpg
            │   ├── image_1.jpg }
            │   ├── image_2.jpg } # non grouped image will be imported as a regular image
            │   └── image_3.jpg }
            └── ann # optional
                ├── car_id_105
                │   ├── car_105_front.jpg.json
                │   └── car_105_top.jpg.json
                ├── car_id_202
                │   ├── car_202_front.jpg.json
                │   └── car_202_top.jpg.json
                ├── car_id_357
                │   ├── car_357_front.jpg.json
                │   └── car_357_top.jpg.json
                ├── image_1.jpg.json }
                ├── image_2.jpg.json } # non grouped image will be imported as a regular image
                └── image_3.jpg.json }
```

### Folder:
```text
.
└── project
    └── dataset_1
        ├── img
        │   ├── car_id_105
        │   │   ├── car_105_front.jpg
        │   │   └── car_105_top.jpg
        │   ├── car_id_202
        │   │   ├── car_202_front.jpg
        │   │   └── car_202_top.jpg
        │   ├── car_id_357
        │   │   ├── car_357_front.jpg
        │   │   └── car_357_top.jpg
        │   ├── image_1.jpg }
        │   ├── image_2.jpg } # non grouped image will be imported as a regular image
        │   └── image_3.jpg }
        └── ann # optional
            ├── car_id_105
            │   ├── car_105_front.jpg.json
            │   └── car_105_top.jpg.json
            ├── car_id_202
            │   ├── car_202_front.jpg.json
            │   └── car_202_top.jpg.json
            ├── car_id_357
            │   ├── car_357_front.jpg.json
            │   └── car_357_top.jpg.json
            ├── image_1.jpg.json }
            ├── image_2.jpg.json } # non grouped image will be imported as a regular image
            └── image_3.jpg.json }
```

## How To Run 
**Step 1**: Add app to your team from [Ecosystem](https://ecosystem.supervise.ly/apps/import-images-groups).

**Step 2**: Run app from `Team` -> `Files` page.

After running the app you will be redirected to the `Tasks` page.

<img src=""/>


**Step 3**: Define group tag name in modal window.

Once app is started, new task will appear in workspace tasks. Wait for message `Application is started ...` (1) and then press `Open` button (2).

<img src=""/>
