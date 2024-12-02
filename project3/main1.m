function main()
    g = [
    [0, 0, 0, 0, 0],
    [0, 5, 1, 6, 0],
    [0, 4, 6, 3, 0],
    [0, 7, 2, 1, 0],
    [0, 0, 0, 0, 0]
    ];
    new_g = mean_filter(g, 3);
    disp(new_g)
end

function out = mean_filter(img, k)
    if nargin < 2
        k = 3;  % 默认窗口大小为3
    end
    
    [H, W] = size(img);
    out = zeros(H, W);
    
    % 判断窗口作用范围
    for i = 1:H
        for j = 1:W
            if i-1 < floor(k/2) || i-1 >= H - floor(k/2) || j-1 < floor(k/2) || j-1 >= W - floor(k/2)
                out(i, j) = img(i, j);
            else
                % 计算均值
                out(i, j) = mean(mean(img(i - floor(k/2):i + floor(k/2), j - floor(k/2):j + floor(k/2))));
            end
        end
    end
end

