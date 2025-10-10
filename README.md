<div align="center" markdown>
<img src="https://github.com/user-attachments/assets/33d3c99d-6acb-417c-b63a-c1e780989435"/>

# Import Multiview Image Groups

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Run">How To Run</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Additional-Settings">Additional Settings</a> •
  <a href="#Demo-Video">Demo Video</a>
</p>
  
[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](../../../../supervisely-ecosystem/import-images-groups)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-images-groups)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/import-images-groups.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/import-images-groups.png)](https://supervisely.com)

</div>

# Overview
Import multiview image groups and create a new project in the current `Team` -> `Workspace`.

Application key points:
* Tag for images is defined by user in the modal window when starting the app
* All images in groups in the created project will be tagged
* `Images Grouping` option will be turned on by default in the created project
* Images will be grouped by tag's value
* Tag value is defined by group directory name
* Works with `.nrrd` image format (2D only)
* Projects with `.nrrd` images format can be exported only with [Export to Supervisely format](../../../../supervisely-ecosystem/export-to-supervisely-format) app

# Preparation

**Archive** `zip`, `tar`, `tar.xz`, `tar.gz`

Archive structure:

```text
.
└── my_project.zip
    └── cars catalog 
        └── used cars 
            ├── 105 
            │   ├── car_105_front.jpg
            │   └── car_105_top.jpg
            ├── 202 
            │   ├── car_202_front.jpg
            │   └── car_202_top.jpg
            ├── 357 
            │   ├── car_357_front.jpg
            │   └── car_357_top.jpg
            ├── car_401_front.jpg
            ├── car_401_top.jpg
            └── car_401_side.jpg
```

**Folder**

Folder structure:

```text
.
└── cars catalog
    └── used cars
        ├── car_id_105
        │   ├── car_105_front.jpg
        │   └── car_105_top.jpg
        ├── car_id_202
        │   ├── car_202_front.jpg
        │   └── car_202_top.jpg
        ├── car_id_357
        │   ├── car_357_front.jpg
        │   └── car_357_top.jpg
        ├── car_401_front.jpg
        ├── car_401_top.jpg
        └── car_401_side.jpg
```

Structure explained:

1. Archive must contain only 1 project directory. Name of the project directory will be used for created supervisely project.
2. Inside project directory must be dataset directory. Name of the dataset directory will be used for created dataset. 
3. Group directories must be populated with images and placed inside dataset directory. All images inside groups will be tagged.
4. All images in the root dataset directory will be uploaded as a regular images and will not be tagged.

Example of created project using the example below and tag `car id` as user input:
* Project name: cars catalog
* Dataset name: used cars
* Images:

|     Image name     |       Tag       |
| :----------------: | :-------------: |
| car\_105_front.jpg | `car id`: `105` |
|  car\_105_top.jpg  | `car id`: `105` |
| car\_202_front.jpg | `car id`: `202` |
|  car\_202_top.jpg  | `car id`: `202` |
| car\_357_front.jpg | `car id`: `357` |
|  car\_357_top.jpg  | `car id`: `357` |
| car\_401_front.jpg |
|  car\_401_top.jpg  |
| car\_401_side.jpg  |


**Download example data:** [**IMAGES**](https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.1/cars.catalog.zip) **|** [**NRRD**](https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.1/research.zip)

Prepare project and drag and drop it to `Team Files`.

<img src="https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.2/drag-n-drop.gif?raw=true"/>

# How To Run 
**Step 1.** Add [Import Multiview Image Groups](../../../../supervisely-ecosystem/import-images-groups) app to your team from Ecosystem

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-images-groups" src="https://github.com/user-attachments/assets/1788313e-8ef3-4f42-9277-38e32aa9dfa6" width="70%"/>


**Step 2.** Run app from the context menu of your data on Team Files page:
<img src="https://i.imgur.com/Y0dTDzC.png"/>


**Step 3.** Define group tag name in modal window and enable/disable synchronized view for images group.

<img src="https://github.com/user-attachments/assets/ba14e4ea-3236-4aee-becd-aa8c3ff686c1" width="70%"/>


**Step 4.** Once app is started, new task will appear in workspace tasks. Wait for the app to process your data.

# How To Use

**Step 1.** Open imported project.

<img src="https://i.imgur.com/DAIOzN0.png"/>

**Step 2.** Open dataset using new image annotator.

<img src="https://i.imgur.com/sSCtInH.png"/>

# Additional Settings

**1.** To display single images switch off `Images Grouping` setting.

<img src="https://github.com/supervisely-ecosystem/import-images-groups/releases/download/v0.0.2/enabled-disabled.gif?raw=true"/>

**2.** If you want to disable images groupping for the whole project, go to `Project`->`Settings`->`Visuals` uncheck

<img src="https://i.imgur.com/qOGICD3.png"/>

**3.** Windowing tool is available when working with `.nrrd` files. It helps to filter pixels to see bones, air, liquids and etc

<img src="https://i.imgur.com/gW37Tyn.png"/>

**4.** Images view synchronization

<div>
  <table>
    <tr style="width: 100%">
      <td>
        <b>Synchronization OFF</b>
        <img src="https://user-images.githubusercontent.com/48913536/172838253-4817336b-814b-4504-86cc-870c6665a14b.png" style="width:100%;"/>
      </td>
      <td>
        <b>Synchronization ON</b>
        <img src="https://user-images.githubusercontent.com/48913536/172838244-45fa76cc-50e2-41e5-819a-81ceb3387ade.png" style="width:100%;"/>
      </td>
    </tr>
  </table>
</div>

# Demo Video
<a data-key="sly-embeded-video-link" href="https://www.youtube.com/watch?v=4JOjK2HlLXo" data-video-code="4JOjK2HlLXo">
    <img src="https://i.imgur.com/mb4CPK1.png" alt="SLY_EMBEDED_VIDEO_LINK"  width="70%">
</a>
