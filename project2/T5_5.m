function histogram_equalization_example()
    n = 10; 
    m = 10; 
    k = 7;

    img = [ones(n/2, m); zeros(n/2, m)];
    img = img;
    
    display(img, k);
    
    hist = histcounts(img, 0:k);
    cdf = cumsum(hist);
    
    cdf_normalized = cdf * max(hist) / max(cdf);
    
    cdf_m = cdf;
    cdf_m(cdf == 0) = [];
    if ~isempty(cdf_m)
        cdf_m = (cdf_m - min(cdf_m)) * k / (max(cdf_m) - min(cdf_m));
        cdf(cdf > 0) = round(cdf_m);
    end
    image_new = cdf(img + 1);

    display(image_new, k);
end

function display(image, k)
    figure;
    imshow(image, [0 k], 'InitialMagnification', 'fit');
    colormap(gray(k));
    colorbar;
end
