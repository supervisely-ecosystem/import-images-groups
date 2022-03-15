<div align="center" markdown>
<img src="https://i.imgur.com/5HiyGWS.png"/>

# Import Images Groups

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Run</a>
</p>
  
[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/import-pascal-voc)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-images-groups)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-groups&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-groups&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/import-images-groups&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview
Import images groups in [Supervisely format](https://docs.supervise.ly/data-organization/00_ann_format_navi) and creates a new project in the current `Team` -> `Workspace`.

Application key points:
* Define group tag name in modal window when starting the application
* Grouped images will be tagged with a user defined tag (tag value type: `ANY_STRING`). e.g. tag: group_name value: car_id_105
* If grouped image doesn't have annotation, it will be automatically created

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
                ├── image_2.jpg.json } # non grouped annotation will be imported as a regular annotation
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
            ├── image_2.jpg.json } # non grouped annotation will be imported as a regular annotation
            └── image_3.jpg.json }
```

# How To Run 
### 1. Add [Import Images Groups](https://ecosystem.supervise.ly/apps/import-images-groups) app to your team from Ecosystem
<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-groups" src="https://i.imgur.com/wAiE0ld.png" width="70%"/>

### 2. Run app from `Team` -> `Files` page.
<img src="https://i.imgur.com/Y0dTDzC.png"/>


### 3. Define group tag name in modal window.
<img src="https://i.imgur.com/oMCsnvK.png" width="70%"/>

### 4. Once app is started, new task will appear in workspace tasks. Wait for the app to process your data.
