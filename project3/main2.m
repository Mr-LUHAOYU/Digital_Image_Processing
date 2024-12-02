function main()
    g = [
        [0, 0, 0, 0, 0],
        [0, 5, 1, 6, 0],
        [0, 4, 6, 3, 0],
        [0, 7, 2, 1, 0],
        [0, 0, 0, 0, 0]
    ];
    disp('sigma=0.8')
    g1 = gauss_filter(g, 3, 0.8);
    disp(g1);
    disp('sigma=1')
    g2 = gauss_filter(g, 3, 1);
    disp(g2);
end

function out = gauss_filter(img, k, sigma)
    [H, W] = size(img);
    out = zeros(H, W);
    
    % 判断窗口作用范围
    for i = 1:H
        for j = 1:W
            if i-1 < floor(k/2) || i-1 >= H - floor(k/2) || j-1 < floor(k/2) || j-1 >= W - floor(k/2)
                out(i, j) = img(i, j);
            else
                kernal = zeros(k, k);
                for x = 0:k-1
                    for y = 0:k-1
                        kernal(x+1, y+1) = -(x * x + y * y) / (2 * sigma * sigma);
                    end
                end
                kernal = exp(kernal);
                kernal = kernal / sum(kernal(:));
                out(i, j) = sum(sum(img(i - floor(k/2):i + floor(k/2), j - floor(k/2):j + floor(k/2)) .* kernal));
            end
        end
    end
end