from pathlib import Path
import imageio.v2 as imageio  # pip install imageio imageio-ffmpeg
import os

MAP_OUTPUT_DIR = "map_output"
MAP_OUTPUT_DBSCAN_DIR = "data_preprocessing/map_output/dbscan"
MAP_OUTPUT_RAW_DIR = "data_preprocessing/map_output/raw"
DBSCAN = "dbscan"
RAW = "raw"
WEEKLY_FOLDER = "weekly"
SEASONAL_FOLDER = "seasonal"

def main():
    # Map animations output.

    combine_imgs_to_video(f"{MAP_OUTPUT_DBSCAN_DIR}/{WEEKLY_FOLDER}", f"{DBSCAN}/{WEEKLY_FOLDER}", "map_output_osprey_dbscan_weekly")
    combine_imgs_to_video(f"{MAP_OUTPUT_RAW_DIR}/{WEEKLY_FOLDER}", f"{RAW}/{WEEKLY_FOLDER}", "map_output_osprey_raw_weekly")
    combine_imgs_to_video(f"{MAP_OUTPUT_DBSCAN_DIR}/{SEASONAL_FOLDER}", f"{DBSCAN}/{SEASONAL_FOLDER}", "map_output_osprey_dbscan_seasonal")
    combine_imgs_to_video(f"{MAP_OUTPUT_RAW_DIR}/{SEASONAL_FOLDER}", f"{RAW}/{SEASONAL_FOLDER}", "map_output_osprey_raw_seasonal")

    #combine_imgs_to_video(f"{MAP_OUTPUT_RAW_DIR}/{WEEKLY_FOLDER}", f"{RAW}/{WEEKLY_FOLDER}", "map_output_puffin_raw_weekly")
    #combine_imgs_to_video(f"{MAP_OUTPUT_RAW_DIR}/{SEASONAL_FOLDER}", f"{RAW}/{SEASONAL_FOLDER}", "map_output_puffin_raw_seasonal")
    #combine_imgs_to_video(f"{MAP_OUTPUT_DBSCAN_DIR}/{WEEKLY_FOLDER}", f"{DBSCAN}/{WEEKLY_FOLDER}", "map_output_puffin_dbscan_weekly")
    combine_imgs_to_video(f"{MAP_OUTPUT_DBSCAN_DIR}/{SEASONAL_FOLDER}", f"{DBSCAN}/{SEASONAL_FOLDER}", "map_output_puffin_dbscan_seasonal")

    #combine_imgs_to_video(f"{MAP_OUTPUT_RAW_DIR}/{WEEKLY_FOLDER}", f"{RAW}/{WEEKLY_FOLDER}", "map_output_ca_condor_raw_weekly")
    #combine_imgs_to_video(f"{MAP_OUTPUT_RAW_DIR}/{SEASONAL_FOLDER}", f"{RAW}/{SEASONAL_FOLDER}", "map_output_ca_condor_raw_seasonal")
    #combine_imgs_to_video(f"{MAP_OUTPUT_DBSCAN_DIR}/{WEEKLY_FOLDER}", f"{DBSCAN}/{WEEKLY_FOLDER}", "map_output_ca_condor_dbscan_weekly")
    combine_imgs_to_video(f"{MAP_OUTPUT_DBSCAN_DIR}/{SEASONAL_FOLDER}", f"{DBSCAN}/{SEASONAL_FOLDER}", "map_output_ca_condor_dbscan_seasonal")


def combine_imgs_to_video(input_image_parent_directory, output_subdir, input_image_immediate_dir_name):
    input_image_directory = Path(input_image_parent_directory, input_image_immediate_dir_name)
    folder = Path(input_image_directory)
    frames = sorted(folder.glob("frame_*.png"))  # adjust pattern if needed
    if not frames:
        raise SystemExit(f"No PNGs found in {input_image_directory}")

    # (Optional) ensure consistent size by resizing to the first frame’s size
    im0 = imageio.imread(frames[0])
    H, W = im0.shape[:2]

    def read_and_fit(p):
        print(p)
        im = imageio.imread(p)
        if im.shape[:2] != (H, W):
            # quick resize to match the first frame
            import PIL.Image as Image
            im = Image.fromarray(im).resize((W, H), Image.BILINEAR)
            im = imageio.core.util.Array(im)
        return im

    # Create directory "animations" if it doesn't exist
    if not os.path.exists("animations"):
        os.makedirs("animations")
    if not os.path.exists(f"animations/{output_subdir}"):
        os.makedirs(f"animations/{output_subdir}")


    file_full_path_name = f"animations/{output_subdir}/{input_image_immediate_dir_name}_animation.mp4"
    with imageio.get_writer(file_full_path_name, fps=2, codec="libx264", macro_block_size=None) as writer:
        for p in frames:
            writer.append_data(read_and_fit(p))
    print(f"Wrote {input_image_directory}_animation.mp4")

if __name__ == "__main__":
    main()

