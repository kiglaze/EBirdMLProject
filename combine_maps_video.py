from pathlib import Path
import imageio.v2 as imageio  # pip install imageio imageio-ffmpeg

if __name__ == "__main__":
    folder = Path("map_output_raw")
    frames = sorted(folder.glob("frame_*.png"))  # adjust pattern if needed
    if not frames:
        raise SystemExit("No PNGs found in map_output/")

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

    with imageio.get_writer("animation.mp4", fps=2, codec="libx264", macro_block_size=None) as writer:
        for p in frames:
            writer.append_data(read_and_fit(p))
    print("Wrote animation.mp4")
