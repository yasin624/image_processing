import numpy as np
import cv2,time
from tqdm import tqdm as tqdm

"""
____________________________________________________________________________________________________________
||                                                                                                          ||  
||        ###               ####                    ####                         ###########                || 
||        ###              ######                  ######                      ##                           ||
||                        ##    ##                ##    ##                   ##                             ||
||        ###            ##      ##              ##      ##                 ##                              ||
||        ###           ##        ##            ##        ##                ##                              ||
||        ###          ##          ##          ##          ##               ##      #########               ||
||        ###         ##            ##        ##            ##              ##             ##               ||
||        ###        ##              ##      ##              ##             ##             ##               ||
||        ###       ##                ##    ##                ##             ##            ##               ||
||        ###      ##                  ######                  ##             ##          ##                ||
||        ###     ##                    ####                    ##              ##########                  ||
||                                                                                                          ||
||__________________________________________________________________________________________________________||
||__________________________________________________________________________________________________________||

"""


class img_optimize():
    def __init__(self,bilgi=1):
        if bilgi==1:
            print("""
            
        information!!!
        -------------
        
            Burda img dosyaniz üzerinde genel olarak grid (ızgaralama ) model mimarisi için gerekli tüm optimizeleri yapmaniza olanak tanir
            
            img_size_optimize = yeniden şekillendir ve obje kutu optimizesi veya sadece resim boyutunu optimize etme
            
            orta_noktayi_optimize_etme = orta noktaları başka bir boyuta optimize etme sistemi
            
            img_x_y_w_h = obje kare sistemini x,y,weihgt,height sistemine dönüştürür
            
            grid_img = model izgarama sistemi için orta noktaları arka plana yayma
            
            """)
    def img_size_optimize(self,img, first_img_shape, new_img_shape, object_boxs=None):
        #####################################  yeniden şekillendir ve kutuyu yerleştir

        # if object_boxs is None, just return new img size

        deneme_resim = cv2.resize(img, (new_img_shape[1], new_img_shape[0]))

        if object_boxs == None:
            return deneme_resim
        else:

            istenilen_w = new_img_shape[1]
            istenilen_h = new_img_shape[0]

            varolan_w = first_img_shape[1]
            varolan_h = first_img_shape[0]

            x0, y0, x1, y1 = object_boxs

            # formüller;

            # istenilen_x0 = ( first_img_x0 * new_img_weight ) / first_img_weight
            # istenilen_y0 = ( first_img_y0* new_img_height ) / first_img_height
            # istenilen_x1 = ( first_img_x1 * new_img_weight ) / first_img_weight
            # istenilen_y1 = ( first_img_y1* new_img_height ) / first_img_height

            gerçek_x = (x0 * istenilen_w) / varolan_w

            gerçek_y = (y0 * istenilen_h) / varolan_h

            gerçek_w = (x1 * istenilen_w) / varolan_w
            gerçek_h = (y1 * istenilen_h) / varolan_h

            return deneme_resim, (gerçek_x, gerçek_y, gerçek_w, gerçek_h)


    ############################# orta noktaları başka bir boyuta optimize etme sistemi

    def orta_noktayi_optimize_etme(self,center_point=("x", "y"), w_h_size=("w", "h"), img_shape=("w0", "h0"),
                                   new_img_shape=("w1", "h1")):
        # formüller;

        # new_center_x = ( x * new_img_weight ) / first_img_weight
        # new_center_y = ( y * new_img_height ) / first_img_height

        # new_object_w = ( first_object_w * new_img_weight ) / first_img_weight
        # new_object_h = ( first_object_h * new_img_weight ) / first_img_weight

        x = (center_point[0] * new_img_shape[0]) / img_shape[0]
        y = (center_point[1] * new_img_shape[1]) / img_shape[1]

        if w_h_size[0] != "w" and w_h_size[1] != "h":

            w = (w_h_size[0] * new_img_shape[0]) / img_shape[0]
            h = (w_h_size[1] * new_img_shape[1]) / img_shape[1]

            return x, y, w, h
        else:
            return x, y

        ############################# kare sistemini x,y,weihgt,height sistemine dönüştürür


    def img_x_y_w_h(self,x0, y0, x1, y1):
        # formüller;

        # weight=x_son-x_ilk            height = y_son-y_ilk
        # orta_x = weight/2 + x_ilk     orta_y = height/2 + y_ilk

        new_x = ((x1 - x0) / 2 + x0)
        new_y = ((y1 - y0) / 2 + y0)
        new_w = (x1 - x0)
        new_h = (y1 - y0)

        return new_x, new_y, new_w, new_h


    ######################################## arka plan için bir ızgara sistemi

    def grid_img(self,img_shape, center_x_y_w_h, ondalik_kesir=False):
        # ondalık kesir Turu ise tam sayıdan sonraki degeri alır

        x, y, w, h = center_x_y_w_h

        if ondalik_kesir:
            kesir_x = abs(x - int(x))
            kesir_y = abs(y - int(y))

        h1, w1, z = img_shape

        grid = np.zeros((h1, w1, 5))

        grid[:][:]=[0,0,0,0,0]

        grid[int(y)][int(x)] = (1,kesir_x, kesir_y, w, h)

        grid = grid.reshape(-1, 5)

        return grid



####################################    orantılı buyutmce sistemi



class veri_icin_dolgulama():
    def __init__(self, bilgi=1):

        if bilgi == 1:
            print("""
                        warning!! : 

                                arr deişkeni liste biçiminde olmali

                                tam_dolgu deişkeni tuble olmali  3 karakteri olmali
                                tam_dolgu aynı zamanda çıktı degerinin shape sini verir

                                dolgu_mallzemesi 1 veya 0 olmali
                                1 ise arka plan beyaz 
                                o ise arka plan siyah

                    """)
        elif bilgi == 0:
            pass

    def orantılı(self, arr, tam_dolgu, kare_size,orantisiz):

        yeni_kare = []
        new_arry = []

        for s in tqdm(range(len(arr))):

            #####################################  yeniden şekillendir ve kutuyu yerleştir
            istenilen_x = tam_dolgu[1]
            istenilen_y = tam_dolgu[0]
            arr_size = arr[s].shape

            if not orantisiz:


                orantı = arr_size[1] / arr_size[0]
                orantı_x = istenilen_y * orantı

                if orantı_x > istenilen_x:
                    eksik_deger = orantı_x - istenilen_x

                    orantı_x = int(orantı_x - eksik_deger)

                    orantı_y = int((arr_size[0] / arr_size[1]) * istenilen_x)
                else:
                    orantı_y = istenilen_y

                yeni_resim = cv2.resize(arr[s], (int(orantı_x), orantı_y))

                x, y, w, h = kare_size[s][0], kare_size[s][1], kare_size[s][2], kare_size[s][3]

                gerçek_x = int((x * orantı_x) / arr_size[1])

                gerçek_y = int((y * orantı_y) / arr_size[0])

                gerçek_w = int((w * orantı_x) / arr_size[1])
                gerçek_h = int((h * orantı_y) / arr_size[0])



            elif orantisiz:
                yeni_resim = cv2.resize(arr[s], (int(istenilen_y), int(istenilen_x)))

                x, y, w, h = kare_size[s][0], kare_size[s][1], kare_size[s][2], kare_size[s][3]

                gerçek_x = int((x * istenilen_x) / arr_size[1])

                gerçek_y = int((y * istenilen_y) / arr_size[0])

                gerçek_w = int((w * istenilen_x) / arr_size[1])
                gerçek_h = int((h * istenilen_y) / arr_size[0])

            """
            normal degerler;

            normal_x : {x}
            normal_y : {y}
            normal_w : {w}
            normal_h : {h}

            yaratılan degerler ;

            gerçek_x : {gerçek_x}
            gerçek_y : {gerçek_y}
            gerçek_w : {gerçek_w}
            gerçek_h : {gerçek_h}


            """

            yeni_kare.append([gerçek_x, gerçek_y, gerçek_w, gerçek_h])
            new_arry.append(yeni_resim)

        return new_arry, yeni_kare

    def dolgula(self, arr, tam_dolgu=None, dolgu_malzemesi=0, kare_size=None,orantisiz=False):

        if kare_size:
            print("\n\n resimler orantılı olarak ayarlaniyor... \n\n")
            new_arry, yeni_kare = self.orantılı(arr, tam_dolgu, kare_size,orantisiz)
            print("resimler dolgulama için hazır.\n\n")
            time.sleep(2)

        else:
            new_arry = arr

        # dolgu değişkeni tuble olmalı
        ##################################################### dolgu malzemesini bulma
        print("resimlere uygun dolgu ile dolgulanıyor ...\n\n")
        new_arr = []
        for s in tqdm(range(len(arr))):
            size = new_arry[s].shape

            dolgu_x = None
            dolgu_y = None
            x_dolgu = np.array((1))
            y_dolgu = np.array((1))

            if size[1] != tam_dolgu[1]:
                dolgu_x = (abs(tam_dolgu[1] - size[1]), tam_dolgu[2])

            if size[0] != tam_dolgu[0]:
                dolgu_y = (abs(tam_dolgu[0] - size[0]), tam_dolgu[1], tam_dolgu[2])

            #########################################################  dolgu malzemesi yaratımı
            if dolgu_malzemesi == 0:
                if dolgu_x:
                    x_dolgu = np.zeros(dolgu_x)
                if dolgu_y:
                    y_dolgu = np.zeros(dolgu_y)

            elif dolgu_malzemesi == 1:

                if dolgu_x:
                    x_dolgu = np.ones(dolgu_x)
                if dolgu_y:
                    y_dolgu = np.ones(dolgu_y)

            else:
                print ("!!! erorr dolgu_malzemesi 1 veya 0 olmalı")

            new_img = self.doldur(new_arry[s], size, x_dolgu, y_dolgu, tam_dolgu)

            new_arr.append(new_img)

        print("resimlere dolgu işlemi bitti iyi şanslar dileriz :-) \n\n")

        if kare_size:
            return new_arr, yeni_kare
        else:
            return new_arr

    def doldur(self, imgs, size, x_dolgu, y_dolgu, tam_dolgu):

        new_img = imgs

        if len(x_dolgu.shape) > 1:
            dol = []

            for img in imgs:
                bak = np.append(img, x_dolgu)
                dol.append(bak)

            dol = np.array(dol, dtype=np.uint8).reshape(imgs.shape[0], tam_dolgu[1], tam_dolgu[2])

            new_img = dol

        imgs = new_img

        if len(y_dolgu.shape) > 1:
            dol = np.append(imgs, y_dolgu)

            dol = np.array(dol, dtype=np.uint8).reshape(tam_dolgu[0], imgs.shape[1], tam_dolgu[2])

            new_img = dol

        return new_img





