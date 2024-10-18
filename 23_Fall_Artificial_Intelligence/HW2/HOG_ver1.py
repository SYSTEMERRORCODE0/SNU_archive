import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_differential_filter():
    # TODO: implement this function

    # Sobel Filter (I think Sobel filter in slide's sign is reversed)
    filter_x = np.array([[1, 0, -1],
                         [2, 0 ,-2],
                         [1, 0, -1]])
    filter_y = np.array([[1, 2, 1],
                         [0, 0, 0],
                         [-1, -2, -1]])

    return filter_x, filter_y


def filter_image(im, filter):
    # TODO: implement this function

    im_filtered = np.zeros_like(im)

    im_height, im_width = im.shape
    filter_height, filter_width = filter.shape

    padding_height = filter_height // 2
    padding_width = filter_width // 2

    # also filtering boundary with (out-of-boundary : 0)
    im_add_boundary = np.zeros((im_height + 2 * padding_height, im_width + 2 * padding_width))
    im_add_boundary[padding_height : im_height+padding_height, padding_width : im_width+padding_width] = im

    # multiplication between elements, not matrix mult
    for i in range(padding_height, im_height + padding_height):
        for j in range(padding_width, im_width + padding_width):
            im_region = im_add_boundary[i-padding_height : i+padding_height+1, j-padding_width : j+padding_width+1]
            im_filtered[i-padding_height, j-padding_width] = np.sum(im_region * filter)

    return im_filtered


def get_gradient(im_dx, im_dy):
    # TODO: implement this function

    grad_mag = np.sqrt(im_dx ** 2 + im_dy ** 2)
    grad_angle = (np.arctan(im_dy / (im_dx + 1e-10)) + np.pi) % np.pi # avoid division by 0

    return grad_mag, grad_angle


def build_histogram(grad_mag, grad_angle, cell_size):
    # TODO: implement this function

    num_bins = 6
    cell_nums_height = grad_mag.shape[0] // cell_size
    cell_nums_width = grad_mag.shape[1] // cell_size

    ori_histo = np.zeros((cell_nums_height, cell_nums_width, num_bins), dtype=float)

    for i in range(cell_nums_height):
        for j in range(cell_nums_width):
            # get mag, angle each cell
            cell_mag = grad_mag[i*cell_size : (i+1)*cell_size, j*cell_size : (j+1)*cell_size]
            cell_angle = grad_angle[i*cell_size : (i+1)*cell_size, j*cell_size : (j+1)*cell_size]

            # add mag into right angle class
            for h in range(cell_size):
                for w in range(cell_size):
                    angle_class = int(round(cell_angle[h, w] / (np.pi / num_bins))) % num_bins
                    ori_histo[i, j, angle_class] += cell_mag[h, w]

    return ori_histo


def get_block_descriptor(ori_histo, block_size):
    # TODO: implement this function

    cell_nums_height, cell_nums_width, num_bins = ori_histo.shape
    block_nums_height = cell_nums_height - block_size + 1
    block_nums_width = cell_nums_width - block_size + 1

    ori_histo_normalized = np.zeros((block_nums_height, block_nums_width, block_size**2 * num_bins), dtype=float)
    e = 0.001

    for i in range(block_nums_height):
        for j in range(block_nums_width):
            block_histo = ori_histo[i : i+block_size, j : j+block_size, :].flatten()
            block_descriptor = block_histo / np.sqrt(np.sum(block_histo**2) + e**2)
            ori_histo_normalized[i, j, :] = block_descriptor

    return ori_histo_normalized


# visualize histogram of each block
def visualize_hog(im, hog, cell_size, block_size):
    num_bins = 6
    max_len = 7  # control sum of segment lengths for visualized histogram bin of each block
    im_h, im_w = im.shape
    num_cell_h, num_cell_w = int(im_h / cell_size), int(im_w / cell_size)
    num_blocks_h, num_blocks_w = num_cell_h - block_size + 1, num_cell_w - block_size + 1
    histo_normalized = hog.reshape((num_blocks_h, num_blocks_w, block_size**2, num_bins))
    histo_normalized_vis = np.sum(histo_normalized**2, axis=2) * max_len  # num_blocks_h x num_blocks_w x num_bins
    angles = np.arange(0, np.pi, np.pi/num_bins)
    mesh_x, mesh_y = np.meshgrid(np.r_[cell_size: cell_size*num_cell_w: cell_size], np.r_[cell_size: cell_size*num_cell_h: cell_size])
    mesh_u = histo_normalized_vis * np.sin(angles).reshape((1, 1, num_bins))  # expand to same dims as histo_normalized
    mesh_v = histo_normalized_vis * -np.cos(angles).reshape((1, 1, num_bins))  # expand to same dims as histo_normalized
    plt.imshow(im, cmap='gray', vmin=0, vmax=1)
    for i in range(num_bins):
        plt.quiver(mesh_x - 0.5 * mesh_u[:, :, i], mesh_y - 0.5 * mesh_v[:, :, i], mesh_u[:, :, i], mesh_v[:, :, i],
                   color='red', headaxislength=0, headlength=0, scale_units='xy', scale=1, width=0.002, angles='xy')
    # plt.show()
    plt.savefig('hog.png')


def extract_hog(im, visualize=False, cell_size=8, block_size=2):
    # TODO: implement this function

    im = im.astype(float) / 255.0

    filter_x, filter_y = get_differential_filter()

    im_filtered_x = filter_image(im, filter_x)
    im_filtered_y = filter_image(im, filter_y)

    grad_mag, grad_angle = get_gradient(im_filtered_x, im_filtered_y)

    ori_histo = build_histogram(grad_mag, grad_angle, cell_size)

    hog = get_block_descriptor(ori_histo, block_size)

    if visualize:
        visualize_hog(im, hog, cell_size, block_size)

    return hog


def face_recognition(I_target, I_template):
    # TODO: implement this function

    I_target_hog = extract_hog(I_target, visualize=False)
    I_template_hog = extract_hog(I_template, visualize=False)

    # get cell_size using target height & hog height
    cell_size = I_target.shape[0] // (I_target_hog.shape[0]+1)

    I_target_hog_height, I_target_hog_width, _ = I_target_hog.shape
    I_template_hog_height, I_template_hog_width, _ = I_template_hog.shape

    compare_height = I_target_hog_height - I_template_hog_height + 1
    compare_width = I_target_hog_width - I_template_hog_width + 1

    # Get NCC
    ncc = np.zeros((compare_height, compare_width))
    for i in range(compare_height):
        for j in range(compare_width):
            target_region_hog = I_target_hog[i : i+I_template_hog_height, j : j+I_template_hog_width, :]
            ncc[i, j] = np.sum(target_region_hog * I_template_hog) / (np.linalg.norm(target_region_hog) * np.linalg.norm(I_template_hog))

    # thresholding
    threshold = 0.6
    face_detected = np.argwhere(ncc > threshold)

    bounding_boxes = []
    for (i, j) in face_detected:
        bounding_boxes.append([i*cell_size, j*cell_size, ncc[i, j]])

    bounding_boxes = np.array(bounding_boxes)

    # inner function for calculating IoU
    def iou(box1, box2):
        h1 = max(box1[0], box2[0])
        w1 = max(box1[1], box2[1])
        h2 = min(box1[0], box2[0]) + I_template.shape[0]
        w2 = min(box1[1], box2[1]) + I_template.shape[1]

        intersection = max(0, h2 - h1) * max(0, w2 - w1)
        total = 2 * I_template.shape[0] * I_template.shape[1] - intersection
        return intersection / total

    # Non-Max Suppression
    bounding_boxes_iou = []
    IOU_PERCENT = 0.5
    
    for i in range(len(bounding_boxes)):
        discard = False
        for j in range(len(bounding_boxes)):
            if i == j:
                continue
            box1 = bounding_boxes[i]
            box2 = bounding_boxes[j]
            if iou(box1[:2], box2[:2]) > IOU_PERCENT:
                if box1[2] < box2[2]:
                    discard = True
        if not discard:
            bounding_boxes_iou.append(box1)

    # transposed for visualize_face_detection
    bounding_boxes = []
    for box in bounding_boxes_iou:
        bounding_boxes.append([box[1], box[0], box[2]])

    bounding_boxes = np.array(bounding_boxes)

    return bounding_boxes


def visualize_face_detection(I_target, bounding_boxes, box_size):

    hh,ww,cc=I_target.shape

    fimg=I_target.copy()
    for ii in range(bounding_boxes.shape[0]):

        x1 = bounding_boxes[ii,0]
        x2 = bounding_boxes[ii, 0] + box_size 
        y1 = bounding_boxes[ii, 1]
        y2 = bounding_boxes[ii, 1] + box_size

        if x1<0:
            x1=0
        if x1>ww-1:
            x1=ww-1
        if x2<0:
            x2=0
        if x2>ww-1:
            x2=ww-1
        if y1<0:
            y1=0
        if y1>hh-1:
            y1=hh-1
        if y2<0:
            y2=0
        if y2>hh-1:
            y2=hh-1
        fimg = cv2.rectangle(fimg, (int(x1),int(y1)), (int(x2),int(y2)), (255, 0, 0), 1)
        cv2.putText(fimg, "%.2f"%bounding_boxes[ii,2], (int(x1)+1, int(y1)+2), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    plt.figure(3)
    plt.imshow(fimg, vmin=0, vmax=1)
    plt.imsave('result_face_detection.png', fimg, vmin=0, vmax=1)
    plt.show()


if __name__=='__main__':

    im = cv2.imread('cameraman.tif', 0)
    hog = extract_hog(im, visualize=False)

    I_target= cv2.imread('target.png', 0) # MxN image

    I_template = cv2.imread('template.png', 0) # mxn  face template

    bounding_boxes = face_recognition(I_target, I_template)

    I_target_c= cv2.imread('target.png') # MxN image (just for visualization)
    
    visualize_face_detection(I_target_c, bounding_boxes, I_template.shape[0]) # visualization code



