import mdata as md
import cv2

def eachFileter (img_cursor, result_images, cmdFilter, tag, name):
    for idx, filter in enumerate(cmdFilter):
        param = filter['param']
        if filter['name'] == 'box':
            ksize = int(param['ksize'])
            img_cursor = cv2.boxFilter(img_cursor, ddepth=-1, ksize=ksize)
        elif filter['name'] == 'bilateral':
            d = int(param['d'])
            sColor = int(param['s-color'])
            sSpace = int(param['s-space'])
            img_cursor = cv2.bilateralFilter(img_cursor, d, sColor, sSpace)
        elif filter['name'] == 'median':
            ksize = int(param['ksize'])
            img_cursor = cv2.medianBlur(img_cursor, ksize=ksize)
        elif filter['name'] == 'blur':
            ksize = int(param['ksize'])
            img_cursor = cv2.blur(img_cursor, ksize=(ksize, ksize))
        elif filter['name'] == 'gaussian':
            ksize = int(param['ksize'])
            sigmaX = int(param['sigmaX'])
            img_cursor = cv2.GaussianBlur(img_cursor, (ksize, ksize), sigmaX)

        tmp = md.savetemp('filter', '%s-%d-%s' % (tag, idx, name), img_cursor)
        result_images.append(tmp)

    return img_cursor,  result_images

def run_filter(img_name, filter_param):
    # src
    img_cursor = md.loadimg(md.src, img_name)
    result_images = []

    # prev filter
    img_cursor, result_images = eachFileter(
        img_cursor, result_images, filter_param['prev-filter'], 'prev', img_name)

    # gray
    img_cursor = cv2.cvtColor(img_cursor, cv2.COLOR_BGRA2GRAY)
    tmp = md.savetemp('filter', 'gray-' + img_name, img_cursor)
    result_images.append(tmp)

    # after filter
    img_cursor, result_images = eachFileter(
        img_cursor, result_images, filter_param['after-filter'], 'after', img_name)

    # cany
    img_cursor = cv2.Canny(img_cursor, filter_param['cany-0'], filter_param['cany-1'])
    tmp = md.savetemp('filter', 'cany-' + img_name, img_cursor)
    result_images.append(tmp)

    # dilate
    dilate_param = filter_param['dilate']
    if dilate_param['on']:
        kernel_size = int(dilate_param['kernel'])
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        img_cursor = cv2.dilate(img_cursor, kernel=kernel, iterations=dilate_param['it'])
        tmp = md.savetemp('filter', 'dilate-' + img_name, img_cursor)
        result_images.append(tmp)

    contours, _ = cv2.findContours(img_cursor, cv2.RETR_LIST, cv2.cv2.CHAIN_APPROX_NONE)
    lstCoords = [md.contour2coords(contour) for contour in contours]

    # poly
    polydp = filter_param['polydp']
    polies = [md.contour2coords(cv2.approxPolyDP(contour, polydp, False)) for contour in contours]

    return {
        'images': result_images,
        'lst-coords': lstCoords,
        'polies': polies
    }