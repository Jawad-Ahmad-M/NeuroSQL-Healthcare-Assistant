from PIL import Image

def convert_to_grayscale(image_path, save_path):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Convert the image to 8-bit grayscale (L mode)
        grayscale_image = image.convert('L')

        # Save the grayscale image
        grayscale_image.save(save_path)

        print(f"✅ Image successfully converted to grayscale and saved at: {save_path}")
    except Exception as e:
        print(f"❌ Error converting image: {e}")

# Example usage
image_path = r"C:\Users\zbook\Desktop\Gui Project\known_faces\InShot_20241122_143803794.jpgq"  # Path to the original image
save_path = r"C:\Users\zbook\Desktop\Gui Project\known_faces\grayscale_image.jpg"  # Path where the converted image will be saved

convert_to_grayscale(image_path, save_path)