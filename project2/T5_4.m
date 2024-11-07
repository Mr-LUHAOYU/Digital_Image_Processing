hist = [560, 920, 1046, 705, 356, 267, 170, 72;];
bins = [0, 1, 2, 3, 4, 5, 6, 7;];

p = data(2, :) / sum(data(2, :)) * max(data(1, :));

p = cumsum(p);

p = round(p);
disp(p);
