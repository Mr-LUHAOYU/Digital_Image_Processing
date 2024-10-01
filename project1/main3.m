f = imread('img.png');
[rows, cols, channels] = size(f);

rotated_img = rotate_image(f, 20);
show_image(f, 'Original Image');
show_image(rotated_img, 'Rotated Image (20°)');
flipped_img = horizontal_flip(rotated_img);
show_image(flipped_img, 'Horizontally Flipped Image');
sheared_img = shear_transform(flipped_img, 0.3, 0.5);
show_image(sheared_img, 'Sheared Image (kx=0.3, ky=0.5)');
scaled_img = scale_image(sheared_img, 0.6, 0.6);
show_image(scaled_img, 'Scaled Image (kx=ky=0.6)');
show_image(scaled_img, 'Final Transformed Image');

function value = bilinear_interpolate(f, x, y, rows, cols)
    if x < 0 || x >= cols - 1 || y < 0 || y >= rows - 1
        value = 0;
        return;
    end

    x1 = floor(x); y1 = floor(y);
    x2 = min(x1 + 1, cols - 1); y2 = min(y1 + 1, rows - 1);

    dx = x - x1;
    dy = y - y1;

    value = (1 - dx) * (1 - dy) * double(f(y1 + 1, x1 + 1, :)) + ...
             dx * (1 - dy) * double(f(y1 + 1, x2 + 1, :)) + ...
             (1 - dx) * dy * double(f(y2 + 1, x1 + 1, :)) + ...
             dx * dy * double(f(y2 + 1, x2 + 1, :));
end

function show_image(img, title_str)
    figure;
    imshow(uint8(img));
    title(title_str);
end

function rotated_img = rotate_image(f, angle)
    [rows, cols, channels] = size(f);
    cx = (cols - 1) / 2;
    cy = (rows - 1) / 2;
    angle_rad = deg2rad(angle);

    rotated_img = ones(rows, cols, channels) * 255;

    for i = 0:rows-1
        for j = 0:cols-1
            x_shifted = j - cx;
            y_shifted = i - cy;

            new_x_shifted = x_shifted * cos(angle_rad) + y_shifted * sin(angle_rad);
            new_y_shifted = -x_shifted * sin(angle_rad) + y_shifted * cos(angle_rad);

            new_x = new_x_shifted + cx;
            new_y = new_y_shifted + cy;

            if new_x >= 0 && new_x <= cols-1 && new_y >= 0 && new_y <= rows-1
                rotated_img(i + 1, j + 1, :) = bilinear_interpolate(f, new_x, new_y, rows, cols);
            end
        end
    end
end

function flipped_img = horizontal_flip(f)
    flipped_img = f(:, end:-1:1, :);
end


function sheared_img = shear_transform(f, kx, ky)
    [rows, cols, channels] = size(f);
    sheared_img = ones(rows, cols, channels) * 255;

    for i = 0:rows-1
        for j = 0:cols-1
            new_x = j + kx * i;
            new_y = i + ky * j;

            if new_x >= 0 && new_x <= cols-1 && new_y >= 0 && new_y <= rows-1
                sheared_img(i + 1, j + 1, :) = bilinear_interpolate(f, new_x, new_y, rows, cols);
            end
        end
    end
end


function scaled_img = scale_image(f, scale_x, scale_y)
    [rows, cols, channels] = size(f);
    new_rows = round(rows * scale_y);
    new_cols = round(cols * scale_x);

    scaled_img = ones(new_rows, new_cols, channels) * 255;

    for i = 0:new_rows-1
        for j = 0:new_cols-1
            src_x = j / scale_x;
            src_y = i / scale_y;

            if src_x >= 0 && src_x <= cols-1 && src_y >= 0 && src_y <= rows-1
                scaled_img(i + 1, j + 1, :) = bilinear_interpolate(f, src_x, src_y, rows, cols);
            end
        end
    end
end

