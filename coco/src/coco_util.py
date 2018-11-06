def convertBBox(img, cocoBbox):
    # turn bbox into yolo format- bbox center relative to img width and height

    #voc formar x,y,w,h
    dw = 1. / img['width']
    dh = 1. / img['height']

    centerX = cocoBbox[0] + cocoBbox[2] / 2.0
    centerX = centerX * dw

    centerY = cocoBbox[1] + cocoBbox[3] / 2.0
    centerY = centerY * dh

    rw = cocoBbox[2] * dw
    rh = cocoBbox[3] * dh
    return (centerX, centerY, rw, rh)