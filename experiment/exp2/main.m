Image1=im2double(imread('lotus.bmp'));
gray=rgb2gray(Image1);
imhist(gray);
[h,w]=size(gray);
NewImage1=zeros(h,w);
a=80/256; b=180/256; c=30/256; d=220/256;
for x=1:w
    for y=1:h
        if gray(y,x)<a
            NewImage1(y,x)=gray(y,x)*c/a;
        elseif gray(y,x)<b
            NewImage1(y,x)=(gray(y,x)-a)*(d-c)/(b-a)+c;
        else
            NewImage1(y,x)=(gray(y,x)-b)*(255-d)/(255-b)+d;
        end
    end
end
figure,imshow(NewImage1),title('分段线性变换');

NewImage2=histeq(gray);
figure,imshow(NewImage2),title('直方图均衡化');

NewImage3=zeros(h,w,3);
for x=1:w
    for y=1:h
        if gray(y,x)<64/256
            NewImage3(y,x,1)=0;
            NewImage3(y,x,2)=4*gray(y,x);
            NewImage3(y,x,3)=1;
        elseif gray(y,x)<128/256
            NewImage3(y,x,1)=0;
            NewImage3(y,x,2)=1;
            NewImage3(y,x,3)=2-4*gray(y,x);
        elseif gray(y,x)<192/256
            NewImage3(y,x,1)=4*gray(y,x)-2;
            NewImage3(y,x,2)=1;
            NewImage3(y,x,3)=0;
        else
            NewImage3(y,x,1)=1;
            NewImage3(y,x,2)=4-4*gray(y,x);
            NewImage3(y,x,3)=0;
        end
    end
end
figure,imshow(NewImage3);

noiseIsp=imnoise(gray,'salt & pepper',0.1);
noiseIg=imnoise(gray,'gaussian');
result1=medfilt2(noiseIsp);
result2=medfilt2(noiseIg);
figure;
subplot(121),imshow(result1),title('椒盐噪声3×3中值滤波');
subplot(122),imshow(result2),title('高斯噪声3×3中值滤波');

H1=[-1 -2 -1;0 0 0;1 2 1];
H2=[-1 0 1;-2 0 2;-1 0 1];
R1=imfilter(gray,H1);
R2=imfilter(gray,H2);
edgeImage=abs(R1)+abs(R2);
sharpImage=gray+edgeImage;
figure;
subplot(121),imshow(edgeImage),title('Sobel梯度图像');
subplot(122),imshow(sharpImage),title('Sobel锐化图像');
