import functools
import os
import shutil
from typing import List, Tuple, Callable
from functools import partial

import supervisely as sly
from supervisely.io.fs import (dir_exists, file_exists, get_file_name,
                               get_file_name_with_ext, get_file_ext)

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
    image_name, image_ext = get_file_name(image_name), get_file_ext(image_name)
    suffix = 1
    res_name = '{}_{}_{:03d}.{}'.format(image_name, group_name, suffix, image_ext)
    return res_name


def remote_dir_exists(api: sly.Api, team_id: int, remote_directory: str) -> bool:
    """Check if directory exists in remote Team Files storage."""
    files_infos = api.file.list(team_id=team_id, path=remote_directory)
    if len(files_infos) > 1:
        return True
    return False


def download_data_from_team_files(api: sly.Api, task_id, remote_path: str, save_path: str) -> str:
    """Download data from remote directory in Team Files."""
    if remote_dir_exists(api, g.TEAM_ID, remote_path):
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
        return project_path
    elif api.file.exists(g.TEAM_ID, remote_path):
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
        project_path = os.path.join(save_path, get_file_name(remote_path))
        shutil.unpack_archive(save_path, project_path)
        return project_path
    else:
        raise Exception("{} doesn't exists".format(remote_path))


def add_group_name_tag(project_meta: sly.ProjectMeta, group_tag_name: str) -> Tuple[sly.ProjectMeta, sly.TagMeta]:
    """Adds user input tag name to project meta."""
    group_tag = project_meta.get_tag_meta(group_tag_name)
    if group_tag is None:
        group_tag_meta = sly.TagMeta(
            group_tag_name, sly.TagValueType.ANY_STRING)
        project_meta = project_meta.add_tag_meta(group_tag_meta)
    else:
        g.my_app.logger.error(f"Tag with name {group_tag_name} already exists")
        raise Exception(f"Tag with name {group_tag_name} already exists")
    return project_meta, group_tag_meta


def get_project_meta(path_to_project: str) -> sly.ProjectMeta:
    """Get project meta from project directory or creates new meta if not found."""
    project_meta_path = os.path.join(path_to_project, "meta.json")
    if project_meta_path in os.listdir(path_to_project):
        project_meta_path = os.path.join(path_to_project, "meta.json")
        project_meta = sly.ProjectMeta.from_json(
            sly.json.load_json_file(project_meta_path))
    else:
        project_meta = sly.ProjectMeta()
    return project_meta


def process_images_groups(dataset_path: str, group_name_tag_meta: sly.TagMeta) -> Tuple[
    List[str], List[str], List[sly.Annotation]]:
    """Forms lists with images paths, names and anns by image groups."""
    images_by_group_paths, images_by_group_names, images_by_group_anns = [], [], []

    images_dir = os.path.join(dataset_path, "img")
    ann_dir = os.path.join(dataset_path, "ann")

    images_groups_paths = [os.path.join(images_dir, item) for item in os.listdir(images_dir) if
                           dir_exists(os.path.join(images_dir, item))]

    for image_group_path in images_groups_paths:
        images_paths = [os.path.join(image_group_path, item) for item in os.listdir(
            image_group_path) if file_exists(os.path.join(image_group_path, item))]
        group_name = os.path.basename(os.path.normpath(image_group_path))
        group_tag = sly.Tag(meta=group_name_tag_meta, value=group_name)
        for image_path in images_paths:
            image_name = get_file_name_with_ext(image_path)
            if image_name in images_by_group_names:
                image_name = get_free_name(group_name=group_name, image_name=image_name)

            images_by_group_paths.append(image_path)
            images_by_group_names.append(image_name)

            ann_name = image_name + ".json"
            ann_path = os.path.join(ann_dir, group_name, ann_name)
            if file_exists(ann_path):
                ann = sly.Annotation.from_json(
                    ann_path, g.project_meta).add_tag(group_tag)
            else:
                ann = sly.Annotation.from_img_path(
                    image_path).add_tag(group_tag)
            images_by_group_anns.append(ann)

    return images_by_group_paths, images_by_group_names, images_by_group_anns


def process_single_images(dataset_path: str) -> Tuple[List[str], List[str], List[sly.Annotation]]:
    """Forms lists with images paths, names and anns for non group images."""
    single_images_paths, single_images_names, single_images_anns = [], [], []

    images_dir = os.path.join(dataset_path, "img")
    ann_dir = os.path.join(dataset_path, "ann")

    images_paths = [os.path.join(images_dir, item) for item in os.listdir(images_dir) if
                    file_exists(os.path.join(images_dir, item))]

    for image_path in images_paths:
        image_name = get_file_name_with_ext(image_path)
        single_images_paths.append(image_path)
        single_images_names.append(image_name)

        ann_name = image_name + ".json"
        ann_path = os.path.join(ann_dir, image_name, ann_name)
        if file_exists(ann_path):
            ann = sly.Annotation.from_json(ann_path, g.project_meta)
        else:
            ann = sly.Annotation.from_img_path(image_path)
        single_images_anns.append(ann)

    return single_images_paths, single_images_names, single_images_anns
