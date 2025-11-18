from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
import os

def apply_oil_painting_effect(image_path, output_path="artistic_image.png", intensity=5):
    """
    Creates an oil painting effect by applying multiple artistic filters.
    
    Args:
        image_path: Path to input image
        output_path: Path to save output image
        intensity: Strength of the effect (1-10, default 5)
    """
    try:
        # Open and resize image
        img = Image.open(image_path)
        img_resized = img.resize((256, 256))
        
        # Step 1: Apply median filter for oil painting base
        img_filtered = img_resized.filter(ImageFilter.MedianFilter(size=3))
        
        # Step 2: Enhance color saturation for vibrant colors
        enhancer = ImageEnhance.Color(img_filtered)
        img_saturated = enhancer.enhance(1.5)
        
        # Step 3: Apply edge enhancement for brush strokes
        img_edges = img_saturated.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
        # Step 4: Blend original with edges for artistic effect
        img_blended = Image.blend(img_saturated, img_edges, alpha=0.3)
        
        # Step 5: Add slight blur for painterly smoothness
        blur_radius = max(1, intensity // 2)
        img_final = img_blended.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Save the result
        plt.imshow(img_final)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close()
        print(f"🎨 Oil painting effect applied! Saved as '{output_path}'.")
        
    except Exception as e:
        print(f"Error processing image: {e}")


def apply_vintage_effect(image_path, output_path="vintage_image.png"):
    """
    Creates a vintage/retro photo effect with warm tones and vignette.
    """
    try:
        img = Image.open(image_path)
        img_resized = img.resize((256, 256))
        
        # Convert to RGB if needed
        if img_resized.mode != 'RGB':
            img_resized = img_resized.convert('RGB')
        
        # Step 1: Reduce contrast for faded look
        contrast = ImageEnhance.Contrast(img_resized)
        img_faded = contrast.enhance(0.7)
        
        # Step 2: Add warm color cast (sepia-like)
        img_array = np.array(img_faded).astype(float)
        
        # Apply warm tone transformation
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.2, 0, 255)  # Red boost
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.1, 0, 255)  # Green slight boost
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 0.8, 0, 255)  # Blue reduction
        
        img_warm = Image.fromarray(img_array.astype('uint8'))
        
        # Step 3: Add vignette effect (darkened edges)
        vignette = create_vignette_mask(256, 256)
        img_array = np.array(img_warm).astype(float)
        for i in range(3):  # Apply to each RGB channel
            img_array[:, :, i] = img_array[:, :, i] * vignette
        
        img_final = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
        
        # Save the result
        plt.imshow(img_final)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close()
        print(f"📷 Vintage effect applied! Saved as '{output_path}'.")
        
    except Exception as e:
        print(f"Error processing image: {e}")


def apply_cartoon_effect(image_path, output_path="cartoon_image.png"):
    """
    Creates a cartoon/comic book effect with bold edges and simplified colors.
    """
    try:
        img = Image.open(image_path)
        img_resized = img.resize((256, 256))
        
        # Step 1: Apply bilateral filter effect (smooth while preserving edges)
        # Using median filter as approximation
        img_smooth = img_resized.filter(ImageFilter.MedianFilter(size=5))
        
        # Step 2: Detect edges
        img_edges = img_resized.filter(ImageFilter.FIND_EDGES)
        img_edges = img_edges.convert('L')  # Convert to grayscale
        img_edges = Image.eval(img_edges, lambda x: 255 if x < 50 else 0)  # Threshold edges
        img_edges = img_edges.convert('RGB')
        
        # Step 3: Boost color saturation for cartoon look
        enhancer = ImageEnhance.Color(img_smooth)
        img_colorful = enhancer.enhance(1.8)
        
        # Step 4: Darken edges on the color image
        img_array = np.array(img_colorful).astype(float)
        edges_array = np.array(img_edges).astype(float) / 255.0
        
        # Darken where edges exist
        for i in range(3):
            img_array[:, :, i] = img_array[:, :, i] * (1 - edges_array[:, :, 0] * 0.7)
        
        img_final = Image.fromarray(np.clip(img_array, 0, 255).astype('uint8'))
        
        # Save the result
        plt.imshow(img_final)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close()
        print(f"🎭 Cartoon effect applied! Saved as '{output_path}'.")
        
    except Exception as e:
        print(f"Error processing image: {e}")


def apply_neon_glow_effect(image_path, output_path="neon_image.png"):
    """
    Creates a vibrant neon glow effect with enhanced edges and colors.
    """
    try:
        img = Image.open(image_path)
        img_resized = img.resize((256, 256))
        
        # Step 1: Enhance edges dramatically
        img_edges = img_resized.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img_edges = img_edges.filter(ImageFilter.EDGE_ENHANCE_MORE)  # Apply twice
        
        # Step 2: Boost color saturation dramatically
        enhancer = ImageEnhance.Color(img_edges)
        img_saturated = enhancer.enhance(2.5)
        
        # Step 3: Increase brightness
        brightness = ImageEnhance.Brightness(img_saturated)
        img_bright = brightness.enhance(1.3)
        
        # Step 4: Add glow by blending with blurred version
        img_blurred = img_bright.filter(ImageFilter.GaussianBlur(radius=3))
        img_final = Image.blend(img_bright, img_blurred, alpha=0.4)
        
        # Save the result
        plt.imshow(img_final)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=150)
        plt.close()
        print(f"✨ Neon glow effect applied! Saved as '{output_path}'.")
        
    except Exception as e:
        print(f"Error processing image: {e}")


def create_vignette_mask(width, height, intensity=0.5):
    """
    Creates a vignette mask (bright center, dark edges).
    
    Args:
        width: Image width
        height: Image height
        intensity: Vignette strength (0-1)
    
    Returns:
        2D numpy array with vignette gradient
    """
    center_x, center_y = width / 2, height / 2
    max_dist = np.sqrt(center_x**2 + center_y**2)
    
    y, x = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    # Normalize and invert (1 at center, 0 at edges)
    vignette = 1 - (dist_from_center / max_dist) * intensity
    vignette = np.clip(vignette, 0.3, 1)  # Don't make edges too dark
    
    return vignette


def show_all_effects(image_path):
    """
    Apply all effects to an image and save them all.
    """
    base, ext = os.path.splitext(image_path)
    
    print("\n🎨 Applying all artistic effects...\n")
    
    apply_oil_painting_effect(image_path, f"{base}_oil_painting{ext}")
    apply_vintage_effect(image_path, f"{base}_vintage{ext}")
    apply_cartoon_effect(image_path, f"{base}_cartoon{ext}")
    apply_neon_glow_effect(image_path, f"{base}_neon{ext}")
    
    print("\n✅ All effects applied successfully!")


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 ARTISTIC FILTER STUDIO 🎨")
    print("=" * 60)
    print("\nAvailable effects:")
    print("  1. Oil Painting - Painterly effect with brush strokes")
    print("  2. Vintage - Retro photo with warm tones and vignette")
    print("  3. Cartoon - Comic book style with bold edges")
    print("  4. Neon Glow - Vibrant colors with glowing edges")
    print("  5. All Effects - Apply all effects at once")
    print("  6. Exit")
    print("=" * 60)
    
    while True:
        print()
        choice = input("Select effect (1-6): ").strip()
        
        if choice == '6':
            print("Goodbye! 🎨")
            break
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("Invalid choice. Please enter 1-6.")
            continue
        
        image_path = input("Enter image filename: ").strip()
        
        if not os.path.isfile(image_path):
            print(f"❌ File not found: {image_path}")
            continue
        
        base, ext = os.path.splitext(image_path)
        
        if choice == '1':
            intensity = input("Enter intensity (1-10, default 5): ").strip()
            intensity = int(intensity) if intensity.isdigit() else 5
            apply_oil_painting_effect(image_path, f"{base}_oil_painting{ext}", intensity)
        elif choice == '2':
            apply_vintage_effect(image_path, f"{base}_vintage{ext}")
        elif choice == '3':
            apply_cartoon_effect(image_path, f"{base}_cartoon{ext}")
        elif choice == '4':
            apply_neon_glow_effect(image_path, f"{base}_neon{ext}")
        elif choice == '5':
            show_all_effects(image_path)
