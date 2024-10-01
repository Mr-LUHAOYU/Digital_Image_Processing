f = [1 2 3; 4 5 6; 7 8 9]';
kx = 2.3;
ky = 1.6;

[rows, cols] = size(f);
new_rows = round(rows * ky);
new_cols = round(cols * kx);
new_f = zeros(new_rows, new_cols);

for i = 0:new_rows-1
    for j = 0:new_cols-1
        src_x = i / ky;
        src_y = j / kx;

        x1 = floor(src_x);
        y1 = floor(src_y);
        x2 = min(x1 + 1, rows - 1);
        y2 = min(y1 + 1, cols - 1);

        dx = src_x - x1;
        dy = src_y - y1;

        x1=x1+1; x2=x2+1;
        y1=y1+1; y2=y2+1;
        
        new_f(i+1, j+1) = (1 - dx) * (1 - dy) * f(x1, y1) + dx * (1 - dy) * f(x2, y1) + ...
                      (1 - dx) * dy * f(x1, y2) + dx * dy * f(x2, y2);
    end
end

disp(new_f)
