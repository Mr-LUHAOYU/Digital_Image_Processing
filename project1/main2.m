f = [1 2 3; 4 5 6; 7 8 9]';
theta = 60;
theta_rad = deg2rad(theta);

[rows, cols] = size(f);
cx = (cols - 1) / 2;
cy = (rows - 1) / 2;

new_f = zeros(rows, cols);
for i = 0:rows-1
    for j = 0:cols-1
        x_shifted = j - cx;
        y_shifted = i - cy;

        new_x_shifted = x_shifted * cos(theta_rad) - y_shifted * sin(theta_rad);
        new_y_shifted = x_shifted * sin(theta_rad) + y_shifted * cos(theta_rad);
        
        new_x = new_x_shifted + cx;
        new_y = new_y_shifted + cy;
        
        if new_x >= 0 && new_x <= cols-1 && new_y >= 0 && new_y <= rows-1
            new_f(i+1, j+1) = bilinear_interpolate(f, new_x, new_y, rows, cols);
        end
    end
end

disp(new_f);


function value = bilinear_interpolate(f, x, y, rows, cols)
    x1 = floor(x); y1 = floor(y);
    x2 = min(x1 + 1, cols-1); y2 = min(y1 + 1, rows-1);
    
    dx = x - x1;
    dy = y - y1;
    
    value = (1 - dx) * (1 - dy) * f(y1+1, x1+1) + dx * (1 - dy) * f(y1+1, x2+1) + ...
            (1 - dx) * dy * f(y2+1, x1+1) + dx * dy * f(y2+1, x2+1);
end
