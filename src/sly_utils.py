import functools
import os
import shutil
from functools import partial
from typing import Callable, List, Tuple

import supervisely as sly
from supervisely.io.fs import (dir_exists, file_exists, get_file_ext,
                               get_file_name, get_file_name_with_ext,
                               silent_remove)

import sly_globals as g


def update_progress(count, api: sly.Api, task_id: int, progress: sly.Progress) -> None:
    count = min(count, progress.total - progress.current)
    progress.iters_done(count)
    if progress.need_report():
        progress.report_progress()


def get_progress_cb(api: sly.Api, task_id: int, message: str, total: int, is_size: bool = False,
                    func: Callable = update_progress) -> functools.partial:
    progress = sly.Progress(message, total, is_size=is_size)
    progress_cb = partial(func, api=api, task_id=task_id, progress=progress)
    progress_cb(0)
    return progress_cb


def get_free_name(group_name: str, image_name: str) -> str:
    """Generates new name for duplicated group image name."""
    original_name = image_name
    image_name, image_ext = get_file_name(image_name), get_file_ext(image_name)
    res_name = '{}_{}{}'.format(
        image_name, group_name, image_ext)
    g.my_app.logger.warn(
        f"Duplicated group image name found. Image: {original_name} has been renamed to {res_name}")
    return res_name


def check_save_path(save_path: str) -> None:
    # remove macosx folder and .DS_Store files
    if "__MACOSX" in os.listdir(save_path):
        shutil.rmtree(os.path.join(save_path, "__MACOSX"))
    for path, dir, files in os.walk(save_path):
        if ".DS_Store" in files:
            silent_remove(os.path.join(path, ".DS_Store"))

    # log project structure
    project_path = os.path.join(save_path, os.listdir(save_path)[0])
    sly.logger.info(f"Project path: {project_path}")
    sly.logger.info(f"{len(os.listdir(project_path))} datasets found in project.")
    for dataset in os.listdir(project_path):
        if not os.path.isdir(os.path.join(project_path, dataset)):
            continue
        dataset_path = os.path.join(project_path, dataset)
        groups = [group for group in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, group))]
        single_images = [image for image in os.listdir(dataset_path) if os.path.isfile(os.path.join(dataset_path, image))]
        sly.logger.info(f"{dataset} dataset:")
        sly.logger.info(f"- {len(groups)} groups found in {dataset} dataset.")
        sly.logger.info(f"- {len(single_images)} single images found in {dataset} dataset.")

    # checks if save path depth is correct.
    MAX_DEPTH = 3
    depth = len(save_path.split(os.sep))
    max_project_depth = max([len(path.split(os.sep)) for path, _, _ in os.walk(save_path)])
    if max_project_depth - depth > MAX_DEPTH:
        sly.logger.warn("Project depth is too big. Please, check your project structure.")
    elif max_project_depth - depth < MAX_DEPTH:
        sly.logger.warn("Project depth is too small. Please, check your project structure.")


def download_data_from_team_files(api: sly.Api, task_id, save_path: str) -> str:
    """Download data from remote directory in Team Files."""
    project_path = None
    if g.INPUT_DIR is not None:
        remote_path = g.INPUT_DIR
        project_path = os.path.join(
            save_path, os.path.basename(os.path.normpath(remote_path)))
        sizeb = api.file.get_directory_size(g.TEAM_ID, remote_path)
        progress_cb = get_progress_cb(api=api,
                                      task_id=task_id,
                                      message=f"Downloading {remote_path.lstrip('/').rstrip('/')}",
                                      total=sizeb,
                                      is_size=True)
        api.file.download_directory(team_id=g.TEAM_ID,
                                    remote_path=remote_path,
                                    local_save_path=project_path,
                                    progress_cb=progress_cb)
        check_save_path(save_path)

    elif g.INPUT_FILE is not None:
        remote_path = g.INPUT_FILE
        save_archive_path = os.path.join(
            save_path, get_file_name_with_ext(remote_path))
        sizeb = api.file.get_info_by_path(g.TEAM_ID, remote_path).sizeb
        progress_cb = get_progress_cb(api=api,
                                      task_id=task_id,
                                      message=f"Downloading {remote_path.lstrip('/')}",
                                      total=sizeb,
                                      is_size=True)
        api.file.download(team_id=g.TEAM_ID,
                          remote_path=remote_path,
                          local_save_path=save_archive_path,
                          progress_cb=progress_cb)
        shutil.unpack_archive(save_archive_path, save_path)
        silent_remove(save_archive_path)
        check_save_path(save_path)
        if len(os.listdir(save_path)) > 1:
            g.my_app.logger.error("There must be only 1 project directory in the archive")
            raise Exception("There must be only 1 project directory in the archive")

        project_name = os.listdir(save_path)[0]
        project_path = os.path.join(save_path, project_name)
    return project_path


def create_project_meta_with_group_tag(group_tag_name: str) -> Tuple[sly.ProjectMeta, sly.TagMeta]:
    """Creates project meta with tag name defined by user input."""
    group_tag_meta = sly.TagMeta(
        group_tag_name, sly.TagValueType.ANY_STRING)
    project_meta = sly.ProjectMeta().add_tag_meta(group_tag_meta)
    return project_meta, group_tag_meta


def process_images_groups(dataset_path: str, group_name_tag_meta: sly.TagMeta, single_images_names: List[str]) -> Tuple[
    List[str], List[str], List[sly.Annotation]]:
    """Forms lists with images paths, names and anns by image groups."""
    images_by_group_paths, images_by_group_names, images_by_group_anns = [], [], []
    images_groups_paths = [os.path.join(dataset_path, item) for item in os.listdir(dataset_path) if
                           dir_exists(os.path.join(dataset_path, item))]

    for image_group_path in images_groups_paths:
        images_paths = [os.path.join(image_group_path, item) for item in os.listdir(
            image_group_path) if file_exists(os.path.join(image_group_path, item))]
        group_name = os.path.basename(os.path.normpath(image_group_path))
        group_tag = sly.Tag(meta=group_name_tag_meta, value=group_name)
        for image_path in images_paths:
            ann = sly.Annotation.from_img_path(image_path).add_tag(group_tag)
            image_name = get_file_name_with_ext(image_path)
            if image_name in images_by_group_names or image_name in single_images_names:
                image_name = get_free_name(
                    group_name=group_name, image_name=image_name)

            images_by_group_paths.append(image_path)
            images_by_group_names.append(image_name)
            images_by_group_anns.append(ann)
    return images_by_group_paths, images_by_group_names, images_by_group_anns


def process_single_images(dataset_path: str) -> Tuple[List[str], List[str], List[sly.Annotation]]:
    """Forms lists with images paths, names and anns for non group images."""
    single_images_paths, single_images_names, single_images_anns = [], [], []
    images_paths = [os.path.join(dataset_path, item) for item in os.listdir(dataset_path) if
                    file_exists(os.path.join(dataset_path, item))]

    for image_path in images_paths:
        ann = sly.Annotation.from_img_path(image_path)
        image_name = get_file_name_with_ext(image_path)
        single_images_paths.append(image_path)
        single_images_names.append(image_name)
        single_images_anns.append(ann)
    return single_images_paths, single_images_names, single_images_anns
