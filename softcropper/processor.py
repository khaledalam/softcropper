import cv2
import numpy as np
import os

def make_square(image):
    height, width = image.shape[:2]
    size = max(height, width)
    square_image = np.zeros((size, size, 3), dtype=np.uint8)
    x_offset = (size - width) // 2
    y_offset = (size - height) // 2
    square_image[y_offset:y_offset + height, x_offset:x_offset + width] = image
    return square_image, x_offset, y_offset, size

def add_borders(image, original_image, x_offset, y_offset, mode="blur"):
    height, width = image.shape[:2]
    final_image = image.copy()

    if mode == "solid" or mode == "gradient":
        avg_color = original_image.mean(axis=(0, 1)).astype(np.uint8)

        if mode == "solid":
            # Fill with a single color
            if x_offset > 0:
                final_image[:, :x_offset] = avg_color
                final_image[:, -x_offset:] = avg_color
            if y_offset > 0:
                final_image[:y_offset, :] = avg_color
                final_image[-y_offset:, :] = avg_color

        elif mode == "gradient":
            # Left & right gradient
            if x_offset > 0:
                for i in range(x_offset):
                    alpha = i / x_offset
                    color = (avg_color * alpha).astype(np.uint8)
                    final_image[:, i] = color
                    final_image[:, -i - 1] = color

            # Top & bottom gradient
            if y_offset > 0:
                for j in range(y_offset):
                    alpha = j / y_offset
                    color = (avg_color * alpha).astype(np.uint8)
                    final_image[j, :] = color
                    final_image[-j - 1, :] = color

    else:
        # Blur mode (default)
        border_width = max(30, original_image.shape[1] // 10)
        border_height = max(30, original_image.shape[0] // 10)
        blur_amount = 51

        if x_offset > 0:
            left_border = original_image[:, :border_width]
            right_border = original_image[:, -border_width:]
            left_expanded = cv2.resize(left_border, (x_offset, height), interpolation=cv2.INTER_CUBIC)
            right_expanded = cv2.resize(right_border, (x_offset, height), interpolation=cv2.INTER_CUBIC)
            final_image[:, :x_offset] = cv2.GaussianBlur(left_expanded, (blur_amount, blur_amount), 0)
            final_image[:, -x_offset:] = cv2.GaussianBlur(right_expanded, (blur_amount, blur_amount), 0)

        if y_offset > 0:
            top_border = original_image[:border_height, :]
            bottom_border = original_image[-border_height:, :]
            top_expanded = cv2.resize(top_border, (width, y_offset), interpolation=cv2.INTER_CUBIC)
            bottom_expanded = cv2.resize(bottom_border, (width, y_offset), interpolation=cv2.INTER_CUBIC)
            final_image[:y_offset, :] = cv2.GaussianBlur(top_expanded, (blur_amount, blur_amount), 0)
            final_image[-y_offset:, :] = cv2.GaussianBlur(bottom_expanded, (blur_amount, blur_amount), 0)

    return final_image

def create_a4_collage(images, output_path, size=765, padding=40):
    A4_WIDTH, A4_HEIGHT = 2480, 3508
    canvas = np.ones((A4_HEIGHT, A4_WIDTH, 3), dtype=np.uint8) * 255

    x, y = padding, padding
    max_row_height = 0
    page = 1

    def save_canvas(current_canvas, index):
        filename = os.path.join(output_path, f"a4_page_{index:02d}.jpg")
        cv2.imwrite(filename, current_canvas)
        print(f"🖨️ A4 Page Saved: {filename}")

    for idx, img in enumerate(images):
        if img.shape[0] != size or img.shape[1] != size:
            img = cv2.resize(img, (size, size))

        if x + size + padding > A4_WIDTH:
            x = padding
            y += max_row_height + padding
            max_row_height = 0

        if y + size + padding > A4_HEIGHT:
            save_canvas(canvas, page)
            canvas = np.ones((A4_HEIGHT, A4_WIDTH, 3), dtype=np.uint8) * 255
            x, y = padding, padding
            page += 1

        canvas[y:y+size, x:x+size] = img
        x += size + padding
        max_row_height = max(max_row_height, size)

    save_canvas(canvas, page)


def add_text_around_image(image, left_text, right_text, top_text, bottom_text):
    final_size = 730       # 6.0 cm at 300 dpi
    photo_size = 640       # 5.4 cm at 300 dpi
    margin = (final_size - photo_size) // 2  # = 20px
    padding = 8

    image_resized = cv2.resize(image, (photo_size, photo_size))
    canvas = np.ones((final_size, final_size, 3), dtype=np.uint8) * 255
    canvas[margin:margin+photo_size, margin:margin+photo_size] = image_resized

    # Draw rounded rectangle
    corner_radius = 20
    border_thickness = 2
    rect_color = (0, 0, 0)

    def draw_rounded_rect(img, top_left, bottom_right, radius, color, thickness):
        x1, y1 = top_left
        x2, y2 = bottom_right
        cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)

    draw_rounded_rect(canvas, (margin, margin), (margin + photo_size, margin + photo_size), corner_radius, rect_color, border_thickness)

    # Font setup
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.9
    text_thickness = 2
    text_color = (0, 0, 0)

    # Draw vertical text properly
    def draw_vertical_text(img, text, start_x, align="left"):
        char_height = cv2.getTextSize("A", font, font_scale, text_thickness)[0][1] + 7
        total_height = len(text) * char_height
        start_y = (final_size - total_height) // 2
        for i, char in enumerate(text):
            y = start_y + i * char_height
            x = start_x
            cv2.putText(img, char, (x, y), font, font_scale, text_color, text_thickness)

    def draw_centered_horizontal_text(img, text, y_pos):
        text_size = cv2.getTextSize(text, font, font_scale, text_thickness)[0]
        x_pos = (final_size - text_size[0]) // 2
        cv2.putText(img, text, (x_pos, y_pos), font, font_scale, text_color, text_thickness)

    # Left side text
    if left_text:
        draw_vertical_text(canvas, left_text, start_x=margin // 3)
    
    # Right side text
    if right_text:
        draw_vertical_text(canvas, right_text, start_x=final_size - margin + (margin // 5))

    if top_text:
        draw_centered_horizontal_text(canvas, top_text, y_pos=padding + margin // 3)
        
    if bottom_text:
        draw_centered_horizontal_text(canvas, bottom_text, y_pos=final_size - padding)


    return canvas


def process_images(
    input_folder,
    output_folder=None,
    mode="solid",
    generate_a4=False,
    add_border=False,
    target_size=None,
    text=False,
    left_text="",
    right_text="",
    top_text="",
    bottom_text=""
):
    
    if output_folder is None:
        output_folder = os.path.join(input_folder, "output")
    os.makedirs(output_folder, exist_ok=True)

    total_images = 0
    processed_images = 0
    skipped_images = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
            total_images += 1
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            image = cv2.imread(image_path)
            if image is None:
                skipped_images += 1
                print(f"⚠️ Skipped: {filename} (unreadable or corrupted)")
                continue
            
            # BORDER
            squared_image, x_offset, y_offset, _ = make_square(image)
            
            final_image = squared_image.copy()
            
            if add_border:
                final_image = add_borders(final_image, image, x_offset, y_offset, mode=mode)
            
            if text and (left_text or right_text or top_text or bottom_text):
                final_image = add_text_around_image(final_image, left_text, right_text, top_text, bottom_text)

            if target_size:
                final_image = cv2.resize(final_image, target_size)


            cv2.imwrite(output_path, final_image)
            processed_images += 1
            print(f"✅ Processed: {filename}")
    
    if generate_a4:
        print("🧩 Generating A4 collage...")
        a4_output_folder = os.path.join(output_folder, "A4")
        os.makedirs(a4_output_folder, exist_ok=True)

        # Reload processed images for A4 layout
        processed_imgs = []
        for filename in sorted(os.listdir(output_folder)):
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
                img_path = os.path.join(output_folder, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    processed_imgs.append(img)

        if generate_a4:
            create_a4_collage(processed_imgs, a4_output_folder, size=(target_size[0] if target_size else 765))


    print("\n📦 Processing Complete")
    print(f"🔢 Total images found: {total_images}")
    print(f"✅ Successfully processed: {processed_images}")
    print(f"⛔ Skipped (unreadable): {skipped_images}")
    print(f"📁 Output folder: {output_folder}")
    