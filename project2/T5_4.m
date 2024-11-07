hist = [560, 920, 1046, 705, 356, 267, 170, 72;];
bins = [0, 1, 2, 3, 4, 5, 6, 7;];

cdf = hist / sum(hist) * max(bins);

cdf = cumsum(cdf);

cdf = round(cdf);
disp(cdf);
