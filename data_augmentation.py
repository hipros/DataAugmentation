import os
import cv2
import argparse
import random
import numpy as np
import math

class DataAugmentation:
    def __init__(self, opts):
        self.save_path = os.path.join(opts.root_dir, opts.save_dir)
        print(self.save_path)
        self.final_img_size = opts.final_img_size
        self.crop_thres = opts.crop_thres

    def five_crop(self, img, img_id, coordinate):

        rows, cols = img.shape[:2]
        #5 - crop
        crop_img_list = [[], img[0:rows - self.crop_thres, 0:cols - self.crop_thres],
                    img[self.crop_thres:rows, 0:cols - self.crop_thres],
                    img[0:rows - self.crop_thres, self.crop_thres:cols],
                    img[self.crop_thres:rows, self.crop_thres:cols],
                    img[self.crop_thres//2:rows - (self.crop_thres//2), self.crop_thres//2:cols - (self.crop_thres//2)]]

        for i in range(1,6):
            crop_img = crop_img_list[i]
            cv2.imwrite(self.save_path+str(img_id)+'_'+str(i)+'.jpg', crop_img)

            f = open(self.save_path+str(img_id)+'_'+str(i)+'.txt', 'w')
            f.write(coordinate)
            f.close()

    def rotation_img(self, img, img_id, degree, coordinate):
        rows, cols = img.shape[:2]
        # +5 degree
        matrix = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
        img = cv2.warpAffine(img,matrix,(cols,rows))
        cv2.imwrite(self.save_path+str(img_id)+'_degree'+str(degree)+'.jpg',img)

        f = open(self.save_path+str(img_id)+'_degree'+str(degree)+'.txt','w')
        f.write(coordinate)
        f.close()


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def search_img(opts):
    data_path = os.path.join(opts.root_dir, opts.data_dir)
    anno_list = os.listdir(data_path)

    for anno_name in anno_list:
        if anno_name.endswith('jpg'):
            img_id = anno_name.split('.')[0]

            im = cv2.imread(os.path.join(data_path, img_id + '.jpg'))
            im = cv2.resize(im,
                dsize=(opts.final_img_size + opts.crop_thres,
                opts.final_img_size + opts.crop_thres),
                interpolation=cv2.INTER_AREA)

            coordinate = None

            with open(os.path.join(data_path, img_id+".txt"), 'r') as f_:
                coordinate = f_.readlines()[0]

            yield (im, img_id, coordinate)


if __name__ == '__main__':

    for week in range(28, 42):
        parser = argparse.ArgumentParser()
        parser.add_argument('--root_dir', default='/home/rtos/바탕화면/test/data_sep_week')
        parser.add_argument('--data_dir', default=str(week)+'/train')
        parser.add_argument('--save_dir', default="image/"+str(week)+"/train/")
        parser.add_argument('--final_img_size', default=110)
        parser.add_argument('--crop_thres', default=20)

        opts = parser.parse_args()
        make_dir(os.path.join(opts.root_dir, "image/"+str(week)+'/'))
        make_dir(os.path.join(opts.root_dir,opts.save_dir))

        dataAugmentation = DataAugmentation(opts)

        for (img, img_id, label) in search_img(opts):
            #dataAugmentation.five_crop(img, img_id, label)
            dataAugmentation.rotation_img(img, img_id, 0, label)
            dataAugmentation.rotation_img(img, img_id, 5, label)
            dataAugmentation.rotation_img(img, img_id, -5, label)
