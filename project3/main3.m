function main()
    g = [
        [1, 3, 6, 8, 6, 3],
        [15, 4, 7, 9, 8, 1],
        [13, 3, 5, 5, 7, 4],
        [3, 4, 0, 2, 5, 7],
        [6, 12, 3, 6, 9, 7],
        [9, 11, 3, 11, 14, 13]
    ];
    g1 = median_filter(g, 3);
    g2 = median_filter(g, 5);
    disp("k=3");
    disp(g1);
    disp("k=5");
    disp(g2);
end

function out = median_filter(img, k)
    [H, W] = size(img);
    out = zeros(H, W);
    
    % 判断窗口作用范围
    for i = 1:H
        for j = 1:W
            if i-1 < floor(k/2) || i-1 >= H - floor(k/2) || j-1 < floor(k/2) || j-1 >= W - floor(k/2)
                out(i, j) = img(i, j);
            else
                region = img(i - floor(k/2):i + floor(k/2), j - floor(k/2):j + floor(k/2));
                out(i, j) = median(region(:));
            end
        end
    end
end