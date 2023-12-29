import os

from os.path import join, basename, normpath
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
    group_name_tag_meta = g.project_meta.get_tag_meta(g.DEFAULT_GROUP_NAME)

    datasets_paths = [path for path in os.scandir(project_dir) if path.is_dir()]

    ds_progress = sly.Progress(message="Importing Datasets", total_cnt=len(datasets_paths))
    for ds_path in datasets_paths:
        ds_name = os.path.basename(os.path.normpath(ds_path))
        single_imgs = sly.fs.list_files(ds_path, valid_extensions=sly.image.SUPPORTED_IMG_EXTS)
        group_imgs = list(join(ds_path, x.name) for x in os.scandir(ds_path) if x.is_dir())
        grouped_imgs = [img for group in group_imgs for img in os.scandir(group) if img.is_file()]
        total_imgs = len(single_imgs) + len(grouped_imgs)

        dataset = api.dataset.create(new_project.id, ds_name, change_name_if_conflict=True)
        existing_names = []

        b_progress = sly.Progress(message=f"Uploading images to {ds_name}", total_cnt=total_imgs)
        for batch in sly.batched(single_imgs, batch_size=50):
            names = [sly.fs.get_file_name_with_ext(path) for path in batch]
            names = f.check_image_names(existing_names, names)
            image_infos = api.image.upload_paths(dataset.id, names, batch)
            sly.logger.warn(f"{len(image_infos)} single images will be hidden in the grouped view")
            b_progress.iters_done_report(len(batch))
        for group in group_imgs:
            img_paths = sly.fs.list_files(group, valid_extensions=sly.image.SUPPORTED_IMG_EXTS)
            base_group_name = basename(normpath(group))
            group_name = base_group_name
            batch_size, group_idx = 20, 1
            if len(img_paths) > batch_size:
                sly.logger.warn("Maximum number of images in a group is 20.")
                sly.logger.info(f"Group {group_name} will be split into several groups.")

            for batch in sly.batched(img_paths, batch_size=batch_size):
                if len(img_paths) > batch_size:
                    group_name = f"{base_group_name}_{group_idx}"
                    group_idx += 1
                names = f.check_image_names(existing_names, names, True, group_name)
                names = [sly.fs.get_file_name_with_ext(path) for path in batch]
                image_infos = api.image.upload_paths(dataset.id, names, batch)
                image_ids = [img_info.id for img_info in image_infos]
                api.image.add_tag_batch(image_ids, group_name_tag_meta.sly_id, group_name)
                b_progress.iters_done_report(len(batch))

        if len(single_imgs) > 0:
            sly.logger.info(f"{len(single_imgs)} grouped images were uploaded to {ds_name}")
        if len(single_imgs) > 0:
            sly.logger.warn(f"{len(single_imgs)} images in {ds_name} weren't attached to any group")
            ds_progress.iter_done_report()

    g.my_app.stop()


@sly.handle_exceptions(has_ui=False)
def main():
    import_images_groups(api=g.api)


if __name__ == "__main__":
    sly.main_wrapper("main", main)
