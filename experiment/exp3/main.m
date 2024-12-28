Image1=im2double(imread('plane.jpg'));
gray=rgb2gray(Image1);
T=graythresh(gray);
BW=im2bw(gray,T);
figure,imshow(BW),title('二值化图像');

SE=strel('square',3);
Morph=imopen(BW,SE);
Morph=imclose(Morph,SE);
figure,imshow(Morph),title('形态学滤波');

[B L]=bwboundaries(1-Morph);
figure,imshow(L),title('划分的区域');
hold on;
for i=1:length(B)
    boundary=B{i};
    plot(boundary(:,2),boundary(:,1),'r','LineWidth',2);
end

M=zeros(length(B));
for k=1:length(B)
    N=length(B{k});
    if N/2~=round(N/2)
        B{k}(end+1,:)=B{k}(end,:);
        N=N+1;
    end
    M(k)=[N*3/4];
end
S=zeros(size(Morph));
figure,imshow(S);
hold on;
for k=1:length(B)
    z=B{k}(:,2)+1i*B{k}(:,1);
    Z=fft(z);
    [Y I]=sort(abs(Z));

    for count=1:M(k)
        Z(I(count))=0;
    end
    zz=ifft(Z);
    plot(real(zz),imag(zz),'w');
end