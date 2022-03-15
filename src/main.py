import os

import supervisely as sly

import sly_globals as g
import sly_utils


@g.my_app.callback("import-images-groups")
@sly.timeit
def import_images_groups(api: sly.Api, task_id: int, context: dict, state: dict, app_logger) -> None:
    """Import images in groups with selected tag."""
    project_dir = sly_utils.download_data_from_team_files(
        api=api, task_id=task_id, remote_path=g.INPUT_PATH, save_path=g.STORAGE_DIR)
    project_name = os.path.basename(os.path.normpath(project_dir))
    g.project_meta = sly_utils.get_project_meta(path_to_project=project_dir)
    g.project_meta, group_name_tag_meta = sly_utils.add_group_name_tag(
        project_meta=g.project_meta, group_tag_name=g.GROUP_TAG_NAME)

    new_project = api.project.create(
        workspace_id=g.WORKSPACE_ID, name=project_name, change_name_if_conflict=True)
    api.project.update_meta(id=new_project.id, meta=g.project_meta.to_json())

    datasets_paths = [os.path.join(project_dir, item) for item in os.listdir(
        project_dir) if os.path.isdir(os.path.join(project_dir, item))]

    ds_progress = sly.Progress(message="Importing Datasets",
                               total_cnt=len(datasets_paths))
    for dataset_path in datasets_paths:
        dataset_name = os.path.basename(os.path.normpath(dataset_path))
        single_images_paths, single_images_names, single_images_anns = sly_utils.process_single_images(
            dataset_path=dataset_path)
        images_by_group_paths, images_by_group_names, images_by_group_anns = sly_utils.process_images_groups(
            dataset_path=dataset_path, group_name_tag_meta=group_name_tag_meta, single_images_names=single_images_names)


        ds_images_paths = images_by_group_paths + single_images_paths
        ds_images_names = images_by_group_names + single_images_names
        ds_images_anns = images_by_group_anns + single_images_anns

        dataset = api.dataset.create(
            project_id=new_project.id, name=dataset_name, change_name_if_conflict=True)

        batch_progress = sly.Progress(message="Processing images",
                                      total_cnt=len(ds_images_paths))
        for ds_images_paths_batch, ds_images_names_batch, ds_images_anns_batch in zip(sly.batched(ds_images_paths, 50),
                                                                                      sly.batched(
                                                                                          ds_images_names, 50),
                                                                                      sly.batched(ds_images_anns, 50)):
            dst_image_infos = api.image.upload_paths(
                dataset_id=dataset.id, names=ds_images_names_batch, paths=ds_images_paths_batch)
            dst_image_ids = [img_info.id for img_info in dst_image_infos]
            api.annotation.upload_anns(
                img_ids=dst_image_ids, anns=ds_images_anns_batch)
            batch_progress.iters_done_report(len(ds_images_paths_batch))

        grouped_images_n = len(images_by_group_paths)
        single_images_n = len(single_images_paths)
        g.my_app.logger.info(
            f"{grouped_images_n} grouped images were uploaded to {dataset_name}")
        g.my_app.logger.warn(
            f"{single_images_n} images in {dataset_name} weren't attached to any group")
        ds_progress.iter_done_report()

    g.my_app.stop()


def main():
    sly.logger.info("Script arguments", extra={
        "TEAM_ID": g.TEAM_ID,
        "WORKSPACE_ID": g.WORKSPACE_ID
    })
    g.my_app.run(initial_events=[{"command": "import-images-groups"}])


if __name__ == '__main__':
    sly.main_wrapper("main", main)
