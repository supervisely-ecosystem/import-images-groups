import os

import supervisely as sly

import sly_globals as g
import sly_functions as f


def import_images_groups(api: sly.Api) -> None:
    """Import images in groups with selected tag."""
    project_dir = f.download_data_from_team_files(api=api, save_path=g.TEMP_DIR)
    project_name = os.path.basename(os.path.normpath(project_dir))
    new_project = api.project.create(
        workspace_id=g.WORKSPACE_ID, name=project_name, change_name_if_conflict=True
    )
    if g.IS_DEFAULT_SETTINGS:
        api.project.set_multiview_settings(new_project.id)
    else:
        g.project_meta, group_name_tag_meta = f.create_project_meta_with_group_tag(
            group_tag_name=g.GROUP_TAG_NAME
        )
        api.project.update_meta(id=new_project.id, meta=g.project_meta.to_json())
        api.project.images_grouping(
            id=new_project.id, enable=True, tag_name=group_name_tag_meta.name, sync=g.SYNC_IMAGES
        )
    g.project_meta = sly.ProjectMeta.from_json(api.project.get_meta(new_project.id))

    datasets_paths = [path for path in os.scandir(project_dir) if path.is_dir()]

    ds_progress = sly.Progress(message="Importing Datasets", total_cnt=len(datasets_paths))
    for ds_path in datasets_paths:
        single_imgs = sly.fs.list_files(ds_path, valid_extensions=sly.image.SUPPORTED_IMG_EXTS)
        groups = list(os.path.join(ds_path, x.name) for x in os.scandir(ds_path) if x.is_dir())
        grouped_imgs_cnt = [img for group in groups for img in os.scandir(group) if img.is_file()]
        total_imgs = len(single_imgs) + len(grouped_imgs_cnt)

        ds_name = os.path.basename(os.path.normpath(ds_path))
        dataset = api.dataset.create(new_project.id, ds_name, change_name_if_conflict=True)
        b_progress = sly.Progress(message=f"Uploading images to {ds_name}", total_cnt=total_imgs)

        # create list of existing image names in dataset (for check_image_names function)
        existing_names = []

        f.upload_single_images(api, single_imgs, dataset.id, existing_names, b_progress)

        for group in groups:
            f.upload_grouped_images(api, group, dataset.id, existing_names, b_progress)

        if len(grouped_imgs_cnt) > 0:
            sly.logger.info(f"{len(grouped_imgs_cnt)} grouped images were uploaded to {ds_name}")
        if len(single_imgs) > 0:
            sly.logger.warn(f"{len(single_imgs)} images in {ds_name} weren't attached to any group")
            ds_progress.iter_done_report()

    g.my_app.stop()


@sly.handle_exceptions(has_ui=False)
def main():
    import_images_groups(api=g.api)


if __name__ == "__main__":
    sly.main_wrapper("main", main)
