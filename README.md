<div align="center" markdown>
<img src="https://i.imgur.com/HQW7m9F.png"/>

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

# Overview
Import images groups and creates a new project in the current `Team` -> `Workspace`.

Application key points:
* Tag for images is defined by user in the modal window when starting the app
* All images in groups in the created project will be tagged
* `Images Grouping` option will be turned on by default in the created project
* Images will be grouped by tag's value
* Tag value is defined by group directory name
* Works with `.nrrd` image format (2D only)

# Preparation

Project structure have to be the following:

**Archive:**
`zip`, `tar`, `gztar`, `bztar`, or `xztar` or any other registered unpacking format
```text
.
└── project.zip
    └── project # project directory - name of created project
        └── dataset_1 # dataset directory - name of the dataset
            ├── car_id_105 # group directory - name of the group (tag value)
            │   ├── car_105_front.jpg
            │   └── car_105_top.jpg
            ├── car_id_202 # group directory - name of the group (tag value)
            │   ├── car_202_front.jpg
            │   └── car_202_top.jpg
            ├── car_id_357 # group directory - name of the group (tag value)
            │   ├── car_357_front.jpg
            │   └── car_357_top.jpg
            ├── image_1.jpg }
            ├── image_2.jpg } # images without groups will be uploaded as a regular images
            └── image_3.jpg }
```

**Folder:**
```text
.
└── project # project directory - name of created project
    └── dataset_1 # dataset directory - name of the dataset
        ├── car_id_105 # group directory - name of the group (tag value)
        │   ├── car_105_front.jpg
        │   └── car_105_top.jpg
        ├── car_id_202 # group directory - name of the group (tag value)
        │   ├── car_202_front.jpg
        │   └── car_202_top.jpg
        ├── car_id_357 # group directory - name of the group (tag value)
        │   ├── car_357_front.jpg
        │   └── car_357_top.jpg
        ├── image_1.jpg }
        ├── image_2.jpg } # images without groups will be uploaded as a regular images
        └── image_3.jpg }
```
[**Download example data**](https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.1/cars_catalog.zip)

Prepare project and drag and drop it to `Team Files`.

<img src="https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.2/drag-n-drop.gif"/>

# How To Run 
**Step 1.** Add [Import Images Groups](https://ecosystem.supervise.ly/apps/import-images-groups) app to your team from Ecosystem
<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-groups" src="https://i.imgur.com/wAiE0ld.png" width="70%"/>

**Step 2.** Run app from the context menu of your data on Team Files page:
<img src="https://i.imgur.com/Y0dTDzC.png"/>


**Step 3.** Define group tag name in modal window.
<img src="https://i.imgur.com/oMCsnvK.png" width="70%"/>

**Step 4.** Once app is started, new task will appear in workspace tasks. Wait for the app to process your data.

# How To Use
**Step 1.** Open imported project.
<img src="https://i.imgur.com/oAPlnmq.png"/>

**Step 2.** Open dataset using new image annotator.
<img src="https://i.imgur.com/sSCtInH.png"/>

**Step 3.** To display single images switch off `Images Grouping` setting.

<img src="https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.2/enabled-disabled.gif"/>
