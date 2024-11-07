function histogram_equalization_example()
    n = 10; 
    m = 10; 
    k = 7;

    img = [ones(n/2, m); zeros(n/2, m)];
    img = img';

    display(img, k);
    
    hist = histcounts(img, 0:k);

    cdf = hist / sum(hist) * k;
    
    cdf = cumsum(cdf);
    
    cdf = round(cdf);
    
    img_new = cdf(img + 1);

    display(img_new, k)
end

function display(image, k)
    figure;
    imshow(image, [0 k], 'InitialMagnification', 'fit');
    colormap(gray(k));
    colorbar;
end
