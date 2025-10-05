from pathlib import Path
import imageio.v2 as imageio  # pip install imageio imageio-ffmpeg
import os

def main():
    # "map_output_raw"
    combine_imgs_to_video("map_output_osprey_raw")

def combine_imgs_to_video(input_image_directory):
    folder = Path(input_image_directory)
    frames = sorted(folder.glob("frame_*.png"))  # adjust pattern if needed
    if not frames:
        raise SystemExit(f"No PNGs found in {input_image_directory}")

    # (Optional) ensure consistent size by resizing to the first frame’s size
    im0 = imageio.imread(frames[0])
    H, W = im0.shape[:2]

    def read_and_fit(p):
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

    with imageio.get_writer(f"animations/{input_image_directory}_animation.mp4", fps=2, codec="libx264", macro_block_size=None) as writer:
        for p in frames:
            writer.append_data(read_and_fit(p))
    print(f"Wrote {input_image_directory}_animation.mp4")

if __name__ == "__main__":
    main()

