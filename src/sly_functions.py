import os
from os.path import join, basename, normpath
from typing import List, Tuple

import supervisely as sly
from supervisely.io.fs import get_file_ext, get_file_name

import sly_globals as g


def get_free_name(existing_names: str, image_name: str, is_grouped: bool, group_name: str) -> str:
    """Generates new name for duplicated image name."""
    original_name = image_name
    image_name, image_ext = get_file_name(image_name), get_file_ext(image_name)
    i = 1
    if is_grouped and group_name is not None:
        image_name = f"{image_name}_{group_name}"
    res_name = f"{image_name}_{i}{image_ext}"
    while res_name in existing_names:
        i += 1
        res_name = f"{image_name}_{i}{image_ext}"
    sly.logger.warn(f"Duplicated group image {original_name} has been renamed to {res_name}")
    return res_name


def check_image_names(
    existing_names: List[str],
    image_names: List[str],
    is_grouped: bool = False,
    group_name: str = None,
) -> List[str]:
    """Checks if image names are unique and renames them if needed."""
    new_names = []
    for image_name in image_names:
        if image_name in existing_names:
            image_name = get_free_name(existing_names, image_name, is_grouped, group_name)
        existing_names.append(image_name)
        new_names.append(image_name)
    return new_names


def check_save_path(save_path: str) -> None:
    sly.fs.remove_junk_from_dir(save_path)
    if len(os.listdir(save_path)) > 1:
        raise Exception("There must be only 1 project directory in the archive")

    # checks if save path depth is correct.
    MAX_DEPTH = 3
    depth = len(save_path.split(os.sep))
    max_project_depth = max([len(path.split(os.sep)) for path, _, _ in os.walk(save_path)])
    if max_project_depth - depth != MAX_DEPTH:
        raise Exception("Project structure is incorrect. Max project structure depth should be 3.")

    # log project structure
    project_path = join(save_path, os.listdir(save_path)[0])
    sly.logger.info(f"Project path: {project_path}")
    datasets_paths = [join(project_path, i) for i in os.scandir(project_path) if i.is_dir()]
    sly.logger.info(f"{len(datasets_paths)} datasets found in project.")
    for dataset_path in datasets_paths:
        groups = [group for group in os.scandir(dataset_path) if group.is_dir()]
        single_images = [image for image in os.scandir(dataset_path) if image.is_file()]
        sly.logger.info(f"{basename(normpath(dataset_path))} dataset:")
        sly.logger.info(f"- {len(groups)} groups found in the dataset.")
        sly.logger.info(f"- {len(single_images)} single images found in the dataset.")


def download_data_from_team_files(api: sly.Api, save_path: str) -> str:
    """Download data from remote directory in Team Files."""
    api.file.download_input(save_path, log_progress=True)
    check_save_path(save_path)
    project_name = os.listdir(save_path)[0]
    project_path = join(save_path, project_name)
    return project_path


def create_project_meta_with_group_tag(group_tag_name: str) -> Tuple[sly.ProjectMeta, sly.TagMeta]:
    """Creates project meta with tag name defined by user input."""
    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_STRING)
    project_meta = sly.ProjectMeta().add_tag_meta(group_tag_meta)
    return project_meta, group_tag_meta


def upload_single_images(api, images, dataset_id, existing_names, progress):
    """Uploads single images to dataset."""
    for batch in sly.batched(images, batch_size=50):
        names = [sly.fs.get_file_name_with_ext(path) for path in batch]
        names = check_image_names(existing_names, names)
        image_infos = api.image.upload_paths(dataset_id, names, batch)
        sly.logger.warn(f"{len(image_infos)} single images will be hidden in the grouped view")
        progress.iters_done_report(len(batch))


def upload_grouped_images(api, group_dir, dataset_id, existing_names, progress):
    """Uploads grouped images to dataset."""
    group_name_tag_meta = g.project_meta.get_tag_meta(g.GROUP_TAG_NAME)
    img_paths = sly.fs.list_files(group_dir, valid_extensions=sly.image.SUPPORTED_IMG_EXTS)
    base_group_name = basename(normpath(group_dir))
    group_name = base_group_name
    batch_size, group_idx = 20, 1
    if len(img_paths) > batch_size:
        sly.logger.warn("Maximum number of images in a group is 20.")
        sly.logger.info(f"Group {group_name} will be split into several groups.")
    for batch in sly.batched(img_paths, batch_size=batch_size):
        if len(img_paths) > batch_size:
            group_name = f"{base_group_name}_{group_idx}"
            group_idx += 1
        names = [sly.fs.get_file_name_with_ext(path) for path in batch]
        names = check_image_names(existing_names, names, True, group_name)
        image_infos = api.image.upload_paths(dataset_id, names, batch)
        image_ids = [img_info.id for img_info in image_infos]
        api.image.add_tag_batch(image_ids, group_name_tag_meta.sly_id, group_name)
        progress.iters_done_report(len(batch))
