Image1=imread('img.jpeg');
%红绿通道互换
Image2=Image1;
Image2(:,:,1)=Image1(:,:,2);
Image2(:,:,2)=Image1(:,:,1);
imshow(Image2);
imwrite(Image2,'changecolor.jpg');
%灰度化
gray=rgb2gray(Image1);
figure;
subplot(121),imshow(Image1),title('Original Image');
subplot(122),imshow(gray),title('Gray Image');
imwrite(gray,'grayimage.jpg');
 %图像旋转
Newgray1=imrotate(gray,15);
Newgray2=imrotate(gray,15,'bilinear');
figure;
subplot(121),imshow(Newgray1),title('旋转15°（最邻近插值）');
subplot(122),imshow(Newgray2),title('旋转15°（双线性插值）');
imwrite(Newgray1,'rotate1.jpg');
imwrite(Newgray2,'rotate2.jpg');
 %图像缩放
Newgray3=imresize(gray,2.5,'nearest');
Newgray4=imresize(gray,2.5,'bilinear');
figure;
subplot(121),imshow(Newgray3),title('放大2.5倍（最邻近插值）');
subplot(122),imshow(Newgray4),title('放大2.5倍（双线性插值）');
imwrite(Newgray3,'scale1.jpg');
imwrite(Newgray4,'scale2.jpg');
 %图像镜像与拼接
Image2=imread('img.jpeg');
HImage=flip(Image2,2);
VImage=flip(Image2,1);
CImage=flip(HImage,1);
[h, w]=size(Image2);
NewImage=zeros(h*2,w*2,3);
NewImage=[Image2 HImage;VImage CImage];
figure,imshow(NewImage);
imwrite(NewImage,'newlotus.jpg');